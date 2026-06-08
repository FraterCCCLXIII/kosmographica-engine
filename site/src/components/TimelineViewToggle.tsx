import Link from "next/link";

export type TimelineView = "vertical" | "horizontal";

export function TimelineViewToggle({ view }: { view: TimelineView }) {
  return (
    <div
      className="inline-flex rounded-lg border border-border bg-surface p-0.5 text-xs"
      role="tablist"
      aria-label="Timeline layout"
    >
      <ViewTab href="/cosmographs/timeline" active={view === "vertical"} label="Vertical" />
      <ViewTab
        href="/cosmographs/timeline?view=horizontal"
        active={view === "horizontal"}
        label="Interactive"
      />
    </div>
  );
}

function ViewTab({
  href,
  active,
  label,
}: {
  href: string;
  active: boolean;
  label: string;
}) {
  return (
    <Link
      href={href}
      role="tab"
      aria-selected={active}
      className={`rounded-md px-3 py-1.5 font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent ${
        active ? "bg-ink text-canvas" : "text-muted hover:text-ink"
      }`}
    >
      {label}
    </Link>
  );
}
