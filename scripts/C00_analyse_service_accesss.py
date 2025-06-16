# %%

# PROCESS RESULTS FROM SERVICE ACCESS ANALYSIS

import pandas as pd
import geopandas as gpd
import yaml
from pathlib import Path
import os
import sys
from src.helper_functions import (
    plot_traveltime_results,
    plot_no_connection,
    highlight_max_traveltime,
    highlight_min_traveltime,
    unpack_modes_from_json,
    transfers_from_json,
)


os.environ["GDAL_DATA"] = os.path.join(
    f"{os.sep}".join(sys.executable.split(os.sep)[:-1]), "Library", "share", "gdal"
)

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
walkspeed_min = config_model["walk_speed"] * 60  # convert to minutes


# load study area for plotting
study_area = gpd.read_file(config_model["study_area_fp"])

# Load results
services = config_model["services"]

summaries = []

for service in services:

    for i in range(1, int(service["n_neighbors"]) + 1):
        dataset = f"{service['service_type']}_{i}"
        # Process each dataset

        print(f"Processing result dataset: {dataset}")
        fp = results_path / f"data/{dataset}_otp.parquet"
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
        df["duration_min"] = df["duration"] / 60

        df["startTime"] = pd.to_datetime(df["startTime"]).dt.strftime("%Y-%m-%d %H:%M")

        df["arrival_time"] = pd.to_datetime(df["startTime"]) + pd.to_timedelta(
            df["duration_min"], unit="m"
        )

        arrival_deadline = pd.to_datetime(
            f"{config_model['travel_date']} {service['arival_time']}"
        )

        # check that all arrival times are less than or equal to the arrival deadline
        if (df["arrival_time"] > arrival_deadline).any():
            print(
                f"Warning: Some arrival times in {dataset} exceed the deadline of {arrival_deadline}."
            )

        result_count = df[df["duration"].notna()].shape[0]
        print(f"{result_count} solutions found in {dataset} with {len(df)} rows.")

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

        ave_duration = df["duration_min"].mean()
        print(f"Average trip duration for {dataset}: {ave_duration:.2f} minutes")

        df["wait_time_dest"] = arrival_deadline - df["arrival_time"]
        df["wait_time_dest_min"] = df["wait_time_dest"].dt.total_seconds() / 60
        ave_wait_time = df["wait_time_dest_min"].mean()
        print(
            f"Average wait time at destination for {dataset}: {ave_wait_time:.2f} minutes"
        )

        df["total_time_min"] = df["duration_min"] + df["wait_time_dest_min"]

        # extract modes
        df = unpack_modes_from_json(df, "mode_durations_json")

        df["transfers"] = df["mode_durations_json"].apply(transfers_from_json)

        # Export min, mean, max, and median duration and wait time
        summary = {
            "dataset": dataset,
            "min_duration": float(f"{df['duration_min'].min():.2f}"),
            "mean_duration": float(f"{df['duration_min'].mean():.2f}"),
            "max_duration": float(f"{df['duration_min'].max():.2f}"),
            "median_duration": float(f"{df['duration_min'].median():.2f}"),
            "min_wait_time": float(f"{df['wait_time_dest_min'].min():.2f}"),
            "mean_wait_time": float(f"{df['wait_time_dest_min'].mean():.2f}"),
            "max_wait_time": float(f"{df['wait_time_dest_min'].max():.2f}"),
            "median_wait_time": float(f"{df['wait_time_dest_min'].median():.2f}"),
            "median_transfers": int(df["transfers"].median()),
            "max_transfers": int(df["transfers"].max()),
        }

        summaries.append(summary)

        plot_columns = [
            "duration_min",
            "wait_time_dest_min",
            "total_time_min",
        ]

        labels = ["Travel time (min)", "Wait time (min)", "Total duration (min)"]

        attribution_text = "KDS, OpenStreetMap"
        font_size = 10

        for i, plot_col in enumerate(plot_columns):
            fp = results_path / f"maps/{dataset}_{plot_col}.png"

            title = f"{labels[i]} to {dataset.split("_")[-1]} nearest {dataset.split("_")[0]} by public transport"

            plot_traveltime_results(
                df,
                plot_col,
                attribution_text,
                font_size,
                title,
                fp,
            )

        no_results = df[df["duration"].isna()].copy()
        if not no_results.empty:
            fp_no_results = results_path / f"maps/{dataset}_no_results.png"
            title_no_results = f"Locations with no results for {dataset.split('_')[-1]} nearest {dataset.split('_')[0]} by public transport"

            plot_no_connection(
                no_results,
                study_area,
                attribution_text,
                font_size,
                title_no_results,
                fp_no_results,
            )

        # export to geoparquet
        all_columns = df.columns.tolist()
        keep_cols = [
            "source_id",
            "target_id",
            "startTime",
            "arrival_time",
            "waitingTime",
            "walkDistance",
            "abs_dist",
            "duration_min",
            "wait_time_dest_min",
            "total_time_min",
            "transfers",
            "geometry",
        ]
        keep_cols.extend([col for col in all_columns if col.endswith("_duration")])
        df["geometry"] = gpd.points_from_xy(df["from_lon"], df["from_lat"])
        gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
        gdf.to_crs("EPSG:25832", inplace=True)
        gdf[keep_cols].to_parquet(
            results_path / f"data/{dataset}_otp_geo.parquet",
            index=False,
            engine="pyarrow",
        )

# %%
# Convert summaries to DataFrame
summary_df = pd.DataFrame(summaries)
summary_df.set_index("dataset", inplace=True)

rows_to_style = [
    "mean_duration",
    "max_duration",
    "median_duration",
    "mean_wait_time",
    "max_wait_time",
    "median_wait_time",
    "median_transfers",
    "max_transfers",
]  # or any list of index values you want


styled_table = (
    summary_df.T.style.apply(
        highlight_max_traveltime,
        axis=1,
        subset=(
            rows_to_style,
            summary_df.T.columns,
        ),  # style only these rows for all columns
    )
    .apply(
        highlight_min_traveltime,
        axis=1,
        subset=(
            rows_to_style,
            summary_df.T.columns,
        ),  # style only these rows for all columns
    )
    .format("{:.2f}")
    .set_table_styles(
        [
            {"selector": "th", "props": [("font-weight", "bold")]},
        ]
    )
    .set_properties(**{"text-align": "left", "font-size": "12px", "width": "100px"})
    .set_caption("Travel times and wait times for public transport to nearest services")
    .set_table_attributes('style="width: 50%; border-collapse: collapse;"')
)

styled_table


# %%

summary_df.to_csv(
    results_path / "data/service_access_summary.csv", index=True, float_format="%.2f"
)

styled_table.to_html(
    results_path / "data/service_access_summary.html",
    table_attributes='style="width: 50%; border-collapse: collapse;"',
)


# %%


# %%
