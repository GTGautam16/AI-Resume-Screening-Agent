import streamlit as st

from services.llm import ask_llm


def generate_interview_questions(parsed_resume, jd_text):

    prompt = f"""
        You are an AI Technical Interviewer.

        Based on this parsed resume and job description, generate:

        - 5 Technical Questions
        - 3 HR Questions
        - 2 Project-based Questions

        Parsed Resume:
        {parsed_resume}

        Job Description:
        {jd_text}
    """

    response = ask_llm(prompt)

    if not response:
        st.stop()

    return response