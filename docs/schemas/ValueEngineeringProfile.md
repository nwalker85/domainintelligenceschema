# ValueEngineeringProfile

# ValueEngineeringProfile v1.6

## Purpose

**NEW IN v1.6:** Captures business value metrics and ROI calculations for a DIS dossier. Enables cost-benefit analysis, value stream mapping, and financial justification for agent implementations.

## v1.6 Changes

- **NEW CONSTRUCT:** Entirely new to v1.6 for enterprise governance
- **MIGRATED:** currency and metricUnit enums to CommonEnums

## Relationships

- Referenced by DISDossier via header.valueEngineeringProfileId
- Links business metrics to technical implementations
- Supports ROI tracking and value demonstration

## Required Fields

valueProfileId, costModel

## Properties (high level)

- valueProfileId (uuid) — Primary key
- description (string) — Value proposition summary
- costModel (object) — Cost structure:
    - avgLaborRatePerHour (number) — Average labor cost
    - currency (enum) — USD, EUR, GBP, JPY, CAD, AUD
    - infrastructureCostPerMonth (number) — Monthly infrastructure cost
- benefitsModel (object) — Expected benefits:
    - timesSavedPerMonth (number, metricUnit: HOURS) — Time savings
    - errorReductionRate (number, metricUnit: PERCENTAGE) — Error reduction
    - customerSatisfactionImpact (number, metricUnit: PERCENTAGE)
- roiMetrics (object) — Return on investment:
    - breakEvenMonths (number) — Months to break even
    - annualizedROI (number, metricUnit: PERCENTAGE) — Annual ROI percentage

## Validation & Invariants

- currency must be valid enum from CommonEnums
- All numeric values should be positive
- ROI calculations should be mathematically consistent

## Examples

### Example 1: Agent Value Profile

`````json
{
  "valueProfileId": "vep-billing-agent",
  "description": "Value engineering profile for billing automation agent",
  "costModel": {
    "avgLaborRatePerHour": 75,
    "currency": "USD",
    "infrastructureCostPerMonth": 5000
  },
  "benefitsModel": {
    "timeSavedPerMonth": 160,
    "errorReductionRate": 85,
    "customerSatisfactionImpact": 25
  },
  "roiMetrics": {
    "breakEvenMonths": 6,
    "annualizedROI": 250
  }
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/ValueEngineeringProfile.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/ValueEngineeringProfile.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/ValueEngineeringProfile.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/ValueEngineeringProfile.schema.json)",
  "title": "ValueEngineeringProfile (v1.6)",
  "type": "object",
  "properties": {
    "valueProfileId": {"type": "string", "format": "uuid"},
    "costModel": {
      "type": "object",
      "properties": {
        "avgLaborRatePerHour": {"type": "number"},
        "currency": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/currency](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/currency)"}
      }
    },
    "roiMetrics": {"type": "object"}
  },
  "required": ["valueProfileId", "costModel"]
}
```