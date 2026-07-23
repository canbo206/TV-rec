"""
FastAPI backend serving two endpoints:
  - /search?q=...          -> semantic search from a text query
  - /shows/{id}/similar    -> shows similar to a given show
we load everything into memory and use numpy/sklearn for nearest neighbor search.
No need for a real vector DB yet.
"""

import json
import numpy as np
from fastapi import FastAPI, HTTPException
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware
 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
model = SentenceTransformer("all-MiniLM-L6-v2")
 
# --- Load data once at startup ---
with open("shows.json") as f:
    SHOWS = json.load(f)
 
EMBEDDINGS = np.array([s["embedding"] for s in SHOWS])
ID_TO_INDEX = {s["id"]: i for i, s in enumerate(SHOWS)}
 
 
def top_matches(query_vector, exclude_index=None, k=16):
    sims = cosine_similarity([query_vector], EMBEDDINGS)[0]
    if exclude_index is not None:
        sims[exclude_index] = -1  # don't recommend the show itself
    top_idx = np.argsort(sims)[::-1][:k]
    return [
        {**SHOWS[i], "embedding": None, "score": float(sims[i])}  # strip embedding from response
        for i in top_idx
    ]
 
 
@app.get("/search")
def search(q: str, k: int = 16):
    query_vector = model.encode(q)
    results = top_matches(query_vector, k=k)
    return {"query": q, "results": results}
 
 
@app.get("/shows/{show_id}/similar")
def similar(show_id: int, k: int = 16):
    if show_id not in ID_TO_INDEX:
        raise HTTPException(status_code=404, detail="Show not found")
    idx = ID_TO_INDEX[show_id]
    query_vector = EMBEDDINGS[idx]
    results = top_matches(query_vector, exclude_index=idx, k=k)
    return {"show_id": show_id, "results": results}
 
 
@app.get("/shows/{show_id}")
def get_show(show_id: int):
    if show_id not in ID_TO_INDEX:
        raise HTTPException(status_code=404, detail="Show not found")
    show = SHOWS[ID_TO_INDEX[show_id]].copy()
    show["embedding"] = None
    return show


"""run uvicorn api:app --reload to test"""