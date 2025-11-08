# CommonEnums

# CommonEnums v1.6

## Purpose

A centralized manifest of all controlled vocabularies (enums) used throughout the DIS 1.6 specification. This construct implements the DRY (Don't Repeat Yourself) principle by extracting all enum definitions into a single, reusable schema.

## v1.6 Changes

- **NEW CONSTRUCT:** CommonEnums is entirely new to v1.6, implementing the Enum Extraction Plan.
- **MIGRATED:** All enum definitions from individual v1.5 schemas have been centralized here.
- **ADDED:** 31 enum definitions covering all controlled vocabularies across the specification.

## Relationships

- Referenced by all 22 other v1.6 schemas that use controlled vocabularies
- Provides enums for: Entity, Role, Application, Endpoint, KnowledgeDocument, AgenticTriplet, DISDossier, ValidationRule, ValueEngineeringProfile, PrivacyManifest, TelemetryConfiguration, MarketplaceEntry, ChangeManagementRecord

## Required Fields

None (this is a definitions-only schema)

## Properties (high level)

This schema contains no properties, only definitions. It provides 31 enum definitions:

**Application/Endpoint:**

- applicationType — Classification of Application constructs (WebApp, MobileApp, API, etc.)
- endpointType — Classification of Endpoint constructs (REST_API, GraphQL_API, etc.)
- httpMethod — HTTP methods (GET, POST, PUT, DELETE, etc.)
- dataFormat — Data formats (JSON, XML, Protobuf, etc.)
- endpointStatus — Endpoint operational status

**Entity/Role:**

- entityType — Entity classification (data, agent)
- roleType — Role classification (human, agent, system)
- agentArchetype — Agent behavioral patterns (worker, supervisor, specialist, orchestrator)
- privacyClassification — Data privacy levels (PUBLIC, INTERNAL, PII, PHI, etc.)

**Behavioral:**

- modeOfInteraction — The 7 canonical modes (CREATE, READ, UPDATE, DELETE, INITIATE, RESPOND, NOTIFY)
- stance — AgenticTriplet stance (ACT, REACT)
- scriptLanguage — Script execution languages (python, javascript, shell, etc.)

**Knowledge:**

- documentType — KnowledgeDocument types (FAQ, Manual, Policy, Guide, etc.)

**Dossier:**

- dossierType — DISDossier classifications (DISCOVERY, DESIGN, DEPLOYMENT, MARKETPLACE_ITEM, TEMPLATE)
- dossierStatus — Lifecycle status (DRAFT, IN_REVIEW, APPROVED, PUBLISHED, DEPRECATED)

**Validation & Metrics:**

- validationSeverity — ValidationRule severity (error, warning, info)
- metricUnit — Measurement units (SECONDS, MINUTES, PERCENTAGE, COUNT, CURRENCY)
- currency — ISO 4217 currency codes (USD, EUR, GBP, etc.)

**Privacy & Governance:**

- dataCategory — Privacy data categories (PII, PHI, PCI, FINANCIAL, etc.)
- processingPurpose — Data processing purposes (OPERATIONS, ANALYTICS, MARKETING, etc.)
- storagePolicy — Storage policies (PLAINTEXT, ENCRYPTED_AT_REST, ANONYMIZED, etc.)

**Telemetry:**

- telemetryLogLevel — Log verbosity (NONE, ERROR, INFO, DEBUG, TRACE)
- telemetryMetricType — Metric types (COUNTER, GAUGE, HISTOGRAM)

**Marketplace:**

- marketplaceCategory — Marketplace categories (FINANCE, HEALTHCARE, IT_SERVICE_MANAGEMENT, etc.)
- marketplacePricingModel — Pricing models (FREE, ONE_TIME_PURCHASE, SUBSCRIPTION_PER_SEAT, etc.)

**Change Management:**

- changeManagementStatus — Change record status (PENDING_REVIEW, APPROVED, REJECTED, IMPLEMENTED, CANCELLED)

## Validation & Invariants

- additionalProperties: false
- This schema contains only definitions; it has no required fields or instance properties
- All enums must be referenced via $ref from other schemas
- Enum values must remain stable across minor versions for backward compatibility

## Examples

### Example 1: Referencing an enum from another schema

`````json
{
  "entityType": {
    "description": "Classification of the entity",
    "$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/entityType](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/entityType)"
  }
}
```

### Example 2: Using multiple enum references

`````json
{
  "privacyClassification": {
    "$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/privacyClassification](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/privacyClassification)"
  },
  "roleType": {
    "$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/roleType](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/roleType)"
  }
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json)",
  "title": "CommonEnums (v1.6)",
  "description": "v1.6: A new, centralized manifest of all controlled vocabularies (enums) used throughout the DIS 1.6 specification.",
  "type": "object",
  "properties": {},
  "definitions": {
    "applicationType": {
      "type": "string",
      "enum": ["WebApp", "MobileApp", "DesktopApp", "Microservice", "API", "Database", "LegacySystem", "SaaSPlatform", "EnterpriseServiceBus", "Other"]
    },
    "endpointType": {
      "type": "string",
      "enum": ["REST_API", "SOAP_API", "GraphQL_API", "gRPC_API", "WebService_URL", "MessageQueue_Producer", "MessageQueue_Consumer", "Database_Connection", "File_Transfer_Location", "Internal_Function_Call", "Other"]
    },
    "httpMethod": {
      "type": "string",
      "enum": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
    },
    "dataFormat": {
      "type": "string",
      "enum": ["JSON", "XML", "Protobuf", "Avro", "CSV", "YAML", "Text", "Binary"]
    },
    "endpointStatus": {
      "type": "string",
      "enum": ["Active", "Deprecated", "Experimental", "Offline", "Restricted"]
    },
    "documentType": {
      "type": "string",
      "enum": ["FAQ", "Manual", "Policy", "Article", "Guide", "WebsiteContent", "ProductSheet", "TechnicalSpecification", "Tutorial", "CaseStudy", "Other"]
    },
    "stance": {
      "type": "string",
      "enum": ["ACT", "REACT"]
    },
    "modeOfInteraction": {
      "type": "string",
      "enum": ["CREATE", "READ", "UPDATE", "DELETE", "INITIATE", "RESPOND", "NOTIFY"]
    },
    "scriptLanguage": {
      "type": "string",
      "enum": ["python", "javascript", "shell", "powershell", "other"]
    },
    "entityType": {
      "type": "string",
      "enum": ["data", "agent"]
    },
    "privacyClassification": {
      "type": "string",
      "enum": ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED", "PII", "PHI"]
    },
    "roleType": {
      "type": "string",
      "enum": ["human", "agent", "system"]
    },
    "agentArchetype": {
      "type": "string",
      "enum": ["worker", "supervisor", "specialist", "orchestrator"]
    },
    "dossierType": {
      "type": "string",
      "enum": ["DISCOVERY", "DESIGN", "DEPLOYMENT", "MARKETPLACE_ITEM", "TEMPLATE"]
    },
    "dossierStatus": {
      "type": "string",
      "enum": ["DRAFT", "IN_REVIEW", "APPROVED", "PUBLISHED", "DEPRECATED"]
    },
    "validationSeverity": {
      "type": "string",
      "enum": ["error", "warning", "info"]
    },
    "metricUnit": {
      "type": "string",
      "enum": ["SECONDS", "MINUTES", "HOURS", "PERCENTAGE", "COUNT", "CURRENCY", "OTHER"]
    },
    "currency": {
      "type": "string",
      "enum": ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"]
    },
    "dataCategory": {
      "type": "string",
      "enum": ["PII", "PHI", "PCI", "FINANCIAL", "AUTHENTICATION", "USAGE_ANALYTICS", "OTHER"]
    },
    "processingPurpose": {
      "type": "string",
      "enum": ["OPERATIONS", "ANALYTICS", "MARKETING", "SECURITY", "LEGAL_COMPLIANCE"]
    },
    "storagePolicy": {
      "type": "string",
      "enum": ["PLAINTEXT", "ENCRYPTED_AT_REST", "ANONYMIZED", "PSEUDONYMIZED", "MASKED", "DELETE_AFTER_PROCESSING"]
    },
    "telemetryLogLevel": {
      "type": "string",
      "enum": ["NONE", "ERROR", "INFO", "DEBUG", "TRACE"]
    },
    "telemetryMetricType": {
      "type": "string",
      "enum": ["COUNTER", "GAUGE", "HISTOGRAM"]
    },
    "marketplaceCategory": {
      "type": "string",
      "enum": ["FINANCE", "HEALTHCARE", "TELECOMMUNICATIONS", "RETAIL", "IT_SERVICE_MANAGEMENT", "HUMAN_RESOURCES", "CUSTOMER_SUPPORT", "UTILITIES"]
    },
    "marketplacePricingModel": {
      "type": "string",
      "enum": ["FREE", "ONE_TIME_PURCHASE", "SUBSCRIPTION_PER_SEAT", "SUBSCRIPTION_PER_EXECUTION"]
    },
    "changeManagementStatus": {
      "type": "string",
      "enum": ["PENDING_REVIEW", "APPROVED", "REJECTED", "IMPLEMENTED", "CANCELLED"]
    }
  },
  "additionalProperties": false
}
```