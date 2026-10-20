@echo off
title OwnSHoes - Shoe Sales Analytics
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
    py -m venv .venv
) else (
    python -m venv .venv
)
if not exist ".venv\Scripts\python.exe" (
    echo Python was not found. Install Python 3.11 or newer, then run this file again.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
".venv\Scripts\python.exe" -m streamlit run app.py
pause
