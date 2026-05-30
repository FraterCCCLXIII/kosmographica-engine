# System & Data Architecture

> **Status:** stub / outline · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> **Blocks:** federation, API, everything downstream. **Resolves:** core meta-model §10 Q1 & Q2.

## Purpose

Define how Kosmographica physically stores and serves the graph across a polystore, and **decide the
canonical store**: extend Mythographica's Postgres assertion store, or stand up a dedicated core DB
that all systems sync into.

## Sections to detail

1. **Architecture overview** — diagram of services and data flow (sources → engine → stores → API → UI).
2. **Canonical store decision** — options, trade-offs, recommendation. Push vs. pull reconciliation.
3. **Polystore roles & sync**
   - Relational (PostgreSQL) — canonical entities, claims, citations, reconciliation tables.
   - Graph (Neo4j / Neptune / ArangoDB) — traversal, motif/lineage queries, GraphRAG.
   - Vector (pgvector / Pinecone / Qdrant) — dense retrieval.
   - Search (Elasticsearch / Typesense) — full-text + faceted.
   - Object storage (S3/R2/GCS) — media, IIIF tiles.
   - Cache (Redis).
   - **Source of truth vs. derived indexes**; how derived stores are rebuilt from canonical.
4. **Consistency & sync model** — event log / CDC vs. batch reindex; eventual consistency boundaries.
5. **Bitemporal storage** — how valid-time vs. transaction-time is physically modeled (core §5).
6. **Deployment topology** — environments, hosting (note Sacred-Lineage uses Coolify + Docker).

## Existing assets to adopt

- Mythographica: FastAPI + Postgres assertion store, `seed_from_json.py`.
- Sacred-Lineage: Prisma schema, Dockerfile, Coolify deployment notes.

## Key decisions / open questions

- [ ] Canonical store (core §10 Q1).
- [ ] One graph with `module` labels vs. per-module namespaces (core §10 Q2).
- [ ] Which graph DB and which vector store.
