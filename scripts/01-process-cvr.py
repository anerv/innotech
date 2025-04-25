# %%[markdown]

# Process CVR data

# %%
import pandas as pd
import geopandas as gpd
import re
import shutil
import yaml
from src.helper_functions import drop_duplicates_custom

# %%

with open(r"../config.yml") as file:
    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    org_cvr_path = parsed_yaml_file["cvr_fp"]
    address_fp_parquet = parsed_yaml_file["address_fp_parquet"]
    hb_codes_dict = parsed_yaml_file["hb_codes_dict"]

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
addresses = gpd.read_parquet(address_fp_parquet)

addresses.drop_duplicates(inplace=True, keep="first")

addresses_cleaned = drop_duplicates_custom(
    addresses, subset_columns=["adresseIdentificerer"], value_column="enh023Boligtype"
)


keep_cols_addresses = [
    "adresseIdentificerer",
    "enh023Boligtype",
    "geometry",
]

addresses_cleaned = addresses_cleaned[keep_cols_addresses]

# %%
cvr_address = addresses_cleaned.merge(
    cvr_data_subset,
    left_on="adresseIdentificerer",
    right_on="Adr_id",
    how="right",
)

# %%

cvr_address["destination_type"] = cvr_address["hb_kode"].map(
    {v: k for k, v in hb_codes_dict.items()}
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

cvr_address[(cvr_address.Adr_id.notnull()) & (cvr_address.geometry.notnull())].to_file(
    "../data/processed/cvr/cvr-destinations-w-address.gpkg",
)

# %%
