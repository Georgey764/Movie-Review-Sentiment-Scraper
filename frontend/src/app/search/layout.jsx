"use client";

import { useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";

export default function Layout({ children }) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [query, setQuery] = useState(searchParams.get("q"));

  return (
    <div className="h-[100vh]">
      <div className="h-16 p-4 bg-white border-b border-slate-200 flex flex-row align-center gap-10 justify-center">
        <span className="font-extralight text-2xl">Search Movie</span>{" "}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            router.push(`/search?q=${query}`);
          }}
        >
          <input
            value={query || " "}
            onChange={(e) => setQuery(e.target.value)}
            className="border border-slate-400 rounded p-1 w-[300px] pl-2"
            placeholder="Search for movies..."
          />
        </form>
      </div>
      <div className="p-8 bg-white h-[calc(100%-4rem)]">{children}</div>
    </div>
  );
}
