import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { api, ApiError } from "@/lib/api";
import {
  BROWSE_GROUPS,
  BROWSE_PAGE_SIZE,
  browseHref,
  getBrowseType,
  loadBrowseCatalog,
} from "@/lib/browse-catalog";
import { BrowsePagination } from "@/components/BrowsePagination";
import { EntityCard } from "@/components/EntityCard";

export const revalidate = 300;

type Params = { type: string };

export async function generateStaticParams() {
  return BROWSE_GROUPS.flatMap((g) => g.types.map((t) => ({ type: t.slug })));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const def = getBrowseType((await params).type);
  if (!def) return { title: "Not found" };
  return {
    title: def.labelPlural,
    description: def.description,
  };
}

export default async function BrowseTypePage({
  params,
  searchParams,
}: {
  params: Promise<Params>;
  searchParams: Promise<{ page?: string }>;
}) {
  const slug = (await params).type;
  const def = getBrowseType(slug);
  if (!def) notFound();

  const pageRaw = Number((await searchParams).page ?? "1");
  const page = Number.isFinite(pageRaw) && pageRaw >= 1 ? Math.floor(pageRaw) : 1;
  const offset = (page - 1) * BROWSE_PAGE_SIZE;

  let items: Awaited<ReturnType<typeof api.listEntities>>["items"] = [];
  let total = 0;
  let offline = false;

  try {
    const result = await api.listEntities({
      type: def.apiType,
      limit: BROWSE_PAGE_SIZE,
      offset,
    });
    items = result.items;
    total = result.total;
  } catch (e) {
    offline = e instanceof ApiError || e instanceof Error;
  }

  const pageCount = Math.max(1, Math.ceil(total / BROWSE_PAGE_SIZE));
  if (!offline && total > 0 && page > pageCount) notFound();

  const catalog = await loadBrowseCatalog();

  return (
    <div>
      <nav className="mb-4 text-xs text-muted">
        <Link href="/" className="hover:text-accent-ink">
          Home
        </Link>
        <span className="px-1.5">/</span>
        <Link href="/browse" className="hover:text-accent-ink">
          Browse
        </Link>
        <span className="px-1.5">/</span>
        <span>{def.labelPlural}</span>
      </nav>

      <header className="mb-8 border-b border-border pb-5">
        <h1 className="font-display text-2xl font-normal uppercase tracking-tight sm:text-3xl">
          {def.labelPlural}
        </h1>
        <p className="mt-2 text-sm text-muted">{def.description}</p>
        {!offline && (
          <p className="mt-2 text-xs text-muted tabular-nums">
            {total.toLocaleString()} {total === 1 ? "entry" : "entries"}
            {slug === "cosmograph" && total > 0 && (
              <>
                {" · "}
                <Link href="/cosmographs/timeline" className="text-accent-ink underline">
                  Timeline view
                </Link>
              </>
            )}
          </p>
        )}
      </header>

      {offline ? (
        <p className="rounded-lg border border-border bg-surface p-4 text-sm text-muted">
          The knowledge engine isn’t reachable right now. Start it on{" "}
          <code>localhost:8088</code> and reload.
        </p>
      ) : items.length === 0 ? (
        <p className="text-sm text-muted">No public entries in this category yet.</p>
      ) : (
        <>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {items.map((e) => (
              <EntityCard key={e.id} entity={e} />
            ))}
          </div>
          <BrowsePagination slug={slug} page={page} total={total} pageSize={BROWSE_PAGE_SIZE} />
        </>
      )}

      <aside className="mt-10 border-t border-border pt-6">
        <h2 className="mb-3 text-sm font-medium text-muted">Other categories</h2>
        <ul className="flex flex-wrap gap-2">
          {catalog.groups.flatMap((g) =>
            g.types
              .filter((t) => t.slug !== slug && t.count > 0)
              .map((t) => (
                <li key={t.slug}>
                  <Link
                    href={browseHref(t.slug)}
                    className="rounded-full border border-border px-3 py-1 text-xs text-muted transition-colors hover:border-accent hover:text-ink"
                  >
                    {t.labelPlural}
                  </Link>
                </li>
              )),
          )}
        </ul>
      </aside>
    </div>
  );
}
