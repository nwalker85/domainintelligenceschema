# AccessGateMatrix

# AccessGateMatrix v1.6

## Purpose

Defines role-based access control (RBAC) rules. Specifies which Roles can perform which operations on which Entities, implementing security and authorization logic.

## v1.6 Changes

- **STABLE:** Unchanged from v1.5 except URI updates
- **NOTE:** Uses modeOfInteraction from CommonEnums for access patterns

## Relationships

- References Entity via entityId
- References Role via roleId
- Uses modeOfInteraction (one of 7 canonical modes) for permission type

## Required Fields

accessGateId, entityId, roleId, allowedModes

## Properties (high level)

- accessGateId (uuid) — Primary key
- entityId (uuid) — FK to Entity being protected
- roleId (uuid) — FK to Role with permissions
- allowedModes (array<enum>) — Which of the 7 modes this role can perform (CREATE, READ, UPDATE, DELETE, INITIATE, RESPOND, NOTIFY)
- conditions (array) — Additional authorization conditions
- description (string) — Human-readable access rule description

## Validation & Invariants

- allowedModes must contain valid modeOfInteraction values
- entityId and roleId must reference valid constructs

## Examples

### Example 1: Admin Full Access

`````json
{
  "accessGateId": "ag-admin-invoice",
  "entityId": "e-invoice",
  "roleId": "r-admin",
  "allowedModes": ["CREATE", "READ", "UPDATE", "DELETE"],
  "description": "Admins have full CRUD access to invoices"
}
```

### Example 2: Agent Read-Only

`````json
{
  "accessGateId": "ag-agent-customer",
  "entityId": "e-customer",
  "roleId": "r-support-agent",
  "allowedModes": ["READ"],
  "description": "Support agents can only read customer data"
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/AccessGateMatrix.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/AccessGateMatrix.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/AccessGateMatrix.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/AccessGateMatrix.schema.json)",
  "title": "AccessGateMatrix (v1.6)",
  "type": "object",
  "properties": {
    "accessGateId": {"type": "string", "format": "uuid"},
    "entityId": {"type": "string", "format": "uuid"},
    "roleId": {"type": "string", "format": "uuid"},
    "allowedModes": {
      "type": "array",
      "items": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/modeOfInteraction](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/modeOfInteraction)"}
    }
  },
  "required": ["accessGateId", "entityId", "roleId", "allowedModes"]
}
```