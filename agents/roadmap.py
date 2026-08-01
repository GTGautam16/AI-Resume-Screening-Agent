import streamlit as st

from services.llm import ask_llm


def generate_learning_roadmap(parsed_resume, analysis, jd_text):

    prompt = f"""
        You are an AI Career Coach.

        Parsed Resume:
        {parsed_resume}

        Resume Analysis:
        {analysis}

        Job Description:
        {jd_text}

        Create a personalized roadmap.

        Include:

        1. Skills to learn
        2. Technologies
        3. Certifications
        4. Projects to build
        5. Estimated timeline

        Keep it structured.
    """

    response = ask_llm(prompt)

    if not response:
        st.stop()

    return response