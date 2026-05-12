@echo off
:: S.E.A.D.S. v14 — Backend Startup Script
:: Runs uvicorn with UTF-8 encoding to prevent Windows cp1252 emoji crashes
:: ============================================================

title SEADS v14 Backend - Port 8000

:: Force UTF-8 for Python console output (fixes emoji UnicodeEncodeError on Windows)
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

:: Change to backend directory
cd /d E:\seads\backend

echo.
echo  ███████╗███████╗ █████╗ ██████╗ ███████╗    ██╗   ██╗ ██╗ ██╗  ██╗
echo  ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝    ██║   ██║███║ ██║  ██║
echo  ███████╗█████╗  ███████║██║  ██║███████╗    ██║   ██║╚██║ ███████║
echo  ╚════██║██╔══╝  ██╔══██║██║  ██║╚════██║    ╚██╗ ██╔╝ ██║ ╚════██║
echo  ███████║███████╗██║  ██║██████╔╝███████║     ╚████╔╝  ██║       ██║
echo  ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝      ╚═══╝  ╚═╝       ╚═╝
echo.
echo  S.E.A.D.S. v14  ^|  Multi-Agent Pipeline Orchestrator
echo  Claude Sonnet 4.6  ^|  100+ Agents  ^|  10K Tokens/Agent
echo  ============================================================
echo  Starting backend on http://localhost:8000
echo.

python -m uvicorn main:app --port 8000 --host 0.0.0.0

pause
