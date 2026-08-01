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

        Use ONLY the resume information provided below.

        If the answer is not present in the resumes, reply:
        "I could not find that information in the stored resumes."

        Resume Context:
        {context}

        Recruiter Question:
        {query}

        Answer professionally using bullet points whenever appropriate.
        """
    
    return ask_llm(prompt)