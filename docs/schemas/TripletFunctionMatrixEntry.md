# TripletFunctionMatrixEntry

# TripletFunctionMatrixEntry v1.6

## Purpose

Binds an AgenticTriplet to executable function implementations. This is the "execution binding" layer that connects behavioral grammar (Entity-Mode-Role) to actual code, APIs, or workflows.

## v1.6 Changes

- **UPDATED:** Expanded execution binding types to support workflows, scripts, and internal code
- **ADDED:** Support for JMESPath expressions in payload transformations
- **MIGRATED:** scriptLanguage enum to CommonEnums

## Relationships

- Referenced by AgenticTriplet via tripletFunctionMatrixEntryId
- Can reference Endpoint for API execution bindings
- Can reference FunctionCatalogEntry for reusable function definitions
- Supports multiple execution types: endpoint, workflow, script, internal code

## Required Fields

tripletFunctionId, executionBinding

## Properties (high level)

- tripletFunctionId (uuid) — Primary key
- executionBinding (object) — Execution configuration, one of:
    - endpointExecutionBinding: Calls an Endpoint (endpointId, httpMethod, payloadTemplate)
    - workflowExecutionBinding: Invokes a workflow (workflowId, workflowEngine)
    - scriptExecutionBinding: Executes a script (scriptContent, scriptLanguage)
    - internalCodeExecutionBinding: Calls internal code (className, methodName)
- payloadTransformations (array) — JMESPath expressions for data transformation
- errorHandling (object) — Retry logic, fallback strategies
- description (string) — Human-readable description

## Validation & Invariants

- executionBinding must contain exactly one binding type
- If endpointExecutionBinding, endpointId must reference valid Endpoint
- payloadTransformations must be valid JMESPath expressions

## Examples

### Example 1: Endpoint Binding

`````json
{
  "tripletFunctionId": "tfm-create-invoice",
  "executionBinding": {
    "endpointExecutionBinding": {
      "endpointId": "ep-create-invoice",
      "httpMethod": "POST",
      "payloadTemplate": "{\"amount\": {{amount}}, \"customerId\": {{customerId}}}"
    }
  },
  "description": "Binds invoice creation to REST API endpoint"
}
```

### Example 2: Script Binding

`````json
{
  "tripletFunctionId": "tfm-calculate-discount",
  "executionBinding": {
    "scriptExecutionBinding": {
      "scriptContent": "def calculate(amount): return amount * 0.1",
      "scriptLanguage": "python"
    }
  },
  "description": "Calculates discount using Python script"
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/TripletFunctionMatrixEntry.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/TripletFunctionMatrixEntry.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/TripletFunctionMatrixEntry.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/TripletFunctionMatrixEntry.schema.json)",
  "title": "TripletFunctionMatrixEntry (v1.6)",
  "type": "object",
  "properties": {
    "tripletFunctionId": {"type": "string", "format": "uuid"},
    "executionBinding": {
      "type": "object",
      "oneOf": [
        {"properties": {"endpointExecutionBinding": {"type": "object"}}},
        {"properties": {"scriptExecutionBinding": {"type": "object"}}}
      ]
    }
  },
  "required": ["tripletFunctionId", "executionBinding"]
}
```