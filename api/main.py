from fastapi import UploadFile, File
from services.pdf_reader import (
    save_uploaded_file,
    extract_text_from_pdf,
    clean_text
)
from services.database import save_resume
from agents.planner import run_resume_pipeline

from pydantic import BaseModel
from services.rag import answer_with_rag

from fastapi import FastAPI

app = FastAPI(
    title="AI Resume Screening Agent API",
    description="AI Resume Screening using LangGraph, Ollama, Groq, ChromaDB and PostgreSQL",
    version="1.0.0"
)

class SearchRequest(BaseModel):
    query: str

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

    analysis = result["analysis"]

    save_resume(
        resume_path=resume_path,
        jd_path=jd_path,
        resume_text=resume_text,
        jd_text=jd_text,
        match_percentage=analysis["match_percentage"],
        strengths="\n".join(analysis["strengths"]),
        missing_skills="\n".join(analysis["missing_skills"]),
        recommendations="\n".join(analysis["recommendations"]),
        analysis_json=analysis
    )

    return {
        "analysis": result.get("analysis"),
        "interview_questions": result.get("interview_questions"),
        "learning_roadmap": result.get("learning_roadmap")
    }

@app.post("/search")
async def search_resume(request: SearchRequest):

    answer = answer_with_rag(request.query)

    return {
        "query": request.query,
        "answer": answer
    }