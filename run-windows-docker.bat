@echo off

echo Setting up HooYooTracker...

:: Build the Docker image
docker build -q -t hooyootracker . >nul 2>&1

:: Create a Docker volume
docker volume create hooyootracker_data >nul 2>&1

:: Run the HooYooTracker through Docker
echo Starting HooYooTracker...
echo.
docker run -q -p 8080:8080 -q -v hooyootracker_data:/app hooyootracker

pause
