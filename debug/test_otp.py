# Temp remove itinerary filters
# change "debug": "limit-to-search-window" or "list-all"?

# %%

import yaml
from pathlib import Path
import pandas as pd
import duckdb
from src.helper_functions import process_adresses
import geopandas as gpd

# Define the path to the config.yml file
script_path = Path(__file__).resolve()
root_path = script_path.parent.parent
data_path = root_path / "data/processed/destinations"
results_path = root_path / "results/data"
config_path = root_path / "config.yml"

# Read and parse the YAML file
with open(config_path, "r") as file:
    config_model = yaml.safe_load(file)

    crs = config_model["crs"]  # Load the coordinate reference system


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

# search_window = config_model["search_window"]  # Load the search window in seconds
search_window = 7200 * 12  # 24 hours
# %%

# DubckDB connection
con = duckdb.connect()

# Open a persistent DuckDB database file Data is stored temporay in Dockdb and then exported to parquet
otp_con = duckdb.connect(otp_db_fp)

dataset = "test"
service = "train_station"  # Choose which service to debug
arrival_time = "07:30"  # Choose which arrival time to use
address_data = pd.read_parquet(
    data_path / f"{service}_1.parquet"
)  # Load the address data

address_data.rename(columns={"source_adress_id": "source_address_id"}, inplace=True)
no_connection = gpd.read_file("no_train_connection_all.gpkg")
source_ids = no_connection.source_id.to_list()

# Choose which starting points to use for debugging
test_data = address_data[address_data.source_address_id.isin(source_ids)]

assert len(test_data) == len(source_ids), "Source IDs do not match the dataset length"

test_data.to_parquet(data_path / f"test.parquet", index=False)
# %%
# Process each dataset
print(
    f"Processing {dataset} with sample size {sample_size} and chunk size {chunk_size}"
)

process_adresses(
    dataset,
    sample_size,
    arrival_time,
    date,
    walk_speed,
    search_window,
    url,
    data_path,
    otp_con,
    con,
    chunk_size,
    parallelism,
)
# Export to parquet
tabelname = dataset.replace("-", "_")
otp_con.execute(
    f"""
    COPY (SELECT * FROM {tabelname}) TO '{results_path}/{dataset}_otp_TEST.parquet' (FORMAT 'parquet')
"""
)
# %%
# Export test results
results = pd.read_parquet(results_path / f"{dataset}_otp_TEST.parquet")
# %%
results["geometry"] = results["geometry"] = gpd.points_from_xy(
    results["from_lon"], results["from_lat"]
)
gdf = gpd.GeoDataFrame(results, geometry="geometry", crs="EPSG:4326")
gdf.to_crs(crs, inplace=True)
gdf.to_file("results.gpkg", driver="GPKG")

# %%
from src.helper_functions import get_travel_info

# %%
source_id = "0a3f50af-e5b2-32b8-e044-0003ba298018"
target_id = "1c965415-e512-40ae-8ccb-00692d55c515"

from_lat = 54.994538304026094
from_lon = 12.426831686463684
to_lat = 55.217142
to_lon = 12.162233

datetime = "2025-02-19T15:23:00.814+02:00"

url = "http://localhost:8080/otp/gtfs/v1"

url = "http://localhost:8080/otp/transmodel/v3"

import json
import os
import requests


def get_travel_info(
    from_lat,
    from_lon,
    to_lat,
    to_lon,
    date_time,
    url,
    walk_speed=1.3,
    search_window=7200,  # 2 hours in seconds
    arrive_by="true",
):
    query = f"""
    {{
      trip(
        from: {{
          coordinates: {{
            latitude: {from_lat}
            longitude: {from_lon}
          }}
        }}
        to: {{
          coordinates: {{
            latitude: {to_lat}
            longitude: {to_lon}
          }}
        }}
        dateTime: "{date_time}"
        walkSpeed: {walk_speed}
        arriveBy: {arrive_by}
        searchWindow: {search_window}
        numTripPatterns: 1
      ) {{
        tripPatterns {{
          expectedStartTime
          duration
          walkDistance
          legs {{
            mode
            duration
          }}
        }}
      }}
    }}
    """

    response = requests.post(url, json={"query": query})

    if response.status_code != 200:
        raise RuntimeError(f"Request failed: {response.status_code}\n{response.text}")

    return response.json()


# %%

test = get_travel_info(
    from_lat=from_lat,
    from_lon=from_lon,
    to_lat=to_lat,
    to_lon=to_lon,
    date_time=datetime,
    url=url,
    walk_speed=walk_speed,
    search_window=60,
)
# %%
