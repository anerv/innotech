# %%

# COMPARISON OF DESTINATION DATA FOR CVR AND OSM DATA

# %%

import pandas as pd
import geopandas as gpd
from src.helper_functions import (
    highlight_nan,
    highlight_max,
    aggregate_points_by_distance,
)
import matplotlib.pyplot as plt

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

destinations_compare.to_csv("../results/cvr-osm-comparison-subcategory.csv", index=True)

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
    "../results/cvr-osm-comparison-main-category.csv", index=True
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

osm_cvr_combined.to_file("../results/osm-cvr-combined.gpkg", driver="GPKG")

# %%
#  Collapse points in same category within XXX distance if they have the same main destination type

aggregated_gdf = aggregate_points_by_distance(osm_cvr_combined, distance_threshold=300)

aggregated_gdf.to_file("../results/osm-cvr-combined-aggregated.gpkg", driver="GPKG")

# TODO: Make maps for each category and sub-category - sep and combined for OSM and CVR?

# TODO: Aggregate to grid - count number of destinations in each grid cell


# %%
