# API & Integration Contract

> **Status:** stub / outline · **Priority:** P0 · Part of the [spec plan](../PLAN.md).

## Purpose

Define the engine's external interface: how clients read/write the graph, how data is imported and
exported, and the query surface that powers the UI and GraphRAG.

## Sections to detail

1. **API style** — REST vs. GraphQL (or both: GraphQL for reads, REST for bulk import). Decide.
2. **Read endpoints** — entity fetch, relationship/claim expansion, comparative edges, developmental
   annotations, search, graph traversal (subgraph around an entity).
3. **Write endpoints** — entity/claim/relationship CRUD; bulk import (the MythGraph JSON contract);
   reconciliation proposals.
4. **Import/export contract** — adopt and generalize Mythographica's `{meta,nodes,edges}` JSON
   (`/import/json`, `/export/json`); JSON-LD / RDF export; IIIF manifests.
5. **Query surface for GraphRAG** — traversal + filter API the retrieval pipeline calls (see
   [../ai/rag-engineering.md](../ai/rag-engineering.md)).
6. **AuthN/AuthZ** — token model, scopes, restricted-content gating (see
   [../governance/security-and-access.md](../governance/security-and-access.md)).
7. **Versioning, pagination, errors, rate limits** — API conventions.
8. **SPARQL endpoint** — for linked-data consumers.

## Existing assets to adopt

- Mythographica M1 API: `GET /graph`, `/export/json`, `POST /import/json`, `/entities/{id}`,
  `/assertions?entity_id=`.

## Key decisions / open questions

- [ ] GraphQL vs. REST for the primary read API.
- [ ] Public read API vs. authenticated-only at launch.
