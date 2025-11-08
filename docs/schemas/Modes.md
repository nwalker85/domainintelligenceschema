# Modes

# Modes v1.6

## Purpose

Defines a collection or grouping of mode definitions for organizing behavioral patterns. Acts as a container for mode-related metadata and organization.

## v1.6 Changes

- **STABLE:** Minimal changes from v1.5, primarily URI updates
- **NOTE:** This schema is primarily organizational; the 7 canonical modes (CREATE, READ, UPDATE, DELETE, INITIATE, RESPOND, NOTIFY) are defined as enums in CommonEnums

## Relationships

- Referenced in DISDossier.referencedConstructs.modes
- Used in EntityModeMatrix to define entity-mode associations
- The canonical 7 modes are defined in CommonEnums.modeOfInteraction

## Required Fields

modesId, name

## Properties (high level)

- modesId (uuid) — Primary key
- name (string) — Display name for this mode collection
- description (string) — Purpose of this mode grouping
- modeList (array<string>) — List of mode identifiers

## Validation & Invariants

- additionalProperties: false
- This is primarily a container construct
- The 7 canonical modes of interaction are defined in CommonEnums, not here

## Examples

### Example 1: Standard Mode Collection

`````json
{
  "modesId": "modes-crud",
  "name": "CRUD Operations",
  "description": "Standard create, read, update, delete operations",
  "modeList": ["CREATE", "READ", "UPDATE", "DELETE"]
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/Modes.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/Modes.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/Modes.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/Modes.schema.json)",
  "title": "Modes (v1.6)",
  "type": "object",
  "properties": {
    "modesId": {"type": "string", "format": "uuid"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "modeList": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["modesId", "name"]
}
```