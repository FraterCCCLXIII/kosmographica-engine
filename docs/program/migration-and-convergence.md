# Migration & Convergence Plan

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

Define how the four existing repositories converge into the Kosmographica engine — in what order,
with what parity checks — without disrupting the apps that already work.

## Sections to detail

1. **Current-state inventory** — each source's data model, size, format, and loader:
   - Mythographica (Postgres assertions + expansion JSON)
   - Sacred-Lineage (Prisma/SQLite lineage data)
   - Kosmotheon (MkDocs prose: developmental frameworks/stages)
   - time-thread (timeline JSON / spreadsheet)
2. **Target mapping** — source → core schema mapping per system (extends core §6.3 table).
3. **Convergence order** — recommended: (a) stand up core + federation, (b) ingest Mythographica
   (already claim-shaped), (c) Sacred-Lineage lineages, (d) time-thread chronology, (e) Kosmotheon
   developmental layer.
4. **Parity & validation** — row-count/coverage parity per source (Sacred-Lineage `db:parity`
   precedent); reconciliation review before cutover.
5. **Coexistence strategy** — do source apps stay live (read-through) or get deprecated? Per system.
6. **Rollback & re-runnability** — idempotent imports; safe re-ingestion.

## Key decisions / open questions

- [ ] Big-bang vs. incremental convergence.
- [ ] Fate of each source app post-convergence (depends on canonical-store ADR).
