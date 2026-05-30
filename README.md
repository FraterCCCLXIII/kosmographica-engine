# Kosmographica

A knowledge-graph engine for a **total record of human thought, culture, development, and history —
through an integral developmental lens.**

Kosmographica federates several existing datasets (comparative mythology, lineage transmission,
developmental/integral models, and a historical timeline) into one claim-based, provenance-first
graph, organized as a thin universal **core** plus pluggable **domain modules**.

## Documentation

| Document | Purpose |
|---|---|
| [`docs/core-meta-model.md`](docs/core-meta-model.md) | The universal core: entity/claim/relationship model, the integral/developmental layer, the temporal layer, and federation/entity-resolution. |
| [`docs/modules/religion-mythology.md`](docs/modules/religion-mythology.md) | The first domain module — World Religion & Mythology — conforming to the core. |

## Repository layout

```
kosmographica/
├── README.md
└── docs/
    ├── core-meta-model.md            # the universal core + cross-cutting layers
    └── modules/
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
