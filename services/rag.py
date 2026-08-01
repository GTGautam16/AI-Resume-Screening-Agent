from services.vector_store import search_similar_resumes


def retrieve_context(query, top_k=3):

    results = search_similar_resumes(
        query,
        n_results=top_k
    )

    context = ""

    if results["documents"]:
        for document in results["documents"][0]:

            context += document
            context += "\n\n"

    return context