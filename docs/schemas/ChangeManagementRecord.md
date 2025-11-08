# ChangeManagementRecord

# ChangeManagementRecord v1.6

## Purpose

**NEW IN v1.6:** Tracks formal change requests, approvals, and deployments for dossiers. Implements ITIL-style change management and audit trails for production deployments.

## v1.6 Changes

- **NEW CONSTRUCT:** Entirely new to v1.6 for enterprise governance
- **MIGRATED:** changeManagementStatus enum to CommonEnums

## Relationships

- Links to DISDossier via dossierId
- Supports change approval workflows
- Maintains audit trail for compliance

## Required Fields

changeRecordId, dossierId, changeDescription, requestedBy, requestedDate, status

## Properties (high level)

- changeRecordId (uuid) — Primary key
- dossierId (uuid) — FK to DISDossier being changed
- changeDescription (string) — Description of changes
- changeType (string) — Type (FEATURE, BUGFIX, SECURITY, CONFIGURATION, etc.)
- impactLevel (string) — LOW, MEDIUM, HIGH, CRITICAL
- requestedBy (string) — Who requested the change
- requestedDate (date-time) — When change was requested
- status (enum) — PENDING_REVIEW, APPROVED, REJECTED, IMPLEMENTED, CANCELLED
- approvers (array) — Approval chain:
    - approverName (string) — Approver name
    - approvalDate (date-time) — When approved
    - comments (string) — Approval comments
- implementationDate (date-time) — When change was deployed
- rollbackPlan (string) — How to rollback if needed
- affectedComponents (array<string>) — Which constructs are affected
- testResults (object) — Pre-deployment testing results

## Validation & Invariants

- status must be valid enum from CommonEnums
- If status is APPROVED, at least one approver is required
- If status is IMPLEMENTED, implementationDate is required
- dossierId must reference valid DISDossier

## Examples

### Example 1: Feature Change Request

`````json
{
  "changeRecordId": "cr-2025-03-001",
  "dossierId": "doss-billing-v2",
  "changeDescription": "Add multi-currency support to billing agent",
  "changeType": "FEATURE",
  "impactLevel": "HIGH",
  "requestedBy": "[product-team@example.com](mailto:product-team@example.com)",
  "requestedDate": "2025-03-01T09:00:00Z",
  "status": "APPROVED",
  "approvers": [
    {
      "approverName": "Jane Smith (Product Owner)",
      "approvalDate": "2025-03-02T14:30:00Z",
      "comments": "Approved pending security review"
    },
    {
      "approverName": "John Doe (Security Lead)",
      "approvalDate": "2025-03-03T10:15:00Z",
      "comments": "Security review complete, approved for deployment"
    }
  ],
  "rollbackPlan": "Revert to doss-billing-v1.8 if critical issues detected",
  "affectedComponents": ["Entity:Invoice", "Endpoint:CreateInvoice", "AgenticTriplet:tri-billing-create"]
}
```

### Example 2: Security Patch

`````json
{
  "changeRecordId": "cr-2025-03-005",
  "dossierId": "doss-customer-portal",
  "changeDescription": "Security patch for authentication vulnerability",
  "changeType": "SECURITY",
  "impactLevel": "CRITICAL",
  "requestedBy": "[security-team@example.com](mailto:security-team@example.com)",
  "requestedDate": "2025-03-10T08:00:00Z",
  "status": "IMPLEMENTED",
  "approvers": [
    {
      "approverName": "Security Committee",
      "approvalDate": "2025-03-10T09:00:00Z",
      "comments": "Emergency approval granted"
    }
  ],
  "implementationDate": "2025-03-10T12:00:00Z",
  "rollbackPlan": "N/A - security fix cannot be rolled back",
  "affectedComponents": ["Endpoint:AuthenticateUser"]
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/ChangeManagementRecord.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/ChangeManagementRecord.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/ChangeManagementRecord.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/ChangeManagementRecord.schema.json)",
  "title": "ChangeManagementRecord (v1.6)",
  "type": "object",
  "properties": {
    "changeRecordId": {"type": "string", "format": "uuid"},
    "dossierId": {"type": "string", "format": "uuid"},
    "changeDescription": {"type": "string"},
    "requestedBy": {"type": "string"},
    "requestedDate": {"type": "string", "format": "date-time"},
    "status": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/changeManagementStatus](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/changeManagementStatus)"},
    "approvers": {"type": "array"},
    "implementationDate": {"type": "string", "format": "date-time"}
  },
  "required": ["changeRecordId", "dossierId", "changeDescription", "requestedBy", "requestedDate", "status"]
}
```