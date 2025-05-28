# %%

# COMPARISON OF DESTINATION DATA FOR CVR AND OSM DATA

import pandas as pd
import geopandas as gpd
import os
import sys
import yaml

os.environ["GDAL_DATA"] = os.path.join(
    f"{os.sep}".join(sys.executable.split(os.sep)[:-1]), "Library", "share", "gdal"
)
from src.helper_functions import (
    highlight_nan,
    highlight_max,
    plot_destinations,
    plot_destinations_combined,
    plot_destinations_combined_subplot,
    create_hex_grid,
    count_destinations_in_hex_grid,
    plot_hex_summaries,
    highlight_next_max,
    replace_nan_with_dash,
    count_destinations_in_municipalities,
)

with open(r"../config.yml", encoding="utf-8") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    osm_export_types = parsed_yaml_file["osm_export_types"]
    cvr_export_types = parsed_yaml_file["cvr_export_types"]

    sub_adm_boundaries_fp = parsed_yaml_file["sub_adm_boundaries_fp"]
    study_area_fp = parsed_yaml_file["study_area_fp"]

    cvr_destinations_fp = parsed_yaml_file["cvr_destinations_fp"]
    cvr_destinations_all_fp = parsed_yaml_file["cvr_destinations_all_fp"]

    osm_destinations_fp = parsed_yaml_file["osm_destinations_fp"]


# %%
# Mapping between service types and subcategories
# sub_service_to_main = {
#     "doctor": ["doctor-gp"],
#     "dentist": ["dentist"],
#     "pharmacy": ["pharmacy"],
#     "kindergarten-nursery": [
#         "kindergarten",
#         "nursery",
#     ],
#     "school": ["school"],
#     "library": ["library"],
#     "sports_facility": ["sports_facility"],
#     "shop": ["supermarket", "discount_supermarket"],
#     "train_station": ["train_station"],
# }

osm_color = "#EE7733"
cvr_color = "#009988"


# Plot services for each subcategory for each data set
study_area = gpd.read_file(study_area_fp)


# %%
# Load the data
cvr_addresses = gpd.read_file(cvr_destinations_fp)
cvr_all = gpd.read_file(cvr_destinations_all_fp)

osm_destinations = gpd.read_file(osm_destinations_fp)

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
    "../results/destination_data_evaluation/cvr-osm-comparison-subcategory.csv",
    index=False,
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

html_file = "../results/destination_data_evaluation/cvr-osm-comparison-subcategory.html"
with open(html_file, "w") as f:
    f.write(html)
    f.close()


# %%
# # Compare number of services in each main category
# cvr_addresses["service_type_main"] = cvr_addresses["service_type"].map(
#     lambda x: next(
#         (key for key, values in sub_service_to_main.items() if x in values), None
#     )
# )

# cvr_all["service_type_main"] = cvr_all["service_type"].map(
#     lambda x: next(
#         (key for key, values in sub_service_to_main.items() if x in values), None
#     )
# )

# osm_destinations["service_type_main"] = osm_destinations["service_type"].map(
#     lambda x: next(
#         (key for key, values in sub_service_to_main.items() if x in values), None
#     )
# )

# osm_destinations.sort_values("service_type_main", inplace=True)
# cvr_all.sort_values("service_type_main", inplace=True)
# cvr_addresses.sort_values("service_type_main", inplace=True)

# destinations_compare_main = pd.DataFrame(
#     {
#         "cvr_addresses": cvr_addresses["service_type_main"].value_counts(),
#         "cvr_all": cvr_all["service_type_main"].value_counts(),
#         "osm": osm_destinations["service_type_main"].value_counts(),
#     }
# )

# # Set the name of the index
# destinations_compare_main.index.name = "service_type_main"

# # Reset the index to move the index into columns
# destinations_compare_main_reset = destinations_compare_main.reset_index()

# # Rename the columns to include the index name
# destinations_compare_main_reset.columns = [destinations_compare_main.index.name] + list(
#     destinations_compare_main.columns
# )

# destinations_compare_main_reset.to_csv(
#     "../results/destination_data_evaluation/cvr-osm-comparison-main-category.csv",
#     index=False,
# )

# styled_table_main = (
#     destinations_compare_main_reset.style.apply(
#         highlight_nan, subset=["cvr_addresses", "cvr_all", "osm"], axis=1
#     )
#     .apply(highlight_max, subset=["cvr_addresses", "cvr_all", "osm"], axis=1)
#     .apply(highlight_next_max, subset=["cvr_addresses", "cvr_all", "osm"], axis=1)
#     .format(replace_nan_with_dash)  # Replace NaN with '-'
#     .hide(axis="index")  # Hide the index column
#     .set_table_styles(
#         [
#             {"selector": "th", "props": [("font-weight", "bold")]},
#             {
#                 "selector": ".col0",
#                 "props": [("font-weight", "bold")],
#             },  # Bold header for 'service_type'
#             {
#                 "selector": ".col0",
#                 "props": [("font-weight", "bold")],
#             },  # Bold values for 'service_type'
#         ]
#     )
#     .set_properties(**{"text-align": "left", "font-size": "12px", "width": "100px"})
#     .set_caption(
#         "Comparison of service types between CVR (w. addresses), CVR (all) and OSM data sets"
#     )
#     .set_table_attributes('style="width: 50%; border-collapse: collapse;"')
# )

# styled_table_main

# %%

# # Export to HTML
# html = styled_table_main.to_html()

# html_file = (
#     "../results/destination_data_evaluation/cvr-osm-comparison-maincategory.html"
# )
# with open(html_file, "w") as f:
#     f.write(html)
#     f.close()

# %%
# Make combined spatial data set
keep_cols = [
    "nace_code",
    "Adr_id",
    "service_type",
    "source",
    "geometry",
]
osm_destinations["source"] = "osm"
cvr_addresses["source"] = "cvr"
osm_cvr_combined = gpd.GeoDataFrame(
    pd.concat(
        [
            osm_destinations[keep_cols],
            cvr_addresses[keep_cols],
        ],
        ignore_index=True,
        sort=False,
    )
)

assert len(osm_cvr_combined) == len(osm_destinations) + len(cvr_addresses)


# %%

# Make one map with all main categories
fp = f"../results/maps/main-all-osm-cvr.png"
attribution_text = "(C) OSM, CVR"
color1 = osm_color
color2 = cvr_color
destination_col = "service_type"
study_area = study_area
font_size = 10


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
# Count number of services in each hexagon for OSM and CVR data sets + combined
hex_grid_osm = count_destinations_in_hex_grid(
    osm_destinations, hex_grid, "service_type"
)

hex_grid_cvr = count_destinations_in_hex_grid(cvr_addresses, hex_grid, "service_type")


destination_col = "service_type"

all_destinations = set(osm_destinations[destination_col].unique()).union(
    cvr_addresses[destination_col].unique()
)

# Catch issue with destination that only exists in one data set
for service_type in all_destinations:
    if service_type not in osm_destinations[destination_col].unique():
        hex_grid_osm[service_type] = 0
    if service_type not in cvr_addresses[destination_col].unique():
        hex_grid_cvr[service_type] = 0


combined_grid = hex_grid_osm.merge(
    hex_grid_cvr, on="grid_id", suffixes=("_osm", "_cvr")
)

combined_grid.drop(["geometry_osm"], axis=1, inplace=True)
combined_grid.rename(columns={"geometry_cvr": "geometry"}, inplace=True)

combined_grid.set_index("grid_id", inplace=True)


for service_type in all_destinations:

    combined_grid[service_type + "_diff"] = (
        combined_grid[service_type + "_osm"] - combined_grid[service_type + "_cvr"]
    )

combined_grid.to_file(
    "../results/destination_data_evaluation/hex-grid-combined-osm-cvr.gpkg",
    driver="GPKG",
)


# %%

for i, service in enumerate(all_destinations):

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

analyse_destinations_per_municipality = True

if analyse_destinations_per_municipality:

    # Load municipality data
    muni_data = gpd.read_file(sub_adm_boundaries_fp)

    # get munis that intersect with the study area # NOTE: requires high quality data with identical boundaries!
    muni_subset = muni_data[muni_data.intersects(study_area.union_all())].copy()
    muni_subset = muni_subset[["kommunekode", "navn", "geometry"]]

    html_fp = "../results/destination_data_evaluation/municipal-service-counts-service-type.html"
    csv_fp = "../results/destination_data_evaluation/municipal-service-counts-service-type.csv"

    dest_count_main = count_destinations_in_municipalities(
        muni_subset,
        "navn",
        osm_cvr_combined,
        "service_type",
        csv_fp,
        html_fp,
    )


# %%
