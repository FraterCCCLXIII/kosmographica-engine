# Controlled Vocabulary & Ontology Governance

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).
> Expands [core meta-model §8](../core-meta-model.md#8-controlled-vocabulary).

## Purpose

Define how Kosmographica's controlled vocabulary is built (**fresh**, not from Panentheon), governed,
versioned, and exported as SKOS — covering tradition taxonomy, relationship-type registry, claim
types, and concept vocabulary.

## Taxonomy design principles (cross-module)

These principles apply to **every** module's vocabulary, not just Religion & Mythology. A good
taxonomy holds several tensions at once instead of forcing one rigid hierarchy.

1. **Multiple overlapping axes, not one tree.** Classify each entity along several axes
   simultaneously (e.g. tradition/lineage, theme, period, geography, scholarly meta). Modules declare
   their own axes (see [module authoring guide](../modules/module-authoring-guide.md)).
2. **Polyhierarchy via facets, not parent tables.** Axis membership is modeled as **tags / typed
   relationships on entities** (per [ADR-007](decision-log.md) — generic `entities` + JSONB), so one
   entity can sit under many axes at once. We do **not** add per-axis hierarchy tables.
3. **Emic vs. etic.** Record where insider terms and outsider/scholarly terms diverge; keep both,
   labeled, rather than collapsing or refusing either (e.g. "Hinduism" as a partly external
   construction). Term records carry an `emic | etic | both` perspective tag.
4. **Synchronic vs. diachronic.** Support both a current-state view and a historical-development view;
   period membership is itself a claim (core temporal layer), not a fixed attribute.
5. **Universalist vs. particularist.** Shared cross-cultural phenomena (a concept axis) and
   tradition-specific meaning (interpretation axis) are distinct layers — "no entity owns a concept."
6. **Granularity tiers.** Tag articles as **overview / mid-level / fine-grained** so navigation and
   RAG can target the right altitude of detail.
7. **Contested flag.** Where scholarly or community consensus is genuinely disputed, flag it
   (derived from `claim_type` / `is_disputed`) rather than picking a winner.
8. **Include absence and critique.** Non-belief, skepticism, and critique of a domain belong *in* its
   taxonomy, not outside it (e.g. atheism, secularization for the Religion module).

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
