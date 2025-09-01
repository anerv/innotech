# %%

# COMPARISON OF DESTINATION DATA FOR CVR AND OSM DATA

import pandas as pd
import geopandas as gpd
import os
import sys
import yaml

from src.helper_functions import (
    aggregate_points_by_distance,
)

with open(r"../config.yml", encoding="utf-8") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    cvr_destinations_fp = parsed_yaml_file["cvr_destinations_fp"]

    adm_boundaries_config = parsed_yaml_file["study_area_config"]
    study_area_fp = adm_boundaries_config["regions"]["outputpath"]

    destinations_combined_fp = parsed_yaml_file["destinations_combined_fp"]
    destinations_combined_agg_fp = parsed_yaml_file["destinations_combined_agg_fp"]


# %%

# Load the  data
cvr_destinations = gpd.read_file(cvr_destinations_fp)

osm_destinations = gpd.read_file("../data/processed/osm/all_osm_services.gpkg")

cvr_destinations.sort_values("service_type", inplace=True)

osm_destinations.sort_values("service_type", inplace=True)


# %%

# Make combined spatial data set
keep_cols = [
    "nace_code",
    "Adr_id",
    "vej_pos_lat",
    "vej_pos_lon",
    "service_type",
    "source",
    "geometry",
]
osm_destinations["source"] = "osm"
cvr_destinations["source"] = "cvr"
osm_cvr_combined = gpd.GeoDataFrame(
    pd.concat(
        [
            osm_destinations[keep_cols],
            cvr_destinations[keep_cols],
        ],
        ignore_index=True,
        sort=False,
    )
)

assert len(osm_cvr_combined) == len(osm_destinations) + len(cvr_destinations)
# %%

# EXPORT

osm_cvr_combined = osm_cvr_combined[
    [
        "service_type",
        "nace_code",
        "Adr_id",
        "vej_pos_lat",
        "vej_pos_lon",
        "source",
        "geometry",
    ]
]

osm_cvr_combined.to_parquet(destinations_combined_fp, index=False)

# %%

#  Collapse points in same category within XXX distance if they have the same main service type

aggregated_gdf = aggregate_points_by_distance(
    osm_cvr_combined,
    distance_threshold=100,
    destination_type_column="service_type",
    inherit_columns=[
        "Adr_id",
        "nace_code",
        "vej_pos_lat",
        "vej_pos_lon",
    ],
)


aggregated_gdf.to_parquet(
    destinations_combined_agg_fp,
)

# %%
