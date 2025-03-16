@echo off

:: Creates virtual environment if not exist
IF NOT EXIST .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate the virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

:: Check if uv is installed. If not, install it
echo Checking for uv installation...
uv --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo uv not found. Installing uv...
    pip install uv==0.6.6
) ELSE (
    echo uv is already installed
)

:: Install/update dependencies using uv
echo Installing/updating dependencies with uv...
uv pip install -r pyproject.toml

:: Run the HooYooTracker package
echo.
echo Starting HooYooTracker...
echo.
python -m hooyootracker
