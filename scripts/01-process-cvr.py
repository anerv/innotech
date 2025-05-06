# %%[markdown]

# Process CVR data

# %%
import pandas as pd
import geopandas as gpd
import re
import shutil
import yaml

# %%

with open(r"../config.yml") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    org_cvr_path = parsed_yaml_file["cvr_fp"]
    address_cvr_fp = parsed_yaml_file["address_cvr_fp"]
    hb_codes_dict = parsed_yaml_file["hb_codes_dict"]


# %%
cvr_address_fp = "../data/input/cvr/CVR_V1_Adressering_TotalDownload_csv_Current_8.csv"
cvr_brancher_fp = "../data/input/cvr/CVR_V1_Branche_TotalDownload_csv_Current_8.csv"
cvr_penhed_fp = (
    "../data/input/cvr/CVR_V1_Produktionsenhed_TotalDownload_csv_Current_8.csv"
)

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

# TODO: penheder are no longer unique! maybe does not matter?


# %%
# TODO: fix, check
cvr_data = cvr_data.merge(
    cvr_addresses, left_on="CVREnhedsId", right_on="CVREnhedsId", how="left"
)

# TODO: compare number of rows with org data
# %%

# %%
# FIX CSV

new_cvr_path = "../data/processed/cvr/Penhed_Region_sj_fixed.csv"

shutil.copyfile(org_cvr_path, new_cvr_path)

replace_dict = {
    "Bogføring og revision; skatterådgivning": "Bogføring og revision, skatterådgivning",
    "Fremstilling af karosserier til motorkøretøjer; fremstilling af påhængsvogne og sættevogne": "Fremstilling af karosserier til motorkøretøjer, fremstilling af påhængsvogne og sættevogne",
    "Kunst, Kjoler, Kaffe og Kiksekage;Andre organisationers og foreningers aktiviteter i.a.n.": "Kunst, Kjoler, Kaffe og Kiksekage, Andre organisationers og foreningers aktiviteter i.a.n.",
}


for find_value, replace_value in replace_dict.items():

    with open(new_cvr_path, "r", encoding="utf") as f:
        my_csv_text = f.read()

    new_csv_str = re.sub(find_value, replace_value, my_csv_text)

    with open(new_cvr_path, "w", encoding="utf") as f:
        f.write(new_csv_str)

cvr_data = pd.read_csv(new_cvr_path, sep=";", encoding="latin1")

cvr_data_subset = cvr_data[cvr_data["hb_kode"].isin(hb_codes_dict.values())]
assert len(cvr_data_subset) > 0, "No matching CVR codes found."

assert (
    49 not in cvr_data_subset["hb_kode"].unique()
), "CVR code 49 (train code) found in data."

assert (
    49 not in cvr_data_subset["hb_kode"].unique()
), "CVR code 93 (sport code) found in data."


cvr_data_subset = cvr_data_subset[
    cvr_data_subset["Status"].isin(["Aktiv"])  # "Under oprettelse"
]

cvr_data_subset.drop_duplicates(inplace=True, keep="first")
# %%
addresses = gpd.read_parquet(address_cvr_fp)

addresses = addresses[["adresseIdentificerer", "geometry"]]

# %%
cvr_address = addresses.merge(
    cvr_data_subset,
    left_on="adresseIdentificerer",
    right_on="Adr_id",
    how="right",
)

# %%

cvr_address["service_type"] = cvr_address["hb_kode"].map(
    {v: k for k, v in hb_codes_dict.items()}
)

print(
    f"{len(cvr_address[cvr_address.adresseIdentificerer.notnull()])} CVR locations matched to addresses."
)
print(
    f"{len(cvr_address[cvr_address.adresseIdentificerer.isnull()])} CVR locations not matched to addresses."
)

print("Unmatched CVR locations in each category:")
cvr_address[cvr_address.adresseIdentificerer.isnull()]["service_type"].value_counts()


# %%
# Export

cvr_address.to_file(
    "../data/processed/cvr/cvr-services-all.gpkg",
)

cvr_address[
    (cvr_address.adresseIdentificerer.notnull()) & (cvr_address.geometry.notnull())
].to_file(
    "../data/processed/cvr/cvr-services-w-address.gpkg",
)

# %%
