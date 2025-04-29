# %%

# Create address data for the project with ids for CVR and geometries
# %%

import pandas as pd
import geopandas as gpd
from shapely import wkt
import yaml

with open(r"../config.yml") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    org_cvr_path = parsed_yaml_file["cvr_fp"]
    address_fp_parquet = parsed_yaml_file["address_fp_parquet"]
    hb_codes_dict = parsed_yaml_file["hb_codes_dict"]
    input_address_fp = parsed_yaml_file["input_address_fp"]
    address_points_fp = parsed_yaml_file["address_points_fp"]
    housenumbers_fp = parsed_yaml_file["housenumbers_fp"]


# %%


address = pd.read_parquet(input_address_fp)
address_points = pd.read_parquet(address_points_fp)
housenumbers = pd.read_parquet(housenumbers_fp)

address_points["geometry"] = address_points["position"].apply(wkt.loads)
address_gdf = gpd.GeoDataFrame(address_points, geometry="geometry", crs="EPSG:25832")

# %%
housenumbers_with_geoms = pd.merge(
    address_gdf[["id_lokalId", "geometry"]],
    housenumbers[["adgangspunkt", "id_lokalId"]],
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

# %%
addresses_with_geoms.rename(
    columns={"id_lokalId": "adresseIdentificerer"}, inplace=True
)

addresses_with_geoms.to_parquet(address_fp_parquet, index=False)

# %%
