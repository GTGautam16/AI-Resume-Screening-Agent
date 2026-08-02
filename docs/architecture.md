```mermaid
flowchart TD

A[Resume PDF] --> B[PDF Reader]
C[Job Description PDF] --> B

B --> D[LangGraph Workflow]

D --> E[Resume Parser]
D --> F[Resume Scorer]
D --> G[Interview Generator]
D --> H[Learning Roadmap]

E --> I[Groq LLM]
F --> I
G --> I
H --> I

I --> J[PostgreSQL]
I --> K[ChromaDB]

K --> L[RAG Search]

M[Streamlit UI] --> D
N[FastAPI API] --> D

L --> N
```