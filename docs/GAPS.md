# Gaps

| Field | Value |
| --- | --- |
| Document ID | DIS-GAPS-001 |
| Status | Controlled |
| Owner | Nathan Walker |
| Domain | Domain Intelligence Schema |
| Scope | Known missing pieces and risks |
| Related Services | GitHub Pages, Cloudflare |
| Related ADRs | ADR-001 |
| Review Cadence | Monthly |
| Retention Rule | Retain until superseded by resolved implementation evidence |
| Last Reviewed | 2026-05-07 |
| Next Review | 2026-06-07 |

## High Priority

- Cloudflare migration is blocked until a token can create zones.
- DNS records must be captured before changing nameservers.
- Add citable definition, FAQ, examples, and versioning pages beyond the current landing page.

## Medium Priority

- Add `domainintelligenceschema.ai` redirect policy.
- Add structured data for `DefinedTermSet`, `TechArticle`, and schema catalog pages.
- Add monitor and alert routing.
- Add release checklist for schema version changes.

## Low Priority

- Add social preview image.
- Add package manager examples for generated clients.
- Add comparison docs against ontology, taxonomy, and architecture-description approaches.
