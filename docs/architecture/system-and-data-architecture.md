# System & Data Architecture

> **Status:** v1 decided (lean) · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> **Decisions recorded in:** [decision log](../governance/decision-log.md) ADR-001, 002, 006–009.

## Purpose

Define how Kosmographica stores and serves the graph. The v1 answer is deliberately small:
**one PostgreSQL database is the source of truth; everything else is optional and deferred.**

## Simplicity principle

Start with the fewest moving parts that deliver the product (wiki pages, structured ontology,
citations, AI search, RAG). Add a new service only when a concrete need forces it — and record that
need as an ADR. We do **not** stand up a graph DB, search cluster, or message queue on day one.

## v1 architecture (4 components)

```text
Sources (Mythographica, Sacred-Lineage, Kosmotheon, …)
        │  batch import scripts
        ▼
┌─────────────────────────────────────────┐
│ PostgreSQL  ← single source of truth     │
│   • entities / relationships / claims    │
│   • sources                              │
│   • FTS (tsvector + GIN)   [ADR-006]     │
│   • pgvector embeddings    [ADR-008]     │
└─────────────────────────────────────────┘
        ▲                         ▲
        │ SQLAlchemy              │
┌───────────────┐         ┌───────────────────┐
│ FastAPI (API) │◀────────│ Python workers     │
│  + RAG        │         │ (import / embed)   │
└───────────────┘         └───────────────────┘
        ▲
        │ HTTP (JSON)
┌──────────────────┐
│ Next.js encyclopedia UI  [ADR-009]        │
│  + client-only D3/timeline islands        │
└──────────────────┘

Object storage (S3/R2) — only when media archives are introduced.
```

That's it: **PostgreSQL + FastAPI + Python workers + Next.js.** No Redis, no Neo4j, no OpenSearch in v1.

## Canonical schema (generic, multi-module) — ADR-007

One polymorphic set of tables hosts every domain module. No per-type tables.

- **`entities`** — `id`, `module`, `type`, `subtype`, `label`, `source_system`, `source_id`,
  `data` (JSONB for type-specific fields), `valid_from` / `valid_to` (valid-time), timestamps.
- **`relationships`** — `id`, `subject_id`, `predicate`, `object_id`, `data` (JSONB), provenance.
- **`claims`** — atomic assertions (the unit that carries confidence + provenance), linked to the
  entity/relationship they describe. Confidence is numeric `0.0–1.0` with a derived band.
- **`sources`** — bibliographic/citation records referenced by claims.
- **`embeddings`** / RAG chunks — `pgvector` column(s) for semantic retrieval, rebuildable from above.

Type-specific access (e.g. "figures," "traditions") is provided via JSONB indexes and optional
materialized views — never via separate base tables.

## Source of truth vs. derived

PostgreSQL is canonical. FTS indexes and embeddings are **derived** and must be fully rebuildable
from the canonical rows by a worker job. No data lives only in a derived store.

## Federation (lean)

Ingestion is **pull, batch** for v1: import scripts read each source system (extending
Mythographica's `seed_from_json.py` pattern) and upsert into `entities`/`relationships`/`claims`,
stamping `source_system` + `source_id` for traceability. No event bus / CDC until real-time sync is
required. Detail in [federation & ingestion](./federation-and-ingestion.md).

## Deployment

Docker Compose: one Postgres container, one FastAPI container, one Next.js container; workers run as
one-off jobs / cron. Host on Coolify (matching Sacred-Lineage). Single environment to start.

## Existing assets to adopt

- **Mythographica:** FastAPI + Postgres assertion store, `seed_from_json.py` (import + claim model).
- **Sacred-Lineage:** Prisma schema as a reference ontology, Dockerfile, Coolify deployment notes.

## Explicitly deferred (add only when forced)

| Capability | v1 approach | Promote to | Trigger |
| --- | --- | --- | --- |
| Graph traversal | SQL recursive CTEs | Apache AGE → Neo4j | multi-hop queries too slow/complex in SQL |
| Full-text search | Postgres FTS | OpenSearch | need fuzzy / faceted / multilingual at scale |
| Vector search | pgvector | Qdrant / Pinecone | embedding volume outgrows Postgres |
| Async jobs | inline / cron | Redis + Celery/RQ | ingestion/embedding needs real async |
| Media | (none) | S3/R2 + IIIF | media archives introduced |
| Caching | (none) | Redis | measured read hotspots |

## Open questions

- [ ] Altitude scale (core §10 Q3) — see ADR-003.
- [ ] Kosmotheon prose modeling (core §10 Q4) — see ADR-004.
