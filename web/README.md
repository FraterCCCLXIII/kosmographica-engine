# Kosmographica Web — Audit Console

A small **read-only** Next.js (App Router) console over the engine's REST API, so an
AI-populated corpus is observable from day one. The editorial/authoring layer (NextWiki)
stays deferred — AI is the only writer (publish-then-verify); humans observe and audit.

Screens:

- **Overview** (`/`) — corpus counts, claims by trust tier, by generator, disputes.
- **AI-validated queue** (`/queue`) — `machine_validated` claims (filter by generator/batch).
- **Disputes** (`/disputes`) — contradicting claims that coexist with provenance.
- **Entity view** (`/entities/[kid]`) — claims + 1-hop relationships.
- **Claim verification** (`/claims/[kid]`) — assertion, support spans, sources, verifier history.

## Develop

```bash
# 1. Engine API (separate terminal, from ../engine)
uv run uvicorn kge.api.app:app --port 8000

# 2. Console
npm install
KGE_API_URL=http://localhost:8000 npm run dev   # http://localhost:3000
```

`KGE_API_URL` points the console at the engine (default `http://localhost:8000`). See
[`../docs/frontend/app-architecture.md`](../docs/frontend/app-architecture.md) and
[`../docs/frontend/design-system.md`](../docs/frontend/design-system.md).
