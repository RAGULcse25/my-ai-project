@echo off
:: S.E.A.D.S. v14 — One-Click Full Stack Launcher
title S.E.A.D.S. v14 Launcher

echo.
echo  =========================================================
echo    S.E.A.D.S. v14  --  Full Stack Launcher
echo  =========================================================
echo.

:: Step 1: Install backend Python packages
echo  [1/3] Installing backend Python packages...
cd /d E:\seads\backend
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo  ERROR: pip install failed. Is Python installed?
    pause
    exit /b 1
)
echo  Backend packages OK.
echo.

:: Step 2: Launch backend in a new terminal window
echo  [2/3] Starting Backend on http://localhost:8000 ...
start "SEADS-Backend" cmd /k "cd /d E:\seads\backend && set PYTHONIOENCODING=utf-8 && set PYTHONUTF8=1 && python -m uvicorn main:app --port 8000 --host 0.0.0.0 --reload"

:: Wait for backend to boot
timeout /t 4 /nobreak >nul

:: Step 3: Launch frontend in a new terminal window
echo  [3/3] Starting Frontend on http://localhost:5173 ...
start "SEADS-Frontend" cmd /k "cd /d E:\seads\frontend && npm run dev"

:: Wait for Vite to boot
timeout /t 5 /nobreak >nul

:: Open browser
echo  Opening browser at http://localhost:5173 ...
start http://localhost:5173

echo.
echo  Both services are launching!
echo  Backend  --^>  http://localhost:8000
echo  Frontend --^>  http://localhost:5173
echo.
echo  Close the backend and frontend windows to stop.
pause
