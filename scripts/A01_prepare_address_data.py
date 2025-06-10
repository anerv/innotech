# %%

# Create address data for the project with ids for CVR and geometries

import pandas as pd
import geopandas as gpd
from shapely import wkt
import yaml


with open(r"../config.yml", encoding="utf-8") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    # address_cvr_fp = parsed_yaml_file["address_cvr_fp"]
    addresses_fp_all = parsed_yaml_file["addresses_fp_all"]
    address_bbr_fp = parsed_yaml_file["address_bbr_fp"]
    input_address_fp = parsed_yaml_file["input_address_fp"]
    address_points_fp = parsed_yaml_file["address_points_fp"]
    housenumbers_fp = parsed_yaml_file["housenumbers_fp"]

    study_area_fp = parsed_yaml_file["study_area_fp"]
    adm_boundaries_fp = parsed_yaml_file["adm_boundaries_fp"]
    study_area_name = parsed_yaml_file["study_area_name"]


# %%

if input_address_fp.endswith(".parquet"):

    address = pd.read_parquet(input_address_fp)
    address_points = pd.read_parquet(address_points_fp)
    housenumbers = pd.read_parquet(housenumbers_fp)

elif input_address_fp.endswith(".csv"):
    address = pd.read_csv(input_address_fp, sep=",")
    address_points = pd.read_csv(address_points_fp, sep=",")
    housenumbers = pd.read_csv(housenumbers_fp, sep=",")

else:
    raise ValueError("Input file must be a .parquet or .csv file.")
# %%

address.drop_duplicates(subset=["id_lokalId"], inplace=True)

address_points["geometry"] = address_points["position"].apply(wkt.loads)
address_gdf = gpd.GeoDataFrame(address_points, geometry="geometry", crs="EPSG:25832")

# %%
housenumbers_with_geoms = pd.merge(
    address_gdf[["id_lokalId", "geometry"]],
    housenumbers[["adgangspunkt", "id_lokalId", "vejpunkt"]],
    left_on="id_lokalId",
    right_on="adgangspunkt",
    how="inner",
    suffixes=("_adg", "_hus"),
)

housenumbers_with_geoms.drop(columns=["adgangspunkt"], inplace=True)
housenumbers_with_geoms.rename(
    columns={"id_lokalId_hus": "husnummer", "id_lokalId_adg": "adgangspunkt"},
    inplace=True,
)

# %%

addresses_with_geoms = pd.merge(
    housenumbers_with_geoms,
    address[["status", "id_lokalId", "husnummer"]],
    on="husnummer",
    how="inner",
)

addresses_with_geoms.rename(
    columns={"id_lokalId": "adresseIdentificerer"}, inplace=True
)

# %%
addresses_with_geoms = pd.merge(
    addresses_with_geoms,
    address_gdf[["id_lokalId", "geometry"]],
    left_on="vejpunkt",
    right_on="id_lokalId",
    how="left",
    suffixes=("_adr", "_vej"),
)


# Analysis requires WGS84 coordinates
addresses_with_geoms["vej_pos_lat"] = addresses_with_geoms.geometry_vej.to_crs("4326").y
addresses_with_geoms["vej_pos_lon"] = addresses_with_geoms.geometry_vej.to_crs("4326").x


addresses_with_geoms.rename(
    columns={
        "geometry_adr": "geometry",
    },
    inplace=True,
)
addresses_with_geoms.drop(columns=["id_lokalId", "geometry_vej"], inplace=True)


addresses_with_geoms.to_parquet(addresses_fp_all, index=False)

# %%
