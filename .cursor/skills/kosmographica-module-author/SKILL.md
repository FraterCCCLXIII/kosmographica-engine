---
name: kosmographica-module-author
description: Author or scaffold a Kosmographica domain module (e.g. Philosophy & Science, Art & Culture, Polity & Society, Technology) that conforms to the core meta-model. Use when adding, drafting, expanding, or reviewing a domain module under docs/modules/ in the kosmographica repo.
---

# Kosmographica Module Author

Author a domain module that **extends the universal core consistently** — same claim model, same
cross-cutting layers, different entity-subtype vocabulary. A module never reinvents the core.

## Read first (paths from the kosmographica repo root)

- `docs/core-meta-model.md` — the thin universal core a module profiles.
- `docs/modules/module-authoring-guide.md` — the binding template and rules.
- `docs/modules/religion-mythology.md` — the reference example to imitate (structure, depth, tone).
- `docs/governance/controlled-vocabulary.md` — taxonomy design principles for the axes section.

## Hard rules

- **May:** define module `EntityType` subtypes, module-specific relationship/claim types, and
  module-specific entity-page sections.
- **May not:** redefine core fields, invent a parallel claim/confidence model, or bypass the
  federation, developmental, temporal, or provenance layers.
- **Cross-link to core sections — do not restate schema.** Confidence is numeric `0.0–1.0` + derived
  band. Every contestable assertion is a claim with sources.

## Required sections (in order)

1. **Conformance preamble** — declare the module, link the core, state "core governs on conflict."
2. **Scope & vision** — what the domain covers and its boundary with adjacent modules.
3. **Entity ontology** — module entity types/subtypes (a profile of core `Entity`).
4. **Module relationship & claim types** — additions registered in the controlled vocabulary.
5. **Information architecture** — navigation + entity-page sections.
6. **Classification axes** — overlapping axes (tradition/theme/period/geography/meta as applicable)
   modeled as **polyhierarchical facets**, not parent tables. **Must include the domain's
   absence/critique stances**, not only its positive content.
7. **Developmental layer usage** — how core §4 applies in this domain.
8. **Federation & source systems** — which datasets feed this module.
9. **Examples** — worked entity + claim examples.

## Checklist before "specified"

```text
- [ ] Conformance preamble links the core and states "core governs on conflict"
- [ ] Entity types + vocabulary additions registered (controlled-vocabulary.md)
- [ ] Classification axes are facets/tags, with absence/critique included
- [ ] Federation sources identified
- [ ] Developmental + temporal usage stated (cross-linked, not restated)
- [ ] Confidence numeric (0–1) + band everywhere; every assertion sourced
- [ ] Reviewed against module-authoring-guide.md
```

## House style

Start each doc with a status banner blockquote (status · priority · link to `docs/PLAN.md`).
Insert new sub-sections to avoid renumbering downstream sections where possible. Proper-noun and
table-formatting spellcheck/markdownlint warnings are expected noise — do not "fix" domain terms.
