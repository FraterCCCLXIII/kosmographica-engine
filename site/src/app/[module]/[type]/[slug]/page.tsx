import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { ApiError, api } from "@/lib/api";
import { lifespan, TIER_META } from "@/lib/format";
import { entityHref } from "@/lib/types";
import { hasLineageView } from "@/lib/lineage";
import type { EntityDetailOut, GraphOut, LineageOut } from "@/lib/types";
import { ConfidenceBar, DisputedBadge, ReviewBadge, StatusBadge, TrustBadge } from "@/components/Badges";
import { ClaimSources } from "@/components/ClaimSources";
import { GraphExplorer } from "@/components/GraphExplorer";
import { LineageViewer } from "@/components/LineageViewer";

type Params = { module: string; type: string; slug: string };

async function load(
  params: Params,
): Promise<{ entity: EntityDetailOut; graph: GraphOut; lineage: LineageOut | null }> {
  const entity = await api.entityBySlug(params.module, params.type, params.slug);
  const graph = await api.graph(entity.id);
  let lineage: LineageOut | null = null;
  if (hasLineageView(entity.type)) {
    try {
      lineage = await api.lineage(entity.id);
    } catch (e) {
      if (!(e instanceof ApiError && e.status === 404)) throw e;
    }
  }
  return { entity, graph, lineage };
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const p = await params;
  try {
    const entity = await api.entityBySlug(p.module, p.type, p.slug);
    const desc =
      typeof entity.data.description === "string"
        ? entity.data.description
        : `${entity.label} — ${entity.type} in the Kosmographica graph.`;
    return { title: entity.label, description: desc.slice(0, 200) };
  } catch {
    return { title: "Not found" };
  }
}

export default async function EntityPage({ params }: { params: Promise<Params> }) {
  const p = await params;
  let entity: EntityDetailOut;
  let graph: GraphOut;
  let lineage: LineageOut | null;
  try {
    ({ entity, graph, lineage } = await load(p));
  } catch (e) {
    if (e instanceof ApiError && e.status === 404) notFound();
    throw e;
  }

  const description = typeof entity.data.description === "string" ? entity.data.description : null;
  const status = typeof entity.data.status === "string" ? entity.data.status : null;
  const needsReview = entity.data.needs_taxonomy_review === true;
  const reviewReason =
    typeof entity.data.taxonomy_review_reason === "string"
      ? entity.data.taxonomy_review_reason
      : undefined;
  const dates = lifespan(entity.valid_from, entity.valid_to);
  const nodeById = new Map(graph.nodes.map((n) => [n.id, n]));
  const outgoing = graph.edges.filter((e) => e.subject_id === entity.id);
  const incoming = graph.edges.filter((e) => e.object_id === entity.id);
  const facts = infoboxFacts(entity);
  const hasConnections = outgoing.length > 0 || incoming.length > 0;

  return (
    <article>
      <nav className="mb-4 text-xs text-muted">
        <Link href="/" className="hover:text-accent-ink">Home</Link>
        <span className="px-1.5">/</span>
        <Link href="/browse" className="hover:text-accent-ink">Browse</Link>
        <span className="px-1.5">/</span>
        <span>{entity.type}</span>
      </nav>

      <header className="border-b border-border pb-5">
        <div className="flex flex-wrap items-center gap-3">
          <h1 className="text-3xl font-semibold tracking-tight">{entity.label}</h1>
          <TrustBadge tier={entity.tier} />
          {status && <StatusBadge status={status} />}
          {needsReview && <ReviewBadge reason={reviewReason} />}
        </div>
        <p className="mt-2 text-sm text-muted">
          {entity.type}
          {entity.subtype ? ` · ${entity.subtype}` : ""}
          {dates ? ` · ${dates}` : ""}
        </p>
        {description && (
          <p className="mt-4 max-w-2xl text-base leading-relaxed">{description}</p>
        )}
      </header>

      <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-[minmax(0,1fr)_18rem]">
        {/* Main column */}
        <div className="order-2 min-w-0 lg:order-1">
          {hasLineageView(entity.type) && lineage && (
            <section className="mb-8">
              <div className="mb-3 flex flex-wrap items-baseline justify-between gap-2">
                <h2 className="text-lg font-semibold tracking-tight">Lineage</h2>
                {lineage.transmission_count > 0 && (
                  <span className="text-xs text-muted tabular-nums">
                    {lineage.transmission_count} transmission
                    {lineage.transmission_count === 1 ? "" : "s"}
                  </span>
                )}
              </div>
              {lineage.chart.id !== entity.id && (
                <p className="mb-3 text-sm text-muted">
                  Showing transmission tree for{" "}
                  <Link href={entityHref(lineage.chart)} className="text-ink underline-offset-2 hover:underline">
                    {lineage.chart.label}
                  </Link>
                </p>
              )}
              <LineageViewer lineage={lineage} />
            </section>
          )}

          {entity.claims.length > 0 && (
            <section>
              <h2 className="mb-3 text-lg font-semibold tracking-tight">Claims</h2>
              <ul className="space-y-3">
                {entity.claims.map((c) => (
                  <li key={c.id} className="rounded-lg border border-border bg-surface p-4">
                    <p className="leading-relaxed">{c.assertion}</p>
                    <div className="mt-2 flex flex-wrap items-center gap-3">
                      <TrustBadge tier={c.tier} />
                      <ConfidenceBar value={c.confidence} />
                      {c.disputed && <DisputedBadge />}
                    </div>
                    <ClaimSources sources={c.sources} spans={c.support_spans} />
                  </li>
                ))}
              </ul>
            </section>
          )}

          {graph.nodes.length > 1 && !hasLineageView(entity.type) && (
            <section className="mt-8">
              <h2 className="mb-3 text-lg font-semibold tracking-tight">Graph</h2>
              <GraphExplorer graph={graph} rootId={entity.id} />
            </section>
          )}
        </div>

        {/* Right rail: infobox metadata + connections */}
        <aside className="order-1 lg:order-2 lg:sticky lg:top-4 lg:self-start">
          <div className="rounded-lg border border-border bg-surface">
            <div className="border-b border-border px-4 py-3">
              <h2 className="text-sm font-semibold tracking-tight">Details</h2>
            </div>
            <dl className="divide-y divide-border">
              <FactRow label="Type" value={entity.subtype ? `${entity.type} · ${entity.subtype}` : entity.type} />
              {dates && <FactRow label="Dates" value={dates} />}
              <FactRow label="Module" value={entity.module} />
              <FactRow label="Trust" value={TIER_META[entity.tier].label} />
              {entity.generator && <FactRow label="Source" value={entity.generator} />}
              {facts.map((f) => (
                <FactRow key={f.label} label={f.label} value={f.value} />
              ))}
            </dl>
          </div>

          {hasConnections && (
            <div className="mt-4 rounded-lg border border-border bg-surface">
              <div className="border-b border-border px-4 py-3">
                <h2 className="text-sm font-semibold tracking-tight">Connections</h2>
              </div>
              <ul className="divide-y divide-border text-sm">
                {outgoing.map((e) => {
                  const n = nodeById.get(e.object_id);
                  return (
                    <li key={e.id} className="px-4 py-2.5">
                      <span className="block text-xs text-muted">{e.predicate.replace(/_/g, " ")}</span>
                      {n ? (
                        <Link href={entityHref(n)} className="font-medium text-accent-ink hover:underline">
                          {n.label}
                        </Link>
                      ) : (
                        <span className="text-muted">(hidden)</span>
                      )}
                    </li>
                  );
                })}
                {incoming.map((e) => {
                  const n = nodeById.get(e.subject_id);
                  return (
                    <li key={e.id} className="px-4 py-2.5">
                      <span className="block text-xs text-muted">{e.predicate.replace(/_/g, " ")} this</span>
                      {n ? (
                        <Link href={entityHref(n)} className="font-medium text-accent-ink hover:underline">
                          {n.label}
                        </Link>
                      ) : (
                        <span className="text-muted">(hidden)</span>
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          )}
        </aside>
      </div>
    </article>
  );
}

function FactRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="px-4 py-2.5">
      <dt className="text-xs text-muted">{label}</dt>
      <dd className="mt-0.5 text-sm text-ink">{value}</dd>
    </div>
  );
}

// Surfaces primitive scalar fields from entity.data as infobox facts
// (skips description, which is shown in the header, and any nested objects).
function infoboxFacts(entity: EntityDetailOut): { label: string; value: string }[] {
  const facts: { label: string; value: string }[] = [];
  // Keys surfaced elsewhere (header badges / title) — don't repeat them as raw facts.
  const SKIP = new Set([
    "description",
    "status",
    "needs_taxonomy_review",
    "taxonomy_review_reason",
    "is_collective",
    "myth_type",
  ]);
  for (const [key, raw] of Object.entries(entity.data)) {
    if (SKIP.has(key) || raw === null || raw === undefined) continue;
    if (typeof raw === "object") continue;
    const value = typeof raw === "boolean" ? (raw ? "Yes" : "No") : String(raw);
    if (!value.trim()) continue;
    const label = key.replace(/_/g, " ").replace(/^\w/, (c) => c.toUpperCase());
    facts.push({ label, value });
    if (facts.length >= 8) break;
  }
  return facts;
}
