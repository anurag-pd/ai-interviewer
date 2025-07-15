#!/bin/bash
# Bash script to stop backend (uvicorn) and frontend (node) processes

echo "Stopping backend (uvicorn) and frontend (node) processes..."
# Stop uvicorn
pkill -f "uvicorn app:app"
# Stop node (Vite dev server)
pkill -f "node.*vite"
echo "All relevant processes stopped."
