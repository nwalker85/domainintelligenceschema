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
- **The remaining v1.6.0 constructs, ported to Turtle/SHACL**: `TagDefinition`,
  `PrivacyManifest`, `TelemetryConfiguration`, `MarketplaceEntry`,
  `ChangeManagementRecord`, `ValueEngineeringProfile`, `DossierComparison`. Plus
  dossier-level metadata (`dossierType`, `dossierStatus`) as ontology-style
  triples on a dossier's own root IRI, replacing the `DISDossier` JSON wrapper
  object — in Turtle the file/named graph already is the dossier.
- Three real naming/semantic collisions found and resolved while porting:
  `applicationType` (old: technology shape; new: domain role — technology shape
  drove no constraint anywhere and was dropped, not duplicated), `httpMethod`
  (old: 7 values including `OPTIONS`/`HEAD`; new: 5, and `DELETE` → `HTTP_DELETE`
  to dodge SPARQL's own `DELETE` keyword — `OPTIONS`/`HEAD` don't represent
  agent-invokable actions and were dropped), and legacy `Modes` (v1.5-era
  "operational personas an Entity adopts" — folds into the existing `Role`
  rather than becoming its own class, since it's the same concept).

### Fixed (pre-release, found by the conformance suite)
- **Gap 1** — `kronos.ttl`/`dadjoke.ttl` did not conform: ported both to the
  Systems layer (an `Application` and `Endpoint` each, `dis:name`/
  `dis:callsEndpoint`/`dis:readsEntity`/`dis:inputFields`/`dis:outputFields`
  on each `FunctionCatalogEntry`, `dis:mutates` moved onto the Endpoint).
- **Gap 2** — `VocabularyBoundShape`, `LifecycleNeedsPhaseShape`,
  `StructuralMedicalShape` were each declared twice, byte-identical; removed
  the second copies.
- **Gap 3** — `Application.baseUrl`, `Endpoint.mutates`, and
  `FunctionCatalogEntry.readsEntity`/`inputFields`/`outputFields` are now
  `sh:minCount 1`, matching the spec text that already called them required.
- **Gap 4** — `dis:roleType` and `dis:entityType`, used as `sh:path` in
  `RoleShape`/`EntityShape`, are now declared as `owl:DatatypeProperty`.
- **Gap 5** — added NodeShapes for the eight ungoverned `Construct`
  subclasses (`TagDefinition`, `PrivacyManifest`, `TelemetryConfiguration`,
  `MarketplaceEntry`, `ChangeManagementRecord`, `ValueEngineeringProfile`,
  `DossierComparison`, `KnowledgeDocument`), plus
  `ApprovedChangeNamesApproverShape` and `ComparisonIsBetweenTwoDossiersShape`.
  `dis:AccessGate` — a leftover duplicate of `dis:AccessGateMatrix` with no
  properties and no uses — was removed from the vocabulary rather than given
  a shape; its two prose mentions now say `AccessGateMatrix`. `dis:APPROVED`
  is now typed as both `dis:ChangeManagementStatus` and `dis:DossierStatus`,
  as the vocabulary's own comment already claimed.
- **Gap 6** — `dis:FullView` now shows every class targeted by a
  `dis:paletteConstruct true` shape. Added `dis:SystemsView` and
  `dis:GrammarView`.
- **Gap 7** — `kronos-candies.ttl`/`dadjoke.ttl` used
  `dis:Dossier`/`dis:domainName`/`dis:disSpecificationRef`, none of which
  dis.ttl declares; replaced with the vocabulary's own
  `owl:Ontology`/`dis:dossierType`/`dis:dossierStatus`/`owl:versionInfo`
  header, now constrained by `DossierMetadataShape` and
  `DossierStatusMetadataShape`.
- **Gap 8** — all 23 `schemas/v1.6.0/*.schema.json` files now carry
  `"deprecated": true`; see below.

### Deprecated and replaced this version
- **JSON Schema is no longer the published contract.** CUE (canonical source,
  where it exists) and Turtle/SHACL (the graph and its constraints) are. Every
  `schemas/v1.6.0/*.schema.json` file, plus `schemas/v1.7.0/UtterancePolicy.schema.json`,
  is deprecated as of 1.7 — kept for existing consumers during the transition,
  generating no further constructs. `EntityInstance` and the seven constructs
  above are the first built the new way: Turtle/SHACL only, no `.schema.json`
  at all. `queries/*.rq` (SPARQL) is how a store is asked questions about a
  conforming dossier; `pyshacl` is how a dossier is validated.
- **`TripletFunctionMatrixEntry`** — a join-record binding a triplet to a
  function with an execution binding. Superseded by `dis:boundFunction`, a
  direct property already on `AgenticTriplet` (§3.4 of the 1.7 proposal) —
  already flagged as a deprecation candidate in this file's own 1.6.0 history.
- **`ValidationRule`** — a data record holding a free-text `condition` and a
  `severity`. That is what a SHACL shape is; writing one as data instead of as
  a shape is the pre-SHACL indirection this migration removes.
- **`RelationshipMatrix`** — a generic `actor`/`related_actor` join-table. In
  RDF a relationship is a typed triple; the wrapper was JSON's workaround for
  not having one.
- The 1.6.0 files now carry the JSON Schema `deprecated` keyword, and
  `schemas/v1.6.0/index.json` names 1.7.0 as its `supersededBy`.

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
