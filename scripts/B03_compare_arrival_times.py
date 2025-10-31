# %%

# PROCESS RESULTS FROM SERVICE ACCESS ANALYSIS

import pandas as pd
import geopandas as gpd
import yaml
from pathlib import Path
import os
import sys
import re
from os import listdir
from os.path import isfile, join
from src.helper_functions import (
    highlight_max_traveltime,
    highlight_min_traveltime,
    unpack_modes_from_json,
    transfers_from_json,
    plot_traveltime_results,
    plot_no_connection,
)


# Define the path to the config.yml file
script_path = Path(__file__).resolve()
root_path = script_path.parent.parent

results_path = root_path / "results_rural"
config_path = root_path / "config.yml"

# Read and parse the YAML file
with open(config_path, "r") as file:
    config_model = yaml.safe_load(file)

    crs = config_model["crs"]


# %%

# TODO:

# plot kde of travel time distributions for each service, with a curve for each arrival time
# pivot table with service types as rows and arrival times as columns, showing mean/median, min and max travel times

# loop through services and arrival times again
# for each service, read in all arrival time results and combine into a single dataframe

for arrival_time in arrival_times:

    for service in services:

        pass
