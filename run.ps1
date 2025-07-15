# PowerShell script to run backend and frontend only (no setup)

# 1. Start backend
Write-Host "Starting backend (FastAPI)..."
Start-Process powershell -ArgumentList '-NoExit', '-Command', '.\.venv\Scripts\Activate.ps1; uvicorn app:app --reload' -WorkingDirectory $PWD.Path

# 2. Start frontend
Write-Host "Starting frontend (Vite)..."
$frontendPath = Join-Path $PWD.Path 'frontend'
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'npm run dev' -WorkingDirectory $frontendPath

Write-Host "Both backend and frontend are running in new terminals."
