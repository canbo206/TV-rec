import requests
import numpy as np
import json
import time
from sentence_transformers import SentenceTransformer 

TMDB_API_KEY = "2d30a5a140f3dea967a59650d571b262"
TMDB_BASE = "https://api.themoviedb.org/3"

model = SentenceTransformer("all-MiniLM-L6-v2")

def fetch_popular_shows(pages=50):
    """Will pull the most popular shows across multiple pages"""
    shows = []
    for page in range(1, pages + 1):
        response = requests.get(f"{TMDB_BASE}/tv/popular", params={"api_key" : TMDB_API_KEY, "page" : page},).json()
        shows.extend(response.get("results", []))
        time.sleep(.25)
    return shows  
