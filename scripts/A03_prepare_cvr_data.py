# %%

# Process CVR data

import pandas as pd
import geopandas as gpd
import yaml
from itertools import chain
from src.helper_functions import get_service_type

# %%

with open(r"../config.yml") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    cvr_address_input_fp = parsed_yaml_file["cvr_address_input_fp"]
    cvr_brancher_input_fp = parsed_yaml_file["cvr_brancher_input_fp"]
    cvr_penhed_input_fp = parsed_yaml_file["cvr_penhed_input_fp"]
    addresses_fp_all = parsed_yaml_file["addresses_fp_all"]

    services = parsed_yaml_file["services"]

    adm_boundaries_config = parsed_yaml_file["study_area_config"]
    study_area_fp = adm_boundaries_config["regions"]["outputpath"]

    cvr_destinations_fp = parsed_yaml_file["cvr_destinations_fp"]
    cvr_destinations_all_fp = parsed_yaml_file["cvr_destinations_all_fp"]

# %%
nace_dict = {}

for service in services:
    if "nace_codes" in service:
        nace_dict[service["service_type"]] = service["nace_codes"]

# %%

cvr_addresses = pd.read_csv(
    cvr_address_input_fp,
    sep=",",
    encoding="utf-8",
    usecols=[
        "AdresseringAnvendelse",
        "CVREnhedsId",
        "Adresse",
        "CVRAdresse_kommunekode",
    ],
)
cvr_brancher = pd.read_csv(
    cvr_brancher_input_fp,
    sep=",",
    encoding="utf-8",
    usecols=["CVREnhedsId", "vaerdi", "vaerdiTekst"],
)
cvr_penhed = pd.read_csv(
    cvr_penhed_input_fp,
    sep=",",
    encoding="utf-8",
    usecols=["id", "pNummer", "tilknyttetVirksomhedsCVRNummer", "status"],
)

# %%
# Merge dataframes
cvr_data = cvr_penhed.merge(
    cvr_brancher, left_on="id", right_on="CVREnhedsId", how="left"
)

assert (
    cvr_data["CVREnhedsId"].notnull().all()
), "Not all rows in cvr_penhed have a value in cvr enhedsid."
# NOTE penheder are no longer unique! one to many/many to many relation with brancher?


# %%

cvr_data_addresses = cvr_data.merge(
    cvr_addresses, left_on="CVREnhedsId", right_on="CVREnhedsId", how="left"
)

if len(cvr_data_addresses["Adresse"].notnull()) > 0:
    print("Not all rows have an address!")


# %%

cvr_subset = cvr_data_addresses[
    cvr_data_addresses["vaerdi"].isin(list(chain(*nace_dict.values())))
].copy()

assert len(cvr_subset) > 0, "No matching CVR codes found."

# make sure that "homemade" cvr codes are not actually in use (used for osm data)
assert (
    49 not in cvr_subset["vaerdi"].unique()
), "CVR code 49 (train code) found in data."

assert (
    49 not in cvr_subset["vaerdi"].unique()
), "CVR code 93 (sport code) found in data."

# %%
# filter out inactive enheder
cvr_subset = cvr_subset[
    cvr_subset["status"].isin(
        [
            "aktiv",
        ]
    )
]
# %%
# rename to column names expected by the model
cvr_subset = cvr_subset[["vaerdi", "Adresse"]]

cvr_subset.rename(
    columns={
        "vaerdi": "nace_code",
        "Adresse": "Adr_id",
    },
    inplace=True,
)


cvr_subset["service_type"] = cvr_subset["nace_code"].apply(
    lambda nace_code: get_service_type(nace_code=nace_code, nace_dict=nace_dict)
)

assert cvr_subset["service_type"].notnull().all(), "Not all rows have a service type."

# %%
# Join to address data -
cvr_address_geoms = gpd.read_parquet(addresses_fp_all)  # prepared in 00-script

# %%
cvr_address_geoms = pd.merge(
    cvr_address_geoms[
        ["adresseIdentificerer", "vej_pos_lat", "vej_pos_lon", "geometry"]
    ],
    cvr_subset,
    right_on="Adr_id",
    left_on="adresseIdentificerer",
    how="right",
    suffixes=(
        "_adr",
        "_cvr",
    ),
)

print(
    f"{len(cvr_address_geoms[cvr_address_geoms.geometry.isnull()])} CVR locations not matched to addresses."
)

# %%
# find subset in region
region = gpd.read_file(study_area_fp)

cvr_region = gpd.clip(cvr_address_geoms, region)


# %%
print(
    f"{len(cvr_region[cvr_region.adresseIdentificerer.notnull()])} CVR locations in the study area matched to addresses."
)
print(
    f"{len(cvr_region[cvr_region.adresseIdentificerer.isnull()])} CVR locations in the study area not matched to addresses."
)

if len(cvr_region[cvr_region.adresseIdentificerer.isnull()]) > 0:

    print("Unmatched CVR locations in each category:")
    cvr_region[cvr_region.adresseIdentificerer.isnull()]["service_type"].value_counts()

# %%

print("CVR locations in each category:")
cvr_region["service_type"].value_counts()

# %%

# Export
cvr_region = cvr_region[
    ["service_type", "nace_code", "Adr_id", "vej_pos_lat", "vej_pos_lon", "geometry"]
]


cvr_region.to_file(cvr_destinations_all_fp)

cvr_region[(cvr_region.Adr_id.notnull()) & (cvr_region.geometry.notnull())].to_file(
    cvr_destinations_fp
)


# %%
