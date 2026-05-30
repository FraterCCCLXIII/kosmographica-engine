import Link from "next/link";
import { api, ApiError } from "@/lib/api";
import { EntityCard } from "@/components/EntityCard";
import type { EntityOut } from "@/lib/types";

export const revalidate = 300;

function groupByType(items: EntityOut[]): [string, EntityOut[]][] {
  const map = new Map<string, EntityOut[]>();
  for (const e of items) {
    const list = map.get(e.type) ?? [];
    list.push(e);
    map.set(e.type, list);
  }
  return [...map.entries()].sort((a, b) => b[1].length - a[1].length);
}

export default async function HomePage() {
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
      <section className="mb-10 max-w-2xl">
        <h1 className="text-3xl font-semibold leading-tight tracking-tight sm:text-4xl">
          A source-grounded graph of human thought
        </h1>
        <p className="mt-3 text-base leading-relaxed text-muted">
          Religion, mythology, and the figures, concepts, and traditions that connect them —
          federated from multiple sources, with every claim cited and trust-rated.
        </p>
      </section>

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
            Looking for something specific? <Link href="/search" className="text-accent-ink underline">Search the graph</Link>.
          </p>
        </div>
      )}
    </div>
  );
}
