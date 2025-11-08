# Endpoint

# Endpoint v1.6

## Purpose

Defines an API endpoint, service interface, or integration point. Represents a specific callable interface within an Application that can be invoked by agents or systems.

## v1.6 Changes

- **MIGRATED:** endpointType, httpMethod, dataFormat, endpointStatus enums abstracted to CommonEnums
- **UNCHANGED:** Core structure and required fields remain stable from v1.5

## Relationships

- Hosted by Application via applicationId
- Referenced by TripletFunctionMatrixEntry for function execution bindings
- Can be tagged via appliedTags (references TagDefinition)

## Required Fields

endpointId, name, description

## Properties (high level)

- endpointId (uuid) — Primary key
- name (string) — Display name (e.g., "CreateInvoice", "GetUserProfile")
- description (string) — Purpose and capabilities
- endpointType (enum) — REST_API, SOAP_API, GraphQL_API, gRPC_API, WebService_URL, MessageQueue_Producer, MessageQueue_Consumer, Database_Connection, File_Transfer_Location, Internal_Function_Call, Other
- url (string, uri) — Complete URL or endpoint path
- applicationId (uuid) — FK to hosting Application
- httpMethod (enum) — GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD
- requestFormat (enum) — Data format for requests (JSON, XML, Protobuf, etc.)
- responseFormat (enum) — Data format for responses
- status (enum) — Active, Deprecated, Experimental, Offline, Restricted
- authenticationRequired (boolean) — Whether auth is required
- rateLimit (integer) — Requests per minute limit

## Validation & Invariants

- additionalProperties: false
- url must be valid URI if provided
- applicationId must reference valid Application

## Examples

### Example 1: REST API Endpoint

`````json
{
  "endpointId": "ep-create-invoice",
  "name": "CreateInvoice",
  "description": "Creates a new billing invoice",
  "endpointType": "REST_API",
  "url": "[https://api.example.com/billing/v1/invoices](https://api.example.com/billing/v1/invoices)",
  "applicationId": "app-billing-svc",
  "httpMethod": "POST",
  "requestFormat": "JSON",
  "responseFormat": "JSON",
  "status": "Active",
  "authenticationRequired": true
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/Endpoint.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/Endpoint.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/Endpoint.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/Endpoint.schema.json)",
  "title": "Endpoint (v1.6)",
  "type": "object",
  "properties": {
    "endpointId": {"type": "string", "format": "uuid"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "endpointType": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/endpointType](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/endpointType)"},
    "httpMethod": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/httpMethod](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/httpMethod)"},
    "requestFormat": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/dataFormat](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/dataFormat)"},
    "status": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/endpointStatus](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/endpointStatus)"}
  },
  "required": ["endpointId", "name", "description"]
}
```