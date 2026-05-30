import Link from "next/link";
import { api } from "@/lib/api";
import type { SearchHitOut } from "@/lib/types";
import { Card, EmptyState, PageHeader } from "@/components/Card";
import { TierBadge } from "@/components/Badges";

export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q } = await searchParams;
  const hits: SearchHitOut[] = q ? await api.search(q, "machine_unverified") : [];

  return (
    <div className="max-w-3xl">
      <PageHeader title="Browse entities" subtitle="Full-text search across the corpus." />

      <form className="mb-6 flex gap-2">
        <input
          name="q"
          defaultValue={q}
          autoFocus
          placeholder="Search entities…"
          className="flex-1 rounded-lg border border-border bg-surface px-3 py-2 text-sm outline-none focus:border-accent"
        />
        <button className="rounded-lg bg-accent px-4 py-2 text-sm font-medium text-white">
          Search
        </button>
      </form>

      {!q ? (
        <EmptyState>Enter a query to search the corpus.</EmptyState>
      ) : hits.length === 0 ? (
        <EmptyState>No matches for “{q}”.</EmptyState>
      ) : (
        <div className="space-y-2">
          {hits.map(({ entity }) => (
            <Card key={entity.id} className="transition-colors hover:border-accent/50">
              <div className="flex items-center justify-between gap-4">
                <Link href={`/entities/${entity.id}`} className="font-medium hover:text-accent">
                  {entity.label}
                </Link>
                <TierBadge tier={entity.tier} />
              </div>
              <div className="mt-1 text-xs text-muted">
                {entity.type}
                {entity.subtype ? ` · ${entity.subtype}` : ""}
                {typeof entity.data.tradition === "string" ? ` · ${entity.data.tradition}` : ""}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
