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

input_subfolders = ["cvr", "adresser", "bbr", "DK_AdministrativeUnit", "osm", "byzoner"]

processed_subfolders = [
    "cvr",
    "adresser",
    "bbr",
    "adm_boundaries",
    "destinations",
    "osm",
]

for f in input_subfolders:
    if not os.path.exists(os.path.join(input_base, f)):
        os.mkdir(os.path.join(input_base, f))

        print("Successfully created folder: " + os.path.join(input_base, f))

for f in processed_subfolders:
    if not os.path.exists(os.path.join(processed_base, f)):
        os.mkdir(os.path.join(processed_base, f))

        print("Successfully created folder: " + os.path.join(processed_base, f))

result_subfolders = ["data", "maps", "destination_data_evaluation"]

for f in result_subfolders:
    if not os.path.exists(os.path.join("results", f)):
        os.mkdir(os.path.join("results", f))

        print("Successfully created folder: " + os.path.join("results", f))


# illustration folder
if not os.path.exists("illustrations"):
    os.mkdir("illustrations")

    print("Successfully created folder: illustrations")


# Folder for OTP data and results
if not os.path.exists("otp"):
    os.mkdir("otp")

    print("Successfully created folder: illustrations")
