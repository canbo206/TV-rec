"use client";

import { useState } from "react";
import Link from "next/link";

const API_BASE= "https://localhost:8000";

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
}