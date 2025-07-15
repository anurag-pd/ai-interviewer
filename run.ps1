# PowerShell script to run backend and frontend only (no setup)

# 1. Start backend
Write-Host "Starting backend (FastAPI)..."
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd "'+$PWD.Path+'"; .\.venv\Scripts\Activate.ps1; uvicorn app:app --reload'

# 2. Start frontend
Write-Host "Starting frontend (Vite)..."
cd frontend
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd "'+$PWD.Path+'"; npm run dev'
cd ..

Write-Host "Both backend and frontend are running in new terminals."
