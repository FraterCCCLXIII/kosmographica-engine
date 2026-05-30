import type { TrustTier } from "@/lib/types";
import { TIER_META, pct } from "@/lib/format";

export function TierBadge({ tier }: { tier: TrustTier }) {
  const meta = TIER_META[tier] ?? { label: tier, cls: "border-border text-muted" };
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium ${meta.cls}`}
      title={tier}
    >
      {meta.label}
    </span>
  );
}

export function DisputedBadge() {
  return (
    <span className="inline-flex items-center rounded-full border border-disputed px-2 py-0.5 text-xs font-medium text-disputed">
      Disputed
    </span>
  );
}

export function ConfidenceBar({ value }: { value: number }) {
  const clamped = Math.max(0, Math.min(1, value));
  return (
    <div className="flex items-center gap-2" title={`confidence ${pct(value)}`}>
      <div className="h-1.5 w-24 overflow-hidden rounded-full bg-[var(--confidence-track)]">
        <div
          className="h-full rounded-full bg-accent"
          style={{ width: `${clamped * 100}%` }}
        />
      </div>
      <span className="tabular-nums text-xs text-muted">{pct(value)}</span>
    </div>
  );
}
