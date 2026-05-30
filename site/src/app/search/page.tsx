import type { Metadata } from "next";
import { api, ApiError } from "@/lib/api";
import { EntityCard } from "@/components/EntityCard";
import { SearchBox } from "@/components/SearchBox";
import type { SearchHitOut } from "@/lib/types";

export const metadata: Metadata = { title: "Search" };
export const revalidate = 60;

export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const q = (await searchParams).q?.trim() ?? "";
  let hits: SearchHitOut[] = [];
  let error = false;
  if (q) {
    try {
      hits = await api.search(q);
    } catch (e) {
      error = e instanceof ApiError || e instanceof Error;
    }
  }

  return (
    <div>
      <h1 className="mb-4 text-2xl font-semibold tracking-tight">Search</h1>
      <div className="mb-6 max-w-lg">
        <SearchBox autoFocus initialQuery={q} />
      </div>

      {!q && <p className="text-sm text-muted">Type a query to search the graph.</p>}
      {q && error && (
        <p className="text-sm text-muted">The knowledge engine isn’t reachable right now.</p>
      )}
      {q && !error && hits.length === 0 && (
        <p className="text-sm text-muted">
          No matches for <span className="font-medium text-ink">{q}</span>.
        </p>
      )}
      {hits.length > 0 && (
        <>
          <p className="mb-3 text-sm text-muted">
            {hits.length} result{hits.length === 1 ? "" : "s"} for{" "}
            <span className="font-medium text-ink">{q}</span>
          </p>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {hits.map((h) => (
              <EntityCard key={h.entity.id} entity={h.entity} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
