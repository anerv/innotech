#%%

import subprocess
from pathlib import Path

this_path = Path(__file__).resolve()
root_path = this_path.parent.parent
scripts_path = root_path / "scripts"

scripts = [
    "A00_prepare_study_area_boundary_data.py",
    "A01_prepare_address_data.py",
    "A02_prepare_bbr_address_data.py",
    "A03_prepare_cvr_data.py",
    "A04_download_processs_osm_data.py",
    "A05_combine_cvr_osm_data.py",
    "A06_prepare_osm_otp_data.py",
]

for script in scripts:

    print(f"Running script: {script}")
    result = subprocess.run(["python", scripts_path / script], capture_output=True, text=True)

    print(f"Output from {script}:")
    print(result.stdout)

    if result.stderr:
        print("Error output:")
        print(result.stderr)

# Check if the script ran successfully
    if result.returncode != 0:
        print(f"Script {script} failed with return code {result.returncode}")
    else:
        print(f"Script {script} completed successfully.")
# %%
