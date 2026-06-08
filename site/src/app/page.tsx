import Link from "next/link";
import { api, ApiError, engineOfflineHint } from "@/lib/api";
import { apiTypeToSlug, browseHref } from "@/lib/browse-catalog";
import { EntityCard } from "@/components/EntityCard";
import { SearchBox } from "@/components/SearchBox";
import type { EntityOut } from "@/lib/types";

export const revalidate = 300;

export default async function StartPage() {
  let total = 0;
  let featured: EntityOut[] = [];
  let topTypes: { type: string; count: number }[] = [];
  let offline = false;

  try {
    const page = await api.listEntities({ limit: 60 });
    total = page.total;
    featured = page.items.slice(0, 6);
    const counts = new Map<string, number>();
    for (const e of page.items) counts.set(e.type, (counts.get(e.type) ?? 0) + 1);
    topTypes = [...counts.entries()]
      .map(([type, count]) => ({ type, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 6);
  } catch (e) {
    offline = e instanceof ApiError || e instanceof Error;
  }

  return (
    <div className="flex flex-col items-center">
      <section className="flex w-full max-w-2xl flex-col items-center pt-10 text-center sm:pt-20">
        <h1 className="font-display text-4xl font-normal uppercase tracking-tight sm:text-6xl">
          Kosmographica
        </h1>
        <p className="mt-4 text-base leading-relaxed text-muted sm:text-lg">
          A source-grounded graph of human thought — religion, mythology, and the figures,
          concepts, and traditions that connect them. Every claim is cited and trust-rated.
        </p>

        <div className="mt-8 w-full">
          <SearchBox autoFocus />
        </div>

        {!offline && total > 0 && (
          <p className="mt-3 text-xs text-muted">
            Searching{" "}
            <span className="font-medium text-ink tabular-nums">{total.toLocaleString()}</span>{" "}
            cited {total === 1 ? "entity" : "entities"}.
          </p>
        )}

        {topTypes.length > 0 && (
          <div className="mt-6 flex flex-wrap justify-center gap-2">
            {topTypes.map(({ type }) => {
              const slug = apiTypeToSlug(type);
              return (
                <Link
                  key={type}
                  href={slug ? browseHref(slug) : "/browse"}
                  className="rounded-full border border-border px-3 py-1 text-xs text-muted transition-colors hover:border-accent hover:text-ink"
                >
                  {type}
                </Link>
              );
            })}
          </div>
        )}
      </section>

      {offline ? (
        <p className="mt-12 rounded-lg border border-border bg-surface p-4 text-sm text-muted">
          {engineOfflineHint()}
        </p>
      ) : (
        featured.length > 0 && (
          <section className="mt-16 w-full max-w-5xl">
            <div className="mb-3 flex items-baseline justify-between">
              <h2 className="text-lg font-semibold tracking-tight">Explore the graph</h2>
              <Link href="/browse" className="text-sm text-accent-ink underline">
                Browse all
              </Link>
            </div>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {featured.map((e) => (
                <EntityCard key={e.id} entity={e} />
              ))}
            </div>
          </section>
        )
      )}
    </div>
  );
}
