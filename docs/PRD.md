# Product Requirements

| Field | Value |
| --- | --- |
| Document ID | DIS-PRD-001 |
| Status | Controlled |
| Owner | Nathan Walker |
| Domain | Domain Intelligence Schema |
| Scope | Public methodology/spec site and schema catalog |
| Related Services | `domainintelligenceschema.org`, `schemas.domainintelligenceschema.org`, GitHub Pages |
| Related ADRs | ADR-001 |
| Review Cadence | Monthly |
| Retention Rule | Retain for repository lifetime |
| Last Reviewed | 2026-05-07 |
| Next Review | 2026-06-07 |

## Problem

Enterprises need a vendor-neutral way to model business domains, agent behavior, execution bindings, and governance before deploying agentic AI systems. Existing portfolio or opinion pages are not enough; the methodology needs stable, citable, versioned artifacts.

## Goals

- Publish Domain Intelligence Schema as a citable public methodology and schema.
- Maintain stable canonical URLs for the website, documentation, and versioned schema files.
- Make DIS understandable to humans and usable by tools.
- Cross-link back to Nathan Walker's personal authority site without making the personal site the schema runtime.
- Prepare the property for Cloudflare migration without breaking GitHub Pages.

## Non-Goals

- Host Ravenhelm company content.
- Host Runestack product marketing.
- Replace package registries or language-specific SDK repositories.
- Store secrets or registrar credentials.

## MVP Scope

- Public landing page at `https://domainintelligenceschema.org`.
- Versioned JSON Schema files under `schemas/v1.6.0/`.
- Human-readable schema docs under `docs/schemas/`.
- CNAME for GitHub Pages.
- Controlled documentation layout and runbook.

## Success Signals

- Root domain returns `200`.
- Schema index returns `200`.
- README and docs explain what DIS is, how to validate schemas, and where canonical URLs live.
- Cloudflare migration has a documented runbook and token blocker.
