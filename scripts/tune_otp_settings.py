# %%
# Test sensitivity of OTP settings (search window, arrival time, walk speed)

# %%
import yaml
from pathlib import Path
import pandas as pd
import duckdb
from src.helper_functions import process_adresses, get_geo_address_sample
import geopandas as gpd
import time
import matplotlib.pyplot as plt
from IPython.display import display

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

    adm_boundaries_config = config_model["study_area_config"]

    study_area_fp = adm_boundaries_config["regions"]["outputpath"]

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

search_windows = [
    1800,
    3600,
    7200,
    14400,
]  # search windows in seconds [30 min, 1 hour, 2 hours, 4 hours]
arrival_times = [
    "06:00",
    "08:00",
    "12:00",
    "18:00",
    "22:00",
]  # arrival times in HH:MM format
walk_speed = 1.3  # walking speed in m/s
h3_resolution = 5  # H3 resolution for spatial indexing

# %%

services = config_model["services"]

results_parameters = []

for search_window in search_windows:

    print(f"Search window: {search_window} seconds")

    for arrival_time in arrival_times:

        print(f"Arrival time: {arrival_time}")

        for service in services:

            print(f"Service type: {service['service_type']}")

            start_time = time.time()  # Start timing the processing

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

                dataset = f"{service['service_type']}_{i}_{search_window}_{walk_speed}_{arrival_time}"

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
                # print(
                #     f"""Processing {dataset} with sample size {sample_size}, chunk size {chunk_size}, search window {search_window} seconds,
                #     walk speed {walk_speed} m/s, and arrival time {arrival_time}"""
                # )

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

                end_time = time.time()  # End timing the processing
                elapsed_time = end_time - start_time  # Calculate elapsed time

                # Export to parquet
                tabelname = dataset.replace("-", "_")
                otp_con.execute(
                    f"""
                    COPY (SELECT * FROM {tabelname}) TO '{results_path}/{dataset}_otp.parquet' (FORMAT 'parquet')
                """
                )

                # Collect results data
                results = otp_con.execute(f"SELECT * FROM {tabelname}").df()
                no_connection = results[results.duration.isna()]

                results_parameters.append(
                    {
                        "service_type": service["service_type"],
                        "n_neighbors": i,
                        "search_window": search_window,
                        "walk_speed": walk_speed,
                        "arrival_time": arrival_time,
                        "sample_size": len(results),
                        "no_connection_count": len(no_connection),
                        "no_connection_percentage": len(no_connection)
                        / len(results)
                        * 100,
                        "time_elapsed": elapsed_time,
                    }
                )

# %%

# Create a pivot table for results data

results_df = pd.DataFrame(results_parameters)

results_pivot = results_df.pivot_table(
    index=["service_type", "n_neighbors"],
    columns=["search_window", "arrival_time"],
    values=["no_connection_count", "no_connection_percentage", "time_elapsed"],
)

# Save the pivot table to a CSV file
results_pivot.to_csv(results_path / "results_pivot.csv")

display(results_pivot)

# %%

study_area = gpd.read_file(study_area_fp)

for search_window in search_windows:

    for arrival_time in arrival_times:

        for service in services:

            for i in range(1, int(service["n_neighbors"]) + 1):

                dataset = f"{service['service_type']}_{i}_{search_window}_{walk_speed}_{arrival_time}"

                dataset = dataset.replace(":", "-")
                dataset = dataset.replace(".", "-")

                tabelname = dataset.replace("-", "_")

                results = otp_con.execute(f"SELECT * FROM {tabelname}").df()

                no_connection = results[results.duration.isna()]

                results_gdf = gpd.GeoDataFrame(
                    results,
                    geometry=gpd.points_from_xy(
                        results.from_lon, results.from_lat, crs="EPSG:4326"
                    ),
                )
                results_gdf.to_crs(crs, inplace=True)

                fig, ax = plt.subplots(figsize=(5, 5))
                study_area.plot(ax=ax, color="white", edgecolor="grey", linewidth=0.5)
                results_gdf.plot(
                    ax=ax, color="black", markersize=1, label="Connected points"
                )
                results_gdf[results_gdf.duration.isna()].plot(
                    ax=ax, color="red", markersize=3, label="No connection"
                )

                ax.set_axis_off()
                ax.legend(
                    bbox_to_anchor=(-0.2, -0.02),
                    loc="lower left",
                    frameon=False,
                    fontsize=8,
                    markerscale=2,
                )
                ax.set_title(
                    f"{service["service_type"].title()}, search window: {search_window}, arrival time: {arrival_time}",
                    fontsize=10,
                )

                plt.show()
                plt.close()
# %%
