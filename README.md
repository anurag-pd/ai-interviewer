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

## Interview Logic: NUM_SKILLS and USER_DIFFICULTY

The interview process is controlled by two key constants in the backend (`app.py`):

- **NUM_SKILLS**: Determines how many unique skills (extracted from the uploaded resume) the AI will ask questions about during the interview. For example, if `NUM_SKILLS = 3`, the AI will select 3 skills from the candidate's resume and conduct the interview on those topics.

- **USER_DIFFICULTY**: A list that defines the number and difficulty of questions to be asked for each selected skill. Each entry in the list represents a difficulty level (e.g., `["Easy", "Medium", "Hard"]` means the AI will ask 3 questions per skill, one at each difficulty level). The length of this list determines how many questions are asked per skill.

**Example:**

If `NUM_SKILLS = 2` and `USER_DIFFICULTY = ["Medium", "Hard"]`, the AI will select 2 skills from the resume and ask 2 questions for each skill (one Medium, one Hard), for a total of 4 questions.

You can adjust these constants in `app.py` to customize the interview depth and breadth.

---

## How to Build and Run

### 1. Prerequisites

- Python 3.9+
- Node.js (v16+ recommended)
- npm

### 2. Setup (Install dependencies)

- **Windows:**
  ```powershell
  ./setup.ps1
  ```
- **Linux/macOS:**
  ```bash
  bash setup.sh
  ```

### 3. Run the App (Start backend and frontend)

- **Windows:**
  ```powershell
  ./run.ps1
  ```
- **Linux/macOS:**
  ```bash
  bash run.sh
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

- Candidate UI: [http://localhost:3000/](http://localhost:3000/)
- Admin Panel: [http://localhost:3000/admin](http://localhost:3000/admin)

### 6. Stop the App (Stop backend and frontend)

- Simple way would be to close the Terminals created

- **Windows:**
  ```powershell
  ./stop.ps1
  ```
- **Linux/macOS:**
  ```bash
  bash stop.sh
  ```

## Project Structure

```
Zeero/
├── app.py                # FastAPI backend
├── qa_engine.py          # ChromaDB logic
├── resume_parser.py      # Resume parsing logic
├── followup_generator.py # Follow-up question logic
├── requirements.txt      # Python dependencies
├── setup.ps1             # Windows setup script
├── setup.sh              # Linux/macOS setup script
├── run.ps1               # Windows run script
├── run.sh                # Linux/macOS run script
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

## Architecture Diagram

```text
+-------------------+         REST API         +-------------------+
|                   | <---------------------> |                   |
|   Vue 3 Frontend  |                         |   FastAPI Backend  |
|  (Vite, Pinia)    |                         |                   |
+-------------------+                         +-------------------+
        |                                             |
        |                                             |
        |                                             v
        |                                   +-------------------+
        |                                   |   ChromaDB (via   |
        |                                   |   LangChain)      |
        |                                   +-------------------+
        |                                             |
        |                                             v
        |                                   +-------------------+
        |                                   | HuggingFace       |
        |                                   | Embeddings        |
        |                                   +-------------------+
        |
        v
+-------------------+
|  Admin Panel      |
|  (Vue Route /admin)|
+-------------------+
```

### Flow

- Users interact with the Vue 3 SPA (candidate or admin).
- The frontend communicates with the FastAPI backend via REST API.
- The backend handles resume parsing, skill extraction, and interview logic.
- For question management and retrieval, the backend uses ChromaDB (via LangChain) and HuggingFace Embeddings.
- The admin panel (at `/admin`) allows question management through the same backend.
