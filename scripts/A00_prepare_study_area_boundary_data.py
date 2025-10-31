# %%

import geopandas as gpd
import yaml
from src.helper_functions import remove_z

with open(r"../config.yml", encoding="utf-8") as file:

    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    adm_boundaries_config = parsed_yaml_file["study_area_config"]

    adm_boundaries_fp = adm_boundaries_config["regions"]["inputpath"]

    study_area_fp = adm_boundaries_config["regions"]["outputpath"]

    study_area_name = adm_boundaries_config["regions"]["study_area_name"]

    sub_adm_boundaries_fp = adm_boundaries_config["municipalities"]["inputpath"]
    sub_study_areas_fp = adm_boundaries_config["municipalities"]["outputpath"]


# %%

print(
    "Preparing study area boundary data for study area with names/codes:",
    study_area_name,
)

# Subtract the study area (region) from the administrative boundaries input data

administrative_boundaries = gpd.read_file(adm_boundaries_fp)

region = administrative_boundaries[
    administrative_boundaries[adm_boundaries_config["regions"]["id_column"]].isin(
        study_area_name
    )
]

assert (
    len(region) > 0
), "No matching region found in the administrative boundaries data. Check the study area configuration."

region = region[["navn", "geometry"]]

region.to_file(study_area_fp)

# %%

# Convert the municipal boundaries to the format expected by the model

municipalities = gpd.read_file(sub_adm_boundaries_fp)

municipalities = municipalities[
    [adm_boundaries_config["municipalities"]["id_column"], "geometry"]
]

municipalities["geometry"] = municipalities["geometry"].apply(remove_z)

municipalities.to_parquet(sub_study_areas_fp, index=False)
# %%
