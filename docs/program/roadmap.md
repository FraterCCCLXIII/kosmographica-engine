# Program Roadmap

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

A program-level, phased roadmap across the whole of Kosmographica — engine + federation + modules —
distinct from the Religion & Mythology module's internal roadmap (module §12).

## Phases

Architecture decisions are largely resolved (ADR-001..014). Remaining cross-cutting open items are
**ADR-003** (altitude scale) and **ADR-004** (Kosmotheon prose modeling), which gate Phase 4.

| Phase | Focus | Key outcomes |
|---|---|---|
| 0 | Core schema | Implement the generic schema (ADR-007) + contribution envelope + validator |
| 1 | Federation engine | `stage→validate→reconcile→load→index` pipeline; **Mythographica** ingested |
| 2 | Convergence | Sacred-Lineage, time-thread, Kosmotheon ingested with parity (incremental) |
| 3 | API + UI shell | REST API (ADR-014); Next.js shell + design system; entity pages + graph explorer |
| 4 | Developmental layer | Frameworks/stages populated; Developmental Lens (needs ADR-003 + ADR-004) |
| 5 | AI / RAG | GraphRAG retrieval + eval harness; **publish-then-verify** authoring live (ADR-013) |
| 6 | New modules | Philosophy & Science, Art & Culture, Polity & Society, Technology (via module skill) |
| 7 | Hardening | Sovereignty ops, security, licensing, NFRs, public launch |

**Lean sequencing:** go **depth-first on Religion & Mythology** through Phase 5 (prove the whole
stack end-to-end on one rich module) **before** breadth into new modules in Phase 6. This validates
the core/federation/AI loop on real data instead of spreading thin across half-built domains.

## Dependencies

- Phases 1–2 depend on the P0 architecture specs (now drafted) and the Phase 0 schema.
- Phase 4 depends on Kosmotheon ingestion (Phase 2) **and** ADR-003 (altitude) + ADR-004 (prose).
- Phase 5's verifier depends on the RAG retrieval built earlier in Phase 5.

## Key decisions / open questions

- [x] Module sequencing → **depth-first on Religion & Mythology through Phase 5**, then breadth.
