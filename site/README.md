# Kosmographica — Public Encyclopedia

The reader-facing site (Wave 3, W3.1–W3.3): a fast, crawlable, **read-only** encyclopedia over the
engine API. Distinct from the internal Audit Console (`../web`): public audience, public tier clamp,
SSG/ISR + CDN-friendly. Architecturally separated like Grokipedia's public site vs. its editorial pipeline.

## Stack

Next.js 16 (App Router, Server Components, ISR) · React 19 · Tailwind v4 · D3 (graph island).
Design tokens follow `docs/frontend/design-system.md` (warm-canvas).

## Routes

- `/` — landing / browse by type
- `/{module}/{type}/{slug}` — entity page: description, cited + trust-rated claims, connections, graph
- `/search?q=` — keyword search
- `/sitemap.xml`, `/robots.txt`

## Develop

```bash
npm install
cp .env.example .env.local   # point KGE_API_URL at the running engine
npm run dev                  # http://localhost:3099
```

The engine must be running (default `http://localhost:8088`). The public site sends no `min_tier`,
so the engine applies its public clamp (machine_validated+; unverified hidden; sacred/restricted gated).
