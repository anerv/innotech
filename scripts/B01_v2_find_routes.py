# %%%  Step 0 load libraries and configuration

import yaml
from pathlib import Path
import duckdb
from src.helper_functions import process_adresses
import pandas as pd
import os

# %%

# Define the path to the config.yml file
script_path = Path(__file__).resolve()
root_path = script_path.parent.parent
config_path = root_path / "config.yml"

# Read and parse the YAML file
with open(config_path, "r") as file:
    config_model = yaml.safe_load(file)

# %%
data_path = root_path / "data/processed/destinations"

if config_model["filter_rural_addresses"]:
    results_path = root_path / "results_rural/data"

else:
    results_path = root_path / "results/data"

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

search_window_first_run = 7200  # the search window for the first run in seconds
# %%

arrival_times = [
    "06:00",
    "08:00",
    "12:00",
    "18:00",
    "22:00",
]

# DubckDB connection
con = duckdb.connect()

# Open a persistent DuckDB database file Data is stored temporay in Duckdb and then exported to parquet
otp_con = duckdb.connect(otp_db_fp)

# %%

services = config_model["services"]

for arrival_time in arrival_times:

    print(f"Arrival time: {arrival_time}")

    arrival_string = arrival_time.replace(":", "_")

    for service in services:
        for i in range(1, int(service["n_neighbors"]) + 1):
            dataset = f"{service['service_type']}_{i}"
            # Process each dataset
            print(
                f"Processing {dataset} with sample size {sample_size}, chunk size {chunk_size}, arrival time {arrival_time} and search window {search_window_first_run} seconds"
            )
            process_adresses(
                dataset,
                sample_size,
                arrival_time,  # service["arrival_time"],
                date,
                walk_speed,
                search_window_first_run,
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
                    COPY (SELECT * FROM {tabelname}) TO '{results_path}/{dataset}_{arrival_string}_otp.parquet' (FORMAT 'parquet')
                """
            )

# %%

for arrival_time in arrival_times:

    print(f"Arrival time: {arrival_time}")

    arrival_string = arrival_time.replace(":", "_")

    for service in services:
        for i in range(1, int(service["n_neighbors"]) + 1):
            dataset = f"{service['service_type']}_{i}"

            # Load the results
            print(f"Loading results for {dataset}...")

            results = pd.read_parquet(
                f"{results_path}/{dataset}_{arrival_string}_otp.parquet"
            )

            input_data = pd.read_parquet(f"{data_path}/{dataset}.parquet")

            input_data_no_solution = input_data[
                input_data["source_address_id"].isin(
                    results[results.duration.isna()]["source_id"]
                )
            ]

            input_data_no_solution.to_parquet(
                f"{data_path}/{dataset}_second_run.parquet",
                index=False,
            )

            print(
                f"Found {input_data_no_solution.shape[0]} addresses with no solution in the first run."
            )

            print(
                f"Processing {dataset} with sample size {sample_size}, chunk size {chunk_size}, arrival time {arrival_time} and search window {search_window} seconds"
            )

            dataset = f"{dataset}_second_run"  # Update dataset name for second run

            # set this as input for the next run
            process_adresses(
                dataset,
                sample_size,
                arrival_time,  # service["arrival_time"],
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
                COPY (SELECT * FROM {tabelname}) TO '{results_path}/{dataset}_otp.parquet' (FORMAT 'parquet')
            """
            )

            results_first_run = results[results.duration.notna()]

            results_second_run = pd.read_parquet(
                f"{results_path}/{dataset}_otp.parquet"
            )

            print(
                f"Found {results_second_run[results_second_run.duration.notna()].shape[0]} results in the second run for {dataset}."
            )

            # Combine the results
            combined_results = pd.concat(
                [results_first_run, results_second_run], ignore_index=True
            )

            assert (
                combined_results.shape[0]
                == results_first_run.shape[0] + results_second_run.shape[0]
            ), "Combined results do not match the expected number of rows"

            assert (
                combined_results.source_id.is_unique
            ), "Source IDs are not unique in combined results"

            # reset dataset name for export
            dataset = f"{service['service_type']}_{i}"

            # Export the combined results
            combined_results.to_parquet(
                f"{results_path}/{dataset}_{arrival_string}_otp.parquet", index=False
            )

            # remove exported files from second run
            os.remove(f"{results_path}/{dataset}_second_run_otp.parquet")
            os.remove(f"{data_path}/{dataset}_second_run.parquet")


# %%
