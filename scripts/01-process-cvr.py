# %%

# Process CVR data

import pandas as pd
import geopandas as gpd
import yaml

# %%

with open(r"../config.yml") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    cvr_address_fp = parsed_yaml_file["cvr_address_fp"]
    cvr_brancher_fp = parsed_yaml_file["cvr_brancher_fp"]
    cvr_penhed_fp = parsed_yaml_file["cvr_penhed_fp"]
    address_cvr_fp = parsed_yaml_file["address_cvr_fp"]
    addresses_fp_all = parsed_yaml_file["addresses_fp_all"]
    hb_codes_dict = parsed_yaml_file["hb_codes_dict"]

    study_area_fp = parsed_yaml_file["study_area_fp"]


# %%

cvr_addresses = pd.read_csv(
    cvr_address_fp,
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
    cvr_brancher_fp,
    sep=",",
    encoding="utf-8",
    usecols=["CVREnhedsId", "vaerdi", "vaerdiTekst"],
)
cvr_penhed = pd.read_csv(
    cvr_penhed_fp,
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
    cvr_data_addresses["vaerdi"].isin(hb_codes_dict.values())
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
        "vaerdi": "hb_kode",
        "Adresse": "Adr_id",
    },
    inplace=True,
)

cvr_subset["service_type"] = cvr_subset["hb_kode"].map(
    {v: k for k, v in hb_codes_dict.items()}
)

# %%
# Join to address data - just used to find entities in the region and for data quality analysis
cvr_address_geoms = gpd.read_parquet(address_cvr_fp_all)  # prepared in 00-script

cvr_address_geoms = pd.merge(
    cvr_address_geoms[["adresseIdentificerer", "geometry"]],
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
    f"{len(cvr_region[cvr_region.adresseIdentificerer.notnull()])} CVR locations matched to addresses."
)
print(
    f"{len(cvr_region[cvr_region.adresseIdentificerer.isnull()])} CVR locations not matched to addresses."
)

if len(cvr_region[cvr_region.adresseIdentificerer.isnull()]) > 0:

    print("Unmatched CVR locations in each category:")
    cvr_region[cvr_region.adresseIdentificerer.isnull()]["service_type"].value_counts()

# %%

print("CVR locations in each category:")
cvr_region["service_type"].value_counts()

# %%

# Export
cvr_region = cvr_region[["service_type", "hb_kode", "Adr_id", "geometry"]]


cvr_region.to_file(
    "../data/processed/cvr/cvr-services-all.gpkg",
)

cvr_region[(cvr_region.Adr_id.notnull()) & (cvr_region.geometry.notnull())].to_file(
    "../data/processed/cvr/cvr-services-w-address.gpkg",
)


# %%
# # FIX CSV

# import re
# import shutil

# new_cvr_path = "../data/processed/cvr/Penhed_Region_sj_fixed.csv"

# shutil.copyfile(org_cvr_path, new_cvr_path)

# replace_dict = {
#     "Bogføring og revision; skatterådgivning": "Bogføring og revision, skatterådgivning",
#     "Fremstilling af karosserier til motorkøretøjer; fremstilling af påhængsvogne og sættevogne": "Fremstilling af karosserier til motorkøretøjer, fremstilling af påhængsvogne og sættevogne",
#     "Kunst, Kjoler, Kaffe og Kiksekage;Andre organisationers og foreningers aktiviteter i.a.n.": "Kunst, Kjoler, Kaffe og Kiksekage, Andre organisationers og foreningers aktiviteter i.a.n.",
# }


# for find_value, replace_value in replace_dict.items():

#     with open(new_cvr_path, "r", encoding="utf") as f:
#         my_csv_text = f.read()

#     new_csv_str = re.sub(find_value, replace_value, my_csv_text)

#     with open(new_cvr_path, "w", encoding="utf") as f:
#         f.write(new_csv_str)

# cvr_data = pd.read_csv(new_cvr_path, sep=";", encoding="latin1")

# cvr_data_subset = cvr_data[cvr_data["hb_kode"].isin(hb_codes_dict.values())]
# assert len(cvr_data_subset) > 0, "No matching CVR codes found."

# assert (
#     49 not in cvr_data_subset["hb_kode"].unique()
# ), "CVR code 49 (train code) found in data."

# assert (
#     49 not in cvr_data_subset["hb_kode"].unique()
# ), "CVR code 93 (sport code) found in data."


# cvr_data_subset = cvr_data_subset[
#     cvr_data_subset["Status"].isin(["Aktiv"])  # "Under oprettelse"
# ]

# cvr_data_subset.drop_duplicates(inplace=True, keep="first")
# # %%
# addresses = gpd.read_parquet(address_cvr_fp)

# addresses = addresses[["adresseIdentificerer", "geometry"]]

# # %%
# cvr_address = addresses.merge(
#     cvr_data_subset,
#     left_on="adresseIdentificerer",
#     right_on="Adr_id",
#     how="right",
# )

# # %%

# cvr_address["service_type"] = cvr_address["hb_kode"].map(
#     {v: k for k, v in hb_codes_dict.items()}
# )

# print(
#     f"{len(cvr_address[cvr_address.adresseIdentificerer.notnull()])} CVR locations matched to addresses."
# )
# print(
#     f"{len(cvr_address[cvr_address.adresseIdentificerer.isnull()])} CVR locations not matched to addresses."
# )

# print("Unmatched CVR locations in each category:")
# cvr_address[cvr_address.adresseIdentificerer.isnull()]["service_type"].value_counts()


# # %%
# # Export

# cvr_address.to_file(
#     "../data/processed/cvr/cvr-services-all.gpkg",
# )

# cvr_address[
#     (cvr_address.adresseIdentificerer.notnull()) & (cvr_address.geometry.notnull())
# ].to_file(
#     "../data/processed/cvr/cvr-services-w-address.gpkg",
# )

# %%
