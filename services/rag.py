import streamlit as st

from services.vector_store import search_similar_resumes
from services.llm import ask_llm


def answer_with_rag(query):

    results = search_similar_resumes(
        query,
        n_results=3
    )

    context = ""

    if results["documents"]:

        for document in results["documents"][0]:
            context += document
            context += "\n\n"

    prompt = f"""
        You are an experienced Technical Recruiter.

        Use ONLY the resume context below.

        Compare all retrieved candidates.

        Return your answer in this format:

        🏆 Rank 1
        - Candidate ID
        - Why selected
        - Strengths

        🥈 Rank 2
        - Candidate ID
        - Why selected
        - Strengths

        🥉 Rank 3
        - Candidate ID
        - Why selected
        - Strengths

        If only one candidate is retrieved, evaluate that candidate only.

        Resume Context:
        {context}

        Recruiter Question:
        {query}
    """

    answer = ask_llm(prompt)

    if not answer:
        st.stop()

    return answer