# TelemetryConfiguration

# TelemetryConfiguration v1.6

## Purpose

**NEW IN v1.6:** Defines observability, logging, and monitoring requirements for a dossier. Enables structured telemetry collection, distributed tracing, and operational monitoring of agent behaviors.

## v1.6 Changes

- **NEW CONSTRUCT:** Entirely new to v1.6 for operational excellence
- **MIGRATED:** telemetryLogLevel, telemetryMetricType, metricUnit enums to CommonEnums

## Relationships

- Referenced by DISDossier via header.telemetryConfigurationId
- Applies to all constructs and executions within the dossier
- Supports OpenTelemetry and distributed tracing standards

## Required Fields

telemetryConfigId, logLevel, metricsEnabled

## Properties (high level)

- telemetryConfigId (uuid) — Primary key
- description (string) — Telemetry policy summary
- logLevel (enum) — NONE, ERROR, INFO, DEBUG, TRACE (from CommonEnums)
- metricsEnabled (boolean) — Whether metrics collection is enabled
- tracingEnabled (boolean) — Whether distributed tracing is enabled
- metrics (array) — Metrics to collect:
    - metricName (string) — Metric identifier
    - metricType (enum) — COUNTER, GAUGE, HISTOGRAM
    - unit (enum) — SECONDS, MINUTES, HOURS, PERCENTAGE, COUNT, CURRENCY, OTHER
    - description (string) — Metric purpose
- logDestination (object) — Where logs are sent:
    - type (string) — stdout, file, syslog, cloudwatch, etc.
    - endpoint (string, uri) — Destination endpoint
- samplingRate (number) — 0.0-1.0 sampling percentage for traces

## Validation & Invariants

- logLevel must be valid enum from CommonEnums
- samplingRate must be between 0.0 and 1.0
- If tracingEnabled is true, samplingRate should be specified

## Examples

### Example 1: Production Telemetry Config

`````json
{
  "telemetryConfigId": "tc-prod-billing",
  "description": "Production telemetry for billing agents",
  "logLevel": "INFO",
  "metricsEnabled": true,
  "tracingEnabled": true,
  "metrics": [
    {
      "metricName": "invoice_creation_duration",
      "metricType": "HISTOGRAM",
      "unit": "SECONDS",
      "description": "Time to create invoice"
    },
    {
      "metricName": "active_agents",
      "metricType": "GAUGE",
      "unit": "COUNT",
      "description": "Number of active agents"
    }
  ],
  "logDestination": {
    "type": "cloudwatch",
    "endpoint": "[logs.us-east-1.amazonaws.com](http://logs.us-east-1.amazonaws.com)"
  },
  "samplingRate": 0.1
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/TelemetryConfiguration.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/TelemetryConfiguration.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/TelemetryConfiguration.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/TelemetryConfiguration.schema.json)",
  "title": "TelemetryConfiguration (v1.6)",
  "type": "object",
  "properties": {
    "telemetryConfigId": {"type": "string", "format": "uuid"},
    "logLevel": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/telemetryLogLevel](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/telemetryLogLevel)"},
    "metricsEnabled": {"type": "boolean"},
    "tracingEnabled": {"type": "boolean"},
    "metrics": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "metricType": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/telemetryMetricType](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/telemetryMetricType)"},
          "unit": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/metricUnit](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/metricUnit)"}
        }
      }
    }
  },
  "required": ["telemetryConfigId", "logLevel", "metricsEnabled"]
}
```