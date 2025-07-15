from fastapi import status, Request

from qa_engine import add_question_to_chroma, list_all_questions, remove_question_by_id

import io
import random
from uuid import uuid4
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from resume_parser import extract_text_from_pdf, extract_skills
from followup_generator import generate_followup
from qa_engine import get_questions_for_skill

# --- Constants ---
USER_DIFFICULTY = ["Medium"]
NUM_SKILLS = 1

# --- In-memory session store (Replace with Redis/db in production) ---
session_store = {}

# --- FastAPI App Initialization ---
app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Upload Resume and Extract Skills ---
@app.post("/api/upload_resume")
async def upload_resume(
    resume: UploadFile = File(...), 
    job_title: str = Form("")
):
    pdf_bytes = await resume.read()
    text = extract_text_from_pdf(io.BytesIO(pdf_bytes))
    skills = extract_skills(text)

    all_skills = [skill for skill_list in skills.values() for skill in skill_list]
    selected_topics = random.sample(all_skills, min(NUM_SKILLS, len(all_skills))) if all_skills else []

    # Create a new session
    session_id = str(uuid4())
    session_store[session_id] = {
        "selected_topics": selected_topics,
        "skills": skills,
        "job_title": job_title,
        "resume_text": text
    }

    response = JSONResponse({
        "resume_text": text,
        "extracted_skills": skills,
        "job_title": job_title,
        "session_id": session_id,
        "user_difficulty": USER_DIFFICULTY
    })
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response

# --- Start Interview with Greeting ---
@app.post("/api/start_interview")
async def start_interview(request: Request):
    session_id = request.cookies.get("session_id")
    session = session_store.get(session_id, {})
    job_title = session.get("job_title", "your role")

    return JSONResponse({
        "greeting": f"Hi there! Thanks for sharing your resume. Let's begin your technical interview for {job_title}.",
        "first_question": "Can you briefly introduce yourself?"
    })

@app.post("/api/rag_question")
async def rag_question(request: Request):
    data = await request.json()
    current_skill_index = data.get("current_skill_index", 0)

    session_id = request.cookies.get("session_id")
    session = session_store.get(session_id, {})
    selected_topics = session.get("selected_topics", [])

    if not selected_topics:
        return JSONResponse({
            "message": "No skills selected. Interview finished.",
            "rag_question": None,
            "end": True
        })

    if current_skill_index >= len(selected_topics):
        return JSONResponse({
            "message": "Interview finished. Thank you!",
            "rag_question": None,
            "end": True
        })

    skill = selected_topics[current_skill_index]
    rag_questions = get_questions_for_skill(skill)
    question = rag_questions[0] if rag_questions else f"Can you discuss your experience with {skill}?"

    # Do NOT increment next_skill_index here; only after all difficulties are done
    return JSONResponse({
        "skill": skill,
        "rag_question": question,
        "next_skill_index": current_skill_index,  # stay on current skill
        "end": False  # explicitly state it's not the end
    })

@app.post("/api/followup")
async def followup(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "")
    current_skill_index = data.get("current_skill_index", 0)
    current_difficulty_index = data.get("current_difficulty_index", 0)

    session_id = request.cookies.get("session_id")
    session = session_store.get(session_id, {})
    selected_topics = session.get("selected_topics", [])
    print(selected_topics, current_skill_index, current_difficulty_index)

    if not selected_topics or current_skill_index >= len(selected_topics):
        return JSONResponse({
            "message": "Interview finished. Thank you!",
            "end": True
        })

    skill = selected_topics[current_skill_index]

    if current_difficulty_index < len(USER_DIFFICULTY):
        difficulty = USER_DIFFICULTY[current_difficulty_index]
        followup_question = generate_followup(user_input, difficulty=difficulty)

        return JSONResponse({
            "skill": skill,
            "followup": {
                "difficulty": difficulty,
                "question": followup_question
            },
            "next_difficulty_index": current_difficulty_index + 1,
            "next_skill_index": current_skill_index,
            "end": False
        })
    else:
        return JSONResponse({
            "message": f"Completed questions for {skill}.",
            "next_skill_index": current_skill_index + 1,
            "next_difficulty_index": 0,
            "end": False
        })



# --- List Questions API (ChromaDB) ---
@app.get("/api/admin/list_questions")
async def list_questions():
    questions = list_all_questions()
    print(f"Retrieved {len(questions)} questions from ChromaDB")
    if not questions:
        return JSONResponse({"success": False, "error": "No questions found"}, status_code=404)
    return {"questions": questions}


# --- Add Question API (ChromaDB) ---
@app.post("/api/admin/add_question")
async def add_question(request: Request):
    data = await request.json()
    skill = data.get("skill")
    difficulty = data.get("difficulty")
    question = data.get("question")
    category = data.get("category", "")
    if not (skill and difficulty and question):
        return JSONResponse({"success": False, "error": "Missing fields"}, status_code=400)
    add_question_to_chroma(question, skill, category, difficulty)
    return JSONResponse({"success": True, "message": "Question added"})

# --- Remove Question API (ChromaDB) ---
@app.post("/api/admin/remove_question")
async def remove_question(request: Request):
    data = await request.json()
    doc_id = data.get("id")
    if not doc_id:
        return JSONResponse({"success": False, "error": "Missing id"}, status_code=status.HTTP_400_BAD_REQUEST)
    remove_question_by_id(doc_id)
    return JSONResponse({"success": True})

