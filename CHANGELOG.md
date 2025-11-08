# Changelog

All notable changes to the Domain Intelligence Schema will be documented in this file.

## [1.6.0] - 2026-Q1

### Added
- **CommonEnums** - Centralized enum definitions (31 enums)
- **ValueEngineeringProfile** - ROI metrics and calculations
- **DossierComparison** - Version delta analysis
- **PrivacyManifest** - GDPR/CCPA compliance
- **TelemetryConfiguration** - Observability requirements
- **MarketplaceEntry** - Publishing metadata
- **ChangeManagementRecord** - ITIL change management
- JMESPath as standard expression language
- Field-level privacy controls
- Comprehensive documentation

### Changed
- All `$id` URIs to canonical domain
- `gateCondition` uses JMESPath
- `parameterMap` uses JMESPath
- `ruleExpression` uses JMESPath

### Removed
- **BREAKING**: Vendor-specific references
- **BREAKING**: `proxiedAmeliaBotInstanceId` from Entity
- **BREAKING**: AmeliaBotInstance construct

[1.6.0]: https://github.com/nwalker85/domainintelligenceschema/releases/tag/v1.6.0
