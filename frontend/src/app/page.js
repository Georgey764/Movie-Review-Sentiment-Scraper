"use client";

import Image from "next/image";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const [query, setQuery] = useState("");
  const router = useRouter();

  return (
    <main className="flex min-h-screen flex-col items-center justify-between">
      <div className="flex flex-col align-center justify-center h-[100vh] mt-[-3rem]">
        <h1 className="font-bold text-3xl mb-4">Search movie to analyze</h1>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            router.push(`/search?q=${query}`);
          }}
          className="text-center"
        >
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="h-8 p-2 rounded w-[22rem]"
            placeholder="Search for movies..."
          />
        </form>
      </div>
    </main>
  );
}
