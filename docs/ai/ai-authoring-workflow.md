# AI Authoring & Agent Contribution Workflow

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

Define how AI agents (and human editors) propose new entities, claims, and relationships at scale,
and the validation + human-review gates that keep the corpus trustworthy — since population will be
largely AI-assisted.

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

- [ ] Which models are approved for authoring vs. review.
- [ ] Auto-accept threshold (likely none for claims; all reviewed).
