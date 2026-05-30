// Mirrors the engine read API (engine/src/kge/api/schemas.py). Public-facing subset.

export type TrustTier =
  | "machine_unverified"
  | "machine_validated"
  | "human_reviewed"
  | "expert_endorsed";

export interface SourceOut {
  id: string;
  citation: string;
  uri: string | null;
}

export interface SupportSpan {
  source_ref: string;
  quote: string;
  locator?: string | null;
}

export interface ClaimOut {
  id: string;
  about_kind: string;
  about_id: string;
  assertion: string;
  confidence: number;
  tier: TrustTier;
  generator: string | null;
  batch_id: string | null;
  disputed: boolean;
  support_spans: SupportSpan[];
  sources: SourceOut[];
  recorded_at: string;
}

export interface EntityOut {
  id: string;
  slug: string;
  module: string;
  type: string;
  subtype: string | null;
  label: string;
  data: Record<string, unknown>;
  valid_from: number | null;
  valid_to: number | null;
  tier: TrustTier;
  generator: string | null;
  sensitivity: string;
  recorded_at: string;
}

export interface EntityDetailOut extends EntityOut {
  claims: ClaimOut[];
}

export interface RelationshipOut {
  id: string;
  subject_id: string;
  predicate: string;
  object_id: string;
  data: Record<string, unknown>;
  tier: TrustTier;
}

export interface GraphOut {
  nodes: EntityOut[];
  edges: RelationshipOut[];
}

export interface SearchHitOut {
  entity: EntityOut;
  rank: number;
}

export interface Page<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

// The public URL for an entity. KIDs stay internal; slugs are the shareable handle.
export function entityHref(e: Pick<EntityOut, "module" | "type" | "slug">): string {
  return `/${e.module}/${encodeURIComponent(e.type)}/${e.slug}`;
}
