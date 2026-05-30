# Frontend / Application Architecture

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

Define the engine's web application architecture: framework, routing, data fetching, state, and how
the views from the module's information architecture are composed.

## Decided method (v1)

**One unified Next.js app** (ADR-009), TypeScript throughout, talking to FastAPI as a pure API client
([../architecture/api-contract.md](../architecture/api-contract.md)). Not federated micro-frontends —
a single app keeps navigation, auth, and the design system coherent; the existing Vite apps'
components are **ported in**, not embedded.

### Rendering strategy

- **Encyclopedia/entity/search pages → SSG/ISR** — crawlable, fast first paint (the SEO rationale for
  Next, ADR-009). Server components fetch from the API at build/revalidate time.
- **Interactive tools → client-only islands** — Graph Explorer, Lineage Builder, Comparison View,
  Comparative Mapping Engine, Developmental Lens, Timeline Explorer, RAG Chat. These hydrate on the
  client and stream from the API.

### Routing & URLs

Shareable, bookmarkable URLs (time-thread precedent): `/{module}/{type}/{slug-or-kid}` for entities,
plus `/graph`, `/compare`, `/timeline`, `/lens`, `/search`, `/chat`. Tool state lives in query params
so views are linkable.

### Data layer

Typed API client generated from the OpenAPI spec; server-component fetches for SSG/ISR pages, a
client cache (TanStack Query) for islands. **Every rendered record shows its trust tier + confidence
badge** (ADR-013) — the UI is the place the publish-then-verify labeling becomes visible to readers,
including an "unverified" filter toggle.

### View composition

Map the module IA (Explore / Research / Tools) and the entity-page sections (religion module §4.2) to
components + routes. Entity page = server-rendered shell + lazy islands for its graph/media panels.

### Editorial UI

Authenticated admin surface for review queues, reconciliation adjudication, and sensitivity/promotion
actions — mapped to the role scopes in
[../governance/security-and-access.md](../governance/security-and-access.md). Writes submit
contribution envelopes; no direct CRUD.

### Graph rendering

**D3** for the graph/lineage views (already proven in Mythographica), wrapped in a React island with
level-of-detail + virtualization for large subgraphs; traversal bounded by the API depth cap.

## Existing assets to adopt

- Sacred-Lineage (Next.js app shell, auth, admin CRUD), Mythographica (D3 graph UI),
  time-thread (timeline UI, URL-based nav, design tokens).

## Key decisions / open questions

- [x] App shape → **one unified Next.js app**, Vite components ported in (not micro-frontends).
- [x] Graph library → **D3** in a client island.
- [x] Public vs. internal split → the **public encyclopedia** is its own read-optimized deployable
  (`site/`, SSG/ISR + CDN), separate from the internal **Audit Console** (`web/`, always-fresh
  operator tooling). Mirrors Grokipedia's public-site / editorial-pipeline separation. "Unified app"
  (ADR-009) applies to the public reader, which later absorbs graph/compare/lens/editorial.
