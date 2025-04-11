# %%

# COMPARISON OF DESTINATION DATA FOR CVR AND OSM DATA

# %%

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
from src.helper_functions import (
    highlight_nan,
    highlight_max,
    aggregate_points_by_distance,
)

from matplotlib_scalebar.scalebar import ScaleBar


destination_to_cvr = {
    "doctor": ["doctor-gp", "doctor-specialist", "dentist"],
    "pharmacy": ["pharmacy"],
    "nursery/kindergarten": ["nursery", "kindergarten"],
    "school": ["school"],
    "recreation": ["theatre", "library", "sports_facility", "fitness", "movie_theater"],
    "shops": ["grocery_store", "supermarket", "discount_store"],
}

destination_to_osm = {
    "doctor": ["doctor-gp", "dentist"],
    "pharmacy": ["pharmacy"],
    "nursery/kindergarten": ["nursery", "kindergarten"],
    "school": ["school"],
    "recreation": [
        "theatre",
        "library",
        "sports_facility",
        "fitness",
        "movie_theater",
        "swimming_hall",
        "football",
        "golf_course",
        "bowling",
        # "forest",
    ],
    "shops": ["grocery_store", "supermarket"],
}


# %%

cvr_addresses = gpd.read_file("../data/processed/cvr/cvr-destinations-w-address.gpkg")
cvr_all = gpd.read_file("../data/processed/cvr/cvr-destinations-all.gpkg")

osm_destinations = gpd.read_file("../data/processed/osm/all_osm_destinations.gpkg")
# %%
cvr_addresses.sort_values("destination_type", inplace=True)
cvr_all.sort_values("destination_type", inplace=True)
osm_destinations.sort_values("destination_type", inplace=True)

# %%

destinations_compare = pd.DataFrame(
    {
        "cvr_addresses": cvr_addresses["destination_type"].value_counts(),
        "cvr_all": cvr_all["destination_type"].value_counts(),
        "osm": osm_destinations["destination_type"].value_counts(),
    }
)

destinations_compare.to_csv(
    "../results/data/cvr-osm-comparison-subcategory.csv", index=True
)

# Apply the styling
styled = (
    destinations_compare.style.apply(
        highlight_nan, subset=["cvr_addresses", "cvr_all", "osm"], axis=1
    )
    .apply(highlight_max, subset=["cvr_addresses", "cvr_all", "osm"], axis=1)
    .set_table_styles([{"selector": "th", "props": [("font-weight", "bold")]}])
    .set_properties(**{"text-align": "left", "font-size": "12px", "width": "100px"})
    .set_caption(
        "Comparison of destination types between CVR (w. addresses), CVR (all) and OSM data sets"
    )
    .set_table_attributes('style="width: 50%; border-collapse: collapse;"')
)

styled
# %%

cvr_addresses["destination_type_main"] = cvr_addresses["destination_type"].map(
    lambda x: next(
        (key for key, values in destination_to_cvr.items() if x in values), None
    )
)

cvr_all["destination_type_main"] = cvr_all["destination_type"].map(
    lambda x: next(
        (key for key, values in destination_to_cvr.items() if x in values), None
    )
)

osm_destinations["destination_type_main"] = osm_destinations["destination_type"].map(
    lambda x: next(
        (key for key, values in destination_to_osm.items() if x in values), None
    )
)

osm_destinations.sort_values("destination_type_main", inplace=True)
cvr_all.sort_values("destination_type_main", inplace=True)
cvr_addresses.sort_values("destination_type_main", inplace=True)

destinations_compare_main = pd.DataFrame(
    {
        "cvr_addresses": cvr_addresses["destination_type_main"].value_counts(),
        "cvr_all": cvr_all["destination_type_main"].value_counts(),
        "osm": osm_destinations["destination_type_main"].value_counts(),
    }
)

destinations_compare_main.to_csv(
    "../results/data/cvr-osm-comparison-main-category.csv", index=True
)

styled_main = (
    destinations_compare_main.style.apply(
        highlight_nan, subset=["cvr_addresses", "cvr_all", "osm"], axis=1
    )
    .apply(highlight_max, subset=["cvr_addresses", "cvr_all", "osm"], axis=1)
    .set_table_styles([{"selector": "th", "props": [("font-weight", "bold")]}])
    .set_properties(**{"text-align": "left", "font-size": "12px", "width": "100px"})
    .set_caption(
        "Comparison of destination types between CVR (w. addresses), CVR (all) and OSM data sets"
    )
    .set_table_attributes('style="width: 50%; border-collapse: collapse;"')
)

styled_main

# %%
osm_destinations["source"] = "osm"
cvr_addresses["source"] = "cvr"
osm_cvr_combined = gpd.GeoDataFrame(
    pd.concat(
        [
            osm_destinations[
                ["destination_type", "destination_type_main", "source", "geometry"]
            ],
            cvr_addresses[
                ["destination_type", "destination_type_main", "source", "geometry"]
            ],
        ],
        ignore_index=True,
        sort=False,
    )
)
assert len(osm_cvr_combined) == len(osm_destinations) + len(cvr_addresses)

osm_cvr_combined.to_file("../results/data/osm-cvr-combined.gpkg", driver="GPKG")

# %%
#  Collapse points in same category within XXX distance if they have the same main destination type

aggregated_gdf = aggregate_points_by_distance(osm_cvr_combined, distance_threshold=300)

aggregated_gdf.to_file(
    "../results/data/osm-cvr-combined-aggregated.gpkg", driver="GPKG"
)

# %%

# TODO: Make maps for each category and sub-category - sep and combined for OSM and CVR?

# Loop through each destination type and create a map for osm and for cvr and combined

region_sj = gpd.read_file("../data/processed/adm_boundaries/region_sj.gpkg")


def plot_destinations(
    data,
    study_area,
    destination_col,
    destination,
    color,
    font_size,
    fp,
    attribution_text,
    title,
    figsize=(7, 7),
    markersize=10,
):

    _, ax = plt.subplots(figsize=figsize)

    label = destination.replace("_", " ").title()

    study_area.plot(ax=ax, color="white", edgecolor="black", linewidth=0.5)

    data[data[destination_col] == destination].plot(
        ax=ax, color=color, markersize=markersize, label=label, legend=True
    )

    # TODO: fix legend position so that it is aligned with scale bar and attribution text
    ax.legend(
        loc="lower left",
        fontsize=font_size,
        # title_fontsize=10,
        # title="OSM",
        markerscale=2,
        frameon=False,
        bbox_to_anchor=(-0.1, -0.01),
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
            location="lower center",
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

    plt.show()

    plt.savefig(
        fp,
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


for destination_type in osm_destinations["destination_type"].unique():

    fp = f"../results/maps/{destination_type}-osm.png"
    attribution_text = "(C) OSM Contributors"
    color = "red"
    dest_col = destination_type
    study_area = region_sj
    font_size = 10
    title = f"OSM {destination_type.replace('_', ' ').title()}"
    destination_col = "destination_type"

    plot_destinations(
        osm_destinations,
        study_area,
        destination_col,
        destination_type,
        color,
        font_size,
        fp,
        attribution_text,
        title,
    )


for destination_type in cvr_addresses["destination_type"].unique():

    fp = f"../results/maps/{destination_type}-cvr.png"
    attribution_text = "(C) CVR"
    color = "blue"
    dest_col = destination_type
    study_area = region_sj
    font_size = 10
    title = f"CVR {destination_type.replace('_', ' ').title()}"
    destination_col = "destination_type"

    plot_destinations(
        cvr_addresses,
        study_area,
        destination_col,
        destination_type,
        color,
        font_size,
        fp,
        attribution_text,
        title,
    )

# %%

for destination_type in osm_destinations["destination_type_main"].unique():

    fp_type = destination_type.replace("/", "-")

    fp = f"../results/maps/main-{fp_type}-osm.png"
    attribution_text = "(C) OSM Contributors"
    color = "red"
    dest_col = destination_type
    study_area = region_sj
    font_size = 10
    title = f"OSM {destination_type.replace('_', ' ').title()}"
    destination_col = "destination_type_main"

    plot_destinations(
        osm_destinations,
        study_area,
        destination_col,
        destination_type,
        color,
        font_size,
        fp,
        attribution_text,
        title,
    )

# %%

for destination_type in cvr_addresses["destination_type_main"].unique():

    fp_type = destination_type.replace("/", "-")

    fp = f"../results/maps/main-{fp_type}-cvr.png"
    attribution_text = "(C) CVR"
    color = "blue"
    dest_col = destination_type
    study_area = region_sj
    font_size = 10
    title = f"CVR {destination_type.replace('_', ' ').title()}"
    destination_col = "destination_type_main"

    plot_destinations(
        cvr_addresses,
        study_area,
        destination_col,
        destination_type,
        color,
        font_size,
        fp,
        attribution_text,
        title,
    )

# %%
for destination_type in osm_cvr_combined["destination_type_main"].unique():

    pass

# %%


# TODO: Make subplot with all categories for osm and cvr

# TODO: Aggregate to grid - count number of destinations in each grid cell


# %%
