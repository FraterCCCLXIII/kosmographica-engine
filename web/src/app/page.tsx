import Link from "next/link";
import { api } from "@/lib/api";
import { TIER_META } from "@/lib/format";
import type { TrustTier } from "@/lib/types";
import { Card, PageHeader, Stat } from "@/components/Card";

export default async function OverviewPage() {
  const stats = await api.stats();
  const totalClaims = Object.values(stats.claims_by_tier).reduce((a, b) => a + b, 0);
  const totalEntities = Object.values(stats.entities_by_tier).reduce((a, b) => a + b, 0);
  const validated = stats.claims_by_tier["machine_validated"] ?? 0;

  return (
    <div>
      <PageHeader
        title="Corpus overview"
        subtitle="A read-only window onto the AI-populated claim graph and its trust tiers."
      />

      <form action="/search" className="mb-8 flex max-w-xl gap-2">
        <input
          name="q"
          placeholder="Search entities…"
          className="flex-1 rounded-lg border border-border bg-surface px-3 py-2 text-sm outline-none focus:border-accent"
        />
        <button className="rounded-lg bg-accent px-4 py-2 text-sm font-medium text-white">
          Search
        </button>
      </form>

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <Stat label="Entities" value={totalEntities.toLocaleString()} />
        <Stat label="Claims" value={totalClaims.toLocaleString()} />
        <Stat
          label="AI-validated claims"
          value={validated.toLocaleString()}
          accent="text-tier-validated"
        />
        <Stat
          label="Disputes"
          value={stats.disputes.toLocaleString()}
          accent={stats.disputes ? "text-disputed" : undefined}
        />
      </div>

      <div className="mt-8 grid gap-4 lg:grid-cols-2">
        <Card>
          <h2 className="mb-4 text-sm font-semibold">Claims by trust tier</h2>
          <TierBreakdown counts={stats.claims_by_tier} total={totalClaims} />
        </Card>
        <Card>
          <h2 className="mb-4 text-sm font-semibold">By generator</h2>
          <div className="space-y-2">
            {stats.claims_by_generator.length === 0 && (
              <p className="text-sm text-muted">No claims yet.</p>
            )}
            {stats.claims_by_generator.map((g, i) => (
              <div key={i} className="flex items-center justify-between text-sm">
                <span className="font-mono text-muted">{g.generator ?? "—"}</span>
                <span className="flex items-center gap-3">
                  <span className="text-xs text-muted">{g.tier}</span>
                  <span className="tabular-nums">{g.count.toLocaleString()}</span>
                </span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <p className="mt-6 text-sm text-muted">
        Review the{" "}
        <Link href="/queue" className="text-accent hover:underline">
          AI-validated queue
        </Link>{" "}
        or the{" "}
        <Link href="/disputes" className="text-accent hover:underline">
          disputes
        </Link>
        .
      </p>
    </div>
  );
}

function TierBreakdown({ counts, total }: { counts: Record<string, number>; total: number }) {
  const tiers: TrustTier[] = [
    "machine_unverified",
    "machine_validated",
    "human_reviewed",
    "expert_endorsed",
  ];
  const colorVar: Record<TrustTier, string> = {
    machine_unverified: "var(--tier-unverified)",
    machine_validated: "var(--tier-validated)",
    human_reviewed: "var(--tier-reviewed)",
    expert_endorsed: "var(--tier-expert)",
  };
  return (
    <div className="space-y-3">
      {tiers.map((tier) => {
        const value = counts[tier] ?? 0;
        const width = total ? (value / total) * 100 : 0;
        return (
          <div key={tier}>
            <div className="mb-1 flex justify-between text-xs">
              <span style={{ color: colorVar[tier] }}>{TIER_META[tier].label}</span>
              <span className="tabular-nums text-muted">{value.toLocaleString()}</span>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-[var(--confidence-track)]">
              <div
                className="h-full rounded-full"
                style={{ width: `${width}%`, background: colorVar[tier] }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}
