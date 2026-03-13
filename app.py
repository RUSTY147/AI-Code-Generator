from fastapi import FastAPI
from repo_loader import load_repo_from_github
from qa_engine import ask_llm
from embedder import create_embeddings
from vector_store import build_index, search
from chunker import chunk_code

app = FastAPI()

repo_data = []

@app.post("/load_repo")
def load_repo(repo_url: str):

    global repo_data

    raw_files = load_repo_from_github(repo_url)

    repo_data = []

    for file in raw_files:
        chunks = chunk_code(file["file"], file["content"])
        repo_data.extend(chunks)

    texts = [chunk["content"] for chunk in repo_data]

    embeddings = create_embeddings(texts)

    build_index(embeddings, repo_data)

    return {
        "files_loaded": len(raw_files),
        "chunks_created": len(repo_data)
    }


@app.post("/ask")
def ask(question: str):

    context = ""

    for file in repo_data[:5]:
        context += file["content"][:2000]

    answer = ask_llm(context, question)

    return {"answer": answer}