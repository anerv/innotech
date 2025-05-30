# %%

# PROCESS RESULTS FROM SERVICE ACCESS ANALYSIS

import pandas as pd
import geopandas as gpd
import yaml
from pathlib import Path
import matplotlib.pyplot as plt
import contextily as cx
from matplotlib_scalebar.scalebar import ScaleBar
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import sys

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


def plot_traveltime_results(df, plot_col, attribution_text, font_size, title, fp=None):
    """
    Plot the results on a map.
    """
    import matplotlib.pyplot as plt
    import geopandas as gpd
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    from matplotlib_scalebar.scalebar import ScaleBar
    import contextily as cx

    # Convert DataFrame to GeoDataFrame
    df["geometry"] = gpd.points_from_xy(df["from_lon"], df["from_lat"])
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    gdf.to_crs("EPSG:25832", inplace=True)

    _, ax = plt.subplots(figsize=(10, 10))

    divider = make_axes_locatable(ax)

    cax = divider.append_axes("right", size="3.5%", pad="1%")
    cax.tick_params(labelsize=font_size)

    gdf.plot(
        ax=ax,
        cax=cax,
        column=plot_col,
        cmap="viridis",
        legend=True,
        markersize=5,
    )

    for spine in cax.spines.values():
        spine.set_visible(False)

    ax.set_title(title, fontsize=font_size + 2, fontdict={"weight": "bold"})

    ax.set_axis_off()

    ax.add_artist(
        ScaleBar(
            dx=1,
            units="m",
            dimension="si-length",
            length_fraction=0.15,
            width_fraction=0.002,
            location="lower left",
            box_alpha=0,
            font_properties={"size": font_size},
        )
    )
    cx.add_attribution(ax=ax, text=attribution_text, font_size=font_size)
    txt = ax.texts[-1]
    txt.set_position([0.99, 0.01])
    txt.set_ha("right")
    txt.set_va("bottom")

    plt.tight_layout()

    if fp:

        plt.savefig(
            fp,
            dpi=300,
            bbox_inches="tight",
        )

    plt.show()
    plt.close()


# %%

# load study area for plotting
study_area = gpd.read_file(config_model["study_area_fp"])

# Load results

services = config_model["services"]

summaries = []

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

        df["startTime"] = pd.to_datetime(df["startTime"]).dt.strftime("%Y-%m-%d %H:%M")

        df["arrival_time"] = pd.to_datetime(df["startTime"]) + pd.to_timedelta(
            df["duration_minutes"], unit="m"
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

        ave_duration = df["duration_minutes"].mean()
        print(f"Average trip duration for {dataset}: {ave_duration:.2f} minutes")

        df["wait_time"] = arrival_deadline - df["arrival_time"]
        df["wait_time_minutes"] = df["wait_time"].dt.total_seconds() / 60
        ave_wait_time = df["wait_time_minutes"].mean()
        print(
            f"Average wait time at destination for {dataset}: {ave_wait_time:.2f} minutes"
        )

        df["duration_wait_time_minutes"] = (
            df["duration_minutes"] + df["wait_time_minutes"]
        )

        # Export min, mean, max, and median duration and wait time
        summary = {
            "dataset": dataset,
            "min_duration": float(f"{df['duration_minutes'].min():.2f}"),
            "mean_duration": float(f"{df['duration_minutes'].mean():.2f}"),
            "max_duration": float(f"{df['duration_minutes'].max():.2f}"),
            "median_duration": float(f"{df['duration_minutes'].median():.2f}"),
            "min_wait_time": float(f"{df['wait_time_minutes'].min():.2f}"),
            "mean_wait_time": float(f"{df['wait_time_minutes'].mean():.2f}"),
            "max_wait_time": float(f"{df['wait_time_minutes'].max():.2f}"),
            "median_wait_time": float(f"{df['wait_time_minutes'].median():.2f}"),
        }

        summaries.append(summary)

        plot_columns = [
            "duration_minutes",
            "wait_time_minutes",
            "duration_wait_time_minutes",
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

        no_results = df[df["duration"].isna()]
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
# %%
# Convert summaries to DataFrame
summary_df = pd.DataFrame(summaries)
summary_df.set_index("dataset", inplace=True)

summary_df.T

# TODO: Style
# For each row, highlight the min values in blue and the max values in orange


summary_df.to_csv(
    results_path / "data/service_access_summary.csv", index=True, float_format="%.2f"
)
# %%


# TODO

# Make maps of the results:
# Travel times for each service


# %%
# TODO: make maps of sources with no results


def plot_no_connection(df, study_area, attribution_text, font_size, title, fp=None):
    """
    Plot the results on a map.
    """
    import matplotlib.pyplot as plt
    import geopandas as gpd
    from matplotlib_scalebar.scalebar import ScaleBar
    import contextily as cx

    # Convert DataFrame to GeoDataFrame
    df["geometry"] = gpd.points_from_xy(df["from_lon"], df["from_lat"])
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    gdf.to_crs("EPSG:25832", inplace=True)

    assert study_area.crs == gdf.crs, "CRS mismatch between study area and GeoDataFrame"

    _, ax = plt.subplots(figsize=(10, 10))

    study_area.plot(
        ax=ax,
        color=None,
        edgecolor="black",
        alpha=0.5,
    )

    gdf.plot(
        ax=ax,
        legend=True,
        markersize=5,
        color="orange",
        edgecolor="orange",
        alpha=0.5,
        legend_kwds={"label": "No connection"},
    )

    ax.set_title(title, fontsize=font_size + 2, fontdict={"weight": "bold"})

    ax.set_axis_off()

    ax.add_artist(
        ScaleBar(
            dx=1,
            units="m",
            dimension="si-length",
            length_fraction=0.15,
            width_fraction=0.002,
            location="lower left",
            box_alpha=0,
            font_properties={"size": font_size},
        )
    )
    cx.add_attribution(ax=ax, text=attribution_text, font_size=font_size)
    txt = ax.texts[-1]
    txt.set_position([0.99, 0.01])
    txt.set_ha("right")
    txt.set_va("bottom")

    plt.tight_layout()

    if fp:

        plt.savefig(
            fp,
            dpi=300,
            bbox_inches="tight",
        )

    plt.show()
    plt.close()


# %%
