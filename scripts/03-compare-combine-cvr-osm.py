# %%

# COMPARISON OF DESTINATION DATA FOR CVR AND OSM DATA

# TODO:
# Remove unnecessary plots
# Export correct columns
# Export to parquet

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
    highlight_next_max,
    replace_nan_with_dash,
)

# Mapping between service types and subcategories
sub_service_to_main = {
    "doctors": ["doctor-gp"],
    "dentists": ["dentist"],
    "pharmacies": ["pharmacy"],
    "nurseries/kindergartens": ["nursery", "kindergarten"],
    "schools": ["school"],
    "recreation": [
        "library",
        "sports_facility",
    ],
    "shops": ["supermarket", "discount_supermarket"],
}

osm_color = "#EE7733"
cvr_color = "#009988"

# %%
# Load the data
cvr_addresses = gpd.read_file("../data/processed/cvr/cvr-services-w-address.gpkg")
cvr_all = gpd.read_file("../data/processed/cvr/cvr-services-all.gpkg")

osm_destinations = gpd.read_file("../data/processed/osm/all_osm_services.gpkg")

cvr_addresses.sort_values("service_type", inplace=True)
cvr_all.sort_values("service_type", inplace=True)
osm_destinations.sort_values("service_type", inplace=True)

# %%
# Compare number of services in each category
destinations_compare = pd.DataFrame(
    {
        "cvr_addresses": cvr_addresses["service_type"].value_counts(),
        "cvr_all": cvr_all["service_type"].value_counts(),
        "osm": osm_destinations["service_type"].value_counts(),
    }
)

# Set the name of the index
destinations_compare.index.name = "service_type"

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
styled_table = (
    destinations_compare_reset.style.apply(
        highlight_nan, subset=["cvr_addresses", "cvr_all", "osm"], axis=1
    )
    .apply(highlight_max, subset=["cvr_addresses", "cvr_all", "osm"], axis=1)
    .apply(highlight_next_max, subset=["cvr_addresses", "cvr_all", "osm"], axis=1)
    .format(replace_nan_with_dash)  # Replace NaN with '-'
    .hide(axis="index")  # Hide the index column
    .set_table_styles(
        [
            {"selector": "th", "props": [("font-weight", "bold")]},
            {
                "selector": ".col0",
                "props": [("font-weight", "bold")],
            },  # Bold header for 'service_type'
            {
                "selector": ".col0",
                "props": [("font-weight", "bold")],
            },  # Bold values for 'service_type'
        ]
    )
    .set_properties(**{"text-align": "left", "font-size": "12px", "width": "100px"})
    .set_caption(
        "Comparison of service types between CVR (w. addresses), CVR (all) and OSM data sets"
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
# Compare number of services in each main category
cvr_addresses["service_type_main"] = cvr_addresses["service_type"].map(
    lambda x: next(
        (key for key, values in sub_service_to_main.items() if x in values), None
    )
)

cvr_all["service_type_main"] = cvr_all["service_type"].map(
    lambda x: next(
        (key for key, values in sub_service_to_main.items() if x in values), None
    )
)

osm_destinations["service_type_main"] = osm_destinations["service_type"].map(
    lambda x: next(
        (key for key, values in sub_service_to_main.items() if x in values), None
    )
)

osm_destinations.sort_values("service_type_main", inplace=True)
cvr_all.sort_values("service_type_main", inplace=True)
cvr_addresses.sort_values("service_type_main", inplace=True)

destinations_compare_main = pd.DataFrame(
    {
        "cvr_addresses": cvr_addresses["service_type_main"].value_counts(),
        "cvr_all": cvr_all["service_type_main"].value_counts(),
        "osm": osm_destinations["service_type_main"].value_counts(),
    }
)

# Set the name of the index
destinations_compare_main.index.name = "service_type_main"

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
    .apply(highlight_next_max, subset=["cvr_addresses", "cvr_all", "osm"], axis=1)
    .format(replace_nan_with_dash)  # Replace NaN with '-'
    .hide(axis="index")  # Hide the index column
    .set_table_styles(
        [
            {"selector": "th", "props": [("font-weight", "bold")]},
            {
                "selector": ".col0",
                "props": [("font-weight", "bold")],
            },  # Bold header for 'service_type'
            {
                "selector": ".col0",
                "props": [("font-weight", "bold")],
            },  # Bold values for 'service_type'
        ]
    )
    .set_properties(**{"text-align": "left", "font-size": "12px", "width": "100px"})
    .set_caption(
        "Comparison of service types between CVR (w. addresses), CVR (all) and OSM data sets"
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

# TODO: Make sure train stations are included

# Export combined spatial data set
osm_destinations["source"] = "osm"
cvr_addresses["source"] = "cvr"
osm_cvr_combined = gpd.GeoDataFrame(
    pd.concat(
        [
            osm_destinations[
                ["service_type", "service_type_main", "source", "geometry"]
            ],
            cvr_addresses[["service_type", "service_type_main", "source", "geometry"]],
        ],
        ignore_index=True,
        sort=False,
    )
)
assert len(osm_cvr_combined) == len(osm_destinations) + len(cvr_addresses)

osm_cvr_combined.to_file("../results/data/osm-cvr-combined.gpkg", driver="GPKG")

# %%
#  Collapse points in same category within XXX distance if they have the same main service type

aggregated_gdf = aggregate_points_by_distance(osm_cvr_combined, distance_threshold=300)

# TODO: Export correct columns
aggregated_gdf.to_file(
    "../results/data/osm-cvr-combined-aggregated.gpkg", driver="GPKG"
)

# %%

# Plot services for each subcategory for each data set
study_area = gpd.read_file("../data/processed/adm_boundaries/region_sj.gpkg")

for service_type in osm_destinations["service_type"].unique():

    fp = f"../results/maps/{service_type}-osm.png"
    attribution_text = "(C) OSM Contributors"
    color = osm_color
    dest_col = service_type
    study_area = study_area
    font_size = 10
    title = f"OSM {service_type.replace('_', ' ').title()}"
    destination_col = "service_type"

    plot_destinations(
        osm_destinations,
        study_area,
        destination_col,
        service_type,
        color,
        font_size,
        fp,
        attribution_text,
        title,
    )


for service_type in cvr_addresses["service_type"].unique():

    fp = f"../results/maps/{service_type}-cvr.png"
    attribution_text = "(C) CVR"
    color = cvr_color
    dest_col = service_type
    study_area = study_area
    font_size = 10
    title = f"CVR {service_type.replace('_', ' ').title()}"
    destination_col = "service_type"

    plot_destinations(
        cvr_addresses,
        study_area,
        destination_col,
        service_type,
        color,
        font_size,
        fp,
        attribution_text,
        title,
    )

# %%

# Plot services for each main category for each data set
for service_type in osm_destinations["service_type_main"].unique():

    fp_type = service_type.replace("/", "-")

    fp = f"../results/maps/main-{fp_type}-osm.png"
    attribution_text = "(C) OSM Contributors"
    color = osm_color
    dest_col = service_type
    study_area = study_area
    font_size = 10
    title = f"OSM {service_type.replace('_', ' ').title()}"
    destination_col = "service_type_main"

    plot_destinations(
        osm_destinations,
        study_area,
        destination_col,
        service_type,
        color,
        font_size,
        fp,
        attribution_text,
        title,
    )

for service_type in cvr_addresses["service_type_main"].unique():

    fp_type = service_type.replace("/", "-")

    fp = f"../results/maps/main-{fp_type}-cvr.png"
    attribution_text = "(C) CVR"
    color = cvr_color
    dest_col = service_type
    study_area = study_area
    font_size = 10
    title = f"CVR {service_type.replace('_', ' ').title()}"
    destination_col = "service_type_main"

    plot_destinations(
        cvr_addresses,
        study_area,
        destination_col,
        service_type,
        color,
        font_size,
        fp,
        attribution_text,
        title,
    )

# %%

# Make combined maps for each main category
for service_type in osm_cvr_combined["service_type_main"].unique():

    fp_type = service_type.replace("/", "-")

    fp = f"../results/maps/main-{fp_type}-osm-cvr.png"
    attribution_text = "(C) OSM, CVR"
    color1 = osm_color
    color2 = cvr_color
    dest_col = service_type
    study_area = study_area
    font_size = 10
    title = f"{service_type.replace('_', ' ').title()}"
    destination_col = "service_type_main"

    plot_destinations_combined(
        osm_destinations,
        cvr_addresses,
        "OSM",
        "CVR",
        study_area,
        destination_col,
        service_type,
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
dest_col = service_type
study_area = study_area
font_size = 10
destination_col = "service_type_main"

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
# Count number of services in each hexagon for OSM and CVR data sets
hex_grid_osm = count_destinations_in_hex_grid(
    osm_destinations, hex_grid, "service_type_main"
)

hex_grid_cvr = count_destinations_in_hex_grid(
    cvr_addresses, hex_grid, "service_type_main"
)

combined_grid = hex_grid_osm.merge(
    hex_grid_cvr, on="grid_id", suffixes=("_osm", "_cvr")
)

combined_grid.drop(["geometry_osm"], axis=1, inplace=True)
combined_grid.rename(columns={"geometry_cvr": "geometry"}, inplace=True)

combined_grid.set_index("grid_id", inplace=True)

for service_type in osm_destinations["service_type_main"].unique():
    combined_grid[service_type + "_diff"] = (
        combined_grid[service_type + "_osm"] - combined_grid[service_type + "_cvr"]
    )

combined_grid.to_file("../results/data/hex-grid-combined-osm-cvr.gpkg", driver="GPKG")


# %%

unique_destinations = sub_service_to_main.keys()

for i, service in enumerate(unique_destinations):

    fp_destination = service.replace("/", "-")

    fp = f"../results/maps/hex-grid-comparison-{fp_destination}.png"

    plot_hex_summaries(
        combined_grid,
        study_area,
        service,
        fp,
        figsize=(20, 10),
        font_size=14,
    )


# %%
