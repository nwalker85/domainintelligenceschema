# Entity

# Entity v1.6

## Purpose

Defines a deployable AI agent or a core data object within the domain. It is the central "noun" of the DIS model (e.g., "Ticket", "User", "BillingAgent"). Entities can represent both data constructs and autonomous agents.

## v1.6 Changes

- **REMOVED:** proxiedAmeliaBotInstanceId (breaking change - removes vendor lock-in to Amelia)
- **ADDED:** entityType enum ("data" | "agent") for framework-agnostic agent classification
- **ADDED:** privacyClassification enum for linking to privacy framework
- **MIGRATED:** All enums abstracted to CommonEnums

## Relationships

- References Role via assignedRoleIds array
- Can be tagged via appliedTags (references TagDefinition)
- Can be classified as "agent" via entityType
- foreignKeys array allows defining explicit relationships to other entities
- Used in AccessGateMatrix for permission rules
- Used in EntityModeMatrix for capability mapping
- Used in AgenticTriplet as the "subject" of behavioral grammar

## Required Fields

entityId, name, description

## Properties (high level)

- entityId (uuid) — Primary key (const: entityId)
- name (string) — Human-readable name (e.g., "Customer", "Ticket", "BillingAgent")
- description (string) — Purpose/capabilities
- entityType (enum) — **(New in 1.6)** "data" (default) or "agent"
- privacyClassification (enum) — **(New in 1.6)** Default privacy level: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED, PII, PHI
- alternateNames (array<string>) — Aliases or synonyms
- primaryKey (string) — Primary key name for the entity type
- foreignKeys (array) — Definitional FKs to other constructs:
    - keyName (string) — FK field name
    - referencesEntity (string) — Referenced entity name or ID
    - description (string) — Relationship description
- attributes (array<attributeItem>) — Core data fields:
    - name (string) — Attribute name
    - type (string) — Data type
    - description (string) — Attribute purpose
    - value (any) — Default or example value
- assignedRoleIds (array<uuid>) — FKs to Role constructs this entity can embody
- appliedTags (array) — TagDefinition applications:
    - tagDefinitionId (uuid) — FK to TagDefinition
    - selectedValues (array<string>) — Selected tag values

## Validation & Invariants

- additionalProperties: false
- The proxiedAmeliaBotInstanceId field from v1.5 is no longer valid and must be migrated
- A compiler/validator must ensure that if entityType is "agent", the entity also has an assigned Role of roleType: "agent"
- primaryKey is const "entityId"

## Examples

### Example 1: A "data" entity (Customer)

`````json
{
  "entityId": "e-customer",
  "name": "Customer",
  "description": "Represents a customer or client",
  "entityType": "data",
  "privacyClassification": "PII",
  "attributes": [
    {
      "name": "email",
      "type": "string",
      "description": "Customer email address",
      "value": null
    },
    {
      "name": "tier",
      "type": "string",
      "description": "Customer tier (bronze, silver, gold, platinum)",
      "value": "bronze"
    }
  ],
  "assignedRoleIds": ["r-end-user"]
}
```

### Example 2: An "agent" entity (BillingAgent)

`````json
{
  "entityId": "e-billing-agent",
  "name": "BillingAgent",
  "description": "Autonomous agent for handling billing inquiries, invoice generation, and payment disputes",
  "entityType": "agent",
  "privacyClassification": "INTERNAL",
  "attributes": [
    {
      "name": "specialization",
      "type": "string",
      "description": "Agent specialization area",
      "value": "billing"
    },
    {
      "name": "maxConcurrentTasks",
      "type": "integer",
      "description": "Maximum concurrent tasks",
      "value": 10
    }
  ],
  "assignedRoleIds": ["r-billing-agent"]
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/Entity.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/Entity.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/Entity.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/Entity.schema.json)",
  "title": "Entity (v1.6)",
  "description": "v1.6: A deployable AI agent or core data object. Removes vendor lock-in (AmeliaBotInstance) and adds entityType to formally classify agents.",
  "type": "object",
  "properties": {
    "entityId": {"type": "string", "format": "uuid"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "entityType": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/entityType](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/entityType)"},
    "privacyClassification": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/privacyClassification](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/privacyClassification)"},
    "alternateNames": {"type": "array", "items": {"type": "string"}},
    "primaryKey": {"type": "string", "const": "entityId"},
    "foreignKeys": {"type": "array"},
    "attributes": {"type": "array"},
    "assignedRoleIds": {"type": "array", "items": {"type": "string", "format": "uuid"}},
    "appliedTags": {"type": "array"}
  },
  "required": ["entityId", "name", "description"],
  "additionalProperties": false
}
```