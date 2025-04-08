# %%[markdown]

# Process CVR data


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
    "physiotherapist": 869020,
    "pharmacy": 477300,
    "kindergarten": 889130,
    "nursery": 889120,
    "school": 852010,
    "grocery_store": 471100,
    "supermarket": 471120,
    "theatre": 900100,
    "library": 910110,
    "sports_facility": 931100,
    "fitness": 931300,
    "movie_theater": 591400,
}

# %%
# FIX CSV

org_cvr_path = "../data/cvr/Penhed_Region_sj.csv"

new_cvr_path = "../data/cvr/Penhed_Region_sj_fixed.csv"

shutil.copyfile(org_cvr_path, new_cvr_path)

replace_dict = {
    "Bogføring og revision; skatterådgivning": "Bogføring og revision, skatterådgivning",
    "Fremstilling af karosserier til motorkøretøjer; fremstilling af påhængsvogne og sættevogne": "Fremstilling af karosserier til motorkøretøjer, fremstilling af påhængsvogne og sættevogne",
    "Kunst, Kjoler, Kaffe og Kiksekage;Andre organisationers og foreningers aktiviteter i.a.n.": "Kunst, Kjoler, Kaffe og Kiksekage, Andre organisationers og foreningers aktiviteter i.a.n.",
}


for find_value, replace_value in replace_dict.items():

    with open(new_cvr_path, "r") as f:
        my_csv_text = f.read()

    new_csv_str = re.sub(find_value, replace_value, my_csv_text)

    with open(new_cvr_path, "w") as f:
        f.write(new_csv_str)


cvr_data = pd.read_csv(new_cvr_path, sep=";", encoding="latin1")

cvr_data_subset = cvr_data[cvr_data["hb_kode"].isin(cvr_codes.values())]
assert len(cvr_data_subset) > 0, "No matching CVR codes found."
# %%

addresses = gpd.read_file("../data/cvr/adresser_utm.gpkg")
addresses_access = gpd.read_file("../data/cvr/adgangs_adresser_utm.gpkg")

# %%
addresses.to_parquet("../data/cvr/adresser_utm.parquet", index=False)
addresses_access.to_parquet("../data/cvr/adgangs_adresser_utm.parquet", index=False)
# %%
addresses = gpd.read_parquet("../data/cvr/adresser_utm.parquet")
addresses_access = gpd.read_parquet("../data/cvr/adgangs_adresser_utm.parquet")

# TODO: Match to addresses - check which ones?

# TODO: count and print how many of each type are matched/unmatched

# %%
