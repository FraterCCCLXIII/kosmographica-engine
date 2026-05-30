# Frontend / Application Architecture

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

Define the engine's web application architecture: framework, routing, data fetching, state, and how
the views from the module's information architecture are composed.

## Sections to detail

1. **Framework & stack** — choose (Next.js per Sacred-Lineage, or Vite/React per Mythographica &
   time-thread); SSR vs. SPA; TypeScript throughout.
2. **Routing & URLs** — entity pages, graph explorer, comparison, timeline, developmental lens,
   search; shareable/bookmarkable URLs (time-thread precedent).
3. **Data layer** — API client, caching, the GraphRAG/query API contract
   ([../architecture/api-contract.md](../architecture/api-contract.md)).
4. **View composition** — map the module's navigation + entity-page sections (Explore / Research /
   Tools; entity-page §4.2) to components and routes.
5. **Key interactive views** — Graph Explorer, Lineage Builder, Comparison View, Comparative Mapping
   Engine, **Developmental Lens**, RAG Chat, Timeline Explorer, Citation Browser.
6. **State management** — client/server state boundaries.
7. **Performance & accessibility** — code-splitting, graph rendering at scale, ARIA/keyboard.
8. **Admin/editorial UI** — CRUD, review queues, reconciliation review (ties to governance roles).

## Existing assets to adopt

- Sacred-Lineage (Next.js app shell, auth, admin CRUD), Mythographica (D3 graph UI),
  time-thread (timeline UI, URL-based nav, design tokens).

## Key decisions / open questions

- [ ] One unified app vs. federated micro-frontends per existing repo.
- [ ] Graph rendering library (D3 already used in Mythographica).
