@echo off
setlocal enabledelayedexpansion
title CustomerInsight Launcher

:: Loyiha ildiz papkasiga o'tish
cd /d "%~dp0"

echo ===================================================================
echo             CustomerInsight - AI Platform Launcher
echo ===================================================================
echo.

:: Python interpreterini aniqlash
set PYTHON_EXE=
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=py"
)

echo [1/2] Backend (FastAPI) ishga tushirilmoqda...
start "CustomerInsight Backend (FastAPI)" cmd /k "cd /d "%~dp0" && "%PYTHON_EXE%" -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000"

echo [2/2] Frontend (React Vite) ishga tushirilmoqda...
start "CustomerInsight Frontend (React)" cmd /k "cd /d "%~dp0frontend" && npm.cmd run dev -- --host 127.0.0.1"

echo.
echo ===================================================================
echo   Platforma muvaffaqiyatli ishga tushirildi!
echo.
echo   - Web Dashboard: http://localhost:5173
echo   - API Swagger:   http://localhost:8000/docs
echo.
echo   Telegram Botni ishga tushirish uchun "start_bot.bat" ni bosing.
echo ===================================================================
echo.
pause
