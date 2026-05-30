# Program Roadmap

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

A program-level, phased roadmap across the whole of Kosmographica — engine + federation + modules —
distinct from the Religion & Mythology module's internal roadmap (module §12).

## Proposed phases (to refine)

| Phase | Focus | Key outcomes |
|---|---|---|
| 0 | Decisions & core | Resolve ADR-001..005; finalize core schema; canonical store stood up |
| 1 | Federation engine | Ingestion pipeline + entity resolution + validation; Mythographica ingested |
| 2 | Convergence | Sacred-Lineage, time-thread, Kosmotheon ingested with parity |
| 3 | API + UI shell | Read/write API; app architecture + design system; graph explorer |
| 4 | Developmental layer | Frameworks/stages populated; Developmental Lens view |
| 5 | AI / RAG | GraphRAG retrieval + eval harness; AI authoring workflow live |
| 6 | New modules | Philosophy & Science, Art & Culture, Polity & Society, Technology |
| 7 | Hardening | Sovereignty ops, security, licensing, NFRs, public launch |

## Dependencies

- Phases 1–2 depend on the P0 architecture docs.
- Phase 4 depends on Kosmotheon ingestion (Phase 2) + altitude-scale decision (ADR-003).

## Key decisions / open questions

- [ ] Sequencing of new modules vs. depth-first on Religion & Mythology.
