@echo off
REM Adventure Communist Save Decoder GUI Launcher

echo Starting Adventure Communist Save Decoder...
echo.

python decoder_gui.py

if errorlevel 1 (
    echo.
    echo Error running the GUI. Make sure Python is installed.
    pause
)
