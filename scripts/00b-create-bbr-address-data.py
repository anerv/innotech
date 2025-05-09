# %%

# Create address household data for the project

import pandas as pd
import geopandas as gpd
from shapely import wkt
import yaml


with open(r"../config.yml", encoding="utf-8") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    address_bbr_fp = parsed_yaml_file["address_bbr_fp"]

    addresses_fp_all = parsed_yaml_file["addresses_fp_all"]

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

### Read address dat
addresses_with_geoms = gpd.read_parquet(addresses_fp_all)

# # filter based on status https://danmarksadresser.dk/adressedata/kodelister/livscyklus

addresses_with_geoms = addresses_with_geoms[addresses_with_geoms["status"].isin([2, 3])]

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
region = gpd.read_file(study_area_fp)


region.sindex
bbr_access_points.sindex

region_bbr = gpd.sjoin(region, bbr_access_points, predicate="intersects")

access_points_region = bbr_access_points[
    bbr_access_points.index.isin(region_bbr.index_right)
]

# EXPORT TO PARQUET
access_points_region.to_parquet(address_bbr_fp, index=False)
# %%
