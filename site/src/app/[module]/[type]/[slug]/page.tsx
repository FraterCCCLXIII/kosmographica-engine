import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { ApiError, api } from "@/lib/api";
import { lifespan } from "@/lib/format";
import { entityHref } from "@/lib/types";
import type { EntityDetailOut, GraphOut } from "@/lib/types";
import { ConfidenceBar, DisputedBadge, TrustBadge } from "@/components/Badges";
import { ClaimSources } from "@/components/ClaimSources";
import { GraphExplorer } from "@/components/GraphExplorer";

type Params = { module: string; type: string; slug: string };

async function load(params: Params): Promise<{ entity: EntityDetailOut; graph: GraphOut }> {
  const entity = await api.entityBySlug(params.module, params.type, params.slug);
  const graph = await api.graph(entity.id);
  return { entity, graph };
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
  try {
    ({ entity, graph } = await load(p));
  } catch (e) {
    if (e instanceof ApiError && e.status === 404) notFound();
    throw e;
  }

  const description = typeof entity.data.description === "string" ? entity.data.description : null;
  const dates = lifespan(entity.valid_from, entity.valid_to);
  const nodeById = new Map(graph.nodes.map((n) => [n.id, n]));
  const outgoing = graph.edges.filter((e) => e.subject_id === entity.id);
  const incoming = graph.edges.filter((e) => e.object_id === entity.id);

  return (
    <article>
      <nav className="mb-4 text-xs text-muted">
        <Link href="/" className="hover:text-accent-ink">Home</Link>
        <span className="px-1.5">/</span>
        <span>{entity.type}</span>
      </nav>

      <header className="border-b border-border pb-5">
        <div className="flex flex-wrap items-center gap-3">
          <h1 className="text-3xl font-semibold tracking-tight">{entity.label}</h1>
          <TrustBadge tier={entity.tier} />
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

      {entity.claims.length > 0 && (
        <section className="mt-8">
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

      {(outgoing.length > 0 || incoming.length > 0) && (
        <section className="mt-8">
          <h2 className="mb-3 text-lg font-semibold tracking-tight">Connections</h2>
          <ul className="space-y-2 text-sm">
            {outgoing.map((e) => {
              const n = nodeById.get(e.object_id);
              return (
                <li key={e.id} className="flex flex-wrap items-baseline gap-2">
                  <span className="text-muted">{e.predicate.replace(/_/g, " ")}</span>
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
                <li key={e.id} className="flex flex-wrap items-baseline gap-2">
                  {n ? (
                    <Link href={entityHref(n)} className="font-medium text-accent-ink hover:underline">
                      {n.label}
                    </Link>
                  ) : (
                    <span className="text-muted">(hidden)</span>
                  )}
                  <span className="text-muted">{e.predicate.replace(/_/g, " ")} this</span>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      {graph.nodes.length > 1 && (
        <section className="mt-8">
          <h2 className="mb-3 text-lg font-semibold tracking-tight">Graph</h2>
          <GraphExplorer graph={graph} rootId={entity.id} />
        </section>
      )}
    </article>
  );
}
