"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { BrowseCatalog } from "@/lib/browse-catalog";
import { browseHref } from "@/lib/browse-catalog";

export function NavBrowseTree({
  catalog,
  onNavigate,
}: {
  catalog: BrowseCatalog;
  onNavigate?: () => void;
}) {
  const pathname = usePathname();
  const onBrowse = pathname === "/browse" || pathname.startsWith("/browse/");

  return (
    <div className="mt-1">
      <Link
        href="/browse"
        onClick={onNavigate}
        aria-current={pathname === "/browse" ? "page" : undefined}
        className={`block rounded-md px-2.5 py-2 text-sm font-medium transition-colors hover:bg-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent ${
          pathname === "/browse" ? "bg-surface text-ink" : "text-ink"
        }`}
      >
        All entries
        <span className="mt-0.5 block text-xs font-normal text-muted tabular-nums">
          {catalog.total.toLocaleString()} total
        </span>
      </Link>

      <div className="mt-2 space-y-3">
        {catalog.groups.map((group) => (
          <details key={group.id} open={onBrowse} className="group/details">
            <summary className="cursor-pointer list-none rounded-md px-2.5 py-1.5 text-xs font-medium uppercase tracking-wide text-muted hover:bg-surface [&::-webkit-details-marker]:hidden">
              {group.label}
            </summary>
            <ul className="mt-0.5 space-y-0.5 pl-1">
              {group.types.map((t) => {
                const href = browseHref(t.slug);
                const active = pathname === `/browse/${t.slug}`;
                if (t.count === 0) return null;
                return (
                  <li key={t.slug}>
                    <Link
                      href={href}
                      onClick={onNavigate}
                      aria-current={active ? "page" : undefined}
                      className={`flex items-baseline justify-between gap-2 rounded-md px-2.5 py-1.5 text-sm transition-colors hover:bg-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent ${
                        active ? "bg-surface font-medium text-ink" : "text-ink"
                      }`}
                    >
                      <span>{t.labelPlural}</span>
                      <span className="shrink-0 text-xs tabular-nums text-muted">
                        {t.count.toLocaleString()}
                      </span>
                    </Link>
                    {t.slug === "cosmograph" && (
                      <Link
                        href="/cosmographs/timeline"
                        onClick={onNavigate}
                        aria-current={pathname === "/cosmographs/timeline" ? "page" : undefined}
                        className={`ml-3 flex rounded-md px-2.5 py-1.5 text-sm transition-colors hover:bg-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent ${
                          pathname === "/cosmographs/timeline"
                            ? "bg-surface font-medium text-ink"
                            : "text-muted"
                        }`}
                      >
                        Timeline
                      </Link>
                    )}
                  </li>
                );
              })}
            </ul>
          </details>
        ))}
      </div>
    </div>
  );
}
