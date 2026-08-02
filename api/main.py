from fastapi import UploadFile, File
from services.pdf_reader import (
    save_uploaded_file,
    extract_text_from_pdf,
    clean_text
)
from agents.planner import run_resume_pipeline

from fastapi import FastAPI

app = FastAPI(
    title="AI Resume Screening Agent API",
    description="AI Resume Screening using LangGraph, Ollama, Groq, ChromaDB and PostgreSQL",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Resume Screening Agent API is Running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):

    resume_path = save_uploaded_file(resume)
    jd_path = save_uploaded_file(jd)

    resume_text = clean_text(
        extract_text_from_pdf(resume_path)
    )

    jd_text = clean_text(
        extract_text_from_pdf(jd_path)
    )

    result = run_resume_pipeline(
        resume_text,
        jd_text
    )

    return result