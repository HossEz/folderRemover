@echo off
pip uninstall -y colorama py7zr rarfile

:: Verify uninstallation
pip show colorama py7zr rarfile
pause
