import Link from "next/link";
import type { EntityOut } from "@/lib/types";
import { entityHref } from "@/lib/types";
import { lifespan } from "@/lib/format";
import { entityImage } from "@/lib/entity-media";
import { TrustBadge } from "./Badges";

export function EntityCard({ entity }: { entity: EntityOut }) {
  const dates = lifespan(entity.valid_from, entity.valid_to);
  const image = entityImage(entity);
  const description =
    entity.type === "Cosmograph" && typeof entity.data.description === "string"
      ? entity.data.description
      : null;
  return (
    <Link
      href={entityHref(entity)}
      prefetch={false}
      className="group block overflow-hidden rounded-lg border border-border bg-surface transition-colors hover:border-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
    >
      {image && (
        <div className="aspect-[16/9] w-full overflow-hidden border-b border-border bg-[#f4f4f2]">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={image.thumbnailUrl}
            alt={image.title ?? entity.label}
            loading="lazy"
            className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-[1.02]"
          />
        </div>
      )}
      <div className="p-4">
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
        {description && (
          <p className="mt-2 line-clamp-3 text-xs leading-relaxed text-muted">{description}</p>
        )}
      </div>
    </Link>
  );
}
