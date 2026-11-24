@echo off
echo ========================================================
echo     CustomerInsight - Platformani Ishga Tushirish
echo ========================================================

echo [1/2] Backend (FastAPI) ishga tushirilmoqda (Port: 8000)...
start "CustomerInsight Backend" cmd /k ".venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000"

echo [2/2] Frontend (React Vite) ishga tushirilmoqda (Port: 5173)...
start "CustomerInsight Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Hammasi tayyor!
echo - Web Dashboard: http://localhost:5173
echo - API Swagger:   http://localhost:8000/docs
echo ========================================================
pause
