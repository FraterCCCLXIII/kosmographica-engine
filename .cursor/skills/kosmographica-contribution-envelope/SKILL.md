---
name: kosmographica-contribution-envelope
description: Produce or validate the Kosmographica contribution envelope ({meta, entities, relationships, claims, sources}) used to write all data. Use when authoring entities/claims/relationships, generating import data, or preparing AI-authored content for the ingestion pipeline.
---

# Kosmographica Contribution Envelope

Every write to Kosmographica — migration or authoring — is **one JSON envelope** that flows through
`stage → validate → reconcile → review → load → index`. Nothing writes to canonical Postgres directly.

## Read first (paths from the kosmographica repo root)

- `docs/architecture/federation-and-ingestion.md` — the envelope + pipeline (ADR-010).
- `docs/ai/ai-authoring-workflow.md` — grounded generation + trust tiers (ADR-013).
- `docs/governance/data-quality-validation.md` — the gate the envelope must pass.

## Envelope shape

```json
{
  "meta":   { "source_system": "...", "batch_id": "...", "generator": "human|model:<id>", "license": "..." },
  "entities":      [ { "external_id": "...", "module": "...", "type": "...", "label": "...", "data": {} } ],
  "relationships": [ { "subject": "...", "predicate": "...", "object": "...", "data": {} } ],
  "claims":        [ { "about": "...", "assertion": "...", "confidence": 0.0,
                       "sources": ["<source id>"], "support_spans": ["<verbatim quote>"] } ],
  "sources":       [ { "id": "...", "citation": "...", "uri": "..." } ]
}
```

## Non-negotiable rules

1. **Grounded generation only** — assert nothing you did not retrieve. Every `claim` carries the
   **exact `support_spans`** (verbatim text) from a real source in `sources`. No span → the claim
   stays `machine_unverified` and will not publish.
2. **Provenance** — medium/high-confidence claims and developmental readings **require** `sources`.
   Record `generator` (`human` or `model:<id>`).
3. **Confidence** — numeric `0.0–1.0`. Default cautious. Speculative links must be low.
4. **No conflation** — never equate linguistic cognate / functional parallel / syncretism; these are
   distinct relationship types, not one "similar to."
5. **Provenance stamping** — every entity carries `source_system` + `external_id` so loads are
   idempotent on `(source_system, external_id)`.
6. **Sacred/restricted (CARE / TK)** content must be flagged in `data` and never marked for
   auto-publish — it routes to community/expert review.

## Self-check before emitting

```text
- [ ] Every relationship/claim endpoint exists as an entity (by external_id)
- [ ] Every medium/high claim has sources AND verbatim support_spans
- [ ] confidence ∈ [0,1]; speculative = low
- [ ] No cognate/parallel/syncretism conflation
- [ ] source_system + external_id on every entity
- [ ] Sacred/restricted content flagged
```

Validate the JSON parses, then hand off to the pipeline — do not write canonical tables yourself.
