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

# Create folder structure
echo "Running setup_folders.py..."
python /home/jovyan/work/setup_folders.py

# Start OpenTripPlanner in the background
echo "Starting OpenTripPlanner..."
java -Xmx2G -jar /usr/src/app/otp.jar &

# Start Jupyter Notebook
echo "Starting Jupyter Notebook..."
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token=''
