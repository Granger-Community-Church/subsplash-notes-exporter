@echo off
REM Quick launcher for the notes viewer

cd /d "%~dp0"

echo Generating notes index...
venv\Scripts\python generate_index.py

if errorlevel 1 (
    echo.
    echo Error generating index. Make sure you have exported notes first.
    pause
    exit /b 1
)

echo.
echo Starting web viewer...
echo.
venv\Scripts\python start_viewer.py

pause
