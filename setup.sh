#!/bin/bash
# Bash script to set up backend and frontend dependencies only

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

echo "Setup complete. You can now run the app using run.sh."
