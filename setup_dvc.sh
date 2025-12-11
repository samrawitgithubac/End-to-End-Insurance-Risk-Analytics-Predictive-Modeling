#!/bin/bash
# DVC Setup Script for Insurance Analytics Project

echo "Setting up DVC for Insurance Analytics Project..."

# Initialize DVC
echo "1. Initializing DVC..."
dvc init

# Create local storage directory (adjust path as needed)
STORAGE_PATH="./dvc_storage"
echo "2. Creating local storage directory at $STORAGE_PATH..."
mkdir -p $STORAGE_PATH

# Add local remote storage
echo "3. Adding local remote storage..."
dvc remote add -d localstorage $STORAGE_PATH

# Configure DVC
echo "4. Configuring DVC..."
dvc config core.autostage true

echo "DVC setup complete!"
echo ""
echo "Next steps:"
echo "1. Place your data files in the data/ directory"
echo "2. Run: dvc add data/your_data_file.csv"
echo "3. Commit the .dvc files: git add data/*.dvc data/.gitignore"
echo "4. Push data: dvc push"

