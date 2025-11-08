# Role

# Role v1.6

## Purpose

Defines a capacity or function that can be embodied by actors (humans, agents, or systems). Roles describe behavioral patterns and responsibilities that can be assigned to entities.

## v1.6 Changes

- **ADDED:** roleType enum (human, agent, system) for classification
- **ADDED:** agentArchetype enum (worker, supervisor, specialist, orchestrator) for AI agent behavioral patterns
- **MIGRATED:** All enums abstracted to CommonEnums

## Relationships

- Referenced by Entity via assignedRoleIds array
- Can be tagged via appliedTags (references TagDefinition)
- Used in AccessGateMatrix to define role-based access permissions
- foreignKeys array allows defining explicit relationships to other constructs

## Required Fields

roleId, name, description

## Properties (high level)

- roleId (uuid) — Primary key
- name (string) — Display name (e.g., "CustomerServiceAgent", "SystemAdmin")
- description (string) — Detailed purpose and responsibilities
- roleType (enum) — **(New in 1.6)** Classification: "human", "agent", or "system"
- agentArchetype (enum) — **(New in 1.6)** Behavioral pattern for AI agents: "worker", "supervisor", "specialist", "orchestrator"
- attributes (array<attributeItem>) — Role-specific attributes
- assignedEntityIds (array<uuid>) — FKs to Entities that can embody this role
- foreignKeys (array) — Definitional FKs to other constructs
- appliedTags (array) — TagDefinition applications

## Validation & Invariants

- additionalProperties: false
- If roleType is "agent", agentArchetype should typically be specified
- primaryKey is const "roleId"

## Examples

### Example 1: Human Role

`````json
{
  "roleId": "r-csr",
  "name": "CustomerServiceRep",
  "description": "Human agent handling customer inquiries",
  "roleType": "human",
  "attributes": [
    {"name": "maxConcurrentChats", "type": "integer", "value": 5}
  ]
}
```

### Example 2: AI Agent Role

`````json
{
  "roleId": "r-billing-agent",
  "name": "BillingAgent",
  "description": "Autonomous agent for billing inquiries and disputes",
  "roleType": "agent",
  "agentArchetype": "specialist",
  "attributes": [
    {"name": "expertise", "type": "string", "value": "billing"}
  ]
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/Role.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/Role.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/Role.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/Role.schema.json)",
  "title": "Role (v1.6)",
  "type": "object",
  "properties": {
    "roleId": {"type": "string", "format": "uuid"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "roleType": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/roleType](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/roleType)"},
    "agentArchetype": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/agentArchetype](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/agentArchetype)"},
    "attributes": {"type": "array"},
    "assignedEntityIds": {"type": "array", "items": {"type": "string", "format": "uuid"}}
  },
  "required": ["roleId", "name", "description"]
}
```