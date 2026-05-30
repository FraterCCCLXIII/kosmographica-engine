---
name: kosmographica-source-adapter
description: Write a migration/source adapter that reads an existing source system (Mythographica, Sacred-Lineage, Kosmotheon, time-thread) and emits the Kosmographica contribution envelope without re-keying. Use when migrating or ingesting a source dataset into the canonical core.
---

# Kosmographica Source Adapter

An adapter is the `extract → normalize` front of the ingestion pipeline. It **reads one source system
and emits contribution envelopes** — it never writes canonical tables and never re-keys data.

## Read first (paths from the kosmographica repo root)

- `docs/architecture/federation-and-ingestion.md` — pipeline + per-source notes.
- `docs/architecture/entity-resolution.md` — the reconcile step the adapter feeds.
- Use the `kosmographica-contribution-envelope` skill for the output format.

## Rules

1. **Pull / batch** — read the source on demand; no push, no event bus (v1).
2. **Preserve native ids** — stamp `source_system` + the source's native id as `external_id` on every
   entity. Loads are idempotent on `(source_system, external_id)`; re-running must not duplicate.
3. **Map, don't invent** — map source fields to the core schema (camelCase↔snake_case, enum coercion).
   Put type-specific fields in `entity.data` (JSONB). Do not fabricate confidence or sources.
4. **Confidence reconciliation** — convert source confidence to numeric `0.0–1.0`; if the source has
   only a band/string, map it to a representative numeric value and record the original.
5. **Emit, then hand off** — output envelopes; let `validate → reconcile → review → load → index` run.

## Known sources

- **Mythographica** — `{meta, nodes, edges}` JSON; node `type` (deity/hero/…), edges are assertions
  with numeric confidence + sources. Map nodes→entities, edges→relationships+claims.
- **Sacred-Lineage** — Prisma/Postgres; `Figure`, `Concept`, `Text`, `Practice`, `Institution`,
  `Place`, `TransmissionRelationship`, `EntityLink` (polymorphic, carries `certainty`+`citation`).
- **Kosmotheon** — MkDocs markdown; extract prose articles + framework/stage entities.
- **time-thread** — timeline JSON → events + canonical chronology.

## Self-check

```text
- [ ] source_system + external_id on every entity; re-run is idempotent
- [ ] confidence numeric; original band preserved in data
- [ ] no canonical writes — only envelopes emitted
- [ ] endpoints resolvable for every relationship/claim
```
