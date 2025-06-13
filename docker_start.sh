#!/bin/bash

# Exit on any error
set -e

# Load conda shell functions
source /opt/conda/etc/profile.d/conda.sh

# Activate the desired conda environment
conda activate innotech

# Optional: Print Python path for debugging
echo "Using Python: $(which python)"
python --version

# Run setup script
echo "Running setup_folders.py..."
python /home/jovyan/work/setup_folders.py

# Configurable OTP version
OTP_VERSION="2.6.0"
OTP_JAR_NAME="otp-${OTP_VERSION}-shaded.jar"
OTP_DIR="/home/jovyan/work/otp"
OTP_JAR_PATH="${OTP_DIR}/otp.jar"

# Download OTP jar if it doesn't exist
if [ ! -f "$OTP_JAR_PATH" ]; then
    echo "Downloading OpenTripPlanner version $OTP_VERSION..."
    wget "https://repo1.maven.org/maven2/org/opentripplanner/otp/${OTP_VERSION}/${OTP_JAR_NAME}" -O "$OTP_JAR_PATH"
else
    echo "OTP jar already exists at $OTP_JAR_PATH"
fi


# Start Jupyter Notebook
echo "Starting Jupyter Notebook..."
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token=''
