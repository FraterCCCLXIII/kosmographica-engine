import type { Metadata } from "next";
import { TIER_META } from "@/lib/format";
import type { TrustTier } from "@/lib/types";

export const metadata: Metadata = {
  title: "How this works",
  description:
    "Kosmographica is authored by AI under a publish-then-verify workflow. Every claim is cited and carries a trust rating.",
};

const TIER_ORDER: TrustTier[] = [
  "machine_unverified",
  "machine_validated",
  "human_reviewed",
  "expert_endorsed",
];

export default function AboutPage() {
  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">How this works</h1>

      <p className="mt-4 text-base leading-relaxed text-muted">
        Kosmographica is a source-grounded graph of human thought. Entries are authored by AI
        under a <strong className="text-ink">publish-then-verify</strong> workflow: content is
        written with citations, then checked against its sources and promoted over time. Every
        claim you see is grounded in a cited source and carries a trust rating.
      </p>

      <h2 className="mt-10 text-lg font-semibold tracking-tight">Trust tiers</h2>
      <dl className="mt-3 space-y-3">
        {TIER_ORDER.map((tier) => (
          <div key={tier} className="rounded-lg border border-border bg-surface p-4">
            <dt
              className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium ${TIER_META[tier].cls}`}
            >
              <span aria-hidden className="h-1.5 w-1.5 rounded-full bg-current" />
              {TIER_META[tier].label}
            </dt>
            <dd className="mt-2 text-sm leading-relaxed text-muted">{TIER_META[tier].title}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
