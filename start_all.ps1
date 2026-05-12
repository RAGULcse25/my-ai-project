# S.E.A.D.S. v14 — Full Stack Startup Script (PowerShell)
# Starts Backend (FastAPI) + Frontend (Vite) simultaneously
# Auto-opens browser after startup

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host " ╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host " ║         S.E.A.D.S. v14 — Full Stack Launcher            ║" -ForegroundColor Cyan
Write-Host " ║   Backend: http://localhost:8000  |  Frontend: :5173    ║" -ForegroundColor Cyan
Write-Host " ╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Paths ─────────────────────────────────────────────────────
$ROOT      = "E:\seads"
$BACKEND   = "$ROOT\backend"
$FRONTEND  = "$ROOT\frontend"

# ── Check Python ──────────────────────────────────────────────
Write-Host "[1/4] Checking Python..." -ForegroundColor Yellow
$pyVer = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Python not found. Install Python 3.10+ and retry." -ForegroundColor Red
    pause; exit 1
}
Write-Host "  ✅ $pyVer" -ForegroundColor Green

# ── Check/Install backend dependencies ────────────────────────
Write-Host "[2/4] Checking backend dependencies..." -ForegroundColor Yellow
$uvicornCheck = python -c "import uvicorn" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  📦 Installing backend requirements..." -ForegroundColor Yellow
    Set-Location $BACKEND
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ❌ pip install failed. Check requirements.txt" -ForegroundColor Red
        pause; exit 1
    }
}
Write-Host "  ✅ Backend dependencies OK" -ForegroundColor Green

# ── Check Node.js ─────────────────────────────────────────────
Write-Host "[3/4] Checking Node.js / npm..." -ForegroundColor Yellow
$nodeVer = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Node.js not found. Install Node.js 18+ and retry." -ForegroundColor Red
    pause; exit 1
}
Write-Host "  ✅ Node $nodeVer" -ForegroundColor Green

# ── Install frontend dependencies if needed ───────────────────
if (-not (Test-Path "$FRONTEND\node_modules")) {
    Write-Host "  📦 Installing frontend dependencies (first run)..." -ForegroundColor Yellow
    Set-Location $FRONTEND
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ❌ npm install failed" -ForegroundColor Red
        pause; exit 1
    }
}
Write-Host "  ✅ Frontend dependencies OK" -ForegroundColor Green

# ── Launch Backend ────────────────────────────────────────────
Write-Host ""
Write-Host "[4/4] Starting services..." -ForegroundColor Yellow
Write-Host "  🚀 Backend  → http://localhost:8000" -ForegroundColor Magenta
Write-Host "  🚀 Frontend → http://localhost:5173" -ForegroundColor Magenta
Write-Host ""

# Start backend in new window
Start-Process powershell -ArgumentList @(
    "-NoProfile",
    "-NoExit",
    "-Command",
    "Set-Location '$BACKEND'; `$env:PYTHONIOENCODING='utf-8'; `$env:PYTHONUTF8='1'; Write-Host 'S.E.A.D.S. Backend Starting...' -ForegroundColor Cyan; python -m uvicorn main:app --port 8000 --host 0.0.0.0 --reload"
) -WindowStyle Normal

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend in new window
Start-Process powershell -ArgumentList @(
    "-NoProfile",
    "-NoExit",
    "-Command",
    "Set-Location '$FRONTEND'; Write-Host 'S.E.A.D.S. Frontend Starting...' -ForegroundColor Cyan; npm run dev"
) -WindowStyle Normal

# Wait for Vite to be ready, then open browser
Write-Host "  ⏳ Waiting for Vite to be ready..." -ForegroundColor Gray
Start-Sleep -Seconds 5

Write-Host "  🌐 Opening browser..." -ForegroundColor Green
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host " ✅ Both services launched successfully!" -ForegroundColor Green
Write-Host " Backend  → http://localhost:8000" -ForegroundColor Cyan
Write-Host " Frontend → http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host " Press Ctrl+C in each terminal to stop." -ForegroundColor Gray
Write-Host ""
pause
