# Controlled Vocabulary & Ontology Governance

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).
> Expands [core meta-model §8](../core-meta-model.md#8-controlled-vocabulary).

## Purpose

Define how Kosmographica's controlled vocabulary is built (**fresh**, not from Panentheon), governed,
versioned, and exported as SKOS — covering tradition taxonomy, relationship-type registry, claim
types, and concept vocabulary.

## Sections to detail

1. **Principles** — build fresh; anchor on Mythographica's guardrailed taxonomy; external glossaries
   (incl. Panentheon) are unverified leads, never load sources.
2. **Tradition taxonomy** — `family / tradition / subtradition` model (from Mythographica's
   `meta.traditionTaxonomy`), hierarchy, legacy-label mapping.
3. **Relationship-type registry** — controlled predicate list with `direction` + `inverse_key`
   (Mythographica `relationType` + Sacred-Lineage `RelationshipType`); the comparative-predicate set.
4. **Claim-type & methodology vocabularies** — enumerations + definitions.
5. **Concept vocabulary** — concept families (core/religion module), SKOS broader/narrower/related.
6. **Per-term quality bar** — definition + sources + confidence required before a term is usable.
7. **Governance process** — proposal → review → accept; who owns the vocabulary; deprecation.
8. **Versioning & SKOS export** — concept scheme IDs, change tracking, RDF/SKOS serialization.

## Existing assets to adopt

- Mythographica `comparative-methodology.md` (epistemic rules), `edgeTypeGuide`, taxonomy scripts.

## Key decisions / open questions

- [ ] Single global vocabulary vs. per-module extensions.
- [ ] Altitude scale naming (ties to core §10 Q3).
