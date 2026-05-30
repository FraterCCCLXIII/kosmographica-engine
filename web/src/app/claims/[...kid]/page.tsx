import Link from "next/link";
import { notFound } from "next/navigation";
import { ApiError, api } from "@/lib/api";
import { fmtDate } from "@/lib/format";
import type { ClaimAuditOut } from "@/lib/types";
import { Card, PageHeader } from "@/components/Card";
import { ConfidenceBar, DisputedBadge, TierBadge } from "@/components/Badges";

export default async function ClaimDetailPage({
  params,
}: {
  params: Promise<{ kid: string[] }>;
}) {
  const kid = (await params).kid.join("/");
  let claim: ClaimAuditOut;
  try {
    claim = await api.claim(kid);
  } catch (e) {
    if (e instanceof ApiError && e.status === 404) notFound();
    throw e;
  }

  return (
    <div className="max-w-3xl">
      <PageHeader
        title="Claim verification"
        subtitle={
          claim.about_label ? (
            <>
              About {claim.about_kind}:{" "}
              {claim.about_kind === "entity" ? (
                <Link href={`/entities/${claim.about_id}`} className="text-accent hover:underline">
                  {claim.about_label}
                </Link>
              ) : (
                <span className="font-medium">{claim.about_label}</span>
              )}
            </>
          ) : (
            claim.about_id
          )
        }
      />

      <Card>
        <div className="flex items-start justify-between gap-4">
          <p className="text-base leading-relaxed">{claim.assertion}</p>
          <div className="flex shrink-0 flex-col items-end gap-2">
            <TierBadge tier={claim.tier} />
            {claim.disputed && <DisputedBadge />}
          </div>
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-x-6 gap-y-2 text-xs text-muted">
          <ConfidenceBar value={claim.confidence} />
          {claim.generator && <span className="font-mono">{claim.generator}</span>}
          {claim.batch_id && <span>batch {claim.batch_id}</span>}
          <span>{fmtDate(claim.recorded_at)}</span>
        </div>
      </Card>

      <Section title="Support spans">
        {claim.support_spans.length === 0 ? (
          <p className="text-sm text-muted">No grounded spans (federated source import).</p>
        ) : (
          <ul className="space-y-2">
            {claim.support_spans.map((span, i) => (
              <li key={i} className="border-l-2 border-accent/40 pl-3 text-sm italic">
                “{span.quote}”
                {span.locator && <span className="not-italic text-muted"> — {span.locator}</span>}
              </li>
            ))}
          </ul>
        )}
      </Section>

      <Section title="Sources">
        <ul className="space-y-1 text-sm">
          {claim.sources.map((s) => (
            <li key={s.id}>
              {s.uri ? (
                <a href={s.uri} className="text-accent hover:underline" rel="noreferrer">
                  {s.citation}
                </a>
              ) : (
                s.citation
              )}
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Verification history">
        {claim.verifications.length === 0 ? (
          <p className="text-sm text-muted">Not machine-verified.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="text-left text-xs uppercase tracking-wide text-muted">
                <tr>
                  <th className="py-2 pr-4">Outcome</th>
                  <th className="py-2 pr-4">Label</th>
                  <th className="py-2 pr-4">Score</th>
                  <th className="py-2 pr-4">Verifier</th>
                  <th className="py-2 pr-4">Reason</th>
                  <th className="py-2">When</th>
                </tr>
              </thead>
              <tbody>
                {claim.verifications.map((v, i) => (
                  <tr key={i} className="border-t border-border">
                    <td className="py-2 pr-4 font-medium">{v.outcome}</td>
                    <td className="py-2 pr-4">{v.support_label}</td>
                    <td className="py-2 pr-4 tabular-nums">{v.support_score.toFixed(2)}</td>
                    <td className="py-2 pr-4 font-mono text-xs">{v.verifier}</td>
                    <td className="py-2 pr-4 text-muted">{v.reason}</td>
                    <td className="py-2 text-muted">{fmtDate(v.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Section>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mt-6">
      <h2 className="mb-2 text-sm font-semibold">{title}</h2>
      <Card>{children}</Card>
    </section>
  );
}
