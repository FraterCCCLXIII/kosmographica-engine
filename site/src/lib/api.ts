// Typed client for the Kosmographica engine REST API — PUBLIC surface.
// The public site never sends min_tier, so the engine applies its public clamp
// (machine_validated+; machine_unverified hidden, sacred/restricted gated).

import type {
  EntityDetailOut,
  EntityOut,
  GraphOut,
  LineageOut,
  Page,
  SearchHitOut,
} from "./types";

const BASE = process.env.KGE_API_URL ?? "http://localhost:8088";

/** Shown when server-side fetches to the engine fail (API down or DB unreachable). */
export function engineOfflineHint(): string {
  const url = new URL(BASE);
  const port = url.port || (url.protocol === "https:" ? "443" : "80");
  return (
    `The knowledge engine isn’t reachable. In engine/, run ` +
    `\`docker compose up -d db\` (Postgres on :5459), then ` +
    `\`uv run uvicorn kge.api.app:app --port ${port}\`, and reload.`
  );
}

// ISR: revalidate public pages periodically rather than rendering on every hit.
const REVALIDATE_SECONDS = 300;

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function apiGet<T>(
  path: string,
  params?: Record<string, string | number | boolean | undefined>,
): Promise<T> {
  const url = new URL(BASE + path);
  for (const [k, v] of Object.entries(params ?? {})) {
    if (v !== undefined && v !== "") url.searchParams.set(k, String(v));
  }
  const res = await fetch(url.toString(), { next: { revalidate: REVALIDATE_SECONDS } });
  if (!res.ok) throw new ApiError(res.status, `${res.status} ${res.statusText} for ${path}`);
  return res.json() as Promise<T>;
}

export const api = {
  listEntities: (params: { module?: string; type?: string; limit?: number; offset?: number }) =>
    apiGet<Page<EntityOut>>("/v1/entities", params),

  entityBySlug: (module: string, type: string, slug: string) =>
    apiGet<EntityDetailOut>(
      `/v1/entities/by-slug/${encodeURIComponent(module)}/${encodeURIComponent(type)}/${encodeURIComponent(slug)}`,
    ),

  graph: (kid: string) => apiGet<GraphOut>(`/v1/entities/${kid}/graph`),

  lineage: (kid: string) => apiGet<LineageOut>(`/v1/entities/${kid}/lineage`),

  search: (q: string) => apiGet<SearchHitOut[]>("/v1/search", { q }),
};
