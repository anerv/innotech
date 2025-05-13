# %%

# PREPARE OSM DATA FOR OTP

import os
from pathlib import Path
import yaml
import geopandas as gpd
import subprocess
from src.helper_functions import remove_z

with open(r"../config-data-prep.yml", encoding="utf-8") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    study_area_fp = parsed_yaml_file["study_area_fp"]
    study_area_name = parsed_yaml_file["study_area_name"]

# %%

datafolder = Path("/Users/anerv/repositories/innotech/data")
input_pbf = datafolder / "input/osm/denmark-latest.osm.pbf"
output_pbf = datafolder / "processed/osm/osm_study_area.pbf"
clipfile = datafolder / f"processed/adm_boundaries/study_area.geojson"


# %%

# make geojson of the study area
study_area = gpd.read_file(study_area_fp)

study_area["geometry"] = study_area["geometry"].apply(remove_z)

study_area.to_crs(epsg=4326, inplace=True)

study_area.to_file(clipfile, driver="GeoJSON")

# %%
# check to see if osmium is available
batcmd = "osmium --version"
result = subprocess.check_output(batcmd, shell=True)
print(result.decode("utf-8"))

# %%
# extract osm data for the study area
os.system(f"osmium extract -p {clipfile} -o {output_pbf} {input_pbf}")

# %%
