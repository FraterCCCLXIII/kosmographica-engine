# Security & Access Control

> **Status:** stub / outline · **Priority:** P2 · Part of the [spec plan](../PLAN.md).

## Purpose

Define authentication, authorization, and the technical access-control model — including the
counterpart to the editorial roles and the enforcement of restricted-content gating.

## Decided method (v1)

The technical enforcement counterpart to the editorial roles (ethics-and-sovereignty) and the API
contract. Lean: one identity model, scoped bearer tokens, server-side sensitivity gating.

### Authentication

Email/credentials sessions to start (Sacred-Lineage's NextAuth precedent), issuing **scoped bearer
tokens** for API calls. A pluggable provider interface so OAuth/SSO can be added later without
rework. **Public read is unauthenticated** for `human_reviewed`+ / `public` content; everything else
requires a token.

### Roles → scopes

| Editorial role | Scopes (illustrative) |
| --- | --- |
| Contributor / AI author agent | `contributions:write` (envelope only; lands at `machine_*`) |
| Domain / Scholar Reviewer | `review:approve`, `claims:promote` (→ `human_reviewed`) |
| Tradition Reviewer | `sensitivity:set`, `sacred:approve` (→ `expert_endorsed`) |
| Comparative Specialist | `comparative:write` |
| AI Curator | `reconciliation:adjudicate`, `quarantine:triage` |
| Administrator | all + `schema:migrate` |

No role writes canonical tables directly — writes flow through the pipeline (ADR-010); roles gate
*review/promotion*, not raw mutation.

### Access-tier enforcement

`sensitivity` is enforced **server-side at the API**, never only hidden in the UI: `sensitive`
requires auth; `sacred`/`restricted` require the appropriate scope + tradition-authority grant. The
verifier/RAG corpus only retrieves content the caller is entitled to see.

### API & data protection

Token scopes on every write path; per-token rate limits; **audit logging** of every write/promotion/
reconciliation (bitemporal trail). Secrets via environment/secret store (never committed — enforced
by the commit rule); TLS in transit; encryption at rest; regular backups (NFR doc).

### Agent / MCP access

Agents get **read-only or `contributions:write` only** — never review/promotion scopes (an author
cannot approve its own work; mirrors ADR-013 verifier independence). Mythographica precedent: MCP
read-only audit, writes via envelope + pipeline.

## Key decisions / open questions

- [x] Launch posture → **public-read for reviewed content; authenticated writes**.
- [ ] Identity provider beyond credentials (OAuth/SSO) — deferred until multi-org editing is needed.
