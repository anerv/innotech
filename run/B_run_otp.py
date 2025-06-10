#%%

import subprocess
from pathlib import Path

this_path = Path(__file__).resolve()
root_path = this_path.parent.parent
scripts_path = root_path / "scripts"

scripts = [
    "B00_find_nearest_destinations.py",
    "B01_find_routes.py",
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
