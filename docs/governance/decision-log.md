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

## ADR-010: One contribution envelope + a staging gate for every write

- **Date:** 2026-05-30
- **Status:** accepted
- **Context:** Two ways data enters the corpus — **migration** from source systems (Mythographica,
  Sacred-Lineage, Kosmotheon, time-thread) and **ongoing authoring** (AI agents + human editors).
  Building two separate write paths would double the validation surface.
- **Decision:** Both paths converge on **one JSON contribution envelope**
  (`{meta, entities, relationships, claims, sources}`, generalizing Mythographica's `{meta,nodes,edges}`)
  and **one pipeline**: `stage → validate → reconcile → review → load → index`. Nothing is written
  directly to canonical Postgres; everything lands in a `staging` area first.
- **Consequences:** Single validation/reconciliation/provenance implementation. Migration adapters
  just emit the envelope. Detail in [federation & ingestion](../architecture/federation-and-ingestion.md).

## ADR-011: Validation failures quarantine, never silently drop

- **Date:** 2026-05-30
- **Status:** accepted
- **Context:** "Hard-fail vs. quarantine" for records that fail validation.
- **Decision:** **Quarantine.** A failing record moves to a quarantine table with a machine-readable
  reason; the rest of its batch still loads (partial success). Structural errors block that one
  record; epistemic issues (e.g. high confidence without a source) may pass **only** by being
  down-ranked to low confidence and flagged. No silent drops, no all-or-nothing batches.
- **Consequences:** Ingestion is resumable and auditable; a quarantine queue must be triaged.

## ADR-012: No auto-accept for AI-authored claims; provenance trust tiers

- **Date:** 2026-05-30
- **Status:** superseded by ADR-013 (trust tiers retained; the human-pre-gate is replaced by an
  automated verifier + post-hoc audit)
- **Context:** Population is largely AI-assisted; we need to keep the corpus trustworthy without a
  human in front of every structural fact.
- **Decision:** Every record carries a **trust tier**:
  `machine_unverified → machine_validated → human_reviewed → expert_endorsed`. Deterministic
  **structural** facts from a trusted source (an entity exists; it has external ID X) may auto-load at
  `machine_validated`. Every **contestable claim or comparative edge** — and anything AI-authored —
  requires human review before it reaches `human_reviewed`; sacred/restricted material (CARE/TK)
  requires community/expert review. Public default surfaces `human_reviewed`+ ; lower tiers are
  visible only with an explicit "unverified" filter.
- **Consequences:** Bounded human-review load (claims, not every node) with a clear trust signal that
  also drives RAG eligibility and public visibility.

## ADR-013: Publish-then-verify — AI writes to canonical, gated by an automated verifier

- **Date:** 2026-05-30
- **Status:** accepted (supersedes ADR-012)
- **Context:** We want a Grokipedia-style model where AI **writes directly to the canonical database**
  at scale, without a human in front of every write — but the corpus must stay auditable and
  trustworthy. ADR-012's human-pre-gate does not scale to encyclopedic coverage.
- **Decision:** Flip from *verify-then-publish* to **publish-then-verify**. Keep the ADR-012 trust
  tiers; change *who/what* gates and *what* the gate controls — **visibility, not the write**:
  1. **Grounded generation only** — an agent may not assert what it didn't retrieve; every claim
     carries the exact supporting source span(s).
  2. **Automated verifier (no human in the loop)** — an independent model + deterministic checks run
     an **entailment check** (does the cited source actually support the claim?) plus the ADR-011
     structural/provenance gate. The support score *becomes* the claim's confidence.
  3. **Direct write, append-only & bitemporal** — verified writes land in canonical immediately at a
     `machine_*` tier; writes **supersede, never overwrite** (core §5), so every AI write is
     reversible and fully auditable.
  4. **Contradiction → dispute, not overwrite** — a conflicting claim opens a dispute; both coexist
     with provenance (no AI edit wars).
  5. **Continuous re-verification** — a scheduled job re-checks claims, recomputes confidence, decays
     stale ones, and flags drift for human spot-audit.
  6. **Humans move to post-hoc audit** — they review *flagged / disputed / low-confidence /
     high-traffic* records and promote to `human_reviewed` / `expert_endorsed`, rather than gating
     every write.
- **Carve-out (non-negotiable):** sacred/restricted material (CARE / TK Labels) **retains the
  pre-publication community/expert gate** — no AI auto-publish.
- **Visibility:** `machine_validated` content is **public but badged** ("AI-generated, unreviewed,
  N sources") with its confidence shown; `machine_unverified` is hidden.
- **Auditability (the payoff):** because every record stores `tier + generator + verifier record +
  sources + bitemporal history`, auditing is a query — e.g. *all `machine_validated`,
  not-yet-`human_reviewed` claims by model X in batch Y* — and any bad write is one supersede away
  from rollback.
- **Consequences:** Scales to AI-driven population; humans audit exceptions, not everything. Cost:
  `machine_validated` content will contain residual errors (hence the mandatory public badge), and
  the **verifier's entailment quality becomes a critical dependency** needing its own eval suite
  (see [rag-engineering.md](../ai/rag-engineering.md)).

## ADR-014: Primary API = REST/JSON; defer GraphQL and SPARQL

- **Date:** 2026-05-30
- **Status:** accepted
- **Context:** The original core question "GraphQL vs. REST" for the read API.
- **Decision:** **REST/JSON over FastAPI**, versioned `/v1`, with `expand=` params for layer loading
  and an `/entities/{kid}/graph` route for bounded subgraph traversal. GraphQL and a SPARQL endpoint
  are deferred (RDF/JSON-LD export covers linked-data needs in v1).
- **Consequences:** Simple client + OpenAPI tooling; deep client-shaped queries wait for GraphQL if a
  real need appears. Detail in [api-contract.md](../architecture/api-contract.md).

## ADR-015: Reuse NextWiki for the human layer; build the engine from scratch

- **Date:** 2026-05-30
- **Status:** **proposed** (needs owner sign-off)
- **Context:** Whether to build the encyclopedia/editorial UI from scratch or reuse an existing wiki.
  [FraterCCCLXIII/NextWiki](https://github.com/FraterCCCLXIII/NextWiki) is our own MIT fork: Next.js
  15 + shadcn + Tailwind + NextAuth + Postgres FTS + an AI widget — matching our frontend specs
  (ADR-006, ADR-009, design-system, security-and-access) almost exactly. But it is a **page/document
  wiki**, not a claim-based entity graph, and its backend is TS (tRPC/Drizzle), not our Python engine.
- **Decision (proposed):** **Hybrid.** Build the canonical graph engine from scratch in
  Python/FastAPI (no equivalent exists). Adopt NextWiki as the **presentation + editorial + prose**
  layer, integrated as an **API client to the engine** (per ADR-009): NextWiki serves long-form
  Article/prose pages (resolving ADR-004), users/permissions, and assets, and re-points its AI widget
  at the engine's RAG/verifier; both share one Postgres (separate schemas). Fallback: harvest
  NextWiki components into a thin client and drop its tRPC/Drizzle backend.
- **Consequences:** Saves rebuilding auth/permissions/editor/search/AI-widget; costs a second (TS) app
  backend alongside FastAPI. Engine work (Wave 1) does not depend on this and can start immediately.
  Detail in [foundation-build-plan.md](../program/foundation-build-plan.md).

---

## Still open

- **ADR-003 (open): Altitude scale** — adopt Wilber colors vs. neutral Kosmographica scale.
- **ADR-004 (open): Kosmotheon prose** — structured entities vs. linked `Article` records.
- **ADR-005 (open): Background jobs** — start with synchronous/inline processing; add Redis + a queue
  (Celery/RQ) only when ingestion/embedding workloads require async. *(Lean default: defer.)*
