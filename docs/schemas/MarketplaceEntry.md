# MarketplaceEntry

# MarketplaceEntry v1.6

## Purpose

**NEW IN v1.6:** Defines metadata for publishing dossiers to a DIS marketplace. Enables discovery, licensing, and distribution of reusable domain models and agent templates.

## v1.6 Changes

- **NEW CONSTRUCT:** Entirely new to v1.6 for ecosystem building
- **MIGRATED:** marketplaceCategory, marketplacePricingModel enums to CommonEnums

## Relationships

- Referenced by DISDossier for marketplace publishing
- Links dossiers to marketplace metadata
- Supports discovery and monetization

## Required Fields

marketplaceEntryId, title, category, pricingModel, publisherInfo

## Properties (high level)

- marketplaceEntryId (uuid) — Primary key
- title (string) — Marketplace listing title
- description (string) — Marketing description
- category (enum) — FINANCE, HEALTHCARE, TELECOMMUNICATIONS, RETAIL, IT_SERVICE_MANAGEMENT, HUMAN_RESOURCES, CUSTOMER_SUPPORT, UTILITIES
- tags (array<string>) — Searchable keywords
- pricingModel (enum) — FREE, ONE_TIME_PURCHASE, SUBSCRIPTION_PER_SEAT, SUBSCRIPTION_PER_EXECUTION
- price (object) — Pricing details:
    - amount (number) — Price amount
    - currency (enum) — USD, EUR, GBP, JPY, CAD, AUD
    - billingCycle (string) — monthly, annual, one-time
- publisherInfo (object) — Publisher details:
    - publisherName (string) — Publisher name
    - contactEmail (string) — Support email
    - website (string, uri) — Publisher website
- version (string) — Semantic version
- licenseType (string) — License (MIT, Apache, Proprietary, etc.)
- supportedDISVersion (string) — Compatible DIS version

## Validation & Invariants

- category and pricingModel must be valid enums from CommonEnums
- If pricingModel is not FREE, price object is required
- supportedDISVersion should match dossier DIS version

## Examples

### Example 1: Free Template

`````json
{
  "marketplaceEntryId": "mkt-billing-template",
  "title": "Enterprise Billing Agent Template",
  "description": "Pre-configured billing automation agent with invoice generation, payment processing, and dunning workflows",
  "category": "FINANCE",
  "tags": ["billing", "invoicing", "payments", "automation"],
  "pricingModel": "FREE",
  "publisherInfo": {
    "publisherName": "DIS Community",
    "contactEmail": "[support@dis-community.org](mailto:support@dis-community.org)",
    "website": "[https://dis-community.org](https://dis-community.org)"
  },
  "version": "1.0.0",
  "licenseType": "Apache-2.0",
  "supportedDISVersion": "1.6.0"
}
```

### Example 2: Commercial Solution

`````json
{
  "marketplaceEntryId": "mkt-healthcare-suite",
  "title": "Healthcare Patient Management Suite",
  "description": "HIPAA-compliant patient management with scheduling, records, and billing",
  "category": "HEALTHCARE",
  "pricingModel": "SUBSCRIPTION_PER_SEAT",
  "price": {
    "amount": 99,
    "currency": "USD",
    "billingCycle": "monthly"
  },
  "publisherInfo": {
    "publisherName": "HealthTech Solutions",
    "contactEmail": "sales@healthtech.example"
  },
  "version": "2.1.0",
  "licenseType": "Proprietary",
  "supportedDISVersion": "1.6.0"
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/MarketplaceEntry.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/MarketplaceEntry.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/MarketplaceEntry.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/MarketplaceEntry.schema.json)",
  "title": "MarketplaceEntry (v1.6)",
  "type": "object",
  "properties": {
    "marketplaceEntryId": {"type": "string", "format": "uuid"},
    "title": {"type": "string"},
    "description": {"type": "string"},
    "category": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/marketplaceCategory](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/marketplaceCategory)"},
    "pricingModel": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/marketplacePricingModel](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/marketplacePricingModel)"},
    "publisherInfo": {"type": "object"}
  },
  "required": ["marketplaceEntryId", "title", "category", "pricingModel", "publisherInfo"]
}
```