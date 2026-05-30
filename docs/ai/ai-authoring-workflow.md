# AI Authoring & Agent Contribution Workflow

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

Define how AI agents (and human editors) propose new entities, claims, and relationships at scale,
and the validation + human-review gates that keep the corpus trustworthy — since population will be
largely AI-assisted.

## Decided method (v1) — publish-then-verify

> Governing decision: [ADR-013](../governance/decision-log.md) (supersedes ADR-012). AI **writes
> directly to canonical**, gated by an automated verifier — not by a human. Humans audit exceptions.

Authoring is the *authoring input* to the shared pipeline
([federation-and-ingestion.md](../architecture/federation-and-ingestion.md), ADR-010): agents emit the
**same contribution envelope** as migration adapters. The difference from migration is the **verifier
loop** that lets AI commit to canonical without a human pre-gate.

### The write loop

```text
author agent ─▶ grounded draft (claim + source spans)
                   │
                   ▼
            VERIFIER (independent model + deterministic checks)
                   │  entailment: does the source actually support the claim?
                   │  + structural/provenance gate (ADR-011)
                   ├─ pass ─▶ WRITE to canonical @ machine_validated (confidence = support score)
                   ├─ conflict with existing claim ─▶ open DISPUTE (both coexist, no overwrite)
                   └─ fail ─▶ quarantine @ machine_unverified
                   ▼
   continuous re-verification job ─▶ recompute confidence · decay stale · flag for human spot-audit
```

1. **Grounded generation only** — an agent may not assert what it didn't retrieve; each claim carries
   the exact supporting source span(s). No span → cannot exceed `machine_unverified`.
2. **Verifier agent** — a *second, independent* model plus deterministic checks runs an entailment
   check (source-supports-claim) and the structural/provenance gate; the support score *becomes* the
   claim's confidence. This is the critical dependency — specced in
   [rag-engineering.md](./rag-engineering.md) with its own eval suite.
3. **Direct write, append-only & bitemporal** — verified claims land in canonical immediately; writes
   **supersede, never overwrite** (core §5), so every AI write is reversible.
4. **Contradiction → dispute** — conflicting claims open a dispute and coexist with provenance; no AI
   edit wars.

### Trust tiers & visibility (retained from ADR-012)

| Tier | How reached | Public default |
| --- | --- | --- |
| `machine_unverified` | staged, failed/pending verification | hidden |
| `machine_validated` | passed the verifier | **visible, badged "AI-generated · unreviewed · N sources"** + confidence |
| `human_reviewed` | editor spot-audit confirmed | visible, trusted |
| `expert_endorsed` | domain/scholar/community (CARE/TK) sign-off | visible, authoritative |

### Auditability (the payoff)

Every record stores `tier + generator + verifier record + sources + bitemporal history`, so auditing
is a query — e.g. *all `machine_validated`, not-yet-`human_reviewed` claims by model X in batch Y* —
and any bad write is one supersede away from rollback.

### Carve-out (non-negotiable)

**Sacred/restricted material (CARE / TK Labels) keeps the pre-publication community/expert gate** — no
AI auto-publish, regardless of verifier outcome.

### Guardrails & human role

- **Agent guardrails:** mandatory sources for medium/high confidence; cautious confidence by default;
  never conflate cognate / parallel / syncretism; developmental readings attributed (`asserted_by` +
  framework). Adopted from Mythographica's `comparative-methodology.md`.
- **Humans audit, not gate:** one queue, role-tagged (AI Curator triage, Domain, Scholar,
  Tradition/community), working the *flagged / disputed / low-confidence / high-traffic* set and
  promoting to `human_reviewed` / `expert_endorsed`.

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

- [x] Auto-accept → **publish-then-verify** (ADR-013): AI writes to canonical at `machine_validated`
  when the verifier passes; humans audit post-hoc. Sacred/CARE content excepted (pre-gate retained).
- [ ] Which models are approved for authoring vs. **verification** (must be independent of the author).
- [ ] Verifier confidence threshold for `machine_validated` vs. quarantine.
