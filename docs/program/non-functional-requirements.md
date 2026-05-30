# Non-Functional Requirements

> **Status:** stub / outline · **Priority:** P2 · Part of the [spec plan](../PLAN.md).

## Purpose

Capture the quality attributes the system must meet — scale, performance, availability, and
operability — to size the architecture appropriately.

## Decided targets (v1)

Sized to validate the architecture, not to over-build. The single-Postgres lean stack (ADR-001/002)
comfortably covers v1 scale; the "deferred until forced" promotions exist for when these are exceeded.

### Scale

- **v1 target:** ~10⁴–10⁵ entities, ~10⁵–10⁶ claims/relationships (Religion & Mythology depth-first).
  Postgres + pgvector handle this on a single node.
- **Design ceiling:** schema + IDs (UUIDv7, generic table) must not preclude **10⁷+** entities; that
  scale is when graph DB / OpenSearch / external vector store promotions trigger.

### Performance budgets (p95)

| Operation | Budget |
| --- | --- |
| Entity page (SSG/ISR) | < 200 ms server render; cached edge serve |
| Graph traversal (depth ≤ 2, bounded) | < 500 ms |
| FTS / semantic search | < 400 ms |
| RAG answer (retrieval + synthesis) | < 5 s |
| Ingestion throughput | ≥ 100 records/s/worker (batch) |

### Availability & operability

Single-environment, single-region v1 (no HA requirement yet). **Daily backups** of Postgres with
tested restore; canonical is the source of truth so derived indexes (FTS/pgvector) are always
rebuildable. Observability: structured logs + basic metrics; the **bitemporal audit trail** (writes,
promotions, reconciliations) is a hard requirement from day one (it's the ADR-013 auditability story).

### Cost & portability

Watch the **embedding/LLM spend** (publish-then-verify runs author + independent verifier passes per
write) — budget per-batch and cache embeddings. Deploy via **Docker Compose on Coolify**
(Sacred-Lineage precedent); fully containerized for portability.

## Key decisions / open questions

- [x] Initial scale → **10⁴–10⁵ entities on single-node Postgres**, design ceiling 10⁷+.
