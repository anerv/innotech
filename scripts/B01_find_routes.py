# %%%  Step 0 load libraries and configuration

import yaml
from pathlib import Path
import duckdb
from src.helper_functions import process_adresses

# %%

# Define the path to the config.yml file
script_path = Path(__file__).resolve()
root_path = script_path.parent.parent
data_path = root_path / "data/processed/destinations"
results_path = root_path / "results/data"
config_path = root_path / "config.yml"

# Read and parse the YAML file
with open(config_path, "r") as file:
    config_model = yaml.safe_load(file)


sample_size = config_model[
    "sample_size"
]  # Number of rows to sample from the data 0 = all
chunk_size = config_model["chunk_size"]  # number of rows to load into memory
parallelism = config_model["parallelism"]  # number of parallel processes to use
url = config_model["otp_url"]  # Load the OTP endpoint URL
date = config_model["travel_date"]  # Load the date of the travel
otp_db_fp = (
    results_path / config_model["otp_results"]
)  # Load the persistant OTP database file path

walk_speed = config_model["walk_speed"]  # Load the walk speed in m/s
search_window = config_model["search_window"]  # Load the search window in seconds
# %%

# DubckDB connection
con = duckdb.connect()

# Open a persistent DuckDB database file Data is stored temporay in Dockdb and then exported to parquet
otp_con = duckdb.connect(otp_db_fp)

# %%
services = config_model["services"]

for service in services:
    for i in range(1, int(service["n_neighbors"]) + 1):
        dataset = f"{service['service_type']}_{i}"
        # Process each dataset
        print(
            f"Processing {dataset} with sample size {sample_size} and chunk size {chunk_size}"
        )
        process_adresses(
            dataset,
            sample_size,
            service["arival_time"],
            date,
            search_window,
            url,
            data_path,
            otp_con,
            con,
            chunk_size,
            parallelism,
        )
        # Export to parquet
        tabelname = dataset.replace("-", "_")
        otp_con.execute(
            f"""
            COPY (SELECT * FROM {tabelname}) TO '{results_path}/{dataset}_otp.parquet' (FORMAT 'parquet')
        """
        )

# %%
