# %%

# PROCESS RESULTS FROM SERVICE ACCESS ANALYSIS

import pandas as pd
import geopandas as gpd
import yaml
from pathlib import Path

# %%

# Define the path to the config.yml file
script_path = Path(__file__).resolve()
root_path = script_path.parent.parent
data_path = root_path / "data/processed/destinations"
results_path = root_path / "results"
config_path = root_path / "config.yml"

# Read and parse the YAML file
with open(config_path, "r") as file:
    config_model = yaml.safe_load(file)

# %%

# TODO
# drop duplicates
# convert duration to minutes

# some NaN values are because source and target are the same
# Some are because the result was empty!

# %%
# Load results

services = config_model["services"]

for service in services[0:1]:
    for i in range(1, int(service["n_neighbors"]) + 1):
        dataset = f"{service['service_type']}_{i}"
        # Process each dataset

        print(f"Processing result dataset: {dataset}")
        fp = results_path / f"{dataset}_otp.parquet"
        if not fp.exists():
            print(f"File {fp} does not exist. Skipping.")
            continue
        df = pd.read_parquet(fp)
        print(f"Loaded {len(df)} rows from {fp}")

        # Check for duplicates
        if df.duplicated(subset=["source_id", "target_id"]).any():
            print(f"Duplicates found in {dataset}. Dropping duplicates.")
            df = df.drop_duplicates(subset=["source_id", "target_id"])

        # Convert duration to minutes
        df["duration_minutes"] = df["duration"] / 60
        df["arrival_time"] = df["startTime"] + pd.to_timedelta(
            df["duration_minutes"], unit="m"
        )

        arrival_deadline = pd.to_datetime(
            f"{config_model['travel_date']} {service['arival_time']}"
        )

        # check that arrival time is before the deadline
        if not df["arrival_time"].le(arrival_deadline).all():
            print(
                f"Warning: Some arrival times in {dataset} exceed the deadline of {arrival_deadline}."
            )

        result_count = df[df["duration"].notna()].shape[0]
        print(f"{result_count} solutions found in {dataset} with{len(df)} rows.")

        print(
            f"{len(df[df["source_id"] == df["target_id"]])} rows where source and target are the same."
        )

        # Count sources with no results
        # Exclude rows where source and target are the same
        df_subset = df[df["source_id"] != df["target_id"]]
        no_results_count = df_subset[df_subset["duration"].isna()].shape[0]
        if no_results_count > 0:
            print(
                f"{no_results_count} sources have no results in {dataset}. This may indicate that the search window was too small or that no transit solution is available."
            )


# %%
# TODO

# Analyse average duration
# Analyse arrival time compared to deadline
# Make maps of the results:
# Travel times for each service
