# Decision Log (ADRs)

> **Status:** active log · **Priority:** P2 (ongoing) · Part of the [spec plan](../PLAN.md).

Architecture Decision Records. Each entry captures a significant decision, its context, the options
considered, and the resolution. Append-only; supersede rather than edit.

## Template

```
## ADR-NNN: <title>
- Date:
- Status: proposed | accepted | superseded by ADR-MMM
- Context:
- Options considered:
- Decision:
- Consequences:
```

## Guiding principle

**Start simple. Add services only when a real need forces it.** v1 runs on the fewest moving parts
that deliver wiki pages, structured ontology, citations, AI search, and RAG. Graph DB, dedicated
search cluster, and message queues are deferred until they earn their place.

---

## ADR-001: Canonical store = PostgreSQL

- **Date:** 2026-05-30
- **Status:** accepted
- **Context:** Need one source of truth for entities, claims, relationships, sources. Mythographica
  already runs FastAPI + PostgreSQL + SQLAlchemy with an assertion model.
- **Options:** extend Mythographica's Postgres vs. a new dedicated core DB.
- **Decision:** PostgreSQL is the single source of truth, building on the existing Postgres base.
  All other stores are **derived indexes** rebuilt from it.
- **Consequences:** Lowest-risk, not greenfield. Derived stores must be reproducible from Postgres.

## ADR-002: One Postgres database, `module` column — no separate graph DB in v1

- **Date:** 2026-05-30
- **Status:** accepted
- **Context:** "One graph with module labels vs. per-module namespaces," and whether to run Neo4j.
- **Decision:** One relational schema; entities carry a `module` column. **Graph traversal uses SQL
  recursive CTEs** for v1 (lineage chains, ancestry). **No Neo4j until** traversal needs genuinely
  exceed SQL (then consider Apache AGE in-Postgres before a separate graph DB).
- **Consequences:** Avoids a second datastore. Revisit if deep multi-hop queries become painful.

## ADR-006: Search via Postgres FTS in v1 — defer OpenSearch

- **Date:** 2026-05-30
- **Status:** accepted
- **Context:** Full-text + faceted search. OpenSearch is powerful but a heavy JVM service to operate.
- **Decision:** Use Postgres native FTS (`tsvector`/GIN) + `pgvector` for v1. Add OpenSearch only
  when fuzzy/faceted/multilingual search outgrows Postgres FTS.
- **Consequences:** Fewer services. Search features constrained to Postgres FTS until promoted.

## ADR-007: Generic entity model (no per-type tables)

- **Date:** 2026-05-30
- **Status:** accepted
- **Context:** A tempting design uses tables like `figures`, `traditions`, `texts`. That hardcodes the
  Religion & Mythology module and breaks the multi-module "total record" vision.
- **Decision:** A polymorphic **`entities`** table with `module`, `type`, `subtype`, and a **JSONB**
  column for type-specific fields; generic `relationships`, `claims`, `sources`. `figure`,
  `tradition`, etc. are `type` values (optionally materialized views), not base tables.
- **Consequences:** One schema hosts all modules. Type-specific querying via JSONB/indexes or views.

## ADR-008: Retrieval store = pgvector in v1

- **Date:** 2026-05-30
- **Status:** accepted
- **Context:** Semantic search/RAG vector store.
- **Decision:** Use `pgvector` inside Postgres for v1. Promote to Qdrant/Pinecone only at scale.
- **Consequences:** Keeps embeddings co-located with canonical data; one fewer service.

## ADR-009: Frontend = Next.js (encyclopedia UI)

- **Date:** 2026-05-30
- **Status:** accepted
- **Context:** Public, crawlable encyclopedia is a primary surface; SSG/ISR benefits SEO + first paint.
- **Decision:** Next.js for the encyclopedia UI, talking to FastAPI as a pure API client. Heavy
  interactive tools (D3 graph, timeline) run as client-only islands (ported from the existing Vite apps).
- **Consequences:** Gain SEO/SSG; accept that Next's server/DB features go unused (backend is Python),
  and that Mythographica/time-thread Vite components need porting.

---

## Still open

- **ADR-003 (open): Altitude scale** — adopt Wilber colors vs. neutral Kosmographica scale.
- **ADR-004 (open): Kosmotheon prose** — structured entities vs. linked `Article` records.
- **ADR-005 (open): Background jobs** — start with synchronous/inline processing; add Redis + a queue
  (Celery/RQ) only when ingestion/embedding workloads require async. *(Lean default: defer.)*
