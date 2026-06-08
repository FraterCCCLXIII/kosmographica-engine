import Link from "next/link";
import type { TimelineEraGroup } from "@/lib/cosmograph-timeline";
import { cosmographFacet } from "@/lib/cosmograph-timeline";
import { entityHref } from "@/lib/types";

export function CosmographTimeline({ groups }: { groups: TimelineEraGroup[] }) {
  const total = groups.reduce((sum, g) => sum + g.entries.length, 0);

  return (
    <div className="relative">
      <p className="mb-6 text-sm text-muted">
        {total.toLocaleString()} cosmographs arranged chronologically by earliest attestation.
      </p>

      <div className="space-y-10">
        {groups.map((group) => (
          <section key={group.era.id} aria-labelledby={`era-${group.era.id}`}>
            <div className="mb-4 flex items-baseline gap-3">
              <h2
                id={`era-${group.era.id}`}
                className="font-display text-lg font-normal uppercase tracking-tight"
              >
                {group.era.label}
              </h2>
              <span className="text-xs tabular-nums text-muted">
                {group.entries.length}
              </span>
            </div>

            <ol className="relative border-l border-border pl-6">
              {group.entries.map((entry) => {
                const type = cosmographFacet(entry.entity, "cosmograph_type");
                const tradition = cosmographFacet(entry.entity, "tradition");
                const domain = cosmographFacet(entry.entity, "domain");
                const description =
                  typeof entry.entity.data.description === "string"
                    ? entry.entity.data.description
                    : null;

                return (
                  <li key={entry.entity.id} className="relative pb-6 last:pb-0">
                    <span
                      aria-hidden
                      className="absolute -left-[1.625rem] top-1.5 h-2.5 w-2.5 rounded-full border-2 border-canvas bg-ink"
                    />
                    <div className="rounded-lg border border-border bg-surface p-4 transition-colors hover:border-accent">
                      <div className="flex flex-wrap items-baseline justify-between gap-2">
                        <Link
                          href={entityHref(entry.entity)}
                          className="text-base font-semibold tracking-tight text-ink hover:text-accent-ink"
                        >
                          {entry.entity.label}
                        </Link>
                        <time className="shrink-0 text-xs tabular-nums text-muted">
                          {entry.yearLabel}
                        </time>
                      </div>

                      <p className="mt-1 text-xs text-muted">
                        {[tradition, type, domain].filter(Boolean).join(" · ")}
                      </p>

                      {description && (
                        <p className="mt-2 text-sm leading-relaxed text-ink/90 line-clamp-3">
                          {description}
                        </p>
                      )}
                    </div>
                  </li>
                );
              })}
            </ol>
          </section>
        ))}
      </div>
    </div>
  );
}
