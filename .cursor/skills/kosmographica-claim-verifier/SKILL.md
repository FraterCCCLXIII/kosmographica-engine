---
name: kosmographica-claim-verifier
description: Run the independent claim verifier that gates AI writes to canonical (ADR-013) — check whether a claim's cited sources actually support it via entailment, turn the support score into confidence, and route to machine_validated / dispute / quarantine. Use when verifying staged claims or implementing/operating the verifier.
---

# Kosmographica Claim Verifier

The verifier is what lets AI **write directly to canonical** while staying auditable: publish-then-verify.
It is the trust backbone — treat its judgments conservatively.

## Read first (paths from the kosmographica repo root)

- `docs/governance/decision-log.md` — ADR-013 (publish-then-verify) and ADR-011 (quarantine).
- `docs/ai/rag-engineering.md` — the verifier spec + eval suite.
- `docs/governance/data-quality-validation.md` — gate stage 4 (citation-support / entailment).

## Independence rule

The verifier model **must differ from the author model**. Never let a model verify its own write.

## Procedure (per claim)

1. **Inputs** — the staged claim, its cited `sources` + `support_spans`, the author model id.
2. **Anti-fabrication (deterministic)** — confirm each source exists in the registered corpus and the
   `support_span` text actually occurs in it. A missing source or invented span → fail immediately.
3. **Entailment** — judge the relation of the span to the claim:
   - `supports` → proceed; `unrelated` → fail; `contradicts existing canonical claim` → open a dispute.
4. **Score → confidence** — the support score **becomes** the claim's `confidence` (do not keep the
   author's self-assigned value).
5. **Route (ADR-011 / ADR-013):**
   - `support ≥ threshold` → write at `machine_validated` (public, badged "AI-generated · unreviewed").
   - below threshold → quarantine at `machine_unverified` (hidden), with a machine-readable reason.
   - contradiction → **dispute**: both claims coexist with provenance; never overwrite.

## Carve-out (non-negotiable)

Sacred/restricted (CARE / TK) content is **never** auto-published by the verifier — route it to
community/expert review regardless of entailment score.

## Output

Emit a verification record stored with the claim: `{ verifier_model, support_label, support_score,
sources_checked, span_found, outcome, reason }`. This record is what makes the write auditable.

## Reminders

- Append-only: writes supersede, never overwrite (core §5) — every decision is reversible.
- A weak/over-generous verifier silently poisons the corpus; prefer false-quarantine over
  false-publish, and track verifier quality in the eval suite (`rag-engineering.md`).
