@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"
title Archive Extractor - Setup and Runner

echo ============================================
echo    Archive Extractor - Setup and Runner   
echo ============================================
echo.

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found in PATH
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "py_ver=%%i"
echo Python !py_ver! found.
echo.

:: Create venv if needed
if not exist ".venv" (
    echo Setting up environment for the first time...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
    set "first_run=1"
)

set "VENV_PY=.venv\Scripts\python.exe"

:: Activate environment
call .venv\Scripts\activate.bat

:: Create requirements.txt if missing
if not exist "requirements.txt" (
    echo colorama > requirements.txt
    echo py7zr >> requirements.txt
    echo rarfile >> requirements.txt
)

:: Upgrade pip only on first run
if defined first_run (
    echo Preparing environment, please wait...
    %VENV_PY% -m pip install --disable-pip-version-check --no-cache-dir --upgrade pip >nul 2>&1
)

:: Check if packages are installed
%VENV_PY% -c "import colorama, py7zr, rarfile" >nul 2>&1
if errorlevel 1 (
    echo Installing required components...
    %VENV_PY% -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt >nul 2>&1
    :: Verify again
    %VENV_PY% -c "import colorama, py7zr, rarfile" >nul 2>&1
    if errorlevel 1 (
        echo Failed to install required components. Please check your internet connection or try again later.
        pause
        exit /b 1
    )
    echo All components installed successfully.
    timeout /t 2 >nul
) else (
    echo All components are ready.
    timeout /t 2 >nul
)

echo.

:: Run main script
if exist "removefolder.py" (
    echo Running archive extractor...
    timeout /t 2 >nul
    %VENV_PY% removefolder.py
) else (
    echo Error: removefolder.py not found in the current directory.
)

echo.
echo Press any key to exit...
pause >nul
