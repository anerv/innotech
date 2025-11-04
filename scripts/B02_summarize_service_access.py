# %%

# PROCESS RESULTS FROM SERVICE ACCESS ANALYSIS

import pandas as pd
import geopandas as gpd
import yaml
from pathlib import Path
import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.helper_functions import (
    # highlight_max_traveltime,
    # highlight_min_traveltime,
    unpack_modes_from_json,
    transfers_from_json,
    plot_traveltime_results,
    plot_no_connection,
    summarize_service_access_for_arrival_time,
    summarize_service_access_for_services,
)


# Define the path to the config.yml file
script_path = Path(__file__).resolve()
root_path = script_path.parent.parent
data_path = root_path / "data/processed/destinations"
results_path = root_path / "results"
config_path = root_path / "config.yml"

# Read and parse the YAML file
with open(config_path, "r") as file:
    config_model = yaml.safe_load(file)

    crs = config_model["crs"]


# %%
walkspeed_min = config_model["walk_speed"] * 60  # convert to minutes

# Load address data for original geometries/locations
address_points = gpd.read_parquet(config_model["addresses_fp_all"])

# Load results
services = config_model["services"]

# %%

summaries = []

for service in services:

    service_summaries = []

    arrival_times = service["arrival_time"]

    for i in range(1, int(service["n_neighbors"]) + 1):

        dataset = f"{service['service_type']}_{i}"
        # Process each dataset

        for arrival_time in arrival_times:

            print("-" * 40)
            print(
                f"Processing result dataset: {dataset} with arrival time {arrival_time}"
            )

            fp = (
                results_path
                / f"data/{dataset}_{arrival_time.replace(":","_")}_otp.parquet"
            )
            if not fp.exists():
                print(f"File {fp} does not exist. Skipping.")
                continue
            df = pd.read_parquet(fp)
            print(f"Loaded {len(df)} rows from {fp}")

            # Check for duplicates
            if df.duplicated(subset=["source_id", "target_id"]).any():
                print(f"Duplicates found in {dataset}. Dropping duplicates.")
                df = df.drop_duplicates(subset=["source_id", "target_id"])

            # Fill out rows where source and target are the same
            df.loc[df["source_id"] == df["target_id"], "duration"] = 0
            df.loc[df["source_id"] == df["target_id"], "waitingTime"] = 0
            df.loc[df["source_id"] == df["target_id"], "walkDistance"] = 0
            df.loc[df["source_id"] == df["target_id"], "startTime"] = (
                config_model["travel_date"] + " " + arrival_time
            )

            # Convert duration to minutes
            df["duration_min"] = df["duration"] / 60

            df["startTime"] = pd.to_datetime(df["startTime"]).dt.strftime(
                "%Y-%m-%d %H:%M"
            )

            df["arrival_time"] = pd.to_datetime(df["startTime"]) + pd.to_timedelta(
                df["duration_min"], unit="m"
            )

            arrival_deadline = pd.to_datetime(
                f"{config_model['travel_date']} {arrival_time}"
            )

            # check that all arrival times are less than or equal to the arrival deadline
            if (df["arrival_time"] > arrival_deadline).any():
                print(
                    f"Warning: Some arrival times in {dataset} exceed the deadline of {arrival_deadline}."
                )

            result_count = df[df["duration"].notna()].shape[0]
            print(f"{result_count} solutions found in {dataset} with {len(df)} rows.")

            # extract modes
            df = unpack_modes_from_json(df, "mode_durations_json")

            # count only walk
            mode_cols = [col for col in df.columns if col.endswith("_duration")]
            non_walk_modes = [col for col in mode_cols if col != "walk_duration"]

            count_only_walk = ((df[non_walk_modes] == 0).all(axis=1)).sum()
            percent_only_walk = (count_only_walk / len(df)) * 100
            print(
                f"Percent of trips using only walking for {dataset}: {percent_only_walk:.2f}%"
            )

            df["transfers"] = df["mode_durations_json"].apply(transfers_from_json)

            if config_model["walk_threshold"]:
                # identify trips where walk distance exceeds threshold
                walk_threshold = config_model["walk_threshold"]
                excessive_walks = df[df["walkDistance"] > walk_threshold].shape[0]

                print(
                    f"{excessive_walks} trips ({(excessive_walks / len(df)) * 100:.2f}%) have walk distance exceeding the threshold of {walk_threshold} meters in {dataset}."
                )
                print("Setting these trips to no solution.")
                # set these trips to no solution # nan for duration, duration_min, walkDistance, arrival_time, all duration columns,
                df.loc[
                    df["walkDistance"] > walk_threshold,
                    [
                        "duration",
                        "duration_min",
                        "waitingTime",
                        "walkDistance",
                        "arrival_time",
                        "mode_durations_json",
                    ]
                    + non_walk_modes,
                ] = np.nan

            # Count sources with no results
            no_results_count = df[df["duration"].isna()].shape[0]
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
                "arrival_time": arrival_time,
            }

            service_summaries.append(summary)

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
            gdf.to_crs(crs, inplace=True)
            gdf[keep_cols].to_parquet(
                results_path
                / f"data/{dataset}_{arrival_time.replace(":","_")}_otp_geo.parquet",
                index=False,
                engine="pyarrow",
            )

            # Merge travel times with address points to get original locations (not access points)
            df.drop(columns=["geometry"], inplace=True)

            address_travel_times = pd.merge(
                df,
                address_points[["adresseIdentificerer", "adgangspunkt", "geometry"]],
                left_on="source_id",
                right_on="adresseIdentificerer",
                how="left",
            )

            address_travel_times.drop_duplicates(inplace=True)

            assert (
                address_travel_times["adgangspunkt"].notna().all()
            ), "Some travel time results were not matched with an address. Please check the address data."

            address_travel_times = gpd.GeoDataFrame(
                address_travel_times,
                geometry="geometry",
                crs=crs,
            )

            address_travel_times[keep_cols].to_parquet(
                results_path
                / f"data/{dataset}_{arrival_time.replace(":","_")}_addresses_otp_geo.parquet",
                index=False,
                engine="pyarrow",
            )

            # get travel times for all unique addresses - includes multiple data points for the same locations for apartment buildings etc.
            all_addresses_travel_times = pd.merge(
                address_points[["adresseIdentificerer", "adgangspunkt", "geometry"]],
                address_travel_times,
                right_on="adgangspunkt",
                left_on="adgangspunkt",
                how="left",
                suffixes=("", "_travel_times"),
            )

            all_addresses_travel_times = all_addresses_travel_times[
                all_addresses_travel_times.source_id.notna()
            ]

            keep_cols.extend(
                [
                    "adresseIdentificerer",
                    "adgangspunkt",
                ]
            )

            all_addresses_travel_times = gpd.GeoDataFrame(
                all_addresses_travel_times[keep_cols],
                geometry="geometry",
                crs=crs,
            )

            all_addresses_travel_times.to_parquet(
                results_path
                / f"data/{dataset}_{arrival_time.replace(":","_")}_addresses_all_otp_geo.parquet",
                index=False,
                engine="pyarrow",
            )

    summaries.append(service_summaries)

# %%

# Summarize arrival times across all services

all_arrival_times = set()

for service in services:
    arrival_times = service["arrival_time"]
    all_arrival_times.update(arrival_times)

all_arrival_times = sorted(list(all_arrival_times))

summarize_service_access_for_arrival_time(summaries, all_arrival_times, results_path)

# %%

# Summarize for each service across all arrival times

summarize_service_access_for_services(summaries, results_path)

# %%

# Plot travel time results

# load study area for plotting

study_area = gpd.read_file(config_model["study_area_config"]["regions"]["outputpath"])

services = config_model["services"]

for service in services:

    for i in range(1, int(service["n_neighbors"]) + 1):

        dataset = f"{service['service_type']}_{i}"

        for arrival_time in arrival_times:

            gdf = gpd.read_parquet(
                results_path
                / f"data/{dataset}_{arrival_time.replace(":","_")}_otp_geo.parquet"
            )
            # Process each dataset

            plot_columns = [
                "duration_min",
                "wait_time_dest_min",
                "total_time_min",
            ]

            labels = ["Travel time (min)", "Wait time (min)", "Total duration (min)"]

            attribution_text = "KDS, OpenStreetMap"
            font_size = 10

            for e, plot_col in enumerate(plot_columns):
                fp = (
                    results_path
                    / f"maps/{dataset}_{arrival_time.replace(":","_")}_{plot_col}.png"
                )

                label = dataset.rsplit("_", 1)[0]

                title = f"{labels[e]} to {dataset.split("_")[-1]}. nearest {label.replace("_", " ")} with arrival time {arrival_time}"

                plot_traveltime_results(
                    gdf,
                    plot_col,
                    study_area,
                    attribution_text,
                    font_size,
                    title,
                    fp,
                )

            no_results = gdf[(gdf["duration_min"].isna()) & (gdf.abs_dist > 0)].copy()
            if not no_results.empty:
                fp_no_results = (
                    results_path
                    / f"maps/{dataset}_{arrival_time.replace(":","_")}_no_results.png"
                )
                title_no_results = f"Locations with no results for {dataset.split('_')[-1]}. nearest {label.replace("_", " ")} with arrival time {arrival_time}"

                plot_no_connection(
                    no_results,
                    study_area,
                    attribution_text,
                    font_size,
                    title_no_results,
                    fp_no_results,
                )

# %%


for service in services:

    time_dist_ratios_all = {}

    arrival_times = service["arrival_time"]

    # for i in range(1, int(service["n_neighbors"]) + 1):

    dataset = f"{service['service_type']}_{1}"

    service_time_dist_ratios = {}

    fig, axes = plt.subplots(1, len(arrival_times), figsize=(20, 6))

    axes = axes.flatten()

    for i, arrival_time in enumerate(arrival_times):

        gdf = gpd.read_parquet(
            results_path
            / f"data/{dataset}_{arrival_time.replace(':','_')}_otp_geo.parquet"
        )

        gdf["distance_time_ratio"] = gdf["abs_dist"] / gdf["duration_min"]

        service_time_dist_ratios["min"] = gdf.distance_time_ratio.min()
        service_time_dist_ratios["max"] = gdf.distance_time_ratio.max()
        service_time_dist_ratios["mean"] = gdf.distance_time_ratio.mean()
        service_time_dist_ratios["median"] = gdf.distance_time_ratio.median()

        time_dist_ratios_all[arrival_time] = service_time_dist_ratios

        study_area.boundary.plot(ax=axes[i], color="black", linewidth=1)
        gdf.plot(
            ax=axes[i],
            column="distance_time_ratio",
            legend=True,
            legend_kwds={"shrink": 0.5},
            cmap="viridis",
        )

        # TODO: set color scale to be the same for all plots

        axes[i].set_title(f"Arrival time {arrival_time}")
        axes[i].set_axis_off()

        plt.suptitle(
            f"Distance vs. travel time ratio for nearest {service['service_type']} by arrival time",
            fontsize=16,
        )

        plt.tight_layout()

        plt.savefig(
            results_path
            / f"maps/{dataset}_distance_vs_travel_time_ratio_by_arrival_time.png",
            dpi=300,
        )

    times = list(time_dist_ratios_all.keys())
    mins = [v["min"] for v in time_dist_ratios_all.values()]
    means = [v["mean"] for v in time_dist_ratios_all.values()]
    medians = [v["median"] for v in time_dist_ratios_all.values()]
    maxs = [v["max"] for v in time_dist_ratios_all.values()]

    # Create line plot
    plt.figure(figsize=(8, 5))
    plt.plot(times, mins, marker="o", label="Min", linestyle="--", color="blue")
    plt.plot(times, means, marker="o", label="Mean", linestyle="-", color="green")
    plt.plot(times, medians, marker="o", label="Median", linestyle="-.", color="orange")
    plt.plot(times, maxs, marker="o", label="Max", linestyle=":", color="red")

    # Add labels and title
    plt.title("Distance/travel time ratio for nearest " + service["service_type"])
    plt.xlabel("Arrival Time")
    plt.ylabel("Distance/travel time ratio")

    plt.legend(loc="upper left", bbox_to_anchor=(1, 1), frameon=False)
    plt.grid(True)
    sns.despine(bottom=True, left=True)
    plt.tight_layout()
    plt.savefig(
        results_path
        / f"plots/{dataset}_distance_vs_travel_time_ratio_summary_by_arrival_time.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()

# %%

all_stats_travel = {}
all_stats_wait = {}

for service in services:

    arrival_times = service["arrival_time"]

    dataset = f"{service['service_type']}_{1}"

    stats_travel = {}
    stats_wait = {}

    for i, arrival_time in enumerate(arrival_times):

        gdf = gpd.read_parquet(
            results_path
            / f"data/{dataset}_{arrival_time.replace(':','_')}_otp_geo.parquet"
        )

        # Compute summary stats
        stats_travel[arrival_time] = {
            "min": gdf["duration_min"].min(),
            "mean": gdf["duration_min"].mean(),
            "max": gdf["duration_min"].max(),
        }
        stats_wait[arrival_time] = {
            "min": gdf["wait_time_dest_min"].min(),
            "mean": gdf["wait_time_dest_min"].mean(),
            "max": gdf["wait_time_dest_min"].max(),
        }

    all_stats_travel[service["service_type"]] = stats_travel
    all_stats_wait[service["service_type"]] = stats_wait


def plot_single_stat(all_stats, stat, ylabel, title, results_path):
    """Plot a single statistic (min, mean, or max) for each service."""
    plt.figure(figsize=(10, 6))
    for service_type, stats_dict in all_stats.items():
        times = list(stats_dict.keys())
        values = [v[stat] for v in stats_dict.values()]
        plt.plot(times, values, marker="o", label=service_type)

    plt.title(f"{title} ({stat})")
    plt.xlabel("Arrival time")
    plt.ylabel(ylabel)
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1), frameon=False)
    plt.grid(True)
    sns.despine(bottom=True, left=True)
    plt.tight_layout()
    plt.savefig(
        results_path
        / f"plots/{stat}_{ylabel[0:-6].replace(' ', '_').lower()}_by_arrival_time.png",
        dpi=300,
        bbox_inches="tight",
    )


# Plot travel time stats (min, mean, max)
for stat in ["min", "mean", "max"]:
    plot_single_stat(
        all_stats_travel,
        stat,
        "Travel time (min)",
        "Travel time by arrival time",
        results_path,
    )

# Plot wait time stats (min, mean, max)
for stat in ["mean", "max"]:
    plot_single_stat(
        all_stats_wait,
        stat,
        "Wait time (min)",
        "Wait time by arrival time",
        results_path,
    )

plt.show()

# %%

# heatmap showing the arrival-time dependent travel time for each service and location

for service in services:
    arrival_times = service["arrival_time"]

    dataset = f"{service['service_type']}_{1}"

    heatmap_data = pd.DataFrame()

    for i, arrival_time in enumerate(arrival_times):

        gdf = gpd.read_parquet(
            results_path
            / f"data/{dataset}_{arrival_time.replace(':','_')}_otp_geo.parquet"
        )

        temp_df = gdf[["abs_dist", "duration_min"]].copy()
        temp_df["arrival_time"] = arrival_time

        heatmap_data = pd.concat([heatmap_data, temp_df], ignore_index=True)

    # Pivot the data for heatmap
    heatmap_pivot = heatmap_data.pivot_table(
        index="abs_dist",
        columns="arrival_time",
        values="duration_min",
        aggfunc="mean",
    )

    heatmap_pivot.sort_index(inplace=True, ascending=False)

    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(
        heatmap_pivot,
        cmap="viridis",
        cbar_kws={"label": "Travel time"},
    )
    plt.title(
        f"Travel time heatmap for nearest: {service['service_type'].replace('_', ' ').title()}"
    )
    plt.xlabel("Arrival time")
    plt.ylabel("Distance to destination (m)")

    # --- Custom Y-axis ticks ---
    distances = heatmap_pivot.index.values
    ymin, ymax = ax.get_ylim()

    # Generate 10 evenly spaced tick positions along the data index range
    yticks = np.linspace(0, len(distances) - 1, 10)

    # Get the corresponding distance values for those positions
    # ylabels = [int(round(distances[int(i)] / 100) * 100) for i in yticks]
    ylabels = [int(round(distances[int(i)], -2)) for i in yticks]

    # Apply the ticks and labels
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels)

    ax.set_ylim(len(distances), 0)

    # # Ensure the plot orientation is correct (lowest distance at bottom)
    # ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(
        results_path / f"plots/{dataset}_travel_time_heatmap.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()

# %%
# travel time variation

max_service_differences = []

for service in services:

    arrival_times = service["arrival_time"]

    dataset = f"{service['service_type']}_{1}"

    all_arrival_times_df = pd.DataFrame()

    for arrival_time in arrival_times:

        gdf = gpd.read_parquet(
            results_path
            / f"data/{dataset}_{arrival_time.replace(':','_')}_otp_geo.parquet"
        )

        gdf_temp = gdf[["source_id", "duration_min"]].copy()
        gdf_temp["arrival_time"] = arrival_time
        gdf_temp["service_type"] = service["service_type"]

        all_arrival_times_df = pd.concat(
            [all_arrival_times_df, gdf_temp], ignore_index=True
        )

    assert len(all_arrival_times_df) == len(gdf["source_id"].unique()) * len(
        arrival_times
    ), "Merged GeoDataFrame has unexpected length."

    grouped = all_arrival_times_df.groupby("source_id")["duration_min"].agg(
        ["min", "max"]
    )
    grouped[f"max_variation_{service["service_type"]}"] = (
        grouped["max"] - grouped["min"]
    )

    gdf_grouped = gpd.GeoDataFrame(
        grouped,
        geometry=gdf.set_index("source_id").loc[grouped.index, "geometry"],
        crs=crs,
    )

    max_service_differences.append(gdf_grouped)

# plot max variation maps
fig, axes = plt.subplots(2, math.ceil(len(services) / 2), figsize=(15, 8))
axes = axes.flatten()

# remove last unused axis if odd number of services
if len(services) % 2 != 0:
    fig.delaxes(axes[-1])

# set color scale to be the same for all plots
vmin = min(
    gdf[f"max_variation_{service["service_type"]}"].min()
    for gdf, service in zip(max_service_differences, services)
)
vmax = max(
    gdf[f"max_variation_{service["service_type"]}"].max()
    for gdf, service in zip(max_service_differences, services)
)


for i, service in enumerate(services):
    gdf_grouped = max_service_differences[i]
    study_area.boundary.plot(ax=axes[i], color="black", linewidth=1)
    gdf_grouped.plot(
        ax=axes[i],
        column=f"max_variation_{service["service_type"]}",
        legend=True,
        vmin=vmin,
        vmax=vmax,
        markersize=1,
        legend_kwds={"shrink": 0.5},
        cmap="viridis",
    )
    axes[i].set_title(f"{service['service_type'].replace('_',' ').title()}")
    axes[i].set_axis_off()

plt.suptitle("Max travel time variation by service type", fontsize=16)
plt.tight_layout()
plt.savefig(
    results_path / f"maps/all_services_max_travel_time_variation.png",
    dpi=300,
)

# %%
