# Entity Resolution & Reconciliation

> **Status:** stub / outline · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> Makes [core meta-model §6.2](../core-meta-model.md#6-federation--entity-resolution) executable.

## Purpose

Define how the engine decides that records from different source systems (and external authorities)
refer to **the same entity**, and how that decision is recorded, reviewed, and revised.

## Sections to detail

1. **Matching signals** — name + alternate names (transliteration-aware), tradition/family, type,
   date range, region, external IDs (Wikidata bridge), embedding similarity.
2. **Scoring & thresholds** — combine signals into a match score; auto-merge / review / reject bands.
3. **`sameAs` lifecycle** — proposal → review → accepted/rejected; `match_method` and `confidence`
   on each reconciliation row.
4. **Human-in-the-loop** — review queue, who adjudicates (ties to editorial roles), audit trail.
5. **Merge & split semantics** — what happens to KIDs, claims, and relationships on merge/split
   (coordinate with [identifiers-and-versioning.md](./identifiers-and-versioning.md)).
6. **Conflict handling** — when sources disagree on attributes: keep both as claims, never silently
   overwrite (consistent with the claim layer).
7. **Cross-tradition caution** — do **not** auto-merge across traditions on name similarity alone
   (e.g. Inanna ≠ Ishtar by default); such links are comparative claims, not identity.
8. **Evaluation** — precision/recall on a labeled reconciliation set (ties to evaluation-metrics).

## Existing assets to adopt

- Mythographica taxonomy + `legacyMapping` (normalizes old labels) as a reconciliation precedent.

## Key decisions / open questions

- [ ] Embedding model + similarity threshold for candidate generation.
- [ ] Degree of automation vs. mandatory human review per match band.
