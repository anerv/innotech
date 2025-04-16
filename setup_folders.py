# Run this while while in the main folder

import os

parent_folders = ["data", "results"]

for f in parent_folders:
    if not os.path.exists(f):
        os.mkdir(f)

        print("Successfully created folder: " + f)


data_folders = ["input", "processed"]
for f in data_folders:
    if not os.path.exists(os.path.join("data", f)):
        os.mkdir(os.path.join("data", f))

        print("Successfully created folder: " + f)

input_base = "data/input"
processed_base = "data/processed"

input_subfolders = ["cvr", "adresser", "DK_AdministrativeUnit"]
processed_subfolders = ["cvr", "adresser", "adm_boundaries"]

for f in input_subfolders:
    if not os.path.exists(os.path.join(input_base, f)):
        os.mkdir(os.path.join(input_base, f))

        print("Successfully created folder: " + os.path.join(input_base, f))

for f in processed_subfolders:
    if not os.path.exists(os.path.join(processed_base, f)):
        os.mkdir(os.path.join(processed_base, f))

        print("Successfully created folder: " + os.path.join(processed_base, f))

result_subfolders = ["data", "maps"]

for f in result_subfolders:
    if not os.path.exists(os.path.join("results", f)):
        os.mkdir(os.path.join("results", f))

        print("Successfully created folder: " + os.path.join("results", f))
