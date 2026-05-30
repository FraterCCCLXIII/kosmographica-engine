# Foundation Build Plan — Wave 1

> **Status:** active plan · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> The first wave of building: what to build, what to reuse, and in what order.

## Primary needs (recap)

| # | Capability | Spec | Build or reuse |
| --- | --- | --- | --- |
| 1 | Canonical data layer (generic `entities`/`relationships`/`claims`/`sources`) | [system-and-data-architecture](../architecture/system-and-data-architecture.md) | **build** (novel; no equivalent) |
| 2 | Contribution envelope + deterministic validator | [federation-and-ingestion](../architecture/federation-and-ingestion.md) | **build** |
| 3 | Ingestion pipeline + first source adapter (Mythographica) | federation-and-ingestion | **build** (reuse Mythographica `seed_from_json.py`) |
| 4 | Read API (REST/FastAPI) | [api-contract](../architecture/api-contract.md) | **build** (extend Mythographica API) |
| 5 | RAG retrieval + publish-then-verify verifier | [rag-engineering](../ai/rag-engineering.md), ADR-013 | **build** (Wave 2) |
| 6 | Encyclopedia + editorial UI, auth, permissions, search UX, AI widget | [app-architecture](../frontend/app-architecture.md), [design-system](../frontend/design-system.md) | **reuse — NextWiki** (see below) |
| 7 | Long-form prose / Article layer | core §, ADR-004 | **reuse — NextWiki pages** |

The **engine (1–5) has no off-the-shelf equivalent** — a claim graph with provenance, confidence,
reconciliation, comparative/developmental layers, and a verifier is exactly what general tools lack.
The **human layer (6–7) is largely solved** by existing wiki tooling.

## Build vs. reuse: NextWiki evaluation

[FraterCCCLXIII/NextWiki](https://github.com/FraterCCCLXIII/NextWiki) is our own MIT-licensed fork of a
WikiJS-inspired wiki. Stack: **Next.js 15, React 19, shadcn/ui, Tailwind, NextAuth, PostgreSQL,
Drizzle ORM, tRPC, Tiptap, Turborepo**, with **Postgres full-text + trigram fuzzy search** and an
**AI assistant/widget** (retrieval grounding, page-context awareness, **write-intent guards**).

### Fit matrix

| Strong fit (reuse) | Misfit / gap (don't force) |
| --- | --- |
| Next.js 15 + shadcn + Tailwind = our exact frontend stack (ADR-009, design-system) | Page/document model ≠ claim-based **entity graph** (our core) |
| NextAuth + group/granular permissions = our auth + roles→scopes (security-and-access) | TS backend (tRPC/Drizzle) ≠ our **Python FastAPI** engine + workers |
| Postgres FTS + trigram = our search decision (ADR-006) | No claims/confidence/provenance, no reconciliation, no federation |
| AI widget w/ retrieval grounding + write-intent guards ≈ our RAG chat + publish-then-verify UX | No comparative/developmental layers, no pgvector GraphRAG, no verifier |
| Tiptap editor, asset manager, themes, light/dark | Page tree/folders ≠ typed-relationship navigation |

### Recommendation — hybrid (ADR-015, proposed)

**Build the engine from scratch in Python; adopt NextWiki as the presentation + editorial + prose
layer**, integrated as an **API client to the FastAPI engine** (consistent with ADR-009).

- The FastAPI engine remains the **canonical source for all graph data** (entities/claims/…).
- NextWiki keeps its own tables only for **wiki-native concerns**: long-form Article/prose pages
  (this resolves **ADR-004** toward "linked Article records"), users/permissions, assets.
- Both share **one Postgres instance** (separate schemas) to stay near the lean footprint.
- NextWiki's AI widget is re-pointed at the engine's RAG + verifier endpoints.

This saves rebuilding auth, permissions, editor, asset manager, search UX, themes, and an AI widget —
all of which match our specs — while keeping the novel graph engine clean and Python-native.

**Leaner alternative (fallback):** if running a second (TS) app backend is unwanted, *harvest*
NextWiki's components (shadcn UI, Tiptap config, NextAuth setup, widget pattern) into a thin Next.js
client and drop its tRPC/Drizzle layer. More integration work, fewer moving parts. *Decide in ADR-015.*

## Wave 1 scope — engine spine (UI-decision-independent)

Start here regardless of the NextWiki decision; nothing downstream is coherent without it.

1. **Repo skeleton** — monorepo: `engine/` (Python, `uv`), `web/` reserved. CI lint/test.
2. **Canonical schema** — SQLAlchemy 2.0 models for generic `entities`/`relationships`/`claims`/
   `sources` (+ JSONB, `source_system`/`external_id`, bitemporal `recorded_at`); Alembic migration.
3. **Contribution envelope** — Pydantic v2 models for `{meta, entities, relationships, claims, sources}`.
4. **Deterministic validator** — structural + provenance + epistemic checks (data-quality §); the
   single source of truth the `kosmographica-contribution-envelope` skill calls.
5. **Mythographica adapter** — `{nodes,edges}` → envelope (reuse `seed_from_json.py`).
6. **Ingestion MVP** — `stage → validate → reconcile(external-id + exact) → load → index(FTS+pgvector)`.
7. **Read API MVP** — FastAPI `/v1/entities/{kid}`, `/graph`, `/search` (tier-aware).
8. **Seed end-to-end** — ingest real Mythographica data; prove the loop on one module.

**Deferred to later waves:** full RAG + verifier loop (Wave 2), NextWiki integration + editorial UI
(Wave 2), Sacred-Lineage/time-thread/Kosmotheon adapters (Wave 2–3), developmental lens (needs ADR-003/004).

## Open decisions

- [ ] **ADR-015 (proposed):** adopt NextWiki as the human layer (hybrid) vs. harvest-only thin client.
- [ ] Engine/corpus license + `kosmographica.org` domain (carried from licensing/IDs specs).
