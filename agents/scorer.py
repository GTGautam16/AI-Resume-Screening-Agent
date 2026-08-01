import json

from services.llm import ask_llm


def score_resume(parsed_resume, jd_text):

    prompt = f"""
        You are an AI Resume Scoring Agent.

        Compare this parsed resume with the Job Description.

        Parsed Resume:
        {parsed_resume}

        Job Description:
        {jd_text}

        Return ONLY valid JSON.

        {
            {
            "match_percentage": 0,
            "strengths": [],
            "missing_skills": [],
            "recommendations": []
            }
        }
        """

    response = ask_llm(prompt)

    return json.loads(response)