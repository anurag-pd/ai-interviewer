# AI Interviewer

## Overview

This is a full-stack AI-powered technical interview platform. It allows users to upload their resume, extracts skills, and conducts an interactive interview with AI-generated questions and follow-ups. Admins can manage the question bank via a modern web interface.

## Architecture

- **Backend:** Python (FastAPI)
  - Handles resume upload, skill extraction, interview session management, and question/answer logic.
  - Uses ChromaDB (via LangChain) for storing and retrieving interview questions.
  - Exposes REST APIs for both user and admin operations.
- **Frontend:** Vue 3 SPA (Vite, Pinia)
  - Modern, responsive UI for candidates and admins.
  - State management with Pinia.
  - Communicates with backend via REST APIs.
- **Admin Panel:**
  - List, add, and remove questions from ChromaDB.
  - Accessible at `/admin` route.

## Technologies Used

- **Backend:**
  - Python 3.9+
  - FastAPI
  - Uvicorn
  - LangChain, ChromaDB, HuggingFace Embeddings
  - python-multipart, pydantic
- **Frontend:**
  - Vue 3 (Composition API)
  - Vite
  - Pinia (state management)
  - Modern CSS
- **Other:**
  - Node.js & npm (for frontend)
  - PowerShell/Bash scripts for setup

## How to Run

### 1. Prerequisites

- Python 3.9+
- Node.js (v16+ recommended)
- npm

### 2. Setup & Run (Windows)

Open PowerShell in the project root and run:

```powershell
./setup_and_run.ps1
```

### 3. Setup & Run (Linux/macOS)

Open terminal in the project root and run:

```bash
bash setup_and_run.sh
```

### 4. Manual Steps (if needed)

- Backend:
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # or .venv\Scripts\activate on Windows
  pip install -r requirements.txt
  uvicorn app:app --reload
  ```
- Frontend:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```

### 5. Access the App

- Candidate UI: [http://localhost:5173/](http://localhost:5173/)
- Admin Panel: [http://localhost:5173/admin](http://localhost:5173/admin)

## Project Structure

```
Zeero/
├── app.py                # FastAPI backend
├── qa_engine.py          # ChromaDB logic
├── resume_parser.py      # Resume parsing logic
├── followup_generator.py # Follow-up question logic
├── requirements.txt      # Python dependencies
├── setup_and_run.ps1     # Windows setup script
├── setup_and_run.sh      # Linux/macOS setup script
├── frontend/
│   ├── src/
│   │   ├── components/   # Vue components
│   │   ├── views/        # Vue views (pages)
│   │   ├── stores/       # Pinia stores
│   │   ├── App.vue, main.js, router
│   ├── package.json, vite.config.js
│   └── ...
└── .gitignore
```

ARCHITECTURE OF THE APP

+-------------------+ REST API +-------------------+
| | <---------------------> | |
| Vue 3 Frontend | | FastAPI Backend |
| (Vite, Pinia) | | |
+-------------------+ +-------------------+
| |
| |
| v
| +-------------------+
| | ChromaDB (via |
| | LangChain) |
| +-------------------+
| |
| v
| +-------------------+
| | HuggingFace |
| | Embeddings |
| +-------------------+
|
v
+-------------------+
| Admin Panel |
| (Vue Route /admin)|
+-------------------+

FLOW:

Users interact with the Vue 3 SPA (candidate or admin).
The frontend communicates with the FastAPI backend via REST API.
The backend handles resume parsing, skill extraction, and interview logic.
For question management and retrieval, the backend uses ChromaDB (via LangChain) and HuggingFace Embeddings.
The admin panel (at /admin) allows question management through the same backend.
