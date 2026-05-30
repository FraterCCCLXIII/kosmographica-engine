# API & Integration Contract

> **Status:** stub / outline · **Priority:** P0 · Part of the [spec plan](../PLAN.md).

## Purpose

Define the engine's external interface: how clients read/write the graph, how data is imported and
exported, and the query surface that powers the UI and GraphRAG.

## Decided method (v1)

**REST/JSON over FastAPI** (ADR-014). GraphQL is deferred — the read patterns (entity + bounded
subgraph expansion) are well served by a few REST endpoints with `expand` params, and REST keeps the
client and OpenAPI tooling simple. Versioned under `/v1`.

### Read endpoints

| Endpoint | Returns |
| --- | --- |
| `GET /v1/entities/{kid}?expand=relationships,claims,comparative,developmental` | one entity + chosen layers |
| `GET /v1/entities/{kid}/graph?depth=1&edge_types=...` | bounded subgraph (recursive CTE; capped depth) |
| `GET /v1/claims?about={kid}` | claims about an entity, with sources + confidence + tier |
| `GET /v1/search?q=&module=&type=&tier=` | FTS + filters (Postgres FTS, ADR-006) |
| `GET /v1/search/semantic?q=` | pgvector similarity (ADR-008) |

All read responses carry each record's **trust tier + confidence** so clients can badge/filter
(ADR-013). Default public reads return `human_reviewed`+ unless `?tier=` opts into lower tiers.

### Write endpoints

Writes go **through the pipeline, not direct table CRUD**:

- `POST /v1/contributions` — submit a **contribution envelope** (ADR-010); returns a `batch_id`.
- `GET /v1/contributions/{batch_id}` — staging/validation/quarantine status.
- `POST /v1/reconciliations/{id}:accept|reject` — adjudicate a `sameAs` proposal (review role).

### Import / export

- **Import:** the contribution envelope (`POST /v1/contributions`) is the single ingress; the legacy
  Mythographica `{meta,nodes,edges}` shape is accepted via the source adapter, not a separate route.
- **Export:** `GET /v1/export?module=&format=jsonld|rdf|json` for linked-data + bulk; IIIF manifests
  for media when that layer exists.

### GraphRAG query surface

The retrieval pipeline ([../ai/rag-engineering.md](../ai/rag-engineering.md)) calls the same
`/entities/{kid}/graph` traversal + `/search/semantic` internally — no separate private API.

### Conventions

- **Auth:** bearer tokens with scopes; restricted/sacred content gated server-side
  ([../governance/security-and-access.md](../governance/security-and-access.md)). Public read is
  unauthenticated for `human_reviewed`+ content; writes always authenticated.
- **Pagination:** cursor-based. **Errors:** RFC 9457 problem+json. **Rate limits:** per-token.
- **SPARQL endpoint:** deferred (RDF export covers v1 linked-data needs).

## Existing assets to adopt

- Mythographica M1 API: `GET /graph`, `/export/json`, `POST /import/json`, `/entities/{id}`,
  `/assertions?entity_id=` — generalized into the routes above.

## Key decisions / open questions

- [x] API style → **REST/JSON (ADR-014)**; GraphQL + SPARQL deferred.
- [ ] Public-read vs. authenticated-only at launch (ties to security-and-access).
