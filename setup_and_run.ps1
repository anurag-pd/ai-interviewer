# PowerShell script to set up and run both backend (Python) and frontend (Vue)

# 1. Backend setup
Write-Host "Setting up Python backend..."
if (!(Test-Path .venv)) {
    python -m venv .venv
}
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# 2. Frontend setup
Write-Host "Setting up Vue frontend..."
cd frontend
if (!(Test-Path node_modules)) {
    npm install
}
cd ..

# 3. Start backend
Write-Host "Starting backend (FastAPI)..."
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd "'+$PWD.Path+'"; .\.venv\Scripts\Activate.ps1; uvicorn app:app --reload'

# 4. Start frontend
Write-Host "Starting frontend (Vite)..."
cd frontend
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd "'+$PWD.Path+'"; npm run dev'
cd ..

Write-Host "Setup complete. Both backend and frontend are running in new terminals."
