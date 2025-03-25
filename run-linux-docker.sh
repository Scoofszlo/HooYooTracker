#!/bin/bash

echo "Setting up HooYooTracker..."

# Build the Docker image
sudo docker build -t hooyootracker .

# Create a Docker volume
sudo docker volume create hooyootracker_data

# Run the HooYooTracker package
echo "Starting HooYooTracker..."
echo
sudo docker run -q -p 8080:8080 -q -v hooyootracker_data:/app hooyootracker
