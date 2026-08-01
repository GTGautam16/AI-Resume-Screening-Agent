import chromadb

from services.embeddings import generate_embedding

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(name="resume_embeddings" )

def store_resume_embedding(resume_id,resume_text ):
    embedding = generate_embedding(resume_text)

    collection.add(
        ids=[str(resume_id)],
        embeddings=[embedding],
        documents=[resume_text]
    )

def get_embedding_count():
    return collection.count()

def search_similar_resumes(query_text, n_results=3):

    query_embedding = generate_embedding(query_text)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=[
            "documents",
            "distances",
            "metadatas"
        ]
    )

    return results