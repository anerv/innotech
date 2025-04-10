# %%

# COMPARISON OF DESTINATION DATA FOR CVR AND OSM DATA

# %%

import pandas as pd
import geopandas as gpd
from src.helper_functions import highlight_nan, highlight_max
import matplotlib.pyplot as plt

destination_to_cvr = {
    "doctor": ["doctor-gp", "doctor-specialist", "dentist"],
    "pharmacy": ["pharmacy"],
    "nursery/kindergarten": ["nursery", "kindergarten"],
    "school": ["school"],
    "recreation": ["theatre", "library", "sports_facility", "fitness", "movie_theater"],
    "shops": ["grocery_store", "supermarket"],
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
# TODO: Compare for main categories

# TODO: Make maps for each category and sub-category - sep and combined for OSM and CVR?

# TODO: Make combined data set

# TODO: Collapse points in same category within XXX distance

# %%
