# RelationshipMatrix

# RelationshipMatrix v1.6

## Purpose

Defines explicit relationships between DIS constructs. Captures semantic connections like "Entity A contains Entity B" or "Role X reports to Role Y", enabling graph-based reasoning and navigation.

## v1.6 Changes

- **STABLE:** Unchanged from v1.5 except URI updates
- **NOTE:** Generic relationship schema applicable to any construct pair

## Relationships

- Can reference any two DIS constructs via sourceId and targetId
- Enables graph traversal and dependency analysis
- Complements foreign key relationships with semantic meaning

## Required Fields

relationshipId, sourceId, targetId, relationshipType

## Properties (high level)

- relationshipId (uuid) — Primary key
- sourceId (uuid) — FK to source construct
- targetId (uuid) — FK to target construct
- relationshipType (string) — Semantic relationship type (e.g., "contains", "depends_on", "reports_to")
- bidirectional (boolean) — Whether relationship is symmetric
- metadata (object) — Additional relationship properties
- description (string) — Human-readable description

## Validation & Invariants

- sourceId and targetId must reference valid constructs
- relationshipType should be consistent across dossier

## Examples

### Example 1: Entity Containment

`````json
{
  "relationshipId": "rel-order-items",
  "sourceId": "e-order",
  "targetId": "e-order-item",
  "relationshipType": "contains",
  "bidirectional": false,
  "description": "Order contains OrderItems"
}
```

### Example 2: Role Hierarchy

`````json
{
  "relationshipId": "rel-agent-supervisor",
  "sourceId": "r-agent",
  "targetId": "r-supervisor",
  "relationshipType": "reports_to",
  "bidirectional": false,
  "description": "Agents report to Supervisors"
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/RelationshipMatrix.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/RelationshipMatrix.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/RelationshipMatrix.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/RelationshipMatrix.schema.json)",
  "title": "RelationshipMatrix (v1.6)",
  "type": "object",
  "properties": {
    "relationshipId": {"type": "string", "format": "uuid"},
    "sourceId": {"type": "string", "format": "uuid"},
    "targetId": {"type": "string", "format": "uuid"},
    "relationshipType": {"type": "string"},
    "bidirectional": {"type": "boolean", "default": false}
  },
  "required": ["relationshipId", "sourceId", "targetId", "relationshipType"]
}
```