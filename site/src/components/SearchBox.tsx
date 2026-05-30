"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function SearchBox({
  autoFocus = false,
  initialQuery = "",
}: {
  autoFocus?: boolean;
  initialQuery?: string;
}) {
  const router = useRouter();
  const [q, setQ] = useState(initialQuery);

  return (
    <form
      role="search"
      onSubmit={(e) => {
        e.preventDefault();
        const term = q.trim();
        if (term) router.push(`/search?q=${encodeURIComponent(term)}`);
      }}
    >
      <label htmlFor="site-search" className="sr-only">
        Search the encyclopedia
      </label>
      <input
        id="site-search"
        type="search"
        value={q}
        autoFocus={autoFocus}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search deities, figures, concepts…"
        className="w-full rounded-full border border-border bg-surface px-4 py-1.5 text-sm text-ink outline-none placeholder:text-muted focus-visible:ring-2 focus-visible:ring-accent"
      />
    </form>
  );
}
