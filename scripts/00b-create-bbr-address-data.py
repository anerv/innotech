# %%

# Create address household data for the project
# %%

import pandas as pd
import geopandas as gpd
from shapely import wkt
import yaml


with open(r"../config.yml", encoding="utf-8") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    address_bbr_fp = parsed_yaml_file["address_bbr_fp"]
    input_address_fp = parsed_yaml_file["input_address_fp"]
    address_points_fp = parsed_yaml_file["address_points_fp"]
    housenumbers_fp = parsed_yaml_file["housenumbers_fp"]

    bbr_fp = parsed_yaml_file["bbr_fp"]

    adm_boundaries_fp = parsed_yaml_file["adm_boundaries_fp"]
    study_area_fp = parsed_yaml_file["study_area_fp"]
    study_area_name = parsed_yaml_file["study_area_name"]


# %%

##### BBR Adress data ######

# Read BBR
read_columns = ["id_lokalId", "adresseIdentificerer", "enh023Boligtype", "kommunekode"]
if bbr_fp.endswith(".parquet"):

    bbr = pd.read_parquet(bbr_fp, columns=read_columns)

elif bbr_fp.endswith(".csv"):

    bbr = pd.read_csv(bbr_fp, sep=",", usecols=read_columns)

# Select helårsbeboelse
# use_type = [110, 120, 121, 122, 130, 131, 132, 140, 150, 160, 185, 190]
home_type = ["1"]  # https://teknik.bbr.dk/kodelister/0/1/0/Boligtype

bbr_housing = bbr[bbr["enh023Boligtype"].isin(home_type)]

print(
    f"{len(bbr_housing[bbr_housing.adresseIdentificerer.isna()])} BBR units do not have an address."
)
print(
    f"{len(bbr_housing[bbr_housing.adresseIdentificerer.notna()])} BBR units have an address."
)
print(f"Dropping bbr rows without address...")

bbr_housing = bbr_housing[bbr_housing.adresseIdentificerer.notna()]

# %%
# Read addresse data
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
# Creating address data with geometry
address_points["geometry"] = address_points["position"].apply(wkt.loads)
address_gdf = gpd.GeoDataFrame(address_points, geometry="geometry", crs="EPSG:25832")

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
# Getting position of road access points
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

# %%

# filter based on status https://danmarksadresser.dk/adressedata/kodelister/livscyklus

addresses_with_geoms = addresses_with_geoms[addresses_with_geoms["status"].isin([2, 3])]

# %%
# join addresses with bbr data

bbr_addresses = pd.merge(
    addresses_with_geoms,
    bbr_housing,
    on="adresseIdentificerer",
    how="right",
    suffixes=("_add", "_bbr"),
)

print(
    f"Count of bbr units with address match: {len(bbr_addresses[bbr_addresses.enh023Boligtype.notna()])}"
)

print(
    f"Count of bbr units with no address match: {len(bbr_addresses[bbr_addresses.enh023Boligtype.isna()])}"
)
# %%
# Get unique access points
bbr_access_points = bbr_addresses.drop_duplicates(subset=["adgangspunkt"])

bbr_access_points = bbr_access_points[
    [
        "adresseIdentificerer",
        "adgangspunkt",
        "geometry",
        "enh023Boligtype",
        "id_lokalId",
        "vej_pos_lat",
        "vej_pos_lon",
    ]
]

bbr_access_points.rename(
    columns={
        "id_lokalId": "bbr",
    },
    inplace=True,
)

# %%

# filter addresses to only include those within the region
administrative_boundaries = gpd.read_file(adm_boundaries_fp)

region = administrative_boundaries[administrative_boundaries["navn"] == study_area_name]


region = region[["navn", "geometry"]]


region.sindex
bbr_access_points.sindex

region_bbr = gpd.sjoin(region, bbr_access_points, predicate="intersects")

access_points_region = bbr_access_points[
    bbr_access_points.index.isin(region_bbr.index_right)
]

# EXPORT TO PARQUET
access_points_region.to_parquet(address_bbr_fp, index=False)
# %%
