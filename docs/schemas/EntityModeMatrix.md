# EntityModeMatrix

# EntityModeMatrix v1.6

## Purpose

Defines which modes of interaction are applicable to specific entities. Maps the behavioral capabilities of each entity by specifying which of the 7 canonical modes it supports.

## v1.6 Changes

- **STABLE:** Core structure unchanged from v1.5
- **UPDATED:** Now uses CommonEnums.modeOfInteraction for mode references

## Relationships

- References Entity via entityId
- Uses modeOfInteraction from CommonEnums for supported modes
- Complements AgenticTriplet by defining entity capabilities

## Required Fields

entityModeId, entityId, supportedModes

## Properties (high level)

- entityModeId (uuid) — Primary key
- entityId (uuid) — FK to Entity
- supportedModes (array<enum>) — Which of the 7 modes apply to this entity (CREATE, READ, UPDATE, DELETE, INITIATE, RESPOND, NOTIFY)
- modeConfiguration (object) — Mode-specific configuration
- description (string) — Human-readable description

## Validation & Invariants

- supportedModes must contain valid modeOfInteraction values
- entityId must reference valid Entity
- At least one mode must be specified

## Examples

### Example 1: CRUD Entity

`````json
{
  "entityModeId": "em-invoice-crud",
  "entityId": "e-invoice",
  "supportedModes": ["CREATE", "READ", "UPDATE", "DELETE"],
  "description": "Invoice entity supports all CRUD operations"
}
```

### Example 2: Notification Entity

`````json
{
  "entityModeId": "em-alert-notify",
  "entityId": "e-alert",
  "supportedModes": ["CREATE", "READ", "NOTIFY"],
  "description": "Alert entity can be created, read, and triggers notifications"
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/EntityModeMatrix.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/EntityModeMatrix.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/EntityModeMatrix.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/EntityModeMatrix.schema.json)",
  "title": "EntityModeMatrix (v1.6)",
  "type": "object",
  "properties": {
    "entityModeId": {"type": "string", "format": "uuid"},
    "entityId": {"type": "string", "format": "uuid"},
    "supportedModes": {
      "type": "array",
      "items": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/modeOfInteraction](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/modeOfInteraction)"},
      "minItems": 1
    }
  },
  "required": ["entityModeId", "entityId", "supportedModes"]
}
```