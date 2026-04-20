@echo off
REM Bot launcher script for Windows

setlocal enabledelayexpand

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%

REM Check if .env file exists
if not exist "%PROJECT_DIR%.env" (
    echo ❌ .env file not found!
    echo    Please create .env file from .env.example
    echo.
    echo    Steps:
    echo    1. copy .env.example .env
    echo    2. Edit .env and add your BOT_TOKEN
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "%PROJECT_DIR%venv" (
    echo 📦 Creating virtual environment...
    python -m venv "%PROJECT_DIR%venv"
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call "%PROJECT_DIR%venv\Scripts\activate.bat"

REM Install requirements
echo 📥 Installing requirements...
pip install -q -r "%PROJECT_DIR%requirements.txt"

REM Run the bot
echo 🚀 Starting bot...
cd "%PROJECT_DIR%src"
python main.py

pause
