# FunctionCatalogEntry

# FunctionCatalogEntry v1.6

## Purpose

Defines reusable, domain-agnostic function templates that can be referenced by TripletFunctionMatrixEntry. Enables function reuse across multiple triplets and dossiers.

## v1.6 Changes

- **UPDATED:** Enhanced with JMESPath support for input/output transformations
- **MIGRATED:** scriptLanguage enum to CommonEnums
- **ADDED:** Versioning and deprecation support

## Relationships

- Referenced by TripletFunctionMatrixEntry for function reuse
- Can reference KnowledgeDocument for function documentation
- Supports tagging via appliedTags

## Required Fields

functionId, name, functionType

## Properties (high level)

- functionId (uuid) — Primary key
- name (string) — Function name (e.g., "CalculateDiscount", "SendEmail")
- description (string) — Purpose and behavior
- functionType (string) — Classification (calculation, notification, integration, etc.)
- inputSchema (object) — JSON schema for input parameters
- outputSchema (object) — JSON schema for output
- implementation (object) — Function implementation details
- version (string) — Semantic version
- deprecated (boolean) — Deprecation flag
- replacedBy (uuid) — FK to replacement function if deprecated

## Validation & Invariants

- inputSchema and outputSchema should be valid JSON Schema
- If deprecated is true, replacedBy should be specified

## Examples

### Example 1: Calculation Function

`````json
{
  "functionId": "func-discount-calc",
  "name": "CalculateDiscount",
  "description": "Calculates discount based on customer tier and order amount",
  "functionType": "calculation",
  "inputSchema": {
    "type": "object",
    "properties": {
      "amount": {"type": "number"},
      "tier": {"type": "string"}
    },
    "required": ["amount", "tier"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "discountAmount": {"type": "number"},
      "finalAmount": {"type": "number"}
    }
  },
  "version": "1.2.0",
  "deprecated": false
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/FunctionCatalogEntry.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/FunctionCatalogEntry.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/FunctionCatalogEntry.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/FunctionCatalogEntry.schema.json)",
  "title": "FunctionCatalogEntry (v1.6)",
  "type": "object",
  "properties": {
    "functionId": {"type": "string", "format": "uuid"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "functionType": {"type": "string"},
    "inputSchema": {"type": "object"},
    "outputSchema": {"type": "object"},
    "version": {"type": "string"},
    "deprecated": {"type": "boolean", "default": false}
  },
  "required": ["functionId", "name", "functionType"]
}
```