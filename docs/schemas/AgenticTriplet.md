# AgenticTriplet

# AgenticTriplet v1.6

## Purpose

Defines the core behavioral grammar of DIS: (Entity, Mode, Role) + execution binding. This is the fundamental construct that expresses "WHAT entity, in WHICH mode, performing WHICH role, executes WHICH function." The AgenticTriplet is the atomic unit of agent behavior.

## v1.6 Changes

- **MIGRATED:** stance enum (ACT, REACT) abstracted to CommonEnums
- **UPDATED:** Function binding structure to support multiple execution types
- **ADDED:** Support for workflow, script, and internal code execution bindings

## Relationships

- References Entity via entityId
- References modeOfInteraction (one of the 7 canonical modes from CommonEnums)
- References Role via roleId
- Binds to function execution via tripletFunctionMatrixEntryId (FK to TripletFunctionMatrixEntry)
- Can reference KnowledgeDocument for context

## Required Fields

tripletId, entityId, modeId, roleId

## Properties (high level)

- tripletId (uuid) — Primary key
- entityId (uuid) — FK to Entity (the "noun")
- modeId (string) — One of the 7 canonical modes: CREATE, READ, UPDATE, DELETE, INITIATE, RESPOND, NOTIFY
- roleId (uuid) — FK to Role (the "actor")
- stance (enum) — ACT (proactive) or REACT (responsive)
- priority (integer) — Execution priority (1-10)
- tripletFunctionMatrixEntryId (uuid) — FK to TripletFunctionMatrixEntry for execution binding
- knowledgeDocumentIds (array<uuid>) — FKs to relevant KnowledgeDocuments
- conditions (array) — Preconditions for triplet execution
- description (string) — Human-readable description

## Validation & Invariants

- additionalProperties: false
- entityId, roleId must reference valid constructs
- modeId must be one of the 7 canonical modes
- tripletFunctionMatrixEntryId must reference valid function binding

## Examples

### Example 1: Proactive Billing Agent

`````json
{
  "tripletId": "tri-billing-create",
  "entityId": "e-invoice",
  "modeId": "CREATE",
  "roleId": "r-billing-agent",
  "stance": "ACT",
  "priority": 5,
  "tripletFunctionMatrixEntryId": "tfm-create-invoice",
  "description": "BillingAgent creates invoices proactively"
}
```

### Example 2: Reactive Support Agent

`````json
{
  "tripletId": "tri-support-respond",
  "entityId": "e-ticket",
  "modeId": "RESPOND",
  "roleId": "r-support-agent",
  "stance": "REACT",
  "priority": 8,
  "tripletFunctionMatrixEntryId": "tfm-respond-ticket",
  "knowledgeDocumentIds": ["kd-support-faq"],
  "description": "SupportAgent responds to ticket updates"
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/AgenticTriplet.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/AgenticTriplet.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/AgenticTriplet.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/AgenticTriplet.schema.json)",
  "title": "AgenticTriplet (v1.6)",
  "type": "object",
  "properties": {
    "tripletId": {"type": "string", "format": "uuid"},
    "entityId": {"type": "string", "format": "uuid"},
    "modeId": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/modeOfInteraction](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/modeOfInteraction)"},
    "roleId": {"type": "string", "format": "uuid"},
    "stance": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/stance](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/stance)"},
    "priority": {"type": "integer", "minimum": 1, "maximum": 10},
    "tripletFunctionMatrixEntryId": {"type": "string", "format": "uuid"}
  },
  "required": ["tripletId", "entityId", "modeId", "roleId"]
}
```