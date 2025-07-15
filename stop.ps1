# PowerShell script to stop backend (uvicorn) and frontend (node) processes

Write-Host "Stopping backend (uvicorn) and frontend (node) processes..."
Get-Process uvicorn -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "All relevant processes stopped."
