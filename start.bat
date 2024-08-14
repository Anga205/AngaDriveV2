@echo off

set VENV_DIR=venv

if exist %VENV_DIR% (
    echo Activating virtual environment...
    call %VENV_DIR%\Scripts\activate
) else (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
    echo Activating virtual environment...
    call %VENV_DIR%\Scripts\activate
    reflex init
)

echo Installing requirements...
pip install -r requirements.txt

echo Virtual environment setup complete.

reflex run --env prod