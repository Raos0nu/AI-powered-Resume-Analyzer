@echo off
REM AI-Powered Resume Analyzer - Startup Script for Windows
REM This script starts both the backend server and opens the frontend

echo.
echo ================================
echo AI-Powered Resume Analyzer
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then activate it and install dependencies: pip install -r backend\requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [WARNING] Dependencies not installed!
    echo [INFO] Installing dependencies...
    pip install -r backend\requirements.txt
)

REM Start backend server
echo.
echo [INFO] Starting backend server on http://localhost:5000...
start "Resume Analyzer Backend" cmd /k "cd backend && python app.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend server
echo [INFO] Starting frontend server on http://localhost:8080...
start "Resume Analyzer Frontend" cmd /k "cd frontend && python -m http.server 8080"

REM Wait and then open browser
timeout /t 2 /nobreak >nul
echo.
echo [SUCCESS] Application started successfully!
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:8080
echo.
echo Opening browser...
start http://localhost:8080

echo.
echo Press any key to stop all servers...
pause >nul

REM Cleanup - kill all Python processes started by this script
echo.
echo [INFO] Stopping servers...
taskkill /FI "WindowTitle eq Resume Analyzer Backend*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Resume Analyzer Frontend*" /T /F >nul 2>&1

echo [SUCCESS] All servers stopped. Goodbye!

