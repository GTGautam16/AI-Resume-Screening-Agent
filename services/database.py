import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def save_resume(
    resume_path,
    jd_path,
    resume_text,
    jd_text,
    match_percentage,
    strengths,
    missing_skills,
    recommendations
):
    from models.schemas import Resume

    session = SessionLocal()

    try:
        resume = Resume(
            resume_path=str(resume_path),
            jd_path=str(jd_path),
            resume_text=resume_text,
            jd_text=jd_text,
            match_percentage=match_percentage,
            strengths=strengths,
            missing_skills=missing_skills,
            recommendations=recommendations
        )

        session.add(resume)
        session.commit()

        session.refresh(resume)

        return resume

    finally:
        session.close()

def get_all_resumes():
    from models.schemas import Resume

    session = SessionLocal()

    try:
        resumes = session.query(Resume).all()
        return resumes

    finally:
        session.close()
