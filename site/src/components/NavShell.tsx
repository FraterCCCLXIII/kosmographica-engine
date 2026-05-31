"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useCallback, useEffect, useSyncExternalStore, type ReactNode } from "react";
import { SearchBox } from "@/components/SearchBox";
import { NavBrowseTree } from "@/components/NavBrowseTree";
import type { BrowseCatalog } from "@/lib/browse-catalog";

const STORAGE_KEY = "kg-nav-open";
const NAV_EVENT = "kg-nav-open-change";

// Persisted, SSR-safe open state (defaults open; survives reloads and syncs tabs).
function readOpen(): boolean {
  return window.localStorage.getItem(STORAGE_KEY) !== "false";
}
function writeOpen(value: boolean): void {
  window.localStorage.setItem(STORAGE_KEY, String(value));
  window.dispatchEvent(new Event(NAV_EVENT));
}
function subscribeOpen(callback: () => void): () => void {
  window.addEventListener(NAV_EVENT, callback);
  window.addEventListener("storage", callback);
  return () => {
    window.removeEventListener(NAV_EVENT, callback);
    window.removeEventListener("storage", callback);
  };
}

type NavLink = { href: string; label: string; hint?: string };

const SECONDARY: NavLink[] = [
  { href: "/about", label: "How this works", hint: "Publish-then-verify" },
];

export function NavShell({
  children,
  browseCatalog,
}: {
  children: ReactNode;
  browseCatalog: BrowseCatalog;
}) {
  const pathname = usePathname();
  // Docked-open by default on desktop (Sacred-Lineage behaviour); persisted.
  const open = useSyncExternalStore(subscribeOpen, readOpen, () => true);

  const toggle = useCallback(() => writeOpen(!open), [open]);
  const close = useCallback(() => writeOpen(false), []);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") writeOpen(false);
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open]);

  const isStart = pathname === "/";

  return (
    <div className="relative flex h-svh min-h-0 w-full flex-col overflow-hidden">
      {/* Start page: hamburger only, no bar/border. Other pages: full chrome header. */}
      <header
        className={
          isStart
            ? "absolute left-0 top-0 z-30 flex h-[var(--site-header-height)] items-center p-2"
            : "relative z-30 flex h-[var(--site-header-height)] shrink-0 items-center border-b border-border bg-canvas/85 py-2.5 pl-2 pr-3 backdrop-blur sm:pr-4"
        }
      >
        <div className="flex min-w-0 items-center gap-1.5">
          <button
            type="button"
            aria-label={open ? "Close navigation" : "Open navigation"}
            aria-expanded={open}
            aria-controls="site-nav"
            onClick={toggle}
            className="inline-flex h-9 w-9 items-center justify-center rounded-md text-ink transition-colors hover:bg-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
          >
            <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden fill="none">
              <path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
            </svg>
          </button>

          {!isStart && (
            <Link
              href="/"
              className="truncate font-display text-lg font-normal uppercase tracking-tight sm:text-xl"
            >
              Kosmographica
            </Link>
          )}
        </div>

        {!isStart && (
          <>
            <div className="pointer-events-none absolute left-1/2 top-1/2 hidden w-[min(28rem,50vw)] -translate-x-1/2 -translate-y-1/2 sm:block">
              <div className="pointer-events-auto">
                <SearchBox />
              </div>
            </div>

            <div className="ml-auto" aria-hidden />
          </>
        )}
      </header>

      {/* Body — docked sidebar (desktop) pushes the scrollable main column. */}
      <div className="flex min-h-0 flex-1 overflow-hidden">
        <aside
          id="site-nav"
          aria-hidden={!open}
          className={`hidden h-full min-h-0 shrink-0 overflow-hidden border-border bg-surface/40 transition-[width,border-width] duration-300 ease-in-out md:block ${
            open ? "w-72 border-r" : "w-0 border-r-0"
          }`}
        >
          <div
            className={`site-nav-scroll flex h-full w-72 min-h-0 flex-col overflow-y-auto ${
              isStart ? "pt-[var(--site-header-height)]" : ""
            }`}
          >
            <NavPanel pathname={pathname} browseCatalog={browseCatalog} />
          </div>
        </aside>

        <div className="min-h-0 min-w-0 flex-1 overflow-y-auto">
          <main className="mx-auto max-w-6xl px-4 py-8 sm:px-5">{children}</main>
          <footer className="mx-auto max-w-6xl px-4 pb-10 text-xs leading-relaxed text-muted sm:px-5">
            Every claim shown is grounded in a cited source and carries a trust rating. Authored by
            AI under publish-then-verify; reviewed over time.
          </footer>
        </div>
      </div>

      {/* Mobile — full-viewport-height overlay drawer (same toggle state). */}
      <div className="md:hidden">
        <div
          aria-hidden
          onClick={close}
          className={`fixed inset-0 z-40 bg-ink/30 backdrop-blur-sm transition-opacity duration-200 ${
            open ? "opacity-100" : "pointer-events-none opacity-0"
          }`}
        />
        <aside
          role="dialog"
          aria-modal="true"
          aria-label="Site navigation"
          className={`fixed inset-y-0 left-0 z-50 flex w-72 max-w-[80vw] flex-col border-r border-border bg-canvas transition-transform duration-200 ease-out ${
            open ? "translate-x-0" : "-translate-x-full"
          }`}
        >
          <div className="flex items-center justify-between border-b border-border px-5 py-3.5">
            <span className="font-display text-lg font-normal uppercase tracking-tight">Kosmographica</span>
            <button
              type="button"
              aria-label="Close navigation"
              onClick={close}
              className="inline-flex h-8 w-8 items-center justify-center rounded-md text-muted transition-colors hover:bg-surface hover:text-ink focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
            >
              <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden fill="none">
                <path d="M4 4l10 10M14 4L4 14" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
              </svg>
            </button>
          </div>
          <div className="site-nav-scroll flex-1 overflow-y-auto">
            <NavPanel pathname={pathname} browseCatalog={browseCatalog} onNavigate={close} />
          </div>
        </aside>
      </div>
    </div>
  );
}

function NavPanel({
  pathname,
  browseCatalog,
  onNavigate,
}: {
  pathname: string;
  browseCatalog: BrowseCatalog;
  onNavigate?: () => void;
}) {
  return (
    <nav className="px-3 py-4">
      <p className="mb-2 px-2.5 text-xs font-medium uppercase tracking-wide text-muted">Browse</p>
      <NavBrowseTree catalog={browseCatalog} onNavigate={onNavigate} />
      <div className="my-4 border-t border-border" />
      <NavSection links={SECONDARY} pathname={pathname} onNavigate={onNavigate} />
    </nav>
  );
}

function NavSection({
  links,
  pathname,
  onNavigate,
}: {
  links: NavLink[];
  pathname: string;
  onNavigate?: () => void;
}) {
  return (
    <ul className="space-y-0.5">
      {links.map((l) => {
        const active = l.href === "/" ? pathname === "/" : pathname.startsWith(l.href);
        return (
          <li key={l.href}>
            <Link
              href={l.href}
              onClick={onNavigate}
              aria-current={active ? "page" : undefined}
              className={`block rounded-md px-2.5 py-2 transition-colors hover:bg-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent ${
                active ? "bg-surface" : ""
              }`}
            >
              <span className="block text-sm font-medium text-ink">{l.label}</span>
              {l.hint && <span className="block text-xs text-muted">{l.hint}</span>}
            </Link>
          </li>
        );
      })}
    </ul>
  );
}
