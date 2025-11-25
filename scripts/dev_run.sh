#!/bin/bash
# Development run script for Count-Cups
# Run this script from the project root directory

set -e

echo "Starting Count-Cups in development mode..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install -e .

# Set environment variables for development
export DEBUG=true
export LOG_LEVEL=DEBUG
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run the application
echo "Starting application..."
python -m app.main "$@"
