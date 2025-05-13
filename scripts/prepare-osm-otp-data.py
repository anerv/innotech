# %%

# PREPARE OSM DATA FOR OTP

import os
from pathlib import Path
import yaml
import geopandas as gpd

with open(r"../config-data-prep.yml", encoding="utf-8") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    study_area_fp = parsed_yaml_file["study_area_fp"]
    study_area_name = parsed_yaml_file["study_area_name"]

# %%

# make geojson of the study area
study_area = gpd.read_file(study_area_fp)

study_area

# check to see if osmium is available
# TODO !osmium --version


# %%


datafolder = Path("/Users/anerv/repositories/innotech/data")
input_pbf = datafolder / "input/osm/denmark-latest.osm.pbf"
output_pbf = datafolder / "processed/osm/region_sj.pbf"
clipfile = datafolder / "processed/adm_boundaries/regionsj.geojson"

# %%
os.system(f"osmium extract -p {clipfile} -o {output_pbf} {input_pbf}")

# %%
import subprocess

batcmd = "osmium --version"
result = subprocess.check_output(batcmd, shell=True)
# %%
