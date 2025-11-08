# ModeOfInteractionRegistryEntry

# ModeOfInteractionRegistryEntry v1.6

## Purpose

Defines metadata and constraints for one of the 7 canonical modes of interaction. Provides a registry entry that documents behavioral patterns, rules, and semantics for each mode.

## v1.6 Changes

- **STABLE:** Core structure unchanged from v1.5
- **NOTE:** The 7 modes themselves (CREATE, READ, UPDATE, DELETE, INITIATE, RESPOND, NOTIFY) are now defined in CommonEnums.modeOfInteraction

## Relationships

- Documents one of the 7 canonical modes from CommonEnums.modeOfInteraction
- Referenced by AgenticTriplet via modeId
- Used in EntityModeMatrix for entity-mode associations

## Required Fields

modeId, name

## Properties (high level)

- modeId (string) — One of the 7 canonical modes
- name (string) — Display name (CREATE, READ, UPDATE, DELETE, INITIATE, RESPOND, NOTIFY)
- description (string) — Detailed behavioral semantics
- rules (array) — Constraints and behavioral rules
- metadata (object) — Additional mode metadata

## Validation & Invariants

- modeId must be one of the 7 canonical modes
- This is primarily documentation/metadata schema

## Examples

### Example 1: CREATE Mode Registry

`````json
{
  "modeId": "CREATE",
  "name": "CREATE",
  "description": "Proactively generates new domain objects or initiates new processes",
  "rules": [
    "Must validate input before creation",
    "Must return created object identifier"
  ]
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/ModeOfInteractionRegistryEntry.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/ModeOfInteractionRegistryEntry.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/ModeOfInteractionRegistryEntry.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/ModeOfInteractionRegistryEntry.schema.json)",
  "title": "ModeOfInteractionRegistryEntry (v1.6)",
  "type": "object",
  "properties": {
    "modeId": {"type": "string"},
    "name": {"type": "string"},
    "description": {"type": "string"}
  },
  "required": ["modeId", "name"]
}
```