# TagDefinition

# TagDefinition v1.6

## Purpose

Defines reusable metadata tags that can be applied to any DIS construct for categorization, search, and filtering. Enables flexible taxonomy and organization across the domain model.

## v1.6 Changes

- **STABLE:** Unchanged from v1.5 except URI updates
- **NOTE:** Supports controlled vocabularies via allowedValues

## Relationships

- Applied to constructs via appliedTags arrays (Entity, Role, Application, etc.)
- Enables cross-cutting categorization and search

## Required Fields

tagDefinitionId, name

## Properties (high level)

- tagDefinitionId (uuid) — Primary key
- name (string) — Tag name (e.g., "Department", "Priority", "Customer Segment")
- description (string) — Tag purpose
- allowedValues (array<string>) — Controlled vocabulary (optional; if empty, freeform)
- dataType (string) — Value type (string, number, boolean, date)
- multipleValuesAllowed (boolean) — Whether multiple values can be selected

## Validation & Invariants

- If allowedValues is specified, applied values must match
- dataType should be consistent with allowedValues

## Examples

### Example 1: Controlled Vocabulary Tag

`````json
{
  "tagDefinitionId": "tag-priority",
  "name": "Priority",
  "description": "Priority level classification",
  "allowedValues": ["Low", "Medium", "High", "Critical"],
  "dataType": "string",
  "multipleValuesAllowed": false
}
```

### Example 2: Freeform Tag

`````json
{
  "tagDefinitionId": "tag-notes",
  "name": "Notes",
  "description": "Freeform notes field",
  "allowedValues": [],
  "dataType": "string",
  "multipleValuesAllowed": true
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/TagDefinition.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/TagDefinition.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/TagDefinition.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/TagDefinition.schema.json)",
  "title": "TagDefinition (v1.6)",
  "type": "object",
  "properties": {
    "tagDefinitionId": {"type": "string", "format": "uuid"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "allowedValues": {"type": "array", "items": {"type": "string"}},
    "dataType": {"type": "string"},
    "multipleValuesAllowed": {"type": "boolean", "default": false}
  },
  "required": ["tagDefinitionId", "name"]
}
```