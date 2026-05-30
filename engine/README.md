# Kosmographica Engine

The federation engine for Kosmographica: a single PostgreSQL-backed claim graph, the
contribution-envelope ingestion pipeline, and the AI publish-then-verify write loop.

See the specs in [`../docs`](../docs) — especially
[`architecture/system-and-data-architecture.md`](../docs/architecture/system-and-data-architecture.md),
[`architecture/federation-and-ingestion.md`](../docs/architecture/federation-and-ingestion.md), and
[`governance/decision-log.md`](../docs/governance/decision-log.md) (ADR-001, 007, 010, 013).

## Layout

```text
src/kge/
  config.py         # settings (env-driven)
  db.py             # SQLAlchemy engine/session
  ids.py            # KID minting (UUIDv7, opaque per ADR identifiers-and-versioning)
  models/           # canonical schema: entities, relationships, claims, sources
  envelope.py       # contribution envelope (the single write format, ADR-010)
  validation/       # deterministic validator (ADR-011)
  adapters/         # source adapters (e.g. Mythographica) -> envelope
  pipeline/         # stage -> validate -> reconcile -> load -> index
  api/              # tier-aware FastAPI read API
tests/
```

## Develop

```bash
uv sync            # create venv + install deps
uv run pytest      # run the suite
```

The pipeline, API, and seed steps need Postgres; bring one up with
`docker compose up -d db` (see [`docker-compose.yml`](./docker-compose.yml)).
