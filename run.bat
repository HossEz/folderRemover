@echo off
cd %~dp0

:: Check if Python is installed
echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python first.
    pause
    exit /b
)

:: Check if requirements are already installed
echo Checking for requirements...
pip show colorama py7zr rarfile >nul 2>&1
if %errorlevel% neq 0 (
    :: Display installing message
    echo Installing requirements...
    pip install -r requirements.txt > install.log 2>&1

    :: Check if the installation was successful
    :CheckLoop
    pip show colorama py7zr rarfile >nul 2>&1
    if %errorlevel% neq 0 (
        echo Waiting for requirements to be installed...
        timeout /t 1 >nul
        goto CheckLoop
    )
    echo Requirements installed successfully.
) else (
    echo Requirements already installed.
)

:: Run the Python script
echo Running the script...
python removefolder.py
pause
