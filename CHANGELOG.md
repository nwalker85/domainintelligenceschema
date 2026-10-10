# Changelog

All notable changes to the Domain Intelligence Schema will be documented in this file.

## [Unreleased] — proposals, no artifacts

Ideas that appeared in the withdrawn first draft of the 1.8.0 entry (2026-10-08,
PR #11). They are recorded here as proposals only, and are part of no release.

- Epistemic observation (`dis:Observation`, `observedBy`, `observationTimestamp`,
  `epistemicConfidence`): keep unverified claims apart from ground truth, with an
  observer, a confidence and a decay half-life.
- Bounded authority (`CapabilityLease`, `MandateToken`, `validForDurationSeconds`):
  time-limited, non-escalating grants in place of ambient credentials.
- `DisagreementMatrix` and `consensusThreshold`: arbitration rules for when
  multi-agent observations conflict.

No vocabulary, shapes, CUE or tests exist for these.

## [1.8.0] - 2026-10-09

The first release since 1.6.0. It carries the constructs of the 1.7.0 proposal
(1.7.0 was never tagged) plus six grammar fixes found by the Argus trial. See
[`docs/spec/DIS-1.8.md`](docs/spec/DIS-1.8.md) for the design record.

### Grammar (from the Argus trial; design record in `docs/spec/DIS-1.8.md`)

Transcribing the Argus camera automation engine as a dossier exposed six
structural gaps, G1 to G6, in the 1.7 grammar. Each bullet gives the resolution
as the spec states it, then what is implemented in `vocabulary/v1.8.0` and
`shapes/v1.8.0`.

- **G1, mode and `mutates` disconnect.** Spec: "SHACL-SPARQL consistency rule:
  `READ` requires `mutates false`; `CREATE`, `UPDATE`, `DELETE` require
  `mutates true`." Implemented as `TripletModeMutationConsistencyShape`, which
  checks a triplet's `dis:mode` against `dis:mutates` on the endpoint of its
  `dis:boundFunction`.
- **G2, target blindness on mutation.** Spec: "Introduce `dis:writesEntity`
  (required when `mutates true`). Enforce that triplet `targetEntity ==
  writesEntity`." Implemented: `dis:writesEntity` on `FunctionCatalogEntry`;
  `FunctionMutatesNeedsWritesEntityShape` requires it when the called endpoint
  mutates; `TripletTargetEntityConsistencyShape` requires a `READ` triplet's
  `targetEntity` to equal the bound function's `readsEntity`, and a `CREATE`,
  `UPDATE` or `DELETE` triplet's `targetEntity` to equal its `writesEntity`.
- **G3, unbound mutating triplets.** Spec: "Require `boundFunction` for all
  mutating triplets, or require explicit `dis:bindingStatus dis:UNBOUND` with
  justification." Implemented: `dis:bindingStatus` (`dis:BOUND`,
  `dis:MANUAL_PROCEDURE`, `dis:ABSTRACT_UNBOUND`) and `dis:unboundReason` on
  `AgenticTriplet`, accepted by `AgenticTripletShape`; `healthcare.ttl` and
  `bfsi.ttl` use them for their unbound manual steps. Not yet implemented: no
  shape rejects a mutating `ACT` triplet that has neither a `boundFunction` nor a
  `bindingStatus` (spec §3.2), so such a triplet still conforms. (The §2 table of the
  spec says `dis:UNBOUND`; its §3.2 and the vocabulary use `dis:ABSTRACT_UNBOUND`.)
- **G4, HTTP-only transport trap.** Spec: "Introduce `dis:transport` (`HTTP`,
  `MQTT`, `RTSP`, `NATS`, `GRPC`), transport-specific addressing, and
  `dis:networkScope`." Implemented: `dis:transport` on `Endpoint` with 14
  `dis:Transport` individuals (`TRANSPORT_HTTPS`, `TRANSPORT_MQTT`,
  `TRANSPORT_RTSP`, `TRANSPORT_NATS`, `TRANSPORT_GRPC` and nine more); the
  addressing properties `dis:topic`, `dis:streamUri`, `dis:subject`,
  `dis:peerAddress`, `dis:socketPath` and `dis:channel`; `EndpointShape` no
  longer demands `httpMethod` and `urlPath` for MQTT, RTSP, ESP-NOW, NATS, Unix
  socket, BLE, serial and CAN bus endpoints; `dis:networkScope` on `Application`
  (`SCOPE_PUBLIC`, `SCOPE_INTERNAL`, `SCOPE_LOCAL_IPC`, `SCOPE_RADIO_MESH`), with
  the https-only `baseUrl` check applying to `SCOPE_PUBLIC` or an unscoped
  Application. Not yet implemented: requiring the matching address property per
  transport (for example a `topic` on an MQTT endpoint), and the spec's `qos` and
  gRPC service and method fields.
- **G5, coarse mode gates against asymmetric rights.** Spec: "Add function-scoped
  gates (`dis:allowedFunction`) and value constraints (`dis:allowedTargetValue` /
  `dis:allowedTransition`)." Implemented: `dis:allowedFunction` on
  `AccessGateMatrix`, enforced by `TripletWithinAllowedFunctionGateShape`, which
  rejects a triplet whose bound function is not listed by a function-scoped gate
  for its role, entity and mode. Not yet implemented: `dis:allowedTargetValue` and
  `dis:allowedTransition`.
- **G6, vocabulary loading trap in conformance.** Spec: "Mandate merged-graph
  evaluation in §7 conformance, and bundle core class/enum declarations into
  distribution shapes." Implemented: the single-graph recipe in
  `scripts/validate-dossier.sh` merges `vocabulary/v1.8.0/dis.ttl` into the
  dossier graph and runs pySHACL against `shapes/v1.8.0/dis-shapes.ttl` with no
  inference flag; `tests/test_validation_recipe.py` pins both traps (validating
  without the vocabulary merged, and `-i rdfs`). Not yet implemented: self-contained
  distribution shapes. `dis-shapes.ttl` still needs the vocabulary merged in.

### Carried from the 1.7.0 proposal (never tagged separately)
- **`UtterancePolicy`**: constraints on what an agent may say, distinct from what it
  may do.
- **The Systems layer**: `Application`, `Endpoint`, `FunctionCatalogEntry`.
- **`EntityInstance`**: a closed, known population for an Entity.
- **The remaining 1.6 constructs, ported to Turtle/SHACL**: `TagDefinition`,
  `PrivacyManifest`, `TelemetryConfiguration`, `MarketplaceEntry`,
  `ChangeManagementRecord`, `ValueEngineeringProfile`, `DossierComparison`.
- **Dossier metadata**: `dossierType` and `dossierStatus` on a dossier's own root IRI.

The pre-release fixes and the breaking change to `EntityModeMatrix` and
`AccessGateMatrix` are recorded under [1.7.0] below.

### Artifacts
- Five trees, all under `v1.8.0`: `vocabulary/v1.8.0/dis.ttl`,
  `shapes/v1.8.0/dis-shapes.ttl`, `cue/v1.8.0/UtterancePolicy.cue`,
  `queries/v1.8.0/` (four SPARQL queries), `fixtures/v1.8.0/` (eight dossiers).
  `owl:versionInfo` is `1.8.0`.
- The `dis:` namespace IRI is now `https://schemas.domainintelligenceschema.org/dis/1.8.0/`
  (it was `.../dis/1.7.0/` on main before this release). A dossier written against
  the unreleased 1.7.0 namespace must change its `dis:` prefix.

### Reference dossiers
Everything in `fixtures/v1.8.0/`:
- `bfsi.ttl`: retail banking and insurance claims over FIS Modern Banking Platform,
  Fiserv Signature & Card Services and Guidewire ClaimCenter and PolicyCenter;
  separates an unauthenticated caller from an authenticated accountholder.
- `dadjoke.ttl`: the smallest conforming dossier; one entity, one triplet, one
  utterance policy, one application with one endpoint.
- `deformed.ttl`: the negative fixture; three deliberate violations (a triplet
  targeting a Role, an invented mode, an `OBLIGATION` with no bound value), and the
  suite asserts exactly those three are reported.
- `healthcare.ttl`: patient access over Epic Cadence & MyChart, Cerner Millennium,
  MEDITECH Expanse and Surescripts: appointments, patient lookup, caregiver proxy
  consent and prescription refill; two unbound steps declared `MANUAL_PROCEDURE`.
- `hr.ttl`: an HR assistant over Workday, SAP SuccessFactors and Oracle PeopleSoft
  Time and Labor, with a role per worker population and population-specific policies.
- `itsd-hr.ttl`: a smaller employee IT service desk and HR portal behind one
  gateway application; status `DRAFT`, version `1.0.0`.
- `itsd.ttl`: IT service management over ServiceNow, SailPoint IdentityNow and
  Entra ID, and SAP HANA EAM, with a separate backoffice orchestrator role for
  automated onboarding and offboarding.
- `retail.ttl`: Apex Retail Customer Support; the base graph most conformance tests
  mutate to build negative cases; status `DRAFT`.

### Conformance suite
- 196 tests in 15 files under `tests/`, run with `uv sync --group test && uv run pytest`.
  They use pytest, rdflib, pySHACL and, for the CUE and JSON Schema checks, the `cue`
  command (CI pins v0.17.1); those tests are skipped when `cue` is not on `PATH`.

### Site
- Overhaul of domainintelligenceschema.org and `/docs`: landing page, documentation
  reference and specification link, describing G1 to G6 as implemented.

### JSON Schema
- Deprecated since 1.7. `schemas/v1.6.0` remains the last JSON Schema release and
  stays on the CDN. `schemas/v1.7.0` is unpublished on the CDN (it carries an
  `.unreleased` marker, which the CDN deploy skips) and will not be published there.

### Corrections
- The previous 1.8.0 entry (2026-10-08, PR #11), the pull request body and the site
  described constructs that were never implemented: `dis:Observation`, `observedBy`,
  `observationTimestamp`, `epistemicConfidence`, `CapabilityLease`, `MandateToken`,
  `validForDurationSeconds`, `decayHalfLifeSeconds`, `DisagreementMatrix`,
  `consensusThreshold`, and substrate interchangeability as a construct. None of
  them exists in `vocabulary/`, `shapes/`, `cue/` or `tests/`. They are withdrawn
  from 1.8.0 and recorded under Unreleased above as proposals.
- That entry and the site also credited the dossiers with features the files do not
  contain (NPI attestation, a "Fiserv DNA" system, temporal leases). The dossier list
  above is read from the files.
- `docs/spec/DIS-1.8.md` was marked a draft proposal while the site called 1.8.0 an
  active standard; it is now marked as the design record of the 1.8.0 release.
  The artifacts moved from `v1.7.0` paths to `v1.8.0` paths.

## [1.7.0] - Absorbed into 1.8.0, never tagged

No tag or release exists for 1.7.0. Its constructs shipped in 1.8.0, and
`schemas/v1.7.0` stays unpublished. See
[`docs/spec/DIS-1.7-proposed.md`](docs/spec/DIS-1.7-proposed.md) for the original
proposal.

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
- **Gap 1** — early fixtures / `dadjoke.ttl` did not conform: ported to the
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
- **Gap 7** — early draft fixtures / `dadjoke.ttl` used
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
- The four unencumbered reference industry dossiers (`retail.ttl`, `healthcare.ttl`,
  `bfsi.ttl`, `itsd-hr.ttl`) and `dadjoke.ttl` conform cleanly against the merged vocabulary and shapes.
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

[1.8.0]: https://github.com/nwalker85/domainintelligenceschema/releases/tag/v1.8.0
[1.6.0]: https://github.com/nwalker85/domainintelligenceschema/releases/tag/v1.6.0
