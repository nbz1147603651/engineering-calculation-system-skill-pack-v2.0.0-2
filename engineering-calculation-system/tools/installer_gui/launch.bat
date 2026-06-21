@echo off
REM Engineering Calculation System - one-click deployment console launcher.
REM Double-click this file, or run from a terminal. Requires Python 3.9+.
setlocal
cd /d "%~dp0"
python app.py
if errorlevel 1 (
    echo.
    echo The console exited with an error. See messages above.
    pause
)
endlocal
