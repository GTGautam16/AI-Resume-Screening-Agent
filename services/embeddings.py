from ollama import Client

client = Client(host="http://host.docker.internal:11434")

def generate_embedding(text):
    response = client.embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    return response["embedding"]