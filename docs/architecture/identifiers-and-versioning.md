# Identifiers, URIs & Versioning

> **Status:** stub / outline · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> Expands [core meta-model §6.1](../core-meta-model.md#6-federation--entity-resolution).

## Purpose

Define the canonical identifier scheme (KID), its URI form, persistence guarantees, and how IDs and
schemas evolve over time (including entity merge/split).

## Sections to detail

1. **KID format** — `kg:entity/<uuid>` (and KIDs for claims, relationships, sources, frameworks…).
   UUID strategy; collision/uniqueness guarantees.
2. **URI resolution** — `https://kosmographica.org/id/<uuid>`; content negotiation (HTML / JSON-LD / RDF).
3. **Persistence policy** — KIDs are permanent; never reused; deprecation over deletion.
4. **Merge/split of entities** — redirect/tombstone semantics; how `sameAs` and inbound references
   are preserved (coordinate with [entity-resolution.md](./entity-resolution.md)).
5. **External ID linking** — authorities table (Wikidata, VIAF, GeoNames, Pleiades, Getty AAT/ULAN,
   PeriodO, CTS URNs); one-to-many handling.
6. **Schema versioning** — semantic versioning of the core + module schemas; migration policy;
   compatibility windows.
7. **Record versioning** — change history / bitemporal `recorded_at`; relationship to the change_log.

## Key decisions / open questions

- [ ] KID opacity (pure UUID) vs. readable prefixes (e.g. `kg:deity/...`).
- [ ] Domain ownership of `kosmographica.org` URI namespace.
