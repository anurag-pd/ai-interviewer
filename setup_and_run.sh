#!/bin/bash
# Bash script to set up and run both backend (Python) and frontend (Vue)

# 1. Backend setup
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 2. Frontend setup
cd frontend
if [ ! -d "node_modules" ]; then
  npm install
fi
cd ..

# 3. Start backend (FastAPI)
echo "Starting backend (FastAPI)..."
source .venv/bin/activate
nohup uvicorn app:app --reload > backend.log 2>&1 &

# 4. Start frontend (Vite)
echo "Starting frontend (Vite)..."
cd frontend
nohup npm run dev > frontend.log 2>&1 &
cd ..

echo "Setup complete. Both backend and frontend are running in the background."
