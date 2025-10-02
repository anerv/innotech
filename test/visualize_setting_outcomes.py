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
import math

# Define the path to the config.yml file
script_path = Path(__file__).resolve()
root_path = script_path.parent.parent
data_path = root_path / "data/processed/destinations"
data_test_path = root_path / "test/destinations_test"
results_path_data = root_path / "test/result_data_test"
results_path_plots = root_path / "test/result_plots_test"
config_path = root_path / "config.yml"

# make data_test folder if it does not exist
results_path_plots.mkdir(parents=True, exist_ok=True)
results_path_data.mkdir(parents=True, exist_ok=True)
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
    results_path_data / config_model["otp_results"]
)  # Load the persistant OTP database file path


# DuckDB connection
con = duckdb.connect()

# Open a persistent DuckDB database file Data is stored temporay in Dockdb and then exported to parquet
otp_con = duckdb.connect(otp_db_fp)

search_windows = [
    1800,
    # 3600,
    7200,
    14400,
    28800,
]  # search windows in seconds [30 min, 2 hours, 4 hours, 8 hours]
arrival_times = [
    "06:00",
    "08:00",
    "12:00",
    "18:00",
    "22:00",
]  # arrival times in HH:MM format
walk_speed = 1.3  # walking speed in m/s
h3_resolution = 7  # H3 resolution for spatial sampling. Decrease h3 resolution for a smaller sample size.

services = config_model["services"]

# %%

results_df = pd.read_csv(results_path_data / "results.csv")

# Make a pivot table for results data
values = ["no_connection_count", "no_connection_percentage"]

for value in values:

    # Create a pivot table for results data
    results_pivot = results_df.pivot_table(
        index=["service_type"],
        columns=["search_window", "arrival_time"],
        values=[value],
    )

    # Save the pivot table to a CSV file
    results_pivot.to_csv(results_path_data / f"results_pivot_{value}.csv")

    styled_pivot = results_pivot.style.set_table_styles(
        [
            {"selector": "th", "props": [("font-weight", "bold")]},
            {"selector": "td:hover", "props": [("background-color", "#FFFACD")]},
        ]
    ).format("{:.2f}")

    # Display the styled pivot table
    display(styled_pivot)

# %%
# Compute and plot average time elapsed for each service type, search window, and arrival time combination
avg_time_elapsed = (
    results_df.groupby(["search_window", "arrival_time"])["time_elapsed"]
    .mean()
    .reset_index()
)
display(avg_time_elapsed)
# %%

# Plot connected and disconnected points for each service type, search window, and arrival time combination
study_area = gpd.read_file(study_area_fp)

# Number of services (assumed to be 9)
n_services = len(services)
n_cols = 3
n_rows = math.ceil(n_services / n_cols)

for search_window in search_windows:
    for arrival_time in arrival_times:

        # Create one figure per (search_window, arrival_time)
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 15))
        axes = axes.flatten()

        for idx, service in enumerate(services):

            for i in range(1, int(service["n_neighbors"]) + 1):

                dataset = f"{service['service_type']}_{i}_{search_window}_{walk_speed}_{arrival_time}"
                dataset = dataset.replace(":", "-").replace(".", "-")
                tabelname = dataset.replace("-", "_")

                results = otp_con.execute(f"SELECT * FROM {tabelname}").df()

                results_gdf = gpd.GeoDataFrame(
                    results,
                    geometry=gpd.points_from_xy(
                        results.from_lon, results.from_lat, crs="EPSG:4326"
                    ),
                )
                results_gdf.to_crs(crs, inplace=True)

                ax = axes[idx]

                study_area.plot(ax=ax, color="white", edgecolor="grey", linewidth=0.5)
                results_gdf.plot(ax=ax, color="black", markersize=1)
                results_gdf[results_gdf.duration.isna()].plot(
                    ax=ax, color="red", markersize=3
                )

                ax.set_axis_off()
                ax.set_title(
                    f"{service['service_type'].title().replace("_"," ")} (k={i})",
                    fontsize=9,
                )

                break  # Only plot for the first k (remove this if you want multiple neighbors plotted)

        # Remove unused subplots if services < subplot slots
        for j in range(len(services), len(axes)):
            fig.delaxes(axes[j])

        fig.suptitle(
            f"Search Window: {search_window}, Arrival Time: {arrival_time}", fontsize=14
        )
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.savefig(
            results_path_plots
            / f"connections_{search_window}_{arrival_time.replace(":","-")}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()
        plt.close()

# %%
# DURATION - all arrival times in one plot

study_area = gpd.read_file(study_area_fp)

# Number of services (assumed to be 9)
n_cols = 3
n_rows = math.ceil(len(arrival_times) / n_cols)

for search_window in search_windows:

    for service in services:

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 15))
        axes = axes.flatten()

        for idx, arrival_time in enumerate(arrival_times):

            for i in range(1, int(service["n_neighbors"]) + 1):

                dataset = f"{service['service_type']}_{i}_{search_window}_{walk_speed}_{arrival_time}"
                dataset = dataset.replace(":", "-").replace(".", "-")
                tabelname = dataset.replace("-", "_")

                results = otp_con.execute(f"SELECT * FROM {tabelname}").df()

                results_gdf = gpd.GeoDataFrame(
                    results,
                    geometry=gpd.points_from_xy(
                        results.from_lon, results.from_lat, crs="EPSG:4326"
                    ),
                )
                results_gdf.to_crs(crs, inplace=True)

                ax = axes[idx]

                results_gdf["duration_min"] = results_gdf["duration"] / 60

                study_area.plot(ax=ax, color="white", edgecolor="grey", linewidth=0.5)
                results_gdf.plot(
                    ax=ax,
                    column="duration_min",
                    cmap="viridis",
                    markersize=3,
                    legend=True,
                    legend_kwds={
                        "label": "Travel Time (m)",
                        "shrink": 0.6,
                    },
                )

                ax.set_axis_off()
                ax.set_title(
                    f"{arrival_time} (k={i})",
                    fontsize=9,
                )

                break  # Only plot for the first k (remove this if you want multiple neighbors plotted)

        # Remove unused subplots if services < subplot slots
        for j in range(len(arrival_times), len(axes)):
            fig.delaxes(axes[j])

        fig.suptitle(
            f"{service['service_type'].title().replace('_',' ')} - Search Window: {search_window}",
            fontsize=14,
        )
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.savefig(
            results_path_plots
            / f"traveltime_{service['service_type']}_{search_window}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()
        plt.close()


# %%

# DURATION - all services in one plot

# Number of services (assumed to be 9)
n_cols = 3
n_rows = math.ceil(n_services / n_cols)


for search_window in search_windows:
    for arrival_time in arrival_times:

        # Create one figure per (search_window, arrival_time)
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 15))
        axes = axes.flatten()

        for idx, service in enumerate(services):

            for i in range(1, int(service["n_neighbors"]) + 1):

                dataset = f"{service['service_type']}_{i}_{search_window}_{walk_speed}_{arrival_time}"
                dataset = dataset.replace(":", "-").replace(".", "-")
                tabelname = dataset.replace("-", "_")

                results = otp_con.execute(f"SELECT * FROM {tabelname}").df()

                results_gdf = gpd.GeoDataFrame(
                    results,
                    geometry=gpd.points_from_xy(
                        results.from_lon, results.from_lat, crs="EPSG:4326"
                    ),
                )
                results_gdf.to_crs(crs, inplace=True)

                results_gdf["duration_min"] = (
                    results_gdf["duration"] / 60
                )  # convert to minutes

                ax = axes[idx]

                study_area.plot(ax=ax, color="white", edgecolor="grey", linewidth=0.5)
                results_gdf.plot(
                    ax=ax,
                    column="duration_min",
                    cmap="viridis",
                    markersize=1,
                    legend=True,
                    legend_kwds={"label": "Travel Time (m)", "shrink": 0.6},
                )

                ax.set_axis_off()
                ax.set_title(
                    f"{service['service_type'].title().replace("_"," ")} (k={i})",
                    fontsize=9,
                )

                break  # Only plot for the first k (remove this if you want multiple neighbors plotted)

        # Remove unused subplots if services < subplot slots
        for j in range(len(services), len(axes)):
            fig.delaxes(axes[j])

        fig.suptitle(
            f"Search Window: {search_window}, Arrival Time: {arrival_time}", fontsize=14
        )
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.savefig(
            results_path_plots
            / f"traveltime_{search_window}_{arrival_time.replace(":","-")}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()
        plt.close()

# %%
# WAITTIME - all arrival times in one plot

study_area = gpd.read_file(study_area_fp)

# Number of services (assumed to be 9)
n_cols = 3
n_rows = math.ceil(len(arrival_times) / n_cols)

for search_window in search_windows:

    for service in services:

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 15))
        axes = axes.flatten()

        for idx, arrival_time in enumerate(arrival_times):

            for i in range(1, int(service["n_neighbors"]) + 1):

                dataset = f"{service['service_type']}_{i}_{search_window}_{walk_speed}_{arrival_time}"
                dataset = dataset.replace(":", "-").replace(".", "-")
                tabelname = dataset.replace("-", "_")

                results = otp_con.execute(f"SELECT * FROM {tabelname}").df()

                results_gdf = gpd.GeoDataFrame(
                    results,
                    geometry=gpd.points_from_xy(
                        results.from_lon, results.from_lat, crs="EPSG:4326"
                    ),
                )
                results_gdf.to_crs(crs, inplace=True)

                results_gdf.dropna(subset=["duration"], inplace=True)

                ax = axes[idx]

                # arrival_deadline = pd.to_datetime(
                #     f"{config_model['travel_date']} {arrival_time}"
                # )
                arrival_deadline = pd.to_datetime(f"2025-04-22 {arrival_time}")
                results_gdf["duration_min"] = results_gdf["duration"] / 60

                results_gdf["arrival_time"] = pd.to_datetime(
                    results_gdf["startTime"]
                ) + pd.to_timedelta(results_gdf["duration_min"], unit="m")

                results_gdf["wait_time_dest"] = (
                    arrival_deadline - results_gdf["arrival_time"]
                )

                results_gdf["wait_time_dest_min"] = (
                    results_gdf["wait_time_dest"].dt.total_seconds() / 60
                )

                study_area.plot(ax=ax, color="white", edgecolor="grey", linewidth=0.5)
                results_gdf.plot(
                    ax=ax,
                    column="wait_time_dest_min",
                    cmap="viridis",
                    markersize=3,
                    legend=True,
                    legend_kwds={
                        "label": "Waittime at destination (m)",
                        "shrink": 0.6,
                    },
                )

                ax.set_axis_off()
                ax.set_title(
                    f"{arrival_time} (k={i})",
                    fontsize=9,
                )

                break  # Only plot for the first k (remove this if you want multiple neighbors plotted)

        # Remove unused subplots if services < subplot slots
        for j in range(len(arrival_times), len(axes)):
            fig.delaxes(axes[j])

        fig.suptitle(
            f"{service['service_type'].title().replace('_',' ')} - Search Window: {search_window}",
            fontsize=14,
        )
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.savefig(
            results_path_plots
            / f"waittime_{service['service_type']}_{search_window}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()
        plt.close()

# %%
# TODO: Make histograms instead of maps
# small multiples of histograms of duration and wait time for each service type, search window, and arrival time combination
# Add note with number of connected and disconnected points
# %%
