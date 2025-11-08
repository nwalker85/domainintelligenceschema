# ValidationRule

# ValidationRule v1.6

## Purpose

Defines validation rules that can be applied to DIS constructs to ensure data quality, business logic compliance, and governance requirements. Supports JMESPath expressions for declarative validation.

## v1.6 Changes

- **MIGRATED:** validationSeverity enum abstracted to CommonEnums
- **ADDED:** JMESPath expression support for rule definitions
- **UPDATED:** Enhanced error messaging and remediation guidance

## Relationships

- Can be applied to any DIS construct via validation frameworks
- References CommonEnums for severity levels
- Supports conditional validation logic

## Required Fields

validationRuleId, name, ruleExpression, severity

## Properties (high level)

- validationRuleId (uuid) — Primary key
- name (string) — Rule name (e.g., "RequiredFieldCheck", "BusinessLogicValidation")
- description (string) — Rule purpose and behavior
- ruleExpression (string) — JMESPath expression that returns true/false
- severity (enum) — error, warning, info (from CommonEnums)
- errorMessage (string) — Message displayed when rule fails
- remediationGuidance (string) — How to fix validation failures
- applicableConstructs (array<string>) — Which construct types this rule applies to

## Validation & Invariants

- ruleExpression must be valid JMESPath
- severity must be valid enum from CommonEnums

## Examples

### Example 1: Required Field Validation

`````json
{
  "validationRuleId": "vr-entity-name-required",
  "name": "EntityNameRequired",
  "description": "Ensures all entities have non-empty names",
  "ruleExpression": "length(name) > `0`",
  "severity": "error",
  "errorMessage": "Entity name is required",
  "remediationGuidance": "Provide a descriptive name for the entity",
  "applicableConstructs": ["Entity"]
}
```

### Example 2: Business Logic Validation

`````json
{
  "validationRuleId": "vr-agent-role-check",
  "name": "AgentMustHaveAgentRole",
  "description": "Entities with entityType='agent' must have roleType='agent'",
  "ruleExpression": "entityType != 'agent' || roleType == 'agent'",
  "severity": "error",
  "errorMessage": "Agent entities must have an agent role assigned",
  "applicableConstructs": ["Entity", "Role"]
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/ValidationRule.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/ValidationRule.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/ValidationRule.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/ValidationRule.schema.json)",
  "title": "ValidationRule (v1.6)",
  "type": "object",
  "properties": {
    "validationRuleId": {"type": "string", "format": "uuid"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "ruleExpression": {"type": "string"},
    "severity": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/validationSeverity](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/validationSeverity)"},
    "errorMessage": {"type": "string"},
    "remediationGuidance": {"type": "string"}
  },
  "required": ["validationRuleId", "name", "ruleExpression", "severity"]
}
```