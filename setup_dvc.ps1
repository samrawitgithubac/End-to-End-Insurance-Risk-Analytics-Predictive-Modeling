# DVC Setup Script for Insurance Analytics Project (PowerShell)

Write-Host "Setting up DVC for Insurance Analytics Project..." -ForegroundColor Green

# Initialize DVC
Write-Host "1. Initializing DVC..." -ForegroundColor Yellow
dvc init

# Create local storage directory
$STORAGE_PATH = ".\dvc_storage"
Write-Host "2. Creating local storage directory at $STORAGE_PATH..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $STORAGE_PATH -Force | Out-Null

# Add local remote storage
Write-Host "3. Adding local remote storage..." -ForegroundColor Yellow
dvc remote add -d localstorage $STORAGE_PATH

# Configure DVC
Write-Host "4. Configuring DVC..." -ForegroundColor Yellow
dvc config core.autostage true

Write-Host "`nDVC setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Place your data files in the data/ directory"
Write-Host "2. Run: dvc add data/your_data_file.csv"
Write-Host "3. Commit the .dvc files: git add data/*.dvc data/.gitignore"
Write-Host "4. Push data: dvc push"

