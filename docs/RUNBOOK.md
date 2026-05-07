# Runbook

| Field | Value |
| --- | --- |
| Document ID | DIS-RUNBOOK-001 |
| Status | Controlled |
| Owner | Nathan Walker |
| Domain | Domain Intelligence Schema |
| Scope | Operator workflows for validation, deploy, DNS, and Cloudflare migration |
| Related Services | GitHub Pages, Cloudflare, 1Password |
| Related ADRs | ADR-001 |
| Review Cadence | Monthly |
| Retention Rule | Retain for repository lifetime |
| Last Reviewed | 2026-05-07 |
| Next Review | 2026-06-07 |

## Validate Schemas

```bash
./scripts/validate-schemas.sh
```

## Verify Live Site

```bash
curl -I https://domainintelligenceschema.org
curl -s https://domainintelligenceschema.org | rg 'Domain Intelligence Schema|GitHub Repository'
curl -I https://domainintelligenceschema.org/schemas/v1.6.0/index.json
```

## GitHub Pages Deploy

Push through a PR into `main`. The Pages workflow deploys the static site. Do not bypass the PR process for normal changes.

## Cloudflare Migration

1. Export current DNS records.
2. Create the Cloudflare zone after the token has account-level zone create/edit permission.
3. Add GitHub Pages A records and required `CNAME` records.
4. Add `domainintelligenceschema.ai` redirect rule when the alias zone is available.
5. Change nameservers at Squarespace.
6. Verify `200`, TLS, canonical URL, schema index, and docs after propagation.

## Token Permission Check

```bash
TOKEN="$(op item get 'Cloudflare Manage DNS' --vault ravenmask --fields credential --reveal)"
curl -s https://api.cloudflare.com/client/v4/user/tokens/verify \
  -H "Authorization: Bearer $TOKEN"
```

Zone creation requires account-level zone create/edit permission. DNS-only permissions for existing zones are not enough.
