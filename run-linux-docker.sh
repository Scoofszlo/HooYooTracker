#!/bin/bash

echo "Setting up HooYooTracker..."

# Build the Docker image
docker build -q -t hooyootracker .

# Create a Docker volume
docker volume create hooyootracker_data

# Run the HooYooTracker package
echo "Starting HooYooTracker..."
echo
docker run -q -p 8080:8080 -q -v hooyootracker_data:/app hooyootracker
