# Architecture

| Field | Value |
| --- | --- |
| Document ID | DIS-ARCH-001 |
| Status | Controlled |
| Owner | Nathan Walker |
| Domain | Domain Intelligence Schema |
| Scope | Site, schema distribution, docs, and DNS architecture |
| Related Services | GitHub Pages, `domainintelligenceschema.org`, `schemas.domainintelligenceschema.org` |
| Related ADRs | ADR-001 |
| Review Cadence | Monthly |
| Retention Rule | Retain for repository lifetime |
| Last Reviewed | 2026-05-07 |
| Next Review | 2026-06-07 |

## Boundary

This repository is the public source for Domain Intelligence Schema. It owns the landing page, schema catalog, human-readable schema docs, and release notes for the methodology/specification.

## Runtime

- Hosting: GitHub Pages.
- Root domain: `domainintelligenceschema.org`.
- Current DNS: Google Domains/Squarespace nameservers pointing at GitHub Pages.
- Website: static `index.html`.
- Schema files: versioned JSON Schema files under `schemas/v1.6.0/`.
- Docs: static docs and schema reference files under `docs/`.

## Canonical URL Policy

- Website: `https://domainintelligenceschema.org/`
- Documentation: `https://domainintelligenceschema.org/docs/`
- Schema index: `https://domainintelligenceschema.org/schemas/v1.6.0/index.json`
- Future alias: `domainintelligenceschema.ai` should redirect to `.org`.

## Cross-Linking

DIS should link to Nathan Walker's personal authority site for authorship and context. `nwalker.cc` should link back to DIS as the canonical methodology/spec property.

## Dependencies

- GitHub repository and Pages settings.
- DNS provider until Cloudflare migration.
- Cloudflare after migration.
- 1Password for registrar and API token references.
