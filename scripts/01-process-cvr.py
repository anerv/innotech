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
    address_fp_parquet = parsed_yaml_file["address_fp_parquet"]
    address_access_fp_parquet = parsed_yaml_file["address_access_fp_parquet"]
# %%
cvr_codes = {
    "doctor-gp": 862100,
    "dentist": 862300,
    "pharmacy": 477300,
    "kindergarten": 889130,
    "nursery": 889120,
    "school": 852010,
    "supermarket": 471120,
    "discount_supermarket": 471130,
    "library": 910110,
    # "sports_facility": 931100,
}

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

cvr_data_subset = cvr_data[cvr_data["hb_kode"].isin(cvr_codes.values())]
assert len(cvr_data_subset) > 0, "No matching CVR codes found."

# %%
# TODO: Filter active


# %%
addresses = gpd.read_parquet(address_fp_parquet)

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


addresses = addresses[keep_cols_addresses]

addresses = addresses.rename(
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


# TODO: Match to closest adress within some threshold

# %%
# Export

cvr_address.to_file(
    "../data/processed/cvr/cvr-destinations-all.gpkg",
)

cvr_address[(cvr_address.Adr_id.notnull()) & (cvr_address.geometry.notnull())].to_file(
    "../data/processed/cvr/cvr-destinations-w-address.gpkg",
)

# %%
