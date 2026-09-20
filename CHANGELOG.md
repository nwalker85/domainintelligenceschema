# Changelog

All notable changes to the Domain Intelligence Schema will be documented in this file.

## [1.6.0+ref-fix] - 2026-06-12

### Fixed
- **Cross-schema `$ref` host**: 48 `$ref` URIs in 16 schemas pointed at
  `schemas.domain-intelligence.org` — an unregistered domain — instead of the
  canonical `schemas.domainintelligenceschema.org`. Remote `$ref` resolution
  (including all CommonEnums lookups) failed against the broken host, and the
  unregistered domain was a schema-hijacking risk (anyone could register it
  and serve altered definitions). `$id` URIs were already canonical (fixed in
  1.6.0); this completes that migration for `$ref`s. No structural or
  semantic changes — published 1.6.0 artifacts are corrected in place since
  the broken refs were never resolvable by any consumer.

### Known issues (tracked in docs/GAPS.md)
- Dual function-binding paths: `AgenticTriplet.associatedFunctionIds` vs
  `TripletFunctionMatrixEntry` (which carries `executionBinding`). The matrix
  entry is canonical; the triplet-level array is denormalized convenience and
  can drift. Candidate for deprecation or "derived" designation in 1.7.

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
