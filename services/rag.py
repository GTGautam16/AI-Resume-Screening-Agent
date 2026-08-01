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
You are an expert AI Resume Assistant.

Use ONLY the following resume context to answer.

Resume Context:

{context}

Question:

{query}

Answer clearly and professionally.
"""

    return ask_llm(prompt)