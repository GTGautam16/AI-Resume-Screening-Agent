from agents.parser import parse_resume
from agents.scorer import score_resume
from agents.interviewer import generate_interview_questions
from agents.roadmap import generate_learning_roadmap


def run_resume_pipeline(resume_text, jd_text):

    parsed_resume = parse_resume(resume_text)

    analysis = score_resume(
        parsed_resume,
        jd_text
    )

    interview_questions = generate_interview_questions(
        parsed_resume,
        jd_text
    )

    learning_roadmap = generate_learning_roadmap(
    parsed_resume,
    analysis,
    jd_text
)

    return {
        "parsed_resume": parsed_resume,
        "analysis": analysis,
        "interview_questions": interview_questions,
        "learning_roadmap": learning_roadmap
    }