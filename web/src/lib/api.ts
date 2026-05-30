// Typed client for the Kosmographica engine REST API.
// Read-only: the console never writes. AI is the only writer (Wave 1); humans observe.

import type {
  AuditStats,
  ClaimAuditOut,
  EntityDetailOut,
  GraphOut,
  Page,
  SearchHitOut,
} from "./types";

const BASE = process.env.KGE_API_URL ?? "http://localhost:8000";

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function apiGet<T>(path: string, params?: Record<string, string | number | boolean | undefined>): Promise<T> {
  const url = new URL(BASE + path);
  for (const [k, v] of Object.entries(params ?? {})) {
    if (v !== undefined && v !== "") url.searchParams.set(k, String(v));
  }
  // Audit data must always be live, never cached.
  const res = await fetch(url.toString(), { cache: "no-store" });
  if (!res.ok) {
    throw new ApiError(res.status, `${res.status} ${res.statusText} for ${path}`);
  }
  return res.json() as Promise<T>;
}

// KIDs contain a "/" (e.g. kg:entity/uuid); keep it literal in the path.
const kidPath = (kid: string) => kid;

export const api = {
  stats: () => apiGet<AuditStats>("/v1/audit/stats"),

  entity: (kid: string, minTier = "machine_validated") =>
    apiGet<EntityDetailOut>(`/v1/entities/${kidPath(kid)}`, { min_tier: minTier }),

  graph: (kid: string, minTier = "machine_validated") =>
    apiGet<GraphOut>(`/v1/entities/${kidPath(kid)}/graph`, { min_tier: minTier }),

  search: (q: string, minTier = "machine_validated") =>
    apiGet<SearchHitOut[]>("/v1/search", { q, min_tier: minTier }),

  claims: (params: {
    tier?: string;
    generator?: string;
    batch_id?: string;
    disputed?: boolean;
    limit?: number;
    offset?: number;
  }) => apiGet<Page<ClaimAuditOut>>("/v1/audit/claims", params),

  disputes: (limit = 50) => apiGet<Page<ClaimAuditOut>>("/v1/audit/disputes", { limit }),

  claim: (kid: string) => apiGet<ClaimAuditOut>(`/v1/audit/claims/${kidPath(kid)}`),
};

export { ApiError };
