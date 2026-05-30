# Identifiers, URIs & Versioning

> **Status:** stub / outline · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> Expands [core meta-model §6.1](../core-meta-model.md#6-federation--entity-resolution).

## Purpose

Define the canonical identifier scheme (KID), its URI form, persistence guarantees, and how IDs and
schemas evolve over time (including entity merge/split).

## Decided method (v1)

### KID = opaque UUID

A Kosmographica ID is `kg:<class>/<uuidv7>` where class ∈ `entity | claim | relationship | source |
framework`. The UUID is **opaque** — type/module live in columns, **not** in the id — so an entity's
identity survives re-typing or module moves. (Readable prefixes like `kg:deity/…` were rejected:
they rot when classification changes.) UUIDv7 for time-ordered, index-friendly keys.

### URI resolution

`https://kosmographica.org/id/<uuid>` resolves with content negotiation: HTML (default), JSON-LD, or
RDF/Turtle for linked-data consumers. *(Domain ownership of `kosmographica.org` is a user-owned
action item — flagged below.)*

### Persistence — permanent, never reused

KIDs are permanent and never re-minted. **Deprecate, never delete.** A removed/merged entity becomes
a **tombstone** that 301-redirects to its survivor (or returns `410 Gone` with a reason if no
survivor).

### Merge / split (non-destructive, pairs with entity-resolution)

- **Merge:** pick a survivor KID; the other becomes a tombstone redirecting to it; its `sameAs`,
  claims, and relationships **re-point** to the survivor (re-pointing is recorded, reversible).
- **Split:** mint new KID(s); the original tombstones or remains as the disambiguation hub; claims
  move to the correct target by review. Both operations are logged in the change history.

### External ID linking

An `external_ids` table maps a KID to authority IDs (Wikidata, VIAF, GeoNames, Pleiades, Getty
AAT/ULAN, PeriodO, CTS URNs), **many per entity**, each with the authority name + confidence. This
table is the deterministic-match fuel for [entity-resolution.md](./entity-resolution.md).

### Versioning

- **Schema:** semantic versioning of core + each module schema (`core@1.x`, `religion@1.x`); additive
  changes are minor, breaking changes major with a migration note. Records stamp the schema version
  they were written under.
- **Records:** bitemporal — every row carries `recorded_at` (transaction time) alongside valid-time
  (core §5); history is queryable and supersession is append-only (never in-place mutation).

## Key decisions / open questions

- [x] KID opacity → **opaque UUIDv7**; type/module in columns, not the id.
- [ ] **(user-owned)** Register/confirm ownership of the `kosmographica.org` URI namespace.
