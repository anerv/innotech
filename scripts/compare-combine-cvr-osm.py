# %%

# COMPARISON OF DESTINATION DATA FOR CVR AND OSM DATA

# %%

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
from matplotlib_scalebar.scalebar import ScaleBar
from src.helper_functions import (
    highlight_nan,
    highlight_max,
    aggregate_points_by_distance,
    plot_destinations,
    plot_destinations_combined,
    plot_destinations_combined_subplot,
    create_hex_grid,
    count_destinations_in_hex_grid,
    plot_hex_summaries,
)

# Mapping between destination types and subcategories
destination_to_cvr = {
    "doctors": ["doctor-gp", "doctor-specialist", "dentist"],
    "pharmacies": ["pharmacy"],
    "nurseries/kindergartens": ["nursery", "kindergarten"],
    "schools": ["school"],
    "recreation": ["theatre", "library", "sports_facility", "fitness", "movie_theater"],
    "shops": ["grocery_store", "supermarket", "discount_store"],
}

destination_to_osm = {
    "doctors": ["doctor-gp", "dentist"],
    "pharmacies": ["pharmacy"],
    "nurseries/kindergartens": ["nursery", "kindergarten"],
    "schools": ["school"],
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

osm_color = "#EE7733"
cvr_color = "#009988"

# %%
# Load the data
cvr_addresses = gpd.read_file("../data/processed/cvr/cvr-destinations-w-address.gpkg")
cvr_all = gpd.read_file("../data/processed/cvr/cvr-destinations-all.gpkg")

osm_destinations = gpd.read_file("../data/processed/osm/all_osm_destinations.gpkg")

cvr_addresses.sort_values("destination_type", inplace=True)
cvr_all.sort_values("destination_type", inplace=True)
osm_destinations.sort_values("destination_type", inplace=True)

# %%
# Compare number of destinations in each category
destinations_compare = pd.DataFrame(
    {
        "cvr_addresses": cvr_addresses["destination_type"].value_counts(),
        "cvr_all": cvr_all["destination_type"].value_counts(),
        "osm": osm_destinations["destination_type"].value_counts(),
    }
)

# Set the name of the index
destinations_compare.index.name = "destination_type"

# Reset the index to move the index into columns
destinations_compare_reset = destinations_compare.reset_index()

# Rename the columns to include the index name
destinations_compare_reset.columns = [destinations_compare.index.name] + list(
    destinations_compare.columns
)


destinations_compare_reset.to_csv(
    "../results/data/cvr-osm-comparison-subcategory.csv", index=False
)


# Style
def replace_nan_with_dash(val):
    return "-" if pd.isna(val) else val


styled_table = (
    destinations_compare_reset.style.apply(
        highlight_nan, subset=["cvr_addresses", "cvr_all", "osm"], axis=1
    )
    .apply(highlight_max, subset=["cvr_addresses", "cvr_all", "osm"], axis=1)
    .format(replace_nan_with_dash)  # Replace NaN with '-'
    .hide(axis="index")  # Hide the index column
    .set_table_styles(
        [
            {"selector": "th", "props": [("font-weight", "bold")]},
            {
                "selector": ".col0",
                "props": [("font-weight", "bold")],
            },  # Bold header for 'destination_type'
            {
                "selector": ".col0",
                "props": [("font-weight", "bold")],
            },  # Bold values for 'destination_type'
        ]
    )
    .set_properties(**{"text-align": "left", "font-size": "12px", "width": "100px"})
    .set_caption(
        "Comparison of destination types between CVR (w. addresses), CVR (all) and OSM data sets"
    )
    .set_table_attributes('style="width: 50%; border-collapse: collapse;"')
)

styled_table
# %%
# Export the styled table to HTML
html = styled_table.to_html()

html_file = "../results/data/cvr-osm-comparison-subcategory.html"
with open(html_file, "w") as f:
    f.write(html)
    f.close()
# %%
# Compare number of destinations in each main category
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

# Set the name of the index
destinations_compare_main.index.name = "destination_type_main"

# Reset the index to move the index into columns
destinations_compare_main_reset = destinations_compare_main.reset_index()

# Rename the columns to include the index name
destinations_compare_main_reset.columns = [destinations_compare_main.index.name] + list(
    destinations_compare_main.columns
)

destinations_compare_main_reset.to_csv(
    "../results/data/cvr-osm-comparison-main-category.csv", index=False
)

# %%

styled_table_main = (
    destinations_compare_main_reset.style.apply(
        highlight_nan, subset=["cvr_addresses", "cvr_all", "osm"], axis=1
    )
    .apply(highlight_max, subset=["cvr_addresses", "cvr_all", "osm"], axis=1)
    .format(replace_nan_with_dash)  # Replace NaN with '-'
    .hide(axis="index")  # Hide the index column
    .set_table_styles(
        [
            {"selector": "th", "props": [("font-weight", "bold")]},
            {
                "selector": ".col0",
                "props": [("font-weight", "bold")],
            },  # Bold header for 'destination_type'
            {
                "selector": ".col0",
                "props": [("font-weight", "bold")],
            },  # Bold values for 'destination_type'
        ]
    )
    .set_properties(**{"text-align": "left", "font-size": "12px", "width": "100px"})
    .set_caption(
        "Comparison of destination types between CVR (w. addresses), CVR (all) and OSM data sets"
    )
    .set_table_attributes('style="width: 50%; border-collapse: collapse;"')
)

styled_table_main

# %%

html = styled_table_main.to_html()

html_file = "../results/data/cvr-osm-comparison-maincategory.html"
with open(html_file, "w") as f:
    f.write(html)
    f.close()

# %%
# Export combined spatial data set
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

# Plot destinations for each subcategory for each data set
study_area = gpd.read_file("../data/processed/adm_boundaries/region_sj.gpkg")

for destination_type in osm_destinations["destination_type"].unique():

    fp = f"../results/maps/{destination_type}-osm.png"
    attribution_text = "(C) OSM Contributors"
    color = osm_color
    dest_col = destination_type
    study_area = study_area
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
    color = cvr_color
    dest_col = destination_type
    study_area = study_area
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

# Plot destinations for each main category for each data set
for destination_type in osm_destinations["destination_type_main"].unique():

    fp_type = destination_type.replace("/", "-")

    fp = f"../results/maps/main-{fp_type}-osm.png"
    attribution_text = "(C) OSM Contributors"
    color = osm_color
    dest_col = destination_type
    study_area = study_area
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

for destination_type in cvr_addresses["destination_type_main"].unique():

    fp_type = destination_type.replace("/", "-")

    fp = f"../results/maps/main-{fp_type}-cvr.png"
    attribution_text = "(C) CVR"
    color = cvr_color
    dest_col = destination_type
    study_area = study_area
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

# Make combined maps for each main category
for destination_type in osm_cvr_combined["destination_type_main"].unique():

    fp_type = destination_type.replace("/", "-")

    fp = f"../results/maps/main-{fp_type}-osm-cvr.png"
    attribution_text = "(C) OSM, CVR"
    color1 = osm_color
    color2 = cvr_color
    dest_col = destination_type
    study_area = study_area
    font_size = 10
    title = f"{destination_type.replace('_', ' ').title()}"
    destination_col = "destination_type_main"

    plot_destinations_combined(
        osm_destinations,
        cvr_addresses,
        "OSM",
        "CVR",
        study_area,
        destination_col,
        destination_type,
        color1,
        color2,
        font_size,
        fp,
        attribution_text,
        title,
    )


# %%
# Make one map with all main categories
fp = f"../results/maps/main-all-osm-cvr.png"
attribution_text = "(C) OSM, CVR"
color1 = osm_color
color2 = cvr_color
dest_col = destination_type
study_area = study_area
font_size = 10
destination_col = "destination_type_main"

plot_destinations_combined_subplot(
    osm_destinations,
    cvr_addresses,
    "OSM",
    "CVR",
    study_area,
    destination_col,
    color1,
    color2,
    font_size,
    fp,
    attribution_text,
)


# %%

# Aggregate points to a hex grid

# Create hex grid for the region of interest
hex_grid = create_hex_grid(
    study_area, hex_resolution=6, crs="EPSG:25832", buffer_dist=100
)

hex_grid.sindex
region_union = study_area.union_all()
hex_grid = hex_grid[hex_grid.intersects(region_union)]

# %%
# Count number of destinations in each hexagon for OSM and CVR data sets
hex_grid_osm = count_destinations_in_hex_grid(
    osm_destinations, hex_grid, "destination_type_main"
)

hex_grid_cvr = count_destinations_in_hex_grid(
    cvr_addresses, hex_grid, "destination_type_main"
)

combined_grid = hex_grid_osm.merge(
    hex_grid_cvr, on="grid_id", suffixes=("_osm", "_cvr")
)

combined_grid.drop(["geometry_osm"], axis=1, inplace=True)
combined_grid.rename(columns={"geometry_cvr": "geometry"}, inplace=True)

combined_grid.set_index("grid_id", inplace=True)

for destination_type in osm_destinations["destination_type_main"].unique():
    combined_grid[destination_type + "_diff"] = (
        combined_grid[destination_type + "_osm"]
        - combined_grid[destination_type + "_cvr"]
    )

combined_grid.to_file("../results/data/hex-grid-combined-osm-cvr.gpkg", driver="GPKG")


# %%

unique_destinations = destination_to_osm.keys()

for i, destination in enumerate(unique_destinations):

    fp_destination = destination.replace("/", "-")

    fp = f"../results/maps/hex-grid-comparison-{fp_destination}.png"

    plot_hex_summaries(
        combined_grid,
        study_area,
        destination,
        fp,
        figsize=(20, 10),
        font_size=14,
    )


# %%
