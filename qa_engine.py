from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import os

# --- Set up embedding model ---
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --- Create or load ChromaDB ---
def get_chroma_collection(persist_directory="chroma_store"):
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)
    return db

# --- Add a question to ChromaDB ---
def add_question_to_chroma(question, skill, category=None, difficulty=None, persist_directory="chroma_store"):
    db = get_chroma_collection(persist_directory)
    meta = {"skill": skill}
    if difficulty:
        meta["difficulty"] = difficulty
    doc = Document(page_content=question, metadata=meta)
    result = db.add_documents([doc])
    # Optionally, check result for errors or log
    return result

# --- Retrieve top-k relevant questions ---
def get_questions_for_skill(skill, k=3):
    db = get_chroma_collection()
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    results = retriever.invoke(f"Interview questions about {skill}")
    # Filter by metadata skill field (case-insensitive)
    filtered = [doc.page_content for doc in results if hasattr(doc, 'metadata') and doc.metadata.get('skill', '').lower() == skill.lower()]
    if filtered:
        return filtered
    else:
        return [f"Can you discuss your experience with {skill}?"]

# --- List all questions ---
def list_all_questions(persist_directory="chroma_store"):
    db = get_chroma_collection(persist_directory)
    result = db.get()
    docs = result['documents']
    metas = result['metadatas']
    ids = result['ids']
    return [
        {
            "id": id_,
            "question": doc,
            "skill": meta.get("skill", ""),
            "difficulty": meta.get("difficulty", "")
        }
        for doc, meta, id_ in zip(docs, metas, ids)
    ]

# --- Remove a question by id ---
def remove_question_by_id(doc_id, persist_directory="chroma_store"):
    db = get_chroma_collection(persist_directory)
    db.delete([doc_id])


