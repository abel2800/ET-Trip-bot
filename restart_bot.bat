@echo off
title Trip Ethiopia Bot
color 0A
chcp 65001 > nul
cls
echo.
echo ================================
echo  🇪🇹 Trip Ethiopia Bot
echo ================================
echo.
echo ✅ Fixed import error!
echo 🚀 Starting bot...
echo.
echo Press Ctrl+C to stop
echo.
cd /d "%~dp0"
venv\Scripts\python.exe main.py
pause

