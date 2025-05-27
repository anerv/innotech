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
    aggregate_points_by_distance,
)

with open(r"../config-data-prep.yml", encoding="utf-8") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    cvr_destinations_fp = parsed_yaml_file["cvr_destinations_fp"]

    osm_export_types = parsed_yaml_file["osm_export_types"]
    cvr_export_types = parsed_yaml_file["cvr_export_types"]

    sub_adm_boundaries_fp = parsed_yaml_file["sub_adm_boundaries_fp"]
    study_area_fp = parsed_yaml_file["study_area_fp"]

    sub_service_to_main = parsed_yaml_file["sub_service_to_main"]

    destinations_combined_fp = parsed_yaml_file["destinations_combined_fp"]
    destinations_combined_agg_fp = parsed_yaml_file["destinations_combined_agg_fp"]


# %%

# Load the  data
cvr_destinations = gpd.read_file(cvr_destinations_fp)

osm_destinations = gpd.read_file("../data/processed/osm/all_osm_services.gpkg")

cvr_destinations.sort_values("service_type", inplace=True)

osm_destinations.sort_values("service_type", inplace=True)

cvr_destinations["service_type_main"] = cvr_destinations["service_type"].map(
    lambda x: next(
        (key for key, values in sub_service_to_main.items() if x in values), None
    )
)

osm_destinations["service_type_main"] = osm_destinations["service_type"].map(
    lambda x: next(
        (key for key, values in sub_service_to_main.items() if x in values), None
    )
)

# %%

# Make combined spatial data set
keep_cols = [
    "hb_kode",
    "Adr_id",
    "vej_pos_lat",
    "vej_pos_lon",
    "service_type",
    "service_type_main",
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

# only keep services with this main type

# Drop subtypes and keep only main types in exported data set
osm_cvr_combined["service_type"] = osm_cvr_combined["service_type_main"]
osm_cvr_combined.drop(columns=["service_type_main"], inplace=True)


# Drop subtypes and keep only main types in exported data set
osm_cvr_combined.drop(
    osm_cvr_combined[
        (osm_cvr_combined["source"] == "osm")
        & (~osm_cvr_combined["service_type"].isin(osm_export_types))
    ].index,
    inplace=True,
)


osm_cvr_combined.drop(
    osm_cvr_combined[
        (osm_cvr_combined["source"] == "cvr")
        & (~osm_cvr_combined["service_type"].isin(cvr_export_types))
    ].index,
    inplace=True,
)

osm_cvr_combined = osm_cvr_combined[
    [
        "service_type",
        "hb_kode",
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
        "hb_kode",
        "vej_pos_lat",
        "vej_pos_lon",
    ],
)


aggregated_gdf.to_parquet(
    destinations_combined_agg_fp,
)

# %%
