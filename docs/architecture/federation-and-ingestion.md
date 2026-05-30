# Federation & Ingestion Engine

> **Status:** stub / outline · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> The heart of "kosmographica-engine." Implements [core meta-model §6](../core-meta-model.md#6-federation--entity-resolution).

## Purpose

Specify the pipeline that pulls the existing source datasets into the canonical core **without
re-keying them**, reconciles entities, and keeps derived indexes in sync.

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

- [ ] Push (sources write to core) vs. pull (core ingests on schedule).
- [ ] Whether source systems remain live apps or become pure data feeds over time.
