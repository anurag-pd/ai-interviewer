#!/bin/bash
# Bash script to run backend and frontend only (no setup)

# 1. Start backend (FastAPI)
echo "Starting backend (FastAPI)..."
source .venv/bin/activate
nohup uvicorn app:app --reload > backend.log 2>&1 &

# 2. Start frontend (Vite)
echo "Starting frontend (Vite)..."
cd frontend
nohup npm run dev > frontend.log 2>&1 &
cd ..

echo "Both backend and frontend are running in the background."
