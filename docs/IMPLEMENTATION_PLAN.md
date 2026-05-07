# Implementation Plan

| Field | Value |
| --- | --- |
| Document ID | DIS-PLAN-001 |
| Status | Active |
| Owner | Nathan Walker |
| Domain | Domain Intelligence Schema |
| Scope | Current build plan for the first separate property |
| Related Services | GitHub Pages, Cloudflare, `nwalker.cc` |
| Related ADRs | ADR-001 |
| Review Cadence | Weekly while active |
| Retention Rule | Retain until superseded by next active plan |
| Last Reviewed | 2026-05-07 |
| Next Review | 2026-05-14 |

## Automated Work

- Clone the existing public DIS repository into the portfolio workspace.
- Add controlled repo documentation.
- Verify the live site is serving from GitHub Pages.
- Document the Cloudflare zone-creation blocker.
- Prepare DNS migration runbook.

## Human-Owned Work

- Update Cloudflare token permissions or create a new account-level token.
- Approve nameserver changes at Squarespace.
- Decide whether `schemas.domainintelligenceschema.org` remains a subdomain of the same property or gets a separate deployment boundary.
- Approve final positioning copy for citable methodology pages.

## Immediate Checklist

1. Merge controlled docs.
2. Add FAQ and examples.
3. Create Cloudflare zone once token permission is available.
4. Cut over nameservers after records are staged.
5. Add monitors and alert routing.
