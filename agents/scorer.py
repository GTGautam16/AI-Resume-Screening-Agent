import json
import streamlit as st

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

        {{
            "match_percentage": 0,
            "strengths": [],
            "missing_skills": [],
            "recommendations": []
        }}
    """

    response = ask_llm(prompt)

    if not response:
        st.stop()

    st.write(response)

    response = response.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        st.error("❌ AI returned an invalid JSON response. Please try again.")
        st.stop()