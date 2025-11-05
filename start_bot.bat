@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo.
echo ================================
echo  🇪🇹 Trip Ethiopia Bot
echo ================================
echo.
echo Starting bot...
echo Press Ctrl+C to stop
echo.
venv\Scripts\python.exe main.py
pause

