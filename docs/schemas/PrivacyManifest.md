# PrivacyManifest

# PrivacyManifest v1.6

## Purpose

**NEW IN v1.6:** Declares data privacy requirements, GDPR/CCPA compliance mappings, and data handling policies for a dossier. Enables automated privacy compliance verification.

## v1.6 Changes

- **NEW CONSTRUCT:** Entirely new to v1.6 for privacy governance
- **MIGRATED:** dataCategory, processingPurpose, storagePolicy enums to CommonEnums

## Relationships

- Referenced by DISDossier via header.privacyManifestId
- Maps to Entity privacyClassification fields
- Supports GDPR Article 30 record-keeping requirements

## Required Fields

privacyManifestId, regulatoryFrameworks, dataInventory

## Properties (high level)

- privacyManifestId (uuid) — Primary key
- description (string) — Privacy policy summary
- regulatoryFrameworks (array<string>) — Applicable regulations (GDPR, CCPA, HIPAA, etc.)
- dataInventory (array) — Inventory of data processed:
    - dataCategory (enum) — PII, PHI, PCI, FINANCIAL, AUTHENTICATION, USAGE_ANALYTICS, OTHER
    - processingPurpose (enum) — OPERATIONS, ANALYTICS, MARKETING, SECURITY, LEGAL_COMPLIANCE
    - storagePolicy (enum) — PLAINTEXT, ENCRYPTED_AT_REST, ANONYMIZED, PSEUDONYMIZED, MASKED, DELETE_AFTER_PROCESSING
    - retentionDays (number) — Data retention period
    - dataSubjectRights (array<string>) — Rights granted (access, rectification, erasure, portability)
- consentMechanism (object) — Consent collection details
- dataProcessors (array) — Third-party processors
- lastAuditDate (date-time) — Last privacy audit

## Validation & Invariants

- enums must be valid from CommonEnums
- regulatoryFrameworks should map to recognized standards
- retentionDays should align with regulatory requirements

## Examples

### Example 1: GDPR-Compliant Manifest

`````json
{
  "privacyManifestId": "pm-billing-gdpr",
  "description": "Privacy manifest for billing system under GDPR",
  "regulatoryFrameworks": ["GDPR", "CCPA"],
  "dataInventory": [
    {
      "dataCategory": "PII",
      "processingPurpose": "OPERATIONS",
      "storagePolicy": "ENCRYPTED_AT_REST",
      "retentionDays": 2555,
      "dataSubjectRights": ["access", "rectification", "erasure", "portability"]
    },
    {
      "dataCategory": "FINANCIAL",
      "processingPurpose": "LEGAL_COMPLIANCE",
      "storagePolicy": "ENCRYPTED_AT_REST",
      "retentionDays": 2555,
      "dataSubjectRights": ["access"]
    }
  ],
  "lastAuditDate": "2025-01-15T00:00:00Z"
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/PrivacyManifest.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/PrivacyManifest.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/PrivacyManifest.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/PrivacyManifest.schema.json)",
  "title": "PrivacyManifest (v1.6)",
  "type": "object",
  "properties": {
    "privacyManifestId": {"type": "string", "format": "uuid"},
    "regulatoryFrameworks": {"type": "array", "items": {"type": "string"}},
    "dataInventory": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "dataCategory": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/dataCategory](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/dataCategory)"},
          "processingPurpose": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/processingPurpose](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/processingPurpose)"},
          "storagePolicy": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/storagePolicy](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/storagePolicy)"}
        }
      }
    }
  },
  "required": ["privacyManifestId", "regulatoryFrameworks", "dataInventory"]
}
```