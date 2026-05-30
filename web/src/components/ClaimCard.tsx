import Link from "next/link";
import type { ClaimAuditOut } from "@/lib/types";
import { fmtDate } from "@/lib/format";
import { Card } from "./Card";
import { ConfidenceBar, DisputedBadge, TierBadge } from "./Badges";

export function ClaimCard({ claim }: { claim: ClaimAuditOut }) {
  return (
    <Card className="transition-colors hover:border-accent/50">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          {claim.about_label && (
            <div className="mb-1 text-xs font-medium uppercase tracking-wide text-muted">
              {claim.about_kind}: {claim.about_label}
            </div>
          )}
          <Link href={`/claims/${claim.id}`} className="block">
            <p className="line-clamp-2 text-sm leading-relaxed hover:text-accent">
              {claim.assertion}
            </p>
          </Link>
        </div>
        <div className="flex shrink-0 flex-col items-end gap-2">
          <TierBadge tier={claim.tier} />
          {claim.disputed && <DisputedBadge />}
        </div>
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-muted">
        <ConfidenceBar value={claim.confidence} />
        {claim.generator && <span className="font-mono">{claim.generator}</span>}
        <span>{claim.sources.length} source{claim.sources.length === 1 ? "" : "s"}</span>
        <span>{fmtDate(claim.recorded_at)}</span>
      </div>
    </Card>
  );
}
