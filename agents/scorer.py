import json
import streamlit as st

from services.llm import ask_llm


def score_resume(parsed_resume, jd_text):

    prompt = f"""
    You are an AI Resume Scoring Agent.

    Compare the parsed resume with the Job Description.

    Return ONLY a valid JSON object.

    Do NOT explain anything.
    Do NOT write markdown.
    Do NOT add notes before or after the JSON.

    Parsed Resume:
    {parsed_resume}

    Job Description:
    {jd_text}

    JSON format:

    {{
        "match_percentage": 0,
        "strengths": [],
        "missing_skills": [],
        "recommendations": []
    }}
    """

    response = ask_llm(prompt)

    # Remove markdown if present
    response = (
        response.replace("```json", "")
        .replace("```", "")
        .strip()
    )

    # Extract only the JSON object
    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:
        st.error("❌ AI did not return a valid JSON response.")
        st.stop()

    response = response[start:end + 1]

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        st.error("❌ AI returned an invalid JSON response. Please try again.")
        st.stop()