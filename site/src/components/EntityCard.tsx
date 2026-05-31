import Link from "next/link";
import type { EntityOut } from "@/lib/types";
import { entityHref } from "@/lib/types";
import { lifespan } from "@/lib/format";
import { TrustBadge } from "./Badges";

export function EntityCard({ entity }: { entity: EntityOut }) {
  const dates = lifespan(entity.valid_from, entity.valid_to);
  return (
    <Link
      href={entityHref(entity)}
      prefetch={false}
      className="group block rounded-lg border border-border bg-surface p-4 transition-colors hover:border-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
    >
      <div className="flex items-start justify-between gap-3">
        <h3 className="text-base font-semibold tracking-tight group-hover:text-accent-ink">
          {entity.label}
        </h3>
        <TrustBadge tier={entity.tier} />
      </div>
      <p className="mt-1 text-xs text-muted">
        {entity.type}
        {entity.subtype ? ` · ${entity.subtype}` : ""}
        {dates ? ` · ${dates}` : ""}
      </p>
    </Link>
  );
}
