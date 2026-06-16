@echo off
REM SpareBank 1 Lotteri - Startup Script for Windows

echo.
echo ==========================================
echo   🎰 SpareBank 1 Lotteri
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python er ikke installert.
    echo Last ned fra https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python finnes

REM Check if venv exists, if not create it
if not exist "venv" (
    echo 📦 Setter opp virtuelt miljø...
    python -m venv venv
)

REM Activate venv
echo ✓ Aktiverer virtuelt miljø
call venv\Scripts\activate.bat

REM Install/update packages
echo 📦 Installerer avhengigheter...
pip install -q -r requirements.txt

REM Start the application
echo.
echo 🚀 Starter applikasjonen...
echo.
echo 📍 Åpne nettleseren på: http://localhost:5000
echo.
echo Trykk CTRL+C for å stoppe applikasjonen.
echo.

python app.py

pause
