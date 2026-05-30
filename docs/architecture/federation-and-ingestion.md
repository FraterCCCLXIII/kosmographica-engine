# Federation & Ingestion Engine

> **Status:** stub / outline · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> The heart of "kosmographica-engine." Implements [core meta-model §6](../core-meta-model.md#6-federation--entity-resolution).

## Purpose

Specify how the corpus gets **populated and kept correct** — both the one-time migration of existing
source datasets and the ongoing authoring of new content — through a single, auditable pipeline.

## Decided method (v1)

> Governing decisions: [ADR-010](../governance/decision-log.md) (one envelope + staging gate),
> [ADR-011](../governance/decision-log.md) (quarantine, not hard-fail),
> [ADR-012](../governance/decision-log.md) (no auto-accept for AI claims; trust tiers).

**Two inputs, one path.** Data enters either by **migration** (adapters read each source system) or by
**authoring** (AI agents + human editors). Both emit the *same* contribution envelope and flow through
the *same* gate — there is no direct write to canonical Postgres.

### The contribution envelope

One JSON artifact for every write (generalizes Mythographica's `{meta,nodes,edges}`):

```json
{
  "meta":   { "source_system": "...", "batch_id": "...", "generator": "human|model:<id>", "license": "..." },
  "entities":      [ { "external_id": "...", "module": "...", "type": "...", "label": "...", "data": { } } ],
  "relationships": [ { "subject": "...", "predicate": "...", "object": "...", "data": { } } ],
  "claims":        [ { "about": "...", "assertion": "...", "confidence": 0.0, "sources": ["..."] } ],
  "sources":       [ { "id": "...", "citation": "...", "uri": "..." } ]
}
```

### The pipeline

```text
 migration adapters ─┐
                     ├─▶ envelope ─▶ [1] STAGE ─▶ [2] VALIDATE ─▶ [3] RECONCILE ─▶ [4] REVIEW ─▶ [5] LOAD ─▶ [6] INDEX
 authoring (AI/human)┘                  │            │                                              │
                                    staging tbl   quarantine ◀── fails (ADR-011)            canonical Postgres
```

1. **Stage** — write the envelope to a `staging` table, untrusted, tagged with `batch_id` + generator.
2. **Validate** — automated gate (structural + epistemic + provenance, see
   [data-quality-validation.md](../governance/data-quality-validation.md)). Failures → **quarantine**
   with a machine-readable reason; the rest of the batch proceeds.
3. **Reconcile** — entity resolution against existing records: deterministic match on external IDs
   first, then candidate generation for fuzzy matches → merge/insert proposals
   (see [entity-resolution.md](./entity-resolution.md)).
4. **Review** — apply trust tiers (ADR-012): structural facts from trusted sources auto-pass at
   `machine_validated`; contestable claims, comparative edges, AI-authored content, and sacred/restricted
   (CARE/TK) material wait in a human-review queue.
5. **Load** — upsert approved records into canonical Postgres, stamping `source_system` + native id and
   bitemporal `recorded_at` (core §5). Idempotent on `(source_system, external_id)`.
6. **Index** — rebuild the derived FTS + pgvector indexes from canonical rows.

Every stage is **idempotent** and re-runnable from `staging`; a batch can be replayed without
duplication. This is deliberately a **pull/batch** model for v1 — no event bus, no push from sources.

## Sections to detail

1. **Pipeline stages** — `extract → normalize → reconcile → load → validate → index` (core §6.3).
   - Per-stage inputs/outputs, failure handling, idempotency.
2. **Source adapters** — one per source system:
   - Mythographica (`{meta,nodes,edges}` JSON; `seed_from_json.py`; `/import/json`).
   - Sacred-Lineage (Prisma/SQLite; `db:import-legacy`).
   - Kosmotheon (MkDocs markdown → prose + framework/stage extraction).
   - time-thread (timeline JSON → events + canonical chronology).
3. **Normalization** — field/key mapping to the core schema, camelCase↔snake_case, confidence
   reconciliation (core §3.2), enum coercion.
4. **Full vs. incremental sync** — replace vs. merge semantics; the enrichment/patch pattern
   (Mythographica's deep-merge overlays); dedupe by id.
5. **Reconciliation hand-off** — see [entity-resolution.md](./entity-resolution.md).
6. **Validation gate** — see [../governance/data-quality-validation.md](../governance/data-quality-validation.md).
7. **Indexing** — projection into graph + vector + search; rebuild strategy.
8. **Provenance** — stamping `source_system` + native id on every record; run/batch audit trail.
9. **Scheduling & orchestration** — manual, scheduled, or event-driven; observability.

## Existing assets to adopt

- Mythographica `normalize.py`, `expansion-manifest.json`, enrichment build scripts.
- Sacred-Lineage legacy import + parity check (`db:parity`).

## Key decisions / open questions

- [x] Push vs. pull → **pull/batch** for v1 (ADR-010); revisit if real-time sync is needed.
- [x] Single write path → **one envelope + staging gate** for migration *and* authoring (ADR-010).
- [ ] Whether source systems remain live apps or become pure data feeds over time.
