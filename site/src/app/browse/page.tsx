import Link from "next/link";
import type { Metadata } from "next";
import { api, ApiError } from "@/lib/api";
import { EntityCard } from "@/components/EntityCard";
import type { EntityOut } from "@/lib/types";

export const revalidate = 300;

export const metadata: Metadata = {
  title: "Browse",
  description: "Browse every entity in the Kosmographica graph, grouped by type.",
};

function groupByType(items: EntityOut[]): [string, EntityOut[]][] {
  const map = new Map<string, EntityOut[]>();
  for (const e of items) {
    const list = map.get(e.type) ?? [];
    list.push(e);
    map.set(e.type, list);
  }
  return [...map.entries()].sort((a, b) => b[1].length - a[1].length);
}

export default async function BrowsePage() {
  let items: EntityOut[] = [];
  let offline = false;
  try {
    const page = await api.listEntities({ limit: 60 });
    items = page.items;
  } catch (e) {
    offline = e instanceof ApiError || e instanceof Error;
  }

  return (
    <div>
      <header className="mb-8 border-b border-border pb-5">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Browse the graph</h1>
        <p className="mt-2 text-sm text-muted">
          Figures, concepts, and traditions, grouped by type. Every entry is cited and trust-rated.
        </p>
      </header>

      {offline ? (
        <p className="rounded-lg border border-border bg-surface p-4 text-sm text-muted">
          The knowledge engine isn’t reachable right now. Start it on{" "}
          <code>localhost:8088</code> and reload.
        </p>
      ) : (
        <div className="space-y-8">
          {groupByType(items).map(([type, group]) => (
            <section key={type}>
              <h2 className="mb-3 text-lg font-semibold tracking-tight">{type}</h2>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {group.slice(0, 9).map((e) => (
                  <EntityCard key={e.id} entity={e} />
                ))}
              </div>
            </section>
          ))}
          <p className="text-sm text-muted">
            Looking for something specific?{" "}
            <Link href="/search" className="text-accent-ink underline">
              Search the graph
            </Link>
            .
          </p>
        </div>
      )}
    </div>
  );
}
