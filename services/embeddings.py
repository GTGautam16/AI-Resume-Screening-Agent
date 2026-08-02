from ollama import Client

client = Client(host="http://127.0.0.1:11434")

def generate_embedding(text):
    response = client.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]