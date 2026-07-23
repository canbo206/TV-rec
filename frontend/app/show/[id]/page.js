"use client";
 
import { useEffect, useState } from "react";
import Link from "next/link";
 
const API_BASE = "http://127.0.0.1:8000";
 
export default function ShowDetail({ params }) {
  const { id } = params;
  const [show, setShow] = useState(null);
  const [similar, setSimilar] = useState([]);
 
  useEffect(() => {
    async function load() {
      const [showRes, similarRes] = await Promise.all([
        fetch(`${API_BASE}/shows/${id}`),
        fetch(`${API_BASE}/shows/${id}/similar`),
      ]);
      setShow(await showRes.json());
      const similarData = await similarRes.json();
      setSimilar(similarData.results || []);
    }
    load();
  }, [id]);
 
  if (!show) return <main className="p-6">Loading...</main>;
 
  return (
    <main className="max-w-5xl mx-auto p-6">
      <Link href="/" className="text-indigo-400 hover:underline">
        &larr; Back to search
      </Link>
 
      <div className="flex gap-6 mt-4">
        {show.poster_path && (
          <img
            src={`https://image.tmdb.org/t/p/w342${show.poster_path}`}
            alt={show.title}
            className="w-48 rounded-lg"
          />
        )}
        <div>
          <h1 className="text-2xl font-bold mb-2">{show.title}</h1>
          <p className="text-gray-300 mb-2">{show.overview}</p>
          <p className="text-sm text-gray-500">{(show.genres || []).join(", ")}</p>
        </div>
      </div>
 
      <h2 className="text-xl font-semibold mt-10 mb-4">More like this</h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {similar.map((s) => (
          <Link
            key={s.id}
            href={`/show/${s.id}`}
            className="rounded-lg overflow-hidden bg-gray-900 hover:ring-2 hover:ring-indigo-500 transition"
          >
            {s.poster_path && (
              <img
                src={`https://image.tmdb.org/t/p/w342${s.poster_path}`}
                alt={s.title}
                className="w-full aspect-[2/3] object-cover"
              />
            )}
            <p className="text-sm p-2 truncate">{s.title}</p>
          </Link>
        ))}
      </div>
    </main>
  );
}
 