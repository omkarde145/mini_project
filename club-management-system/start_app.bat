@echo off
title Campus Club Management System
echo ===================================================
echo     Launching Campus Club Management System
echo ===================================================
echo.

:: Ensure current working directory is the script directory
cd /d "%~dp0"

:: Locate backend directory
if exist "backend\app.py" (
    cd backend
) else if exist "club-management-system\backend\app.py" (
    cd club-management-system\backend
) else (
    echo [ERROR] Could not locate backend\app.py!
    pause
    exit /b 1
)

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in your system PATH.
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

:: Run database initialization if database file doesn't exist
if not exist "club_system.db" (
    echo [*] First-time launch detected. Initializing database and seed data...
    python init_db.py
)

:: Launch the default browser after waiting 2 seconds for Flask to bind
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:5000"

:: Start the Flask server
echo [*] Starting Flask application server on http://127.0.0.1:5000...
echo [*] Opening app in your default web browser...
echo [*] Press Ctrl+C in this window anytime to stop the server.
echo.
python app.py

pause
