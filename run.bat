@echo off

:: Creates virtual environment if not exist
IF NOT EXIST .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate the virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

:: Check if poetry is installed. If not, install it
echo Checking for Poetry installation...
poetry --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Poetry not found. Installing Poetry...
    pip install poetry
    :: Install dependencies using poetry
    echo Installing dependencies with Poetry...
    poetry install
) ELSE (
    echo Poetry is already installed
)

:: Run the HooYooTracker package
echo Starting HooYooTracker...
echo.
python -m hooyootracker
