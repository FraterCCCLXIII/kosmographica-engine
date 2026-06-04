# Kosmographica

A knowledge-graph engine for a **total record of human thought, culture, development, and history —
through an integral developmental lens.**

Kosmographica federates several existing datasets (comparative mythology, lineage transmission,
developmental/integral models, and a historical timeline) into one claim-based, provenance-first
graph, organized as a thin universal **core** plus pluggable **domain modules**.

## Documentation

Start with the **[documentation & specification plan](docs/PLAN.md)** — the master index of all specs
and their build order.

| Document | Purpose |
|---|---|
| [`docs/PLAN.md`](docs/PLAN.md) | Master index of the spec set, build order, and status. |
| [`docs/core-meta-model.md`](docs/core-meta-model.md) | The universal core: entity/claim/relationship model, the integral/developmental layer, the temporal layer, and federation/entity-resolution. |
| [`docs/modules/religion-mythology.md`](docs/modules/religion-mythology.md) | The first domain module — World Religion & Mythology — conforming to the core. |

The remaining architecture, governance, AI, frontend, and program specs are scaffolded under
`docs/` as outline stubs to be filled in iteratively; see [`docs/PLAN.md`](docs/PLAN.md).

## Repository layout

```
kosmographica/
├── README.md
└── docs/
    ├── PLAN.md                       # master spec index + build order
    ├── core-meta-model.md            # the universal core + cross-cutting layers
    ├── glossary.md                   # shared internal terminology
    ├── architecture/                 # system/data, federation, entity-resolution, ids, api
    ├── governance/                   # vocabulary, data-quality, ethics, licensing, security, ADRs
    ├── ai/                           # RAG engineering, AI authoring workflow
    ├── frontend/                     # design system, app architecture
    ├── program/                      # migration, roadmap, NFRs, evaluation
    └── modules/                      # domain modules + authoring guide
        └── religion-mythology.md     # Religion & Mythology domain module
```

## Federated datasets

Kosmographica is designed to integrate, not replace, these sibling projects:

- **Mythographica** (comparative mythology graph; assertion/claim model)
- **Sacred-Lineage** (guru/disciple transmission chains)
- **Kosmotheon** (integral developmental models — AQAL, Spiral Dynamics, Gebser, Wilber–Combs)
- **time-thread** (historical timeline spine)

## Status

Design stage — these documents are discussion drafts. See the open questions in
[`docs/core-meta-model.md`](docs/core-meta-model.md) §10.

## Quick Start

```bash
# Start the engine API (requires PostgreSQL with pgvector)
cd engine
docker compose up -d db
uv sync
uv run alembic upgrade head
uv run uvicorn kge.api.app:app --host 0.0.0.0 --port 8088
```

Then visit http://localhost:8088/docs for the interactive API documentation.
