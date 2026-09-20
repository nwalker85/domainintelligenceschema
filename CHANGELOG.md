# Changelog

All notable changes to the Domain Intelligence Schema will be documented in this file.

## [1.7.0] - Proposed, not yet released

See [`docs/spec/DIS-1.7-proposed.md`](docs/spec/DIS-1.7-proposed.md) for the full
proposal. No tag or release exists yet; nothing here is published.

### Added
- **`UtterancePolicy`** — constraints on what an agent may SAY, distinct from what
  it may DO. `policyType`, `requirement`, `enforcement` (STRUCTURAL/INSTRUCTED/
  ADVISORY — a compiler MUST NOT silently downgrade STRUCTURAL).
- **The Systems layer** — `Application`, `Endpoint`, `FunctionCatalogEntry`. Ties
  an `AgenticTriplet` to what it actually reaches: which system, which callable
  operation, whether it mutates state (declared, never inferred from HTTP method).
- **`EntityInstance`** — a closed, known population for an Entity that genuinely
  has one, so a compiler can emit a closed value set instead of a free string.

### Changed (breaking)
- **`EntityModeMatrix` and `AccessGateMatrix` become enforceable.** A triplet is
  now legal only if the target Entity supports the mode (`EntityModeMatrix`) and
  the acting Role has been granted that mode on that Entity (`AccessGateMatrix`).
  A triplet outside either matrix — when matrices are declared — is illegal, not
  merely undeclared. Enforced by two `sh:sparql` SHACL shapes
  (`TripletWithinEntityModeShape`, `TripletWithinAccessGateShape`) since the
  constraint spans three subjects and SHACL Core property paths cannot compare
  across them. Opt-in: a dossier that declares no matrices is unconstrained.

### Resolved
- **Docs-vs-canonical-schema divergence** on `AccessGateMatrix`, `EntityModeMatrix`,
  and `AgenticTriplet` (docs said one shape, `.schema.json` said another). 1.7
  resolves in favor of the documentation's semantics: a JMESPath `gateCondition`
  can only be evaluated at runtime and can observe a block but not prove one is
  impossible; moving modes onto the gate makes the constraint statically checkable.
  `gateCondition` is retained as an optional field for genuinely dynamic conditions.

### Validated
- The 400-line Kronos Candies worked example (`fixtures/v1.7.0/kronos-candies.ttl`)
  conforms cleanly against the merged vocabulary and shapes.
- The negative fixture (`fixtures/v1.7.0/deformed.ttl`) is correctly rejected.

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
