# %%%  Step 0 load libraries and configuration

import yaml
from pathlib import Path
import os
import requests
import numpy as np
import duckdb
from datetime import datetime
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor, as_completed

# %%

# Define the path to the config.yml file
script_path = Path(__file__).resolve()
root_path = script_path.parent.parent
data_path = root_path / "data/processed/destinations"
results_path = root_path / "results/data"
config_path = root_path / "config.yml"

# Read and parse the YAML file
with open(config_path, "r") as file:
    config_model = yaml.safe_load(file)


sample_size = config_model[
    "sample_size"
]  # Number of rows to sample from the data 0 = all
chunk_size = config_model["chunk_size"]  # number of rows to load into memory
parallelism = config_model["parallelism"]  # number of parallel processes to use
url = config_model["otp_url"]  # Load the OTP endpoint URL
date = config_model["travel_date"]  # Load the date of the travel
otp_db_fp = (
    results_path / config_model["otp_results"]
)  # Load the persistant OTP database file path

walk_speed = config_model["walk_speed"]  # Load the walk speed in m/s
search_window = config_model["search_window"]  # Load the search window in seconds
# %%

# DubckDB connection
con = duckdb.connect()

# Open a persistent DuckDB database file Data is stored temporay in Dockdb and then exported to parquet
otp_con = duckdb.connect(otp_db_fp)


# %%
# Define helper functions


def convert_otp_time(millis, tz="Europe/Copenhagen"):
    if isinstance(millis, (int, float)) and millis > 0:
        try:
            return datetime.fromtimestamp(millis / 1000, tz=ZoneInfo(tz)).strftime(
                "%Y-%m-%d %H:%M"
            )
        except Exception as e:
            print(f"Failed to convert timestamp {millis}: {e}")
            return None
    return None


def get_travel_info(
    from_lat,
    from_lon,
    to_lat,
    to_lon,
    date,
    time,
    walk_speed=1.3,
    search_window=7200,  # 2 hours in seconds
    arrive_by="true",
):
    query = f"""
    {{
      plan(
        from: {{lat: {from_lat}, lon: {from_lon}}}
        to: {{lat: {to_lat}, lon: {to_lon}}}
        date: "{date}"
        time: "{time}"
        walkSpeed: {walk_speed}
        arriveBy: {arrive_by},
        searchWindow: {search_window}
        numItineraries: 1
      ) {{
        itineraries {{
          startTime
          waitingTime
          duration
          walkDistance
        }}
      }}
    }} 
    """
    # print(f"Sending request to OTP API with query: {query}")
    response = requests.post(url, json={"query": query})
    # print(f"Error: {response.status_code} - {response.text}")

    # print(response.json())

    return response.json()


# Process the individual service types
def process_adresses(
    dataset, sampelsize, time, chunk_size=1000, max_workers=16, otp_con=otp_con, con=con
):
    filename = dataset + ".parquet"
    data = data_path / filename
    dataset = dataset.replace("-", "_")

    # Create target table

    otp_con.execute(f"DROP TABLE IF EXISTS {dataset};")

    otp_con.execute(
        f"""
        CREATE TABLE {dataset} (
            source_id TEXT,
            target_id TEXT,
            from_lat DOUBLE,
            from_lon DOUBLE,
            startTime TEXT,
            waitingTime DOUBLE,
            duration DOUBLE,
            walkDistance DOUBLE,
            abs_dist DOUBLE
        )
    """
    )

    # Load data into a temporary table
    if sampelsize == 0:
        con.execute(
            f"""
            CREATE OR REPLACE TEMP TABLE data_pairs AS 
            SELECT * 
            FROM '{data}'
        """
        )
    else:
        con.execute(
            f"""
            CREATE OR REPLACE TEMP TABLE data_pairs AS 
            SELECT * 
            FROM '{data}'
            USING SAMPLE {sampelsize} ROWS
        """
        )

    # Function to process a single row
    def process_row(row, date, time, search_window=7200):
        try:
            travel_info = get_travel_info(
                row.source_lat,
                row.source_lon,
                row.dest_lat,
                row.dest_lon,
                date,
                time,
                walk_speed=1.3,
                search_window=search_window,
                arrive_by="true",
            )
            itenerary = travel_info["data"]["plan"]["itineraries"][0]
            return (
                row.source_adress_id,
                row.dest_adress_id,
                row.source_lat,
                row.source_lon,
                convert_otp_time(itenerary["startTime"]),
                itenerary["waitingTime"],
                itenerary["duration"],
                itenerary["walkDistance"],
                row.dest_distance,
            )
        except Exception:
            # except Exception as e:
            # Print the type and message of the exception
            # print(f"Exception type: {type(e).__name__}, Message: {str(e)}")
            # print(row.source_lat, row.source_lon, row.dest_lat, row.dest_lon)

            return (
                row.source_adress_id,
                row.dest_adress_id,
                row.source_lat,
                row.source_lon,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                row.dest_distance,
            )

    # Process in chunks with parallel execution
    offset = 0
    while True:
        chunk = con.execute(
            f"""
            SELECT * FROM data_pairs 
            LIMIT {chunk_size} OFFSET {offset}
        """
        ).fetchdf()

        if chunk.empty:
            break

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(process_row, row, date, time, search_window)
                for row in chunk.itertuples(index=False)
            ]

            for future in as_completed(futures):
                result = future.result()
                otp_con.execute(
                    f"""
                    INSERT INTO {dataset} VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
                """,
                    result,
                )

        offset += chunk_size


# %%
services = config_model["services"]

for service in services:
    for i in range(1, int(service["n_neighbors"]) + 1):
        dataset = f"{service['service_type']}_{i}"
        # Process each dataset
        print(
            f"Processing {dataset} with sample size {sample_size} and chunk size {chunk_size}"
        )
        process_adresses(
            dataset, sample_size, service["arival_time"], chunk_size, parallelism
        )
        # Export to parquet
        tabelname = dataset.replace("-", "_")
        otp_con.execute(
            f"""
            COPY (SELECT * FROM {tabelname}) TO '{results_path}/{dataset}_otp.parquet' (FORMAT 'parquet')
        """
        )

# %%
