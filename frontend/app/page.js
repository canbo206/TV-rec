"use client";

import { useState } from "react";
import Link from "next/link";

const API_BASE= "http://127.0.0.1:8000";

export default function Home() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([])
    const [loading, setLoading] = useState(false);

    async function handleSearch(e) {
        e.preventDefault();
        if(!query.trim()) return;
        setLoading(true);
        try{
            const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
            const data = await res.json();
            setResults(data.results || []);
        } catch (err) {
            console.error("Search failed:", err);
        } finally {
            setLoading(false);
        }
    }

    return(
        <main className="max-w-5x1 mx-auto p-6">
            <h1 className="text-3x1 font-bold mb-6">TV Show Recommender</h1>

            <form onSubmit={handleSearch} className="flex gap-2 mb-8">
                <input value={query} onChange={(e) => setQuery(e.target.value)}
                       placeholder="e.g. time travel comedy"
                       className="flex-1 rounded-lg bg-gray-800 px-4 py-2 outline-none focus-ring-2 focus:ring-indigo-500"/>
                <button type="submit" className="rounded-lg bg-indigo-600 px-5 py-2 font-medium hover:bg-indigo-500">
                    Search
                </button>
            </form>

            {loading && <p className="text-gray-400">Searching...</p>}

            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                {results.map((show) => (
                    <Link key={show.id} href={`/show/${show.id}`} className="group
                     rounded-lg overflow-hidden bg-gray-900 hover:ring-2 hover:ring-indigo-500 transition">
                    {show.poster_path &&(
                        <img
                            src={`https://image.tmdb.org/t/p/w342${show.poster_path}`}
                            alt={show.title}
                            className="w-full aspect-[2/3] object-cover" 
                        />
                    )}
                    <div className="p-2">
                        <p className="text-sm font-medium truncate">{show.title}</p>
                        <p className="text-xs text-gray-400">
                            match{(show.score * 100).toFixed(0)}%
                        </p>
                    </div>
                    </Link>
                ))}
            </div>
        </main>
    );
}