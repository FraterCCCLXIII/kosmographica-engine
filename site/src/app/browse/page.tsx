import Link from "next/link";
import type { Metadata } from "next";
import { ApiError, engineOfflineHint } from "@/lib/api";
import { browseHref, emptyBrowseCatalog, fetchBrowseCatalog } from "@/lib/browse-catalog";

export const revalidate = 300;

export const metadata: Metadata = {
  title: "Browse",
  description: "Browse every entity in the Kosmographica graph by type.",
};

export default async function BrowsePage() {
  let catalog = emptyBrowseCatalog();
  let offline = false;
  try {
    catalog = await fetchBrowseCatalog();
  } catch (e) {
    offline = e instanceof ApiError || e instanceof Error;
  }

  return (
    <div>
      <header className="mb-8 border-b border-border pb-5">
        <h1 className="font-display text-2xl font-normal uppercase tracking-tight sm:text-3xl">
          Browse the graph
        </h1>
        <p className="mt-2 text-sm text-muted">
          {offline
            ? "Figures, deities, traditions, and concepts — every entry is cited and trust-rated."
            : `${catalog.total.toLocaleString()} cited entries across ${catalog.groups.flatMap((g) => g.types).filter((t) => t.count > 0).length} categories.`}
        </p>
      </header>

      {offline ? (
        <p className="rounded-lg border border-border bg-surface p-4 text-sm text-muted">
          {engineOfflineHint()}
        </p>
      ) : (
        <div className="space-y-10">
          {catalog.groups.map((group) => {
            const types = group.types.filter((t) => t.count > 0);
            if (types.length === 0) return null;
            return (
              <section key={group.id}>
                <h2 className="mb-4 text-xs font-medium uppercase tracking-wide text-muted">
                  {group.label}
                </h2>
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {types.map((t) => (
                    <Link
                      key={t.slug}
                      href={browseHref(t.slug)}
                      className="group block rounded-lg border border-border bg-surface p-4 transition-colors hover:border-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
                    >
                      <div className="flex items-baseline justify-between gap-3">
                        <h3 className="text-base font-semibold tracking-tight group-hover:text-accent-ink">
                          {t.labelPlural}
                        </h3>
                        <span className="shrink-0 text-xs tabular-nums text-muted">
                          {t.count.toLocaleString()}
                        </span>
                      </div>
                      <p className="mt-1.5 text-xs leading-relaxed text-muted">{t.description}</p>
                    </Link>
                  ))}
                </div>
              </section>
            );
          })}
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
