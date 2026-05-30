# Entity Resolution & Reconciliation

> **Status:** stub / outline · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> Makes [core meta-model §6.2](../core-meta-model.md#6-federation--entity-resolution) executable.

## Purpose

Define how the engine decides that records from different source systems (and external authorities)
refer to **the same entity**, and how that decision is recorded, reviewed, and revised.

## Decided method (v1)

This is **stage [3] of the ingestion pipeline** — see
[federation-and-ingestion.md](./federation-and-ingestion.md). It runs after validation and produces
**merge/insert proposals**, never destructive merges. Identity is a `sameAs` mapping, not an
overwrite.

### Matching, cheapest signal first

1. **Deterministic (external ID)** — if a staged record shares an external authority ID (Wikidata,
   VIAF, GeoNames, Pleiades…) with an existing entity, it's the **same** entity. No scoring needed.
   This resolves the large majority of cross-source matches for free.
2. **Blocking** — for the rest, generate candidates by cheap keys: normalized name / alternate names
   (transliteration-folded) **within the same `type` and `module`**. Avoids all-pairs comparison.
3. **Scoring** — combine signals into a score: name similarity, type match, date-range overlap,
   region, and — only if still ambiguous — embedding similarity of the entity's summary.

### Bands (lean automation)

| Score | Action |
| --- | --- |
| external-ID match | auto-link `sameAs` at `machine_validated` |
| high | auto-link, flagged for spot-audit |
| medium | **review queue** (human decides) |
| low | insert as a new entity |

### `sameAs` lifecycle & records

Each reconciliation row stores `match_method` (deterministic / scored / manual), `score`,
`confidence`, and status (`proposed → accepted | rejected`). Rejections are remembered so the pair is
not re-proposed. Links are revisable — reconciliation is never final.

### Non-negotiable rules

- **Conflict → keep both as claims.** When sources disagree on an attribute, both values persist as
  claims with their provenance; resolution never silently overwrites (consistent with the claim layer).
- **No cross-tradition auto-merge on name alone.** *Inanna ≠ Ishtar* by default; *Hermes ≠ Thoth*.
  Such links are **comparative edges** (equivalence/parallel), not identity. Identity merges stay
  within a tradition unless an external ID proves otherwise.
- **Merge/split is non-destructive** — see [identifiers-and-versioning.md](./identifiers-and-versioning.md)
  for KID redirect/tombstone semantics; claims and relationships re-point, never vanish.

### Deferred until forced

- Learned/ML matching models — v1 uses the rule+score ladder above.
- Cross-lingual embedding matching at scale — start with transliteration folding + summary embeddings.

## Existing assets to adopt

- Mythographica taxonomy + `legacyMapping` (normalizes old labels) as a reconciliation precedent.

## Key decisions / open questions

- [x] Automation per band → **external-ID & high auto-link; medium → human; low → new entity**.
- [ ] Embedding model + similarity threshold for the ambiguous-case tie-breaker (ties to rag-engineering).
