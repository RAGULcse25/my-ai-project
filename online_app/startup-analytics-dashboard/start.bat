@echo off
echo Starting Startup Analytics Dashboa...
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:3001
echo.

start "Backend" cmd /k "cd backend && npm install && npx prisma generate && npx prisma migrate dev --name init && node prisma/seed.js && npm run dev"
timeout /t 3 /nobreak > nul
start "Frontend" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo Both servers starting...
echo Open http://localhost:5173 in your browser
pause
