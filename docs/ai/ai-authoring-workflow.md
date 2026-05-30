# AI Authoring & Agent Contribution Workflow

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

Define how AI agents (and human editors) propose new entities, claims, and relationships at scale,
and the validation + human-review gates that keep the corpus trustworthy — since population will be
largely AI-assisted.

## Decided method (v1)

Authoring is **not a separate system** — it is the *authoring input* to the shared ingestion pipeline
([federation-and-ingestion.md](../architecture/federation-and-ingestion.md), ADR-010). Agents and
editors emit the **same contribution envelope** as migration adapters and pass through the same
`stage → validate → reconcile → review → load` gate.

**Trust tiers drive review (ADR-012):**

| Tier | How reached | Public by default? |
| --- | --- | --- |
| `machine_unverified` | raw agent output, staged | no |
| `machine_validated` | passed automated validation; deterministic structural facts may rest here | no |
| `human_reviewed` | an editor approved the claim/edge | **yes** |
| `expert_endorsed` | domain/scholar/community (CARE/TK) sign-off | yes |

**Auto-accept policy:** **no AI-authored claim or comparative edge auto-accepts.** Deterministic
*structural* facts from a trusted source can auto-load at `machine_validated`; everything contestable
waits in the human-review queue. Sacred/restricted material always routes to community/expert review.

**Agent guardrails (non-negotiable):** mandatory sources for medium/high confidence; cautious
confidence by default; never conflate cognate / parallel / syncretism; developmental readings must be
attributed (`asserted_by` + framework). Adopted from Mythographica's `comparative-methodology.md`.

**Reviewer roles (lean):** one review queue with role tags — AI Curator (triage), Domain reviewer,
Scholar reviewer, Tradition/community reviewer — rather than a heavy multi-stage workflow tool.

## Sections to detail

1. **Contribution format** — the canonical authoring artifact (generalize Mythographica's MythGraph
   JSON `{meta,nodes,edges}`); required fields per record.
2. **Agent rulebook** — epistemic guardrails agents must follow (adopt Mythographica
   `comparative-methodology.md`): cautious confidence, mandatory sources, no conflation of cognate /
   parallel / syncretism, developmental readings must be attributed.
3. **System prompts** — reusable prompts per task (new tradition, enrichment, comparative edges,
   developmental annotations) — extend Mythographica's contributor prompt.
4. **Submission → validation → review** — pipeline from agent output through
   [../governance/data-quality-validation.md](../governance/data-quality-validation.md) to human
   approval (AI Curator + Domain/Scholar/Tradition reviewers).
5. **Hallucination controls** — source verification, flagging unverifiable claims, mandatory
   citation for high/medium confidence.
6. **Provenance of AI contributions** — mark machine-generated vs. human-reviewed; audit trail.
7. **Incremental enrichment** — patch/overlay workflow (Mythographica enrichment pipeline).

## Existing assets to adopt

- Mythographica `ai-data-format.md` (copy-paste system prompt), `comparative-methodology.md`.

## Key decisions / open questions

- [x] Auto-accept threshold → **none for claims/edges**; deterministic structural facts only, at
  `machine_validated` (ADR-012).
- [ ] Which models are approved for authoring vs. review.
