# %%[markdown]

# Process CVR data

# TODO: Include fitness centers???

# %%
import pandas as pd
import geopandas as gpd
import re
import shutil

# %%
cvr_codes = {
    "doctor-gp": 862100,
    "doctor-specialist": 862200,
    "dentist": 862300,
    # "physiotherapist": 869020,
    "pharmacy": 477300,
    "kindergarten": 889130,
    "nursery": 889120,
    "school": 852010,
    "grocery_store": 471110,
    "supermarket": 471120,
    "discount_store": 471130,
    "theatre": 900100,
    "library": 910110,
    "sports_facility": 931100,
    "fitness": 931300,
    "movie_theater": 591400,
}

# %%
# FIX CSV

org_cvr_path = "../data/input/cvr/Penhed_Region_sj.csv"

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

cvr_data_subset = cvr_data[cvr_data["hb_kode"].isin(cvr_codes.values())]
assert len(cvr_data_subset) > 0, "No matching CVR codes found."

# %%
addresses = gpd.read_parquet("../data/processed/adresser/adresser_utm.parquet")
addresses_access = gpd.read_parquet(
    "../data/processed/adresser/adgangs_adresser_utm.parquet"
)

keep_cols_addresses = [
    "id",
    "status",
    "vejnavn",
    "husnr",
    "etage",
    "dør",
    "postnr",
    "kommunekode",
    "adgangsadresse_status",
    "adgangsadresseid",
    "ddkn_km10",
    "geometry",
]

keep_cols_addresses_access = [
    "id",
    "status",
    "vejnavn",
    "husnr",
    "postnr",
    "kommunekode",
    "ddkn_km10",
    "geometry",
]

addresses = addresses[keep_cols_addresses]
addresses_access = addresses_access[keep_cols_addresses_access]

addresses = addresses.rename(
    columns={
        "status": "adr_status",
    }
)

addresses_access = addresses_access.rename(
    columns={
        "status": "adr_status",
    }
)
# %%
cvr_address = addresses.merge(
    cvr_data_subset,
    left_on="id",
    right_on="Adr_id",
    how="right",
)

cvr_address["destination_type"] = cvr_address["hb_kode"].map(
    {v: k for k, v in cvr_codes.items()}
)

print(
    f"{len(cvr_address[cvr_address.Adr_id.notnull()])} CVR locations matched to addresses."
)
print(
    f"{len(cvr_address[cvr_address.Adr_id.isnull()])} CVR locations not matched to addresses."
)

print("Unmatched CVR locations in each category:")
cvr_address[cvr_address.Adr_id.isnull()]["destination_type"].value_counts()

# %%
# Export

cvr_address.to_file(
    "../data/processed/cvr/cvr-destinations-all.gpkg",
)

cvr_address[cvr_address.Adr_id.notnull()].to_file(
    "../data/processed/cvr/cvr-destinations-w-address.gpkg",
)

# %%
