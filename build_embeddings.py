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

def fetch_show_details(show_id):
    """Get better data(keywords,genres,and overview)"""
    details = requests.get(
        f"{TMDB_BASE}/tv/{show_id}",
        params={"api_key" : TMDB_API_KEY, "append_to_response": "keywords,credits"},
    ).json()

    return details

def build_text_blob(details):
    """Combine metadata into one text string that captures the show's 'vibe'"""
    title = details.get("name", "")
    overview = details.get("overview", "")
    genres = ", ".join(g["name"] for g in details.get("genres", []))
    keywords = ", ".join(
        k["name"] for k in details.get("keywords", {}).get("results", [])
    )
    top_cast = ", ".join(
        c["name"] for c in details.get("credits", {}).get("cast", [])[:5]
    )
    network = ", ".join(n["name"] for n in details.get("networks", []))
 
    blob = f"""
    Title: {title}
    Genres: {genres}
    Overview: {overview}
    Keywords: {keywords}
    Cast: {top_cast}
    Network: {network}
    """
    return blob.strip()


def build_dataset(pages=50, out_path="shows.json"):
    """Pipeline = fetch -> enrich -> embed -> save"""
    popular = fetch_popular_shows(pages=pages)
    data = []

    for show in popular:
        details = fetch_show_details(show["id"])
        blob = build_text_blob(details)
        embedding = model.encode(blob).tolist() # this converts plain list for JSON

        data.append({"id": show["id"], "title": details.get("name"), "overview": details.get("overview"),
                     "genres": [g["name"] for g in details.get("genres", [])],
                     "poster_path": details.get("poster_path"), "text_blob": blob, "embedding": embedding,})
        time.sleep(.25)
    with open(out_path, "w") as f:
        json.dump(data, f)

    print(f"Saved {len(data)} shows to {out_path}")

if __name__ == "__main__":
    build_dataset(pages=50)
    