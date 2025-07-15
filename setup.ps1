# PowerShell script to set up backend and frontend dependencies only

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

Write-Host "Setup complete. You can now run the app using run.ps1."
