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

### PREPATE OSM DATA FOR OTP

datafolder = Path("/Users/anerv/repositories/innotech/data")
input_pbf = datafolder / "input/osm/denmark-latest.osm.pbf"
output_pbf = datafolder / "otp/osm_study_area.pbf"
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
#### BUILD OTP GRAPH

# TODO: test

otp_folder = Path("/Users/anerv/repositories/innotech/otp")
osm_pbf = otp_folder / "osm_study_area.pbf"
netex_file = otp_folder / "netex"

otp_exists = any(
    f.name == "otp-shaded-2.7.0.jar" for f in otp_folder.iterdir() if f.is_file()
)

netex_zip_exists = any(
    f.name.endswith("NeTEx.zip") for f in otp_folder.iterdir() if f.is_file()
)
osm_pbf_exists = any(
    f.name == "osm_study_area.pbf" for f in otp_folder.iterdir() if f.is_file()
)
config_exists = any(
    f.name == "build-config.json" for f in otp_folder.iterdir() if f.is_file()
)

os.chdir("c:\\Users\\anerv\\repositories\\innotech\\otp\\")

if netex_zip_exists and osm_pbf_exists and config_exists and otp_exists:
    print("All required files are in place, building OTP graph...")
    os.system("java -Xmx2G -jar otp-shaded-2.7.0.jar --build --save .")

else:
    print("Missing input data: Netex zip file or osm pbf file not found in otp folder!")

# %%
