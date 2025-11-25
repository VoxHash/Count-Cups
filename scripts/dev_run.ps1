# Development run script for Count-Cups (Windows PowerShell)
# Run this script from the project root directory

Write-Host "Starting Count-Cups in development mode..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
pip install -e .

# Set environment variables for development
$env:DEBUG = "true"
$env:LOG_LEVEL = "DEBUG"
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"

# Run the application
Write-Host "Starting application..." -ForegroundColor Green
python -m app.main $args
