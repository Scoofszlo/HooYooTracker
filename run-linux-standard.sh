#!/bin/bash

# Check if uv is installed. If not, install it
echo "Checking for uv installation..."
if ! command -v uv &> /dev/null; then
    echo uv not found. Installing uv...
    curl -LsSf https://astral.sh/uv/install.sh | sh
else
    echo "uv is already installed"
fi

# Creates virtual environment using uv
uv venv --python=3.10 -q

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install/update dependencies using uv
uv sync --no-dev

# Run the HooYooTracker package
echo "Starting HooYooTracker..."
echo
python3 -m hooyootracker
