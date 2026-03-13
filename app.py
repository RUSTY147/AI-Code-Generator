from fastapi import FastAPI
from repo_loader import load_repo_from_github
from qa_engine import ask_llm
from embedder import create_embeddings
from vector_store import build_index, search

app = FastAPI()

repo_data = []

@app.post("/load_repo")
def load_repo(repo_url: str):

    global repo_data
    repo_data = load_repo_from_github(repo_url)

    # Create embeddings for the loaded repository
    embeddings = create_embeddings([file["content"] for file in repo_data])
    build_index(embeddings, repo_data)

    return {"files_loaded": len(repo_data)}


@app.post("/ask")
def ask(question: str):

    context = ""

    for file in repo_data[:5]:
        context += file["content"][:2000]

    answer = ask_llm(context, question)

    return {"answer": answer}