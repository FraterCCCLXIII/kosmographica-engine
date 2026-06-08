import Link from "next/link";
import type { Metadata } from "next";
import { api, ApiError } from "@/lib/api";
import { browseHref } from "@/lib/browse-catalog";
import { buildCosmographTimeline } from "@/lib/cosmograph-timeline";
import { CosmographTimeline } from "@/components/CosmographTimeline";
import { KnightLabTimeline } from "@/components/KnightLabTimeline";
import { TimelineViewToggle, type TimelineView } from "@/components/TimelineViewToggle";
import { cosmographsToTimelineJs } from "@/lib/timeline-js";

export const revalidate = 300;

export const metadata: Metadata = {
  title: "Cosmograph timeline",
  description:
    "A chronological view of humanity's cosmographs — mythic, metaphysical, scientific, and informational maps of reality.",
};

function parseView(raw: string | undefined): TimelineView {
  return raw === "horizontal" ? "horizontal" : "vertical";
}

export default async function CosmographTimelinePage({
  searchParams,
}: {
  searchParams: Promise<{ view?: string }>;
}) {
  const view = parseView((await searchParams).view);
  let groups: ReturnType<typeof buildCosmographTimeline> = [];
  let offline = false;

  try {
    const result = await api.listEntities({ type: "Cosmograph", limit: 200 });
    groups = buildCosmographTimeline(result.items);
  } catch (e) {
    offline = e instanceof ApiError || e instanceof Error;
  }

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
        <Link href={browseHref("cosmograph")} className="hover:text-accent-ink">
          Cosmographs
        </Link>
        <span className="px-1.5">/</span>
        <span>Timeline</span>
      </nav>

      <header className="mb-8 border-b border-border pb-5">
        <h1 className="font-display text-2xl font-normal uppercase tracking-tight sm:text-3xl">
          Cosmograph timeline
        </h1>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted">
          A history of humanity&apos;s attempts to map reality itself — from shamanic three-world
          cosmologies through medieval mappae mundi, scientific universes, developmental psychologies,
          and contemporary knowledge graphs.
        </p>
        <div className="mt-4 flex flex-wrap items-center gap-4">
          <TimelineViewToggle view={view} />
          <p className="text-xs text-muted">
            <Link href={browseHref("cosmograph")} className="text-accent-ink underline">
              Grid view
            </Link>
            {" · "}
            Each entry links to its full record with sources and connections.
          </p>
        </div>
      </header>

      {offline ? (
        <p className="rounded-lg border border-border bg-surface p-4 text-sm text-muted">
          The knowledge engine isn&apos;t reachable right now. Start it on{" "}
          <code>localhost:8088</code> and reload.
        </p>
      ) : groups.length === 0 ? (
        <p className="text-sm text-muted">No cosmograph entries in the catalog yet.</p>
      ) : (
        view === "horizontal" ? (
          <KnightLabTimeline data={cosmographsToTimelineJs(groups)} />
        ) : (
          <CosmographTimeline groups={groups} />
        )
      )}
    </div>
  );
}
