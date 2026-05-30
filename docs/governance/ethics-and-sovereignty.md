# Ethics & Data Sovereignty Operations

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).
> Operationalizes [core meta-model §9](../core-meta-model.md#9-cross-cutting-standards--ethics).

## Purpose

Make the CARE Principles and Traditional Knowledge (TK) Labels operational: how sacred, restricted,
or culturally sensitive content is flagged, governed, and access-controlled across the corpus.

## Decided method (v1)

A "total record" must not flatten sovereignty or expose restricted knowledge. Indigenous and living
traditions (Andean, Caribbean, Celtic, …) are in scope, so sovereignty controls are **built in from
v1**, not bolted on later — this is the one place the otherwise-lean defaults bend toward caution.

### Sensitivity classification (per record)

Every entity/media record carries `sensitivity ∈ { public | sensitive | sacred | restricted }`.

- **Default for newly ingested indigenous/living-tradition content = `sensitive`** (not `public`),
  pending tradition review. Conservative by default; downgraded only by review.
- **Store-but-gate, do not exclude.** Restricted content is retained (so provenance and takedown are
  auditable) but access-gated — never silently dropped, never openly served. Hard exclusion only on
  an explicit tradition-authority request.

### CARE → concrete behaviors

| CARE principle | Platform behavior |
| --- | --- |
| Collective benefit | export/attribution credits communities, not just scholars |
| Authority to control | tradition authorities can set `sensitivity`, request restriction/takedown |
| Responsibility | sacred/restricted records show provenance + label; no auto-publish (ADR-013 carve-out) |
| Ethics | sensitive material is `sensitive` by default; review before public surfacing |

### TK Labels

Support the standard TK Label set (e.g. TK Attribution, TK Secret/Sacred, TK Community Use Only,
TK Verified) as **badges attached to entities/media**, distinct from licenses (see
[licensing-and-rights.md](./licensing-and-rights.md)). Labels drive display rules (badge + access
gate) but are advisory metadata, not access tiers by themselves.

### Workflow

- **Tradition Reviewer role** — an insider reviewer can set sensitivity/labels, approve `sacred`
  content for `expert_endorsed`, and is the required gate for the ADR-013 sacred-content carve-out.
- **Takedown / correction** — public flag → triage → tradition-authority adjudication → action, all
  recorded in the audit trail (bitemporal; reversible).
- Enforcement of the gates is technical — see [security-and-access.md](./security-and-access.md).

## Key decisions / open questions

- [x] Default classification for new indigenous content → **`sensitive`** (conservative, review to change).
- [x] Restricted content → **stored-but-gated**, not excluded (hard-exclude only on authority request).
