# DISDossier

# DISDossier v1.6

## Purpose

Standardized JSON package for a complete, domain-specific DIS model. Acts as the root container and manifest for all DIS constructs within a domain. This is the top-level document that packages entities, roles, applications, endpoints, and all other constructs into a deployable unit.

## v1.6 Changes

- **REMOVED:** AmeliaBotInstance references (breaking change from v1.5)
- **ADDED:** dossierType and dossierStatus enums to header for lifecycle management
- **ADDED:** References to new v1.6 governance constructs in header:
    - privacyManifestId → PrivacyManifest
    - valueEngineeringProfileId → ValueEngineeringProfile
    - telemetryConfigurationId → TelemetryConfiguration
    - comparisonId → DossierComparison
- **MIGRATED:** All enums abstracted to CommonEnums
- **UPDATED:** disSpecificationRef locked to "1.6.0"

## Relationships

- Contains references to all 14 core schema types in dossierSpecificDefinitions
- References CommonEnums for dossierType, dossierStatus, and modeOfInteraction
- Links to PrivacyManifest via header.privacyManifestId
- Links to ValueEngineeringProfile via header.valueEngineeringProfileId
- Links to TelemetryConfiguration via header.telemetryConfigurationId
- Links to DossierComparison via header.comparisonId
- Supports relatedDossierId for dossier chaining (e.g., design → discovery)

## Required Fields

header.dossierId, header.domainName, header.version, header.disSpecificationRef, dossierSpecificDefinitions

## Properties (high level)

**header (object)** — Metadata about the dossier:

- dossierId (uuid) — Primary key
- domainName (string) — Domain name
- version (string) — Semantic version of this dossier (e.g., "1.3.4")
- author (string) — Author name
- disSpecificationRef (string) — Locked to "1.6.0"
- description (string) — Dossier description
- lastModified (date-time) — Last modification timestamp
- deploymentEnvironment (string) — Target environment (e.g., "Staging", "Prod")
- dossierType (enum) — Type classification (DISCOVERY, DESIGN, DEPLOYMENT, MARKETPLACE_ITEM, TEMPLATE)
- dossierStatus (enum) — Lifecycle status (DRAFT, IN_REVIEW, APPROVED, PUBLISHED, DEPRECATED)
- relatedDossierId (uuid) — Optional FK to related dossier
- comparisonId (uuid) — Optional FK to DossierComparison
- privacyManifestId (uuid) — Optional FK to PrivacyManifest
- valueEngineeringProfileId (uuid) — Optional FK to ValueEngineeringProfile
- telemetryConfigurationId (uuid) — Optional FK to TelemetryConfiguration

**schemaReferences (array)** — External schema references with name and URL

**referencedConstructs (object)** — Lists of globally defined, reused construct IDs:

- entities, modes, modesOfInteraction, roles, applications, endpoints, knowledgeDocuments, tagDefinitions, functionCatalogEntries

**dossierSpecificDefinitions (object)** — Full JSON definitions for constructs owned by this dossier:

- entities, modes, roles, applications, endpoints, knowledgeDocuments, tagDefinitions, agenticTriplets, functionCatalogEntries, entityModeMatrixEntries, relationshipMatrixEntries, accessGateMatrixEntries, tripletFunctionMatrixEntries

## Validation & Invariants

- additionalProperties: false on header
- disSpecificationRef must be "1.6.0"
- All schema references in dossierSpecificDefinitions must use v1.6.0 URIs
- Migration from v1.5 requires removing AmeliaBotInstance references

## Examples

### Example 1: Minimal Dossier

`````json
{
  "header": {
    "dossierId": "doss-12345",
    "domainName": "CustomerSupport",
    "version": "1.0.0",
    "disSpecificationRef": "1.6.0",
    "author": "Platform Team",
    "dossierType": "DESIGN",
    "dossierStatus": "DRAFT"
  },
  "dossierSpecificDefinitions": {
    "entities": [],
    "roles": []
  }
}
```

### Example 2: Dossier with Governance Links

`````json
{
  "header": {
    "dossierId": "doss-67890",
    "domainName": "BillingAutomation",
    "version": "2.1.0",
    "disSpecificationRef": "1.6.0",
    "dossierType": "DEPLOYMENT",
    "dossierStatus": "APPROVED",
    "privacyManifestId": "pm-11111",
    "valueEngineeringProfileId": "vep-22222",
    "telemetryConfigurationId": "tc-33333",
    "deploymentEnvironment": "Production"
  },
  "dossierSpecificDefinitions": {
    "entities": [
      {
        "entityId": "e-invoice",
        "name": "Invoice",
        "description": "Billing invoice entity",
        "entityType": "data"
      }
    ],
    "roles": [
      {
        "roleId": "r-billing-agent",
        "name": "BillingAgent",
        "roleType": "agent"
      }
    ]
  }
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/DISDossier.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/DISDossier.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/DISDossier.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/DISDossier.schema.json)",
  "title": "DISDossier (v1.6)",
  "type": "object",
  "properties": {
    "header": {
      "type": "object",
      "properties": {
        "dossierId": {"type": "string", "format": "uuid"},
        "domainName": {"type": "string"},
        "version": {"type": "string"},
        "author": {"type": "string"},
        "disSpecificationRef": {"type": "string", "const": "1.6.0"},
        "dossierType": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/dossierType](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/dossierType)"},
        "dossierStatus": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/dossierStatus](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/dossierStatus)"},
        "privacyManifestId": {"type": "string", "format": "uuid"},
        "valueEngineeringProfileId": {"type": "string", "format": "uuid"},
        "telemetryConfigurationId": {"type": "string", "format": "uuid"},
        "comparisonId": {"type": "string", "format": "uuid"}
      },
      "required": ["dossierId", "domainName", "version", "disSpecificationRef"]
    },
    "dossierSpecificDefinitions": {
      "type": "object",
      "properties": {
        "entities": {"type": "array", "items": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/Entity.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/Entity.schema.json)"}},
        "roles": {"type": "array", "items": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/Role.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/Role.schema.json)"}},
        "agenticTriplets": {"type": "array", "items": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/AgenticTriplet.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/AgenticTriplet.schema.json)"}}
      }
    }
  },
  "required": ["header", "dossierSpecificDefinitions"]
}
```