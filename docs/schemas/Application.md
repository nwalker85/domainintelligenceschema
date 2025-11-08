# Application

# Application v1.6

## Purpose

Defines a software application or system component that can host endpoints, entities, or services. Represents the runtime environment or platform where domain logic executes.

## v1.6 Changes

- **MIGRATED:** applicationType enum abstracted to CommonEnums
- **UNCHANGED:** Core structure and required fields remain stable from v1.5

## Relationships

- Contains Endpoints via the endpoints array
- Referenced by Endpoint via applicationId
- Can be tagged via appliedTags (references TagDefinition)
- foreignKeys array allows defining explicit relationships

## Required Fields

applicationId, name, description

## Properties (high level)

- applicationId (uuid) — Primary key
- name (string) — Display name (e.g., "CustomerPortal", "BillingMicroservice")
- description (string) — Purpose and capabilities
- applicationType (enum) — Classification: WebApp, MobileApp, DesktopApp, Microservice, API, Database, LegacySystem, SaaSPlatform, EnterpriseServiceBus, Other
- baseUrl (string, uri) — Base URL for the application
- version (string) — Application version
- endpoints (array<Endpoint>) — Endpoints hosted by this application
- attributes (array<attributeItem>) — Application-specific attributes
- foreignKeys (array) — Definitional FKs
- appliedTags (array) — TagDefinition applications

## Validation & Invariants

- additionalProperties: false
- baseUrl must be valid URI if provided
- primaryKey is const "applicationId"

## Examples

### Example 1: Microservice Application

`````json
{
  "applicationId": "app-billing-svc",
  "name": "BillingService",
  "description": "Core billing and payment processing microservice",
  "applicationType": "Microservice",
  "baseUrl": "[https://api.example.com/billing](https://api.example.com/billing)",
  "version": "2.3.1"
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/Application.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/Application.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/Application.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/Application.schema.json)",
  "title": "Application (v1.6)",
  "type": "object",
  "properties": {
    "applicationId": {"type": "string", "format": "uuid"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "applicationType": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/applicationType](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/applicationType)"},
    "baseUrl": {"type": "string", "format": "uri"},
    "version": {"type": "string"}
  },
  "required": ["applicationId", "name", "description"]
}
```