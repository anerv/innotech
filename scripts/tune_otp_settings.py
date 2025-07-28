# %%
# Test sensitivity of OTP settings (search window, arrival time, walk speed)

# %%
import yaml
from pathlib import Path
import pandas as pd
import duckdb
from src.helper_functions import process_adresses, get_geo_address_sample
import geopandas as gpd
import h3

# Define the path to the config.yml file
script_path = Path(__file__).resolve()
root_path = script_path.parent.parent
data_path = root_path / "data/processed/destinations"
data_test_path = root_path / "data/processed/destinations_test"
results_path = root_path / "results/data_test"
config_path = root_path / "config.yml"

# make data_test folder if it does not exist
results_path.mkdir(parents=True, exist_ok=True)
data_test_path.mkdir(parents=True, exist_ok=True)

# Read and parse the YAML file
with open(config_path, "r") as file:
    config_model = yaml.safe_load(file)

    crs = config_model["crs"]  # Load the coordinate reference system

chunk_size = config_model["chunk_size"]  # number of rows to load into memory
parallelism = config_model["parallelism"]  # number of parallel processes to use
url = config_model["otp_url"]  # Load the OTP endpoint URL
date = config_model["travel_date"]  # Load the date of the travel
otp_db_fp = (
    results_path / config_model["otp_results"]
)  # Load the persistant OTP database file path

# %%

# DuckDB connection
con = duckdb.connect()

# Open a persistent DuckDB database file Data is stored temporay in Dockdb and then exported to parquet
otp_con = duckdb.connect(otp_db_fp)

search_window = 3600
arrival_time = "12:00"
walk_speed = 1.3  # walking speed in m/s
h3_resolution = 8  # H3 resolution for spatial indexing

# service = "doctor"
# i = 1
# nearest_neighbors = pd.read_parquet(
#     data_path / f"{service}_{i}.parquet"
# )  # Load the nearest neighbor data for the service

# nn_gdf = gpd.GeoDataFrame(
#     nearest_neighbors,
#     geometry=gpd.points_from_xy(
#         nearest_neighbors.source_lon, nearest_neighbors.source_lat
#     ),
#     crs="EPSG:4326",
# )

# dataset = f"{service}_{i}_{search_window}_{walk_speed}_{arrival_time}"

# sample = get_geo_address_sample(
#     dataset=nn_gdf,
#     data_path=data_test_path,
#     dataset_name=dataset,
# )
# print(
#     f"Sampled {len(sample)} points from {len(nn_gdf)} nearest neighbors for {dataset}. Decrease h3 resolution for a smaller sample size."
# )

# %%

services = config_model["services"]

for service in services:
    for i in range(1, int(service["n_neighbors"]) + 1):

        nearest_neighbors = pd.read_parquet(
            data_path / f"{service["service_type"]}_{i}.parquet"
        )  # Load the nearest neighbor data for the service

        nn_gdf = gpd.GeoDataFrame(
            nearest_neighbors,
            geometry=gpd.points_from_xy(
                nearest_neighbors.source_lon, nearest_neighbors.source_lat
            ),
            crs="EPSG:4326",
        )

        dataset = (
            f"{service['service_type']}_{i}_{search_window}_{walk_speed}_{arrival_time}"
        )

        dataset = dataset.replace(":", "-")
        dataset = dataset.replace(".", "-")

        sample = get_geo_address_sample(
            dataset=nn_gdf,
            data_path=data_test_path,
            dataset_name=dataset,
            h3_resolution=h3_resolution,
        )
        print(
            f"Sampled {len(sample)} points from {len(nn_gdf)} nearest neighbors for {service['service_type']}. Decrease h3 resolution for a smaller sample size."
        )

        sample_size = len(sample)

        # Process each dataset
        print(
            f"""Processing {dataset} with sample size {sample_size}, chunk size {chunk_size}, search window {search_window} seconds, 
            walk speed {walk_speed} m/s, and arrival time {arrival_time}"""
        )

        process_adresses(
            dataset,
            sample_size,
            arrival_time,
            date,
            walk_speed,
            search_window,
            url,
            data_test_path,
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

        # results = otp_con.execute(f"SELECT * FROM {tabelname}").df()

# %%
# TODO: evaluate the number of results and the time it took to process the dataset


# %%
