from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import JSON
from sqlalchemy.sql import func
from services.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    resume_path = Column(String, nullable=False)

    jd_path = Column(String, nullable=False)

    resume_text = Column(Text, nullable=False)

    jd_text = Column(Text, nullable=False)

    match_percentage = Column(Integer)

    strengths = Column(Text)

    missing_skills = Column(Text)

    recommendations = Column(Text)

    analysis_json = Column(JSON, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )