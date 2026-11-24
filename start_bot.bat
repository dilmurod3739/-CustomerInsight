@echo off
title CustomerInsight Telegram Bot
cd /d "%~dp0"

set PYTHON_EXE=
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=py"
)

echo ===================================================================
echo          CustomerInsight - Telegram Bot Launcher
echo ===================================================================
echo.
echo Bot ishga tushirilmoqda...
"%PYTHON_EXE%" -m bot.bot
pause
