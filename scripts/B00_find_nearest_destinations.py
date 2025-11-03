# %% [markdown]
# # 🚀 Nearest Neighbor Search
# This script identifyes the nearest sercive to a given adress using Scikit-Learn.
# The script is designed so it can be run from the command line and takes a configuration file as input.
# The output is a parquet file with the nearest neighbor for each dwelling. and a lat lon coordinate designed for use with Open Trip Planner

# %%%  Step 0 load libaries and configuation

import yaml
from pathlib import Path
import duckdb
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import geopandas as gpd
from src.helper_functions import (
    validate_restriction_config,
    load_table_with_restrictions,
    assign_restriction_if_missing,
)

# %%
con = duckdb.connect()
con.execute("INSTALL spatial;")
con.execute("LOAD spatial;")

# %%
# Define the path to the config.yml file
script_path = Path(__file__).resolve()
root_path = script_path.parent.parent
data_path = root_path / "data"

config_path = root_path / "config.yml"

# Read and parse the YAML file
with open(config_path, "r") as file:
    config_data = yaml.safe_load(file)
# %%

# --- Step 0: Load the configuration file and validate restrictions ---
validated_restrictions = validate_restriction_config(config_data, con, data_path)

# %%
#  --- Step 1: Load the adresses of all dwellings  ---

source_cfg = config_data["data_sources"]["dwellings"]

load_table_with_restrictions(
    con,
    data_path / source_cfg["path"],
    base_columns=source_cfg["base_columns"],
    validated_restrictions=validated_restrictions,
    table_name="dwellings",
)

# If any restrictions are defined, apply them to the dwellings
for name, restriction_config in validated_restrictions.items():
    assign_restriction_if_missing(con, restriction_config, "dwellings", data_path)

dwellings_df = con.execute("SELECT * FROM dwellings").df()


# %%

# ---  Step 2:  iterate over the services
source_cfg = config_data["data_sources"]["services"]

load_table_with_restrictions(
    con,
    data_path / source_cfg["path"],
    base_columns=source_cfg["base_columns"],
    validated_restrictions=validated_restrictions,
    table_name="all_services",
)

# If any restrictions are defined, apply them to the dwellings
for name, restriction_config in validated_restrictions.items():
    assign_restriction_if_missing(con, restriction_config, "all_services", data_path)

# %%
con.execute("SELECT * FROM all_services LIMIT 10").df()
# %%

services = config_data["services"]

for service in services:
    service_type = service["service_type"]
    nace_codes = service["nace_codes"]
    n_neighbors = service["n_neighbors"]
    restriction_name = service.get("spatial_restriction_type")
    restriction_col = f"{restriction_name}_id" if restriction_name else None

    # --- Step 1: Get restriction group keys ---
    if restriction_col:
        group_keys = (
            con.execute(
                f"""
            SELECT DISTINCT {restriction_col}
            FROM dwellings
            WHERE {restriction_col} IS NOT NULL
        """
            )
            .fetchdf()[restriction_col]
            .tolist()
        )
    else:
        group_keys = [None]

    # --- Step 2: Prepare all NACE service matches across groups ---
    nace_list_sql = ", ".join(f"'{code}'" for code in nace_codes)
    all_records_by_n = {n: [] for n in range(1, n_neighbors + 1)}

    for group_key in group_keys:
        # --- Step 3: Build WHERE clause for group ---
        restriction_filter = (
            f"{restriction_col} = '{group_key}'" if group_key else "TRUE"
        )

        # --- Step 4: Query dwellings and services for this group ---
        dwellings_df = con.execute(
            f"""
            SELECT 
                address_id, x, y, road_point_lat, road_point_lon
                {f", {restriction_col}" if restriction_col else ""}
            FROM dwellings
            WHERE {restriction_filter}
        """
        ).df()

        services_df = con.execute(
            f"""
            SELECT 
                address_id, x, y, road_point_lat, road_point_lon
                {f", {restriction_col}" if restriction_col else ""}
            FROM all_services
            WHERE service_type IN ({nace_list_sql})
              AND {restriction_filter}
        """
        ).df()

        if services_df.empty:
            print(
                f"⚠️  No services found for {service_type} in {restriction_col} = {group_key}"
            )
            continue
        if dwellings_df.empty:
            print(f"⚠️  No dwellings found in {restriction_col} = {group_key}")
            continue

        # --- Step 5: Nearest neighbor search ---
        nn = NearestNeighbors(n_neighbors=n_neighbors, algorithm="kd_tree").fit(
            services_df[["x", "y"]]
        )
        distances, indices = nn.kneighbors(dwellings_df[["x", "y"]])

        for n in range(1, n_neighbors + 1):
            for i in range(len(dwellings_df)):
                src = dwellings_df.iloc[i]
                dst_idx = indices[i][n - 1]
                dst = services_df.iloc[dst_idx]
                dist = distances[i][n - 1]

                record = {
                    "source_address_id": src.address_id,
                    "source_lat": src.road_point_lat,
                    "source_lon": src.road_point_lon,
                    "dest_address_id": dst.address_id,
                    "dest_lat": dst.road_point_lat,
                    "dest_lon": dst.road_point_lon,
                    "dest_distance": dist,
                    "n": n,
                }
                if restriction_col:
                    record[restriction_col] = group_key

                all_records_by_n[n].append(record)

    # --- Step 6: Write one file per n_neighbors ---
    for n in range(1, n_neighbors + 1):
        records = all_records_by_n[n]
        if not records:
            print(f"⚠️  No matches found for {service_type} at n={n}")
            continue
        df_out = pd.DataFrame(records)
        output_path = data_path / f"processed/destinations/{service_type}_{n}.parquet"
        df_out.to_parquet(output_path, index=False)
        print(f"✅ Saved {output_path} with {len(df_out)} rows.")


# %%
