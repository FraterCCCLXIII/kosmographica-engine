# Security & Access Control

> **Status:** stub / outline · **Priority:** P2 · Part of the [spec plan](../PLAN.md).

## Purpose

Define authentication, authorization, and the technical access-control model — including the
counterpart to the editorial roles and the enforcement of restricted-content gating.

## Sections to detail

1. **Authentication** — identity model, sessions/tokens (Sacred-Lineage uses NextAuth credentials).
2. **Roles & permissions** — technical mapping of editorial roles (Contributor, Domain Editor,
   Scholar Reviewer, Tradition Reviewer, Comparative Specialist, AI Curator, Administrator) to scopes.
3. **Access tiers** — enforcement of `public | sensitive | sacred | restricted` (ties to
   [ethics-and-sovereignty.md](./ethics-and-sovereignty.md)).
4. **API security** — token scopes, rate limits, write-path authorization, audit logging.
5. **Data protection** — secrets management, encryption at rest/in transit, backups.
6. **MCP / automation access** — read-only vs. write roles for agents (Mythographica precedent:
   MCP read-only audit; writes via JSON + seed).

## Key decisions / open questions

- [ ] Public-read vs. authenticated-only launch posture.
- [ ] Identity provider choice.
