import type { TrustTier } from "@/lib/types";
import { TIER_META, pct } from "@/lib/format";

export function TrustBadge({ tier }: { tier: TrustTier }) {
  const meta = TIER_META[tier];
  return (
    <span
      title={meta.title}
      className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium ${meta.cls}`}
    >
      <span aria-hidden className="h-1.5 w-1.5 rounded-full bg-current" />
      {meta.label}
    </span>
  );
}

export function ConfidenceBar({ value }: { value: number }) {
  return (
    <span className="inline-flex items-center gap-1.5" title={`Confidence ${pct(value)}`}>
      <span className="h-1.5 w-16 overflow-hidden rounded-full bg-confidence-track">
        <span
          className="block h-full rounded-full bg-accent"
          style={{ width: pct(value) }}
        />
      </span>
      <span className="text-xs tabular-nums text-muted">{pct(value)}</span>
    </span>
  );
}

export function DisputedBadge() {
  return (
    <span
      title="A counter-claim exists for this assertion."
      className="inline-flex items-center gap-1 rounded-full border border-disputed px-2 py-0.5 text-xs font-medium text-disputed"
    >
      Disputed
    </span>
  );
}
