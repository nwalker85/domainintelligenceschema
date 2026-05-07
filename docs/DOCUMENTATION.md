# Documentation Map

| Field | Value |
| --- | --- |
| Document ID | DIS-DOCS-001 |
| Status | Controlled |
| Owner | Nathan Walker |
| Domain | Domain Intelligence Schema |
| Scope | Documentation authority order for `domainintelligenceschema.org` |
| Related Services | GitHub Pages, `domainintelligenceschema.org`, `schemas.domainintelligenceschema.org` |
| Related ADRs | ADR-001 |
| Review Cadence | Monthly while the specification is active |
| Retention Rule | Retain for repository lifetime |
| Last Reviewed | 2026-05-07 |
| Next Review | 2026-06-07 |

## Authority Order

1. `README.md` is the developer entrypoint and schema catalog.
2. This file defines the documentation map and authority order.
3. `PRD.md` defines product requirements and MVP scope.
4. `ARCHITECTURE.md` defines boundaries, canonical URLs, schema distribution, and dependencies.
5. `CURRENT_STATE.md` records what exists today.
6. `GAPS.md` records missing pieces and risks.
7. `ROADMAP.md` defines staged direction.
8. `IMPLEMENTATION_PLAN.md` defines the current work plan.
9. `RUNBOOK.md` defines operator workflows.
10. `service-design/` defines service role, anti-role, responsibilities, APIs, data, failure modes, audit, and evidence.
11. `adr/` records durable decisions and supersession.
12. `docs/schemas/` is generated or maintained schema reference documentation.

## Controlled Documents

This repo is the canonical public methodology/spec repository for Domain Intelligence Schema. Website copy, schema versioning, and public docs should preserve citable definitions and stable URLs.
