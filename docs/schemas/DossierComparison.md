# DossierComparison

# DossierComparison v1.6

## Purpose

**NEW IN v1.6:** Captures structured comparisons between dossiers or versions. Enables delta analysis, migration planning, and A/B testing of domain models.

## v1.6 Changes

- **NEW CONSTRUCT:** Entirely new to v1.6 for version control and comparison

## Relationships

- Referenced by DISDossier via header.comparisonId
- Links two dossiers for comparison (baseline vs. candidate)
- Supports migration and evolution tracking

## Required Fields

comparisonId, baselineDossierId, candidateDossierId

## Properties (high level)

- comparisonId (uuid) — Primary key
- baselineDossierId (uuid) — FK to baseline/original dossier
- candidateDossierId (uuid) — FK to candidate/new dossier
- comparisonDate (date-time) — When comparison was performed
- description (string) — Comparison purpose
- differences (array) — Structured list of differences:
    - constructType (string) — Type of construct (Entity, Role, etc.)
    - changeType (string) — ADDED, REMOVED, MODIFIED, UNCHANGED
    - constructId (uuid) — ID of affected construct
    - details (object) — Specific changes
- summary (object) — High-level comparison metrics:
    - totalChanges (number) — Total number of changes
    - breakingChanges (number) — Number of breaking changes
    - compatibilityScore (number) — 0-100 compatibility percentage

## Validation & Invariants

- baselineDossierId and candidateDossierId must reference valid dossiers
- changeType should be consistent enumeration

## Examples

### Example 1: Version Comparison

`````json
{
  "comparisonId": "cmp-v1-v2",
  "baselineDossierId": "doss-billing-v1",
  "candidateDossierId": "doss-billing-v2",
  "comparisonDate": "2025-03-15T10:00:00Z",
  "description": "Comparison of billing domain v1.0 to v2.0",
  "differences": [
    {
      "constructType": "Entity",
      "changeType": "ADDED",
      "constructId": "e-payment-method",
      "details": {"name": "PaymentMethod"}
    },
    {
      "constructType": "Role",
      "changeType": "MODIFIED",
      "constructId": "r-billing-agent",
      "details": {"field": "agentArchetype", "old": "worker", "new": "specialist"}
    }
  ],
  "summary": {
    "totalChanges": 12,
    "breakingChanges": 2,
    "compatibilityScore": 85
  }
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/DossierComparison.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/DossierComparison.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/DossierComparison.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/DossierComparison.schema.json)",
  "title": "DossierComparison (v1.6)",
  "type": "object",
  "properties": {
    "comparisonId": {"type": "string", "format": "uuid"},
    "baselineDossierId": {"type": "string", "format": "uuid"},
    "candidateDossierId": {"type": "string", "format": "uuid"},
    "comparisonDate": {"type": "string", "format": "date-time"},
    "differences": {"type": "array"},
    "summary": {"type": "object"}
  },
  "required": ["comparisonId", "baselineDossierId", "candidateDossierId"]
}
```