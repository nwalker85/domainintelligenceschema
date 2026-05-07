# ADR-001: GitHub Pages Static Spec Site

| Field | Value |
| --- | --- |
| Document ID | DIS-ADR-001 |
| Status | Accepted |
| Owner | Nathan Walker |
| Domain | Domain Intelligence Schema |
| Scope | Initial hosting and deployment model |
| Related Services | GitHub Pages, Cloudflare |
| Related ADRs | None |
| Review Cadence | Quarterly |
| Retention Rule | Retain permanently |
| Last Reviewed | 2026-05-07 |
| Next Review | 2026-08-07 |

## Context

Domain Intelligence Schema needs to be live immediately as a public, citable specification site. The existing domain already resolves to GitHub Pages and serves a static property.

## Decision

Use GitHub Pages and static assets as the initial production deployment model. Migrate DNS to Cloudflare later without changing the repository boundary.

## Consequences

- The site stays simple and cheap.
- Versioned schema URLs can remain stable.
- Cloudflare migration can happen as an infrastructure step after token permissions are fixed.
- If the property later needs dynamic docs or API behavior, that should be a separate ADR.
