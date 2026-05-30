import Link from "next/link";
import { api } from "@/lib/api";
import { Card, PageHeader, Stat, EmptyState } from "@/components/Card";
import { fmtYear } from "@/lib/format";
import type { ReconEntityOut, ReconciliationOut, SourceParityOut } from "@/lib/types";

const STATUSES = ["proposed", "accepted", "rejected", "all"] as const;

function ParityCard({ p }: { p: SourceParityOut }) {
  return (
    <Card>
      <div className="flex items-center justify-between">
        <span className="font-mono text-sm">{p.source_system}</span>
        <span
          className={`rounded-full border px-2 py-0.5 text-xs font-medium ${
            p.converged
              ? "border-tier-validated text-tier-validated"
              : "border-tier-unverified text-tier-unverified"
          }`}
        >
          {p.converged ? "converged" : "incomplete"}
        </span>
      </div>
      <dl className="mt-3 grid grid-cols-3 gap-2 text-sm">
        <div>
          <dt className="text-muted">entities</dt>
          <dd className="tabular-nums">{p.entities.toLocaleString()}</dd>
        </div>
        <div>
          <dt className="text-muted">relations</dt>
          <dd className="tabular-nums">{p.relationships.toLocaleString()}</dd>
        </div>
        <div>
          <dt className="text-muted">claims</dt>
          <dd className="tabular-nums">{p.claims.toLocaleString()}</dd>
        </div>
      </dl>
    </Card>
  );
}

function EntitySide({ e, kid }: { e: ReconEntityOut | null; kid: string }) {
  if (!e) return <div className="text-sm text-muted">missing entity ({kid})</div>;
  const span = [fmtYear(e.valid_from), fmtYear(e.valid_to)].filter(Boolean).join(" – ");
  return (
    <Link href={`/entities/${e.id}`} className="block hover:text-accent">
      <div className="font-medium">{e.label}</div>
      <div className="mt-0.5 text-xs text-muted">
        <span className="font-mono">{e.source_system}</span> · {e.type}
        {span && <> · {span}</>}
      </div>
    </Link>
  );
}

function ProposalCard({ r }: { r: ReconciliationOut }) {
  const statusCls =
    r.status === "accepted"
      ? "border-tier-validated text-tier-validated"
      : r.status === "rejected"
        ? "border-disputed text-disputed"
        : "border-tier-unverified text-tier-unverified";
  return (
    <Card>
      <div className="mb-3 flex items-center justify-between text-xs">
        <span className="font-mono text-muted">#{r.id}</span>
        <div className="flex items-center gap-2">
          <span className="rounded-full border border-border px-2 py-0.5">{r.match_method}</span>
          <span className="tabular-nums text-muted">score {r.score.toFixed(2)}</span>
          <span className={`rounded-full border px-2 py-0.5 font-medium ${statusCls}`}>{r.status}</span>
        </div>
      </div>
      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-3">
        <EntitySide e={r.left} kid={r.left_kid} />
        <span className="text-muted" aria-hidden>
          ≈
        </span>
        <EntitySide e={r.right} kid={r.right_kid} />
      </div>
      {r.reason && <p className="mt-3 text-xs text-muted">{r.reason}</p>}
    </Card>
  );
}

export default async function ReconcilePage({
  searchParams,
}: {
  searchParams: Promise<{ status?: string }>;
}) {
  const { status: rawStatus } = await searchParams;
  const status = STATUSES.includes((rawStatus ?? "") as (typeof STATUSES)[number])
    ? (rawStatus as string)
    : "proposed";

  const [parity, stats, proposals] = await Promise.all([
    api.parity(),
    api.reconciliationStats(),
    api.reconciliationProposals(status, 100),
  ]);

  return (
    <div>
      <PageHeader
        title="Reconciliation"
        subtitle={
          <>
            Cross-source <code className="font-mono">sameAs</code> resolution. Shared external IDs
            auto-link; name matches need review — no cross-tradition auto-merge on name alone.
            Decisions are operator actions via <code className="font-mono">kge reconcile</code>.
          </>
        }
      />

      <section className="mb-8">
        <h2 className="mb-3 text-sm font-semibold text-muted">Source convergence (parity)</h2>
        <div className="grid gap-3 sm:grid-cols-2">
          {parity.map((p) => (
            <ParityCard key={p.source_system} p={p} />
          ))}
        </div>
      </section>

      <section className="mb-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Stat label="Proposals (total)" value={stats.total.toLocaleString()} />
        <Stat label="Awaiting review" value={(stats.by_status.proposed ?? 0).toLocaleString()} />
        <Stat
          label="Accepted (sameAs)"
          value={(stats.by_status.accepted ?? 0).toLocaleString()}
          accent="text-tier-validated"
        />
        <Stat label="Rejected" value={(stats.by_status.rejected ?? 0).toLocaleString()} />
      </section>

      <div className="mb-4 flex flex-wrap gap-2">
        {STATUSES.map((s) => (
          <Link
            key={s}
            href={s === "proposed" ? "/reconcile" : `/reconcile?status=${s}`}
            className={`rounded-lg border px-3 py-1.5 text-sm font-medium capitalize ${
              status === s
                ? "border-accent text-accent"
                : "border-border text-muted hover:bg-foreground/5"
            }`}
          >
            {s}
          </Link>
        ))}
      </div>

      <div className="space-y-3">
        {proposals.items.length === 0 ? (
          <EmptyState>
            No {status === "all" ? "" : status} reconciliations. The two current sources cover largely
            disjoint subjects, so cross-source overlap is rare — the queue grows as overlapping sources
            converge.
          </EmptyState>
        ) : (
          proposals.items.map((r) => <ProposalCard key={r.id} r={r} />)
        )}
      </div>
    </div>
  );
}
