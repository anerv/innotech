# %% [markdown]
# # 🚀 Nearest Neighbor Search
# This script identifyes the cearest sercive to a given adress using Scikit-Learn.
# The script is designed so it can be run from the command line and takes a configuration file as input.
# The output is a parquet file with the nearest neighbor for each dwelling. and a lat lon coordinate designed for use with Open Trip Planner

# %%%  Step 0 load libaries and configuation

import yaml
from pathlib import Path
import duckdb
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import geopandas as gpd

# %%
con = duckdb.connect()
con.execute("INSTALL spatial;")
con.execute("LOAD spatial;")

# %%
# Define the path to the config.yml file
script_path = Path(__file__).resolve()
root_path = script_path.parent.parent
data_path = root_path / "data"

config_path = root_path / "config-model.yml"

# Read and parse the YAML file
with open(config_path, "r") as file:
    config_data = yaml.safe_load(file)
# %%

# Helper functions

# Define a function to validate the restriction configuration


def validate_restriction_config(config, duck_con):
    defined_restrictions = {}
    used_restrictions = set()
    missing_restrictions = set()

    # Validate restriction definitions using DuckDB
    for restriction in config.get("restrictions", []):
        name = restriction["name"]
        file_path = data_path / Path(restriction["file_path"])
        id_attr = restriction["id_attribute"]

        if not file_path.exists():
            raise FileNotFoundError(
                f"Restriction '{name}' references missing file: {file_path}"
            )

        # Use DuckDB to get schema
        try:
            df_columns = (
                duck_con.execute(f"DESCRIBE SELECT * FROM '{file_path}' LIMIT 0")
                .fetchdf()["column_name"]
                .tolist()
            )

            if id_attr not in df_columns:
                raise ValueError(
                    f"Restriction '{name}' expects id_attribute '{id_attr}', "
                    f"but it's not found in file: {file_path}"
                )
        except Exception as e:
            raise RuntimeError(f"Failed to inspect schema for {file_path}: {e}")

        defined_restrictions[name] = restriction

    # Validate service restrictions
    for service in config.get("services", []):
        restriction = service.get("spatial_restriction_type")
        if restriction:
            if restriction in defined_restrictions:
                used_restrictions.add(restriction)
            else:
                missing_restrictions.add(restriction)

    if missing_restrictions:
        raise ValueError(
            f"The following spatial_restriction_type(s) are used in services "
            f"but not defined in restrictions: {', '.join(missing_restrictions)}"
        )

    unused_restrictions = set(defined_restrictions.keys()) - used_restrictions
    if unused_restrictions:
        print(
            f"⚠️ Warning: restrictions defined but not used: {', '.join(unused_restrictions)}"
        )

    return {name: defined_restrictions[name] for name in used_restrictions}


# Enrich adresses with and service data with restriction id.


def assign_restriction_to_table(con, restriction_config, table_name: str):
    """
    Assigns a spatial restriction (e.g., municipality_id) to a DuckDB table.
    Uses bounding box prefiltering + ST_Within.
    The target table (e.g. 'dwellings' or 'services') must already exist in DuckDB.
    """
    name = restriction_config["name"]
    id_col = restriction_config["id_attribute"]
    new_col = f"{name}_id"
    restriction_fp = Path(data_path) / restriction_config["file_path"]
    restriction_table = f"restrictions_{name}"

    # Load restriction polygons (renaming the ID field)
    con.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE {restriction_table} AS
        SELECT 
            "{id_col}" AS {new_col},
            geometry
        FROM '{restriction_fp}'
    """
    )

    # Join using bounding box prefilter and ST_Within
    con.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE {table_name} AS
        SELECT 
            d.*,
            r.{new_col}
        FROM {table_name} d
        LEFT JOIN {restriction_table} r
        ON ST_Intersects(ST_Envelope(d.geometry), ST_Envelope(r.geometry))
        AND ST_Within(d.geometry, r.geometry)
    """
    )


def assign_restriction_if_missing(con, restriction_config, table_name: str):
    """
    Checks if a restriction column is already present in the table.
    If not, assigns it using a spatial join.
    """
    name = restriction_config["name"]
    new_col = f"{name}_id"

    column_names = (
        con.execute(f"PRAGMA table_info('{table_name}')").fetchdf()["name"].tolist()
    )

    if new_col in column_names:
        print(f"✅ Skipping {name}: '{new_col}' already exists in '{table_name}'.")
    else:
        print(f"🔄 Assigning restriction '{new_col}' to '{table_name}'...")
        assign_restriction_to_table(con, restriction_config, table_name)


def load_table_with_restrictions(
    con,
    parquet_path: Path,
    base_columns: dict,
    validated_restrictions: dict,
    table_name: str,
):
    """
    Loads a Parquet dataset into a DuckDB temp table.
    - Uses user-defined aliases from `base_columns` (e.g., "address_id", "geometry" etc.)
    - Automatically extracts x/y from geometry if available
    - Includes any *_id restriction columns if they already exist in the source file
    - Creates or replaces a DuckDB temp table with the given `table_name`
    """
    parquet_path_str = str(parquet_path)

    # Step 1: Expected *_id restriction columns
    restriction_id_cols = [f"{r['name']}_id" for r in validated_restrictions.values()]

    # Step 2: Inspect available columns in the source file
    table_info = con.execute(
        f"DESCRIBE SELECT * FROM '{parquet_path_str}' LIMIT 0"
    ).fetchdf()
    available_columns = table_info["column_name"].tolist()

    # Step 3: Keep only those restriction columns that are present
    present_restriction_cols = [
        col for col in restriction_id_cols if col in available_columns
    ]

    # Step 4: Build select expressions from aliases
    select_expressions = []
    for alias, col in base_columns.items():
        if alias == "x":
            select_expressions.append(f"ST_X({col}) AS x")
        elif alias == "y":
            select_expressions.append(f"ST_Y({col}) AS y")
        else:
            select_expressions.append(f"{col} AS {alias}")

    # Add automatic x/y extraction if geometry is present but x/y not already defined
    if "x" not in base_columns and "geometry" in base_columns:
        select_expressions.append(f"ST_X({base_columns['geometry']}) AS x")
    if "y" not in base_columns and "geometry" in base_columns:
        select_expressions.append(f"ST_Y({base_columns['geometry']}) AS y")

    # Add present restriction columns as-is
    select_expressions += present_restriction_cols

    # Final SELECT clause
    select_clause = ",\n        ".join(select_expressions)

    # Build filter clause based on expected base fields
    geom_col = base_columns.get("geometry", "geometry")
    lat_col = base_columns.get("road_point_lat", "vej_pos_lat")
    lon_col = base_columns.get("road_point_lon", "vej_pos_lon")

    sql = f"""
        CREATE OR REPLACE TEMP TABLE {table_name} AS
        SELECT 
            {select_clause}
        FROM '{parquet_path_str}'
        WHERE {geom_col} IS NOT NULL 
          AND {lat_col} IS NOT NULL 
          AND {lon_col} IS NOT NULL
    """

    try:
        con.execute(sql)
        print(
            f"✅ Loaded '{table_name}' with {len(base_columns)} base fields and {len(present_restriction_cols)} restriction ID(s)"
        )
    except Exception as e:
        print(f"❌ Failed to create table '{table_name}'")
        print(e)
        print("SQL used:")
        print(sql)
        raise


# %%
# --- Step 0: Load the configuration file and validate restrictions ---
validated_restrictions = validate_restriction_config(config_data, con)

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
    assign_restriction_if_missing(con, restriction_config, "dwellings")

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
    assign_restriction_if_missing(con, restriction_config, "all_services")

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
                    "source_adress_id": src.address_id,
                    "source_lat": src.road_point_lat,
                    "source_lon": src.road_point_lon,
                    "dest_adress_id": dst.address_id,
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
