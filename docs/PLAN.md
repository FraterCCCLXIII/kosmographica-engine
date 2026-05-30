# Kosmographica — Documentation & Specification Plan

> The master index of specs that guide building Kosmographica. Each entry links to its document and
> tracks status and build order. Documents marked **stub** are outlines to be filled in iteratively.
>
> **Status:** active · **Date:** 2026-05-30

---

## How to read this

Kosmographica is built in two conceptual halves:

- **What the data is** — the conceptual model and domain ontologies. *(Mostly done.)*
- **How it is built and run** — architecture, federation engine, APIs, governance, AI, UI, ops.
  *(Mostly to do — scaffolded here.)*

Build order is driven by dependency: nothing downstream is coherent until the **canonical-store**
and **federation** decisions are made, so the architecture docs are P0.

---

## Document set

### Foundation (done)

| Doc | Purpose | Status |
|---|---|---|
| [`core-meta-model.md`](./core-meta-model.md) | Universal core: entity/claim/relationship model, developmental layer, temporal layer, federation, modules, vocabulary, standards/ethics | ✅ draft |
| [`modules/religion-mythology.md`](./modules/religion-mythology.md) | First domain module (World Religion & Mythology), conforming to the core | ✅ draft |
| [`glossary.md`](./glossary.md) | Shared internal terminology (KID, altitude, assertion, module, …) | stub |

### P0 — Architecture (before engine code)

| Doc | Purpose | Status |
|---|---|---|
| [`architecture/system-and-data-architecture.md`](./architecture/system-and-data-architecture.md) | Polystore wiring; **resolves the canonical-store decision** (core §10 Q1) | ✅ draft |
| [`architecture/federation-and-ingestion.md`](./architecture/federation-and-ingestion.md) | The ETL engine: extract→normalize→reconcile→load→validate→index | ✅ draft |
| [`architecture/entity-resolution.md`](./architecture/entity-resolution.md) | How two nodes become one: match features, thresholds, `sameAs` lifecycle, merge/split | ✅ draft |
| [`architecture/identifiers-and-versioning.md`](./architecture/identifiers-and-versioning.md) | KID minting, URI resolution, entity merge/split, schema versioning | ✅ draft |
| [`architecture/api-contract.md`](./architecture/api-contract.md) | Read/write API, import/export contract, query surface for UI + GraphRAG | ✅ draft |
| [`modules/module-authoring-guide.md`](./modules/module-authoring-guide.md) | How to write a conforming domain module (template + rules) | ✅ draft |

### P1 — Governance, AI, and UI (before/while populating data)

| Doc | Purpose | Status |
|---|---|---|
| [`governance/controlled-vocabulary.md`](./governance/controlled-vocabulary.md) | Fresh SKOS scheme, relation-type registry, term-addition quality bar | ✅ draft |
| [`governance/data-quality-validation.md`](./governance/data-quality-validation.md) | Validation rules, quality gates, automated audits | ✅ draft |
| [`ai/rag-engineering.md`](./ai/rag-engineering.md) | Chunking pipeline, embeddings, GraphRAG traversal, guardrails, eval harness | ✅ draft |
| [`ai/ai-authoring-workflow.md`](./ai/ai-authoring-workflow.md) | How agents propose entities/claims; validation + human review gates | ✅ draft |
| [`frontend/design-system.md`](./frontend/design-system.md) | Design tokens + components for the engine UI (adopt Sacred-Lineage tokens) | ✅ draft |
| [`frontend/app-architecture.md`](./frontend/app-architecture.md) | Frontend architecture, routing, state, view composition | ✅ draft |
| [`governance/ethics-and-sovereignty.md`](./governance/ethics-and-sovereignty.md) | Restricted/sacred-content flags, access tiers, TK Label workflow | ✅ draft |
| [`program/migration-and-convergence.md`](./program/migration-and-convergence.md) | How the 4 existing repos converge into the engine, with parity checks | ✅ draft |

### P2 — Hardening & completeness

| Doc | Purpose | Status |
|---|---|---|
| [`modules/philosophy-science.md`](./modules/philosophy-science.md) | Domain module (stub) | stub |
| [`modules/art-culture.md`](./modules/art-culture.md) | Domain module (stub) | stub |
| [`modules/polity-society.md`](./modules/polity-society.md) | Domain module (stub) | stub |
| [`modules/technology.md`](./modules/technology.md) | Domain module (stub) | stub |
| [`governance/licensing-and-rights.md`](./governance/licensing-and-rights.md) | Corpus license, source-license propagation, image/IIIF rights | ✅ draft (owner sign-off) |
| [`governance/security-and-access.md`](./governance/security-and-access.md) | Auth, roles, access control (technical counterpart to editorial roles) | ✅ draft |
| [`governance/decision-log.md`](./governance/decision-log.md) | ADRs — records resolutions of open questions and architectural calls | ✅ active |
| [`program/non-functional-requirements.md`](./program/non-functional-requirements.md) | Scale, performance, availability, backup | ✅ draft |
| [`program/evaluation-metrics.md`](./program/evaluation-metrics.md) | Coverage, claim/source ratios, reconciliation precision, RAG quality | ✅ draft |
| [`program/roadmap.md`](./program/roadmap.md) | Program-level phased roadmap across all modules and the engine | ✅ draft |
| [`program/foundation-build-plan.md`](./program/foundation-build-plan.md) | Wave 1 build plan; build-vs-reuse (NextWiki) decision | ✅ shipped |
| [`program/wave-2-build-plan.md`](./program/wave-2-build-plan.md) | Wave 2: real author/verifier + evals, Sacred-Lineage federation + reconciliation, re-verify worker, CI | ✅ shipped |

---

## Existing assets to adopt (don't re-spec)

| Asset | Repo | Adopt for |
|---|---|---|
| `ai-data-format.md` (MythGraph JSON) | Mythographica | ingestion contract, AI authoring |
| `comparative-methodology.md` | Mythographica | vocabulary governance, epistemic rules |
| `seed_from_json.py`, `validate_graph.py`, `audit_graph_quality.py` | Mythographica | ingestion + data quality |
| `prisma/schema.prisma`, `db:import-legacy`, auth models | Sacred-Lineage | data model, migration, security |
| `DESIGN.md` (warm-canvas token system) | Sacred-Lineage | design system |
| timeline JSON + World History Timeline | time-thread | temporal spine, migration |
| developmental content (AQAL, SD, Gebser, Wilber–Combs) | Kosmotheon | developmental layer population |

---

## Open questions to resolve (tracked in `governance/decision-log.md`)

Carried from [`core-meta-model.md`](./core-meta-model.md) §10:

1. Canonical store: extend Mythographica's Postgres, or a dedicated core DB? *(blocks P0 architecture)*
2. One graph with `module` labels, or per-module namespaces?
3. Canonical `altitude` scale: adopt an existing one (Wilber colors) or define a neutral scale?
4. How much of Kosmotheon's prose becomes structured entities vs. linked `Article` records?
