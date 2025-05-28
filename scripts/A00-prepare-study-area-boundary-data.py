# %%

import geopandas as gpd
import yaml
from src.helper_functions import remove_z


with open(r"../config.yml", encoding="utf-8") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    study_area_fp = parsed_yaml_file["study_area_fp"]
    adm_boundaries_fp = parsed_yaml_file["adm_boundaries_fp"]
    study_area_name = parsed_yaml_file["study_area_name"]

    sub_adm_boundaries_fp = parsed_yaml_file["sub_adm_boundaries_fp"]
    sub_study_areas_fp = parsed_yaml_file["sub_study_areas_fp"]


# %%

# Subtract the study area (region) from the administrative boundaries input data

administrative_boundaries = gpd.read_file(adm_boundaries_fp)

region = administrative_boundaries[administrative_boundaries["navn"] == study_area_name]

region = region[["navn", "geometry"]]

region.to_file(study_area_fp)

# %%

# Convert the municipal boundaries to the format expected by the model

municipalities = gpd.read_file(sub_adm_boundaries_fp)

municipalities = municipalities[["id_lokalid", "kommunekode", "geometry"]]

municipalities["geometry"] = municipalities["geometry"].apply(remove_z)

municipalities.to_parquet(sub_study_areas_fp, index=False)
# %%
