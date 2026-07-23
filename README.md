# TV Show Recommender

A personal project that recommends TV shows based on semantic similarity — search by mood, theme, or vibe (not just keyword matching), and get "more like this" recommendations for any show.

## How it works

1. Show metadata (title, genres, overview, keywords, cast) is pulled from [TMDB](https://www.themoviedb.org/)
2. Each show's metadata is combined into a text blob and converted into a vector embedding using `sentence-transformers` (`all-MiniLM-L6-v2`)
3. A FastAPI backend loads all embeddings into memory and uses cosine similarity to find nearest matches — for both text search queries and show-to-show similarity
4. A Next.js + Tailwind frontend provides the search UI and show detail pages

## Stack

- **Data source:** TMDB API
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Backend:** FastAPI + scikit-learn (cosine similarity) + numpy
- **Frontend:** Next.js (App Router) + Tailwind CSS
- **Storage:** JSON file + in memory vectors (no database yet — see Roadmap below)

## Setup

### Prerequisites
- Python 3.11
- Node.js (LTS)
- A free [TMDB API key](https://www.themoviedb.org/settings/api)

### 1. Clone and set up the backend
```bash
git clone <your-repo-url>
cd tv-rec
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add your TMDB API key
Create a `.env` file in the project root:
```
TMDB_API_KEY=your_key_here
```

### 3. Build the show embeddings (one-time step)
```bash
python build_embeddings.py
```
This fetches show data from TMDB, generates embeddings, and saves everything to `shows.json`. Takes a few minutes depending on how many pages you pull.

### 4. Run the backend
```bash
uvicorn api:app --reload
```
API will be running at `http://localhost:8000` — interactive docs at `http://localhost:8000/docs`.

### 5. Run the frontend
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
App will be running at `http://localhost:3000`.

**Both servers need to be running at the same time** for the app to work.

## Roadmap / possible next steps

- [ ] Migrate from JSON + in-memory vectors to PostgreSQL + pgvector
- [ ] User accounts and ratings, for personalized recommendations
- [ ] Genre/year filters alongside semantic search
- [ ] Deploy publicly (backend on Railway/Render, frontend on Vercel)
- [ ] Caching for TMDB API calls

## Notes

Built as a learning project to understand embeddings, semantic search, and full-stack integration end to end.