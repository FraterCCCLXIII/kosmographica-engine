import Link from "next/link";
import { notFound } from "next/navigation";
import { ApiError, api } from "@/lib/api";
import { fmtYear } from "@/lib/format";
import type { EntityDetailOut, GraphOut } from "@/lib/types";
import { Card, PageHeader } from "@/components/Card";
import { ConfidenceBar, DisputedBadge, TierBadge } from "@/components/Badges";

export default async function EntityPage({ params }: { params: Promise<{ kid: string[] }> }) {
  const kid = (await params).kid.join("/");
  let entity: EntityDetailOut;
  let graph: GraphOut;
  try {
    // Audit view: include unverified records so nothing is hidden from the auditor.
    [entity, graph] = await Promise.all([
      api.entity(kid, "machine_unverified"),
      api.graph(kid, "machine_unverified"),
    ]);
  } catch (e) {
    if (e instanceof ApiError && e.status === 404) notFound();
    throw e;
  }

  const description = typeof entity.data.description === "string" ? entity.data.description : null;
  const tradition = typeof entity.data.tradition === "string" ? entity.data.tradition : null;
  const labelById = new Map(graph.nodes.map((n) => [n.id, n.label]));
  const from = fmtYear(entity.valid_from);
  const to = fmtYear(entity.valid_to);

  return (
    <div className="max-w-3xl">
      <PageHeader
        title={entity.label}
        subtitle={
          <span className="flex flex-wrap items-center gap-x-3 gap-y-1">
            <span>
              {entity.type}
              {entity.subtype ? ` · ${entity.subtype}` : ""}
            </span>
            {tradition && <span>· {tradition}</span>}
            {from && <span>· {from}{to ? `–${to}` : ""}</span>}
            <TierBadge tier={entity.tier} />
          </span>
        }
      />

      {description && (
        <Card className="mb-6">
          <p className="text-sm leading-relaxed">{description}</p>
        </Card>
      )}

      <section className="mb-6">
        <h2 className="mb-2 text-sm font-semibold">Claims ({entity.claims.length})</h2>
        <div className="space-y-2">
          {entity.claims.length === 0 && (
            <Card className="text-sm text-muted">No claims at this tier.</Card>
          )}
          {entity.claims.map((c) => (
            <Card key={c.id} className="transition-colors hover:border-accent/50">
              <Link href={`/claims/${c.id}`} className="block">
                <p className="text-sm leading-relaxed hover:text-accent">{c.assertion}</p>
              </Link>
              <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-muted">
                <ConfidenceBar value={c.confidence} />
                <TierBadge tier={c.tier} />
                {c.disputed && <DisputedBadge />}
              </div>
            </Card>
          ))}
        </div>
      </section>

      <section>
        <h2 className="mb-2 text-sm font-semibold">Relationships ({graph.edges.length})</h2>
        <Card>
          {graph.edges.length === 0 ? (
            <p className="text-sm text-muted">No relationships at this tier.</p>
          ) : (
            <ul className="space-y-1 text-sm">
              {graph.edges.map((e) => {
                const neighborId = e.subject_id === entity.id ? e.object_id : e.subject_id;
                const outgoing = e.subject_id === entity.id;
                return (
                  <li key={e.id} className="flex items-center gap-2">
                    <span className="text-muted">{outgoing ? "→" : "←"}</span>
                    <span className="font-mono text-xs text-muted">{e.predicate}</span>
                    <Link href={`/entities/${neighborId}`} className="text-accent hover:underline">
                      {labelById.get(neighborId) ?? neighborId}
                    </Link>
                  </li>
                );
              })}
            </ul>
          )}
        </Card>
      </section>
    </div>
  );
}
