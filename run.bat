@echo off

:: Creates virtual environment if not exist and install the external
:: dependencies needed for program to run
IF NOT EXIST .venv (
    python -m venv .venv
)

:: Activate the virtual environment
call .venv\Scripts\activate.bat

:: Check if poetry is installed, if not, install it
poetry --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    pip install poetry
    :: Install dependencies using poetry
    poetry install
)

:: Run the web application from webapp.py
python webapp.py
