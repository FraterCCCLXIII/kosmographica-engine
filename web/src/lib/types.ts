// Mirrors the engine's read/audit API response models (engine/src/kge/api/schemas.py).

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

export interface VerificationOut {
  verifier: string;
  support_label: string;
  support_score: number;
  outcome: string;
  reason: string;
  created_at: string;
}

export interface ClaimAuditOut extends ClaimOut {
  about_label: string | null;
  verifications: VerificationOut[];
}

export interface EntityOut {
  id: string;
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

export interface AuditStats {
  claims_by_tier: Record<string, number>;
  entities_by_tier: Record<string, number>;
  claims_by_generator: { generator: string | null; tier: string; count: number }[];
  disputes: number;
}

export interface Page<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export interface ReconEntityOut {
  id: string;
  label: string;
  type: string;
  source_system: string | null;
  valid_from: number | null;
  valid_to: number | null;
}

export interface ReconciliationOut {
  id: number;
  left_kid: string;
  right_kid: string;
  left_source: string | null;
  right_source: string | null;
  match_method: "deterministic" | "scored" | "manual";
  score: number;
  status: "proposed" | "accepted" | "rejected";
  reason: string | null;
  created_at: string;
  decided_at: string | null;
  left: ReconEntityOut | null;
  right: ReconEntityOut | null;
}

export interface ReconciliationStats {
  by_status: Record<string, number>;
  by_method: Record<string, number>;
  total: number;
}

export interface SourceParityOut {
  source_system: string;
  entities: number;
  relationships: number;
  claims: number;
  entities_missing_external_id: number;
  converged: boolean;
}
