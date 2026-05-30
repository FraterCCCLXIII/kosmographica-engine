# Foundation Build Plan — Wave 1

> **Status:** Wave 1 **shipped** (1a engine spine · 1b AI write loop · 1c read-only Audit Console) ·
> **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> The first wave of building: what to build, what to reuse, and in what order.

## What shipped (code lives in [`engine/`](../../engine) and [`web/`](../../web))

| Wave | Delivered | Where |
| --- | --- | --- |
| **1a** | Engine spine: canonical schema (generic entity, trust tiers, bitemporal), KID/UUIDv7, contribution envelope, deterministic validator, Mythographica adapter, ingestion pipeline (`stage→validate→reconcile→load→index`), tier-aware read+audit API, `kge` CLI. Seeded the real **244 entities / 354 relationships / 597 claims / 139 sources** end-to-end (idempotent). | `engine/src/kge/{models,envelope,validation,adapters,pipeline,api,cli}` |
| **1b** | AI **publish-then-verify** loop (ADR-013): grounded authoring contract + offline `SentenceAuthor`, independent verifier (anti-fabrication + lexical entailment → confidence → route), `verifications` audit table, `reverify()`. | `engine/src/kge/{authoring,verify}.py` |
| **1c** | **Read-only Audit Console** (Next.js 16, App Router, Tailwind tokens): Overview, AI-validated queue, Disputes, Entity view, Claim verification detail. Typed read-only API client. | `web/src/{app,components,lib}` |

Tests: 34 (pytest, incl. DB-backed pipeline/API/write-loop against an isolated `kosmographica_test` DB).
Run: `cd engine && docker compose up -d db && uv run alembic upgrade head && uv run pytest`.

The **human editorial/authoring layer (NextWiki) stays deferred** — for v1 the AI is the only writer
(publish-then-verify) and humans **observe** through the Audit Console.

## Primary needs (recap)

| # | Capability | Spec | Build or reuse |
| --- | --- | --- | --- |
| 1 | Canonical data layer (generic `entities`/`relationships`/`claims`/`sources`) | [system-and-data-architecture](../architecture/system-and-data-architecture.md) | **build** (novel; no equivalent) |
| 2 | Contribution envelope + deterministic validator | [federation-and-ingestion](../architecture/federation-and-ingestion.md) | **build** |
| 3 | Ingestion pipeline + first source adapter (Mythographica) | federation-and-ingestion | **build** (reuse Mythographica `seed_from_json.py`) |
| 4 | Read API (REST/FastAPI) | [api-contract](../architecture/api-contract.md) | **build** (extend Mythographica API) |
| 5 | RAG retrieval + publish-then-verify verifier | [rag-engineering](../ai/rag-engineering.md), ADR-013 | **built (1b, MVP)** — verifier loop done; RAG retrieval + LLM author/verifier in Wave 2 |
| 6 | Encyclopedia + editorial UI, auth, permissions, search UX, AI widget | [app-architecture](../frontend/app-architecture.md), [design-system](../frontend/design-system.md) | **read-only Audit Console built (1c)**; full editorial UI **reuse — NextWiki** (deferred, see below) |
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

## Wave 1 scope — engine spine (UI-decision-independent) — DONE

Started here regardless of the NextWiki decision; nothing downstream is coherent without it.

- [x] **Repo skeleton** — monorepo: `engine/` (Python, `uv`), `web/` (Next.js). Postgres+pgvector compose.
- [x] **Canonical schema** — SQLAlchemy 2.0 generic `entities`/`relationships`/`claims`/`sources`
  (+ JSONB, `source_system`/`external_id`, trust tiers, bitemporal `recorded_at`); Alembic migrations.
- [x] **Contribution envelope** — Pydantic v2 `{meta, sources, entities, relationships, claims}` with
  `support_spans` and a `requires_grounding` mode.
- [x] **Deterministic validator** — structural + provenance + epistemic checks; quarantine on failure.
- [x] **Mythographica adapter** — `{nodes,edges}` → envelope.
- [x] **Ingestion MVP** — `stage → validate → reconcile(external-id) → load → index(FTS+pgvector)`, idempotent.
- [x] **Read API MVP** — FastAPI `/v1/entities/{kid}`, `/graph`, `/search`, `/v1/audit/*` (tier-aware).
- [x] **Seed end-to-end** — ingested the real Mythographica starter; verified via API/SQL/console.
- [x] **AI write loop (1b)** + **read-only Audit Console (1c)** (see "What shipped").

**Deferred to later waves:** real RAG retrieval + LLM-backed author/verifier (the current verifier is a
deterministic lexical stand-in); NextWiki integration + full editorial UI; Sacred-Lineage / time-thread /
Kosmotheon adapters; developmental lens (needs ADR-003/004); CI; embedding population for semantic search.

## Open decisions

- [ ] **ADR-015 (proposed):** adopt NextWiki as the human editorial layer (hybrid) vs. harvest-only thin
  client. *Not blocking* — Wave 1c shipped a from-scratch read-only console; this decision only governs the
  future **write/editorial** layer.
- [ ] Engine/corpus license + `kosmographica.org` domain (carried from licensing/IDs specs).
- [ ] Swap the lexical verifier for an NLI/LLM entailment model + eval suite (rag-engineering.md).
