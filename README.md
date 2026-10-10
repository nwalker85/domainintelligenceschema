# Domain Intelligence Schema (DIS) 1.8.0

[![Version](https://img.shields.io/badge/version-1.8.0-blue.svg)](https://github.com/nwalker85/domainintelligenceschema/releases/tag/v1.8.0)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Conformance tests](https://img.shields.io/badge/conformance%20tests-196-brightgreen.svg)](tests/README.md)

DIS is an open, platform-agnostic standard — "Terraform for the domain model," not for a runtime. It is a declarative specification that captures:
- **Domain structure** (entities, roles, applications)
- **Behavioral rules** (AgenticTriplets: Entity-Mode-Role)
- **Execution bindings** (functions, endpoints, workflows)
- **Governance** (RBAC, privacy, telemetry, change management)

Think of it as the **BNF for business units**, providing a formal grammar (not taxonomy) for composing valid domain models.

## The grammar

DIS 1.8.0 is a Turtle vocabulary plus a set of SHACL shapes. The vocabulary declares the classes and the closed enumerations (seven modes, two stances, transports, network scopes, and others). The shapes are the contract: a dossier conforms when it validates against the shapes once it is merged with the vocabulary. CUE is the upstream source for `UtterancePolicy`. JSON Schema is legacy (see [Legacy JSON Schema](#legacy-json-schema-160)).

| Artifact | Path | What it is |
|---|---|---|
| Vocabulary | `vocabulary/v1.8.0/dis.ttl` | Classes, closed enumerations, properties |
| Shapes | `shapes/v1.8.0/dis-shapes.ttl` | SHACL constraints, including the SHACL-SPARQL grammar rules |
| CUE | `cue/v1.8.0/UtterancePolicy.cue` | Upstream source for `UtterancePolicy` |
| Queries | `queries/v1.8.0/*.rq` | Four SPARQL audits: full graph, medical liability, structural audit, ungoverned triplets |
| Reference dossiers | `fixtures/v1.8.0/*.ttl` | Eight dossiers, listed [below](#reference-dossiers) |
| Validation recipe | `scripts/validate-dossier.sh` | Merges the vocabulary into a dossier and runs pySHACL |
| Conformance suite | `tests/` | 196 tests |
| JSON Schema (legacy) | `schemas/v1.6.0/`, `schemas/v1.7.0/` | 23 deprecated 1.6.0 schemas; one unpublished 1.7.0 schema |

The `dis:` namespace IRI is `https://schemas.domainintelligenceschema.org/dis/1.8.0/`.

## Quick start

```bash
git clone https://github.com/nwalker85/domainintelligenceschema.git
cd domainintelligenceschema

# Run the conformance suite
uv sync --group test
uv run pytest

# Validate a dossier: scripts/validate-dossier.sh <dossier.ttl> [more.ttl ...]
scripts/validate-dossier.sh fixtures/v1.8.0/healthcare.ttl
```

The script exits 0 and prints `Conforms: True` for a conforming dossier, and exits 1 with a violation report otherwise. It needs `uv` (or `pyshacl` on `PATH`).

A triplet is a Role acting on an Entity in one of seven modes, written as an ordinary RDF node. This one is copied from `fixtures/v1.8.0/dadjoke.ttl` (prefixes `dis:` and `d:` are declared at the top of that file):

```turtle
# ---- The triplet IS a triple ----
d:triplet-tell-joke a dis:AgenticTriplet ;
    dis:name "tell_dad_joke → get_dad_joke" ;
    dis:description "Caller asks for a joke." ;
    dis:actingRole   d:role-agent ;
    dis:stance       dis:REACT ;
    dis:mode         dis:READ ;
    dis:targetEntity d:entity-joke ;
    dis:boundFunction d:fn-get-dad-joke .
```

The seven modes are `CREATE`, `READ`, `UPDATE`, `DELETE`, `INITIATE`, `RESPOND` and `NOTIFY`.

## What 1.8.0 adds

Six grammar fixes found by transcribing the Argus camera automation engine as a dossier. Together they let a triplet state what it reaches, what it mutates, and what it is allowed to call. The design record is [`docs/spec/DIS-1.8.md`](docs/spec/DIS-1.8.md); [CHANGELOG.md](CHANGELOG.md) lists what is implemented and what is not yet.

- **G1, mode and `mutates` consistency.** A `READ` triplet cannot bind a function whose endpoint mutates; `CREATE`, `UPDATE` and `DELETE` triplets must.
- **G2, directed side effects.** `dis:writesEntity` on a function is required when its endpoint mutates, and a triplet's target must match the function's `readsEntity` or `writesEntity`.
- **G3, binding completeness.** `dis:bindingStatus` (`BOUND`, `MANUAL_PROCEDURE`, `ABSTRACT_UNBOUND`) and `dis:unboundReason` mark triplets that have no executable function. The vocabulary and shape accept them; a rule rejecting an unbound mutating triplet that omits one is not yet enforced.
- **G4, multi-transport systems layer.** `dis:transport` on an Endpoint (HTTPS, MQTT, RTSP, NATS, gRPC and others) and `dis:networkScope` on an Application.
- **G5, function-level access gates.** `dis:allowedFunction` on an `AccessGateMatrix` limits a role to named catalog functions.
- **G6, single-graph conformance.** A dossier is validated merged with the vocabulary; `scripts/validate-dossier.sh` is the recipe.

1.8.0 also carries the constructs of the 1.7.0 proposal, which was never tagged: `UtterancePolicy`, the Systems layer (`Application`, `Endpoint`, `FunctionCatalogEntry`), `EntityInstance`, the remaining 1.6 constructs ported to Turtle/SHACL, and dossier metadata.

## Reference dossiers

Everything in `fixtures/v1.8.0/`:

| File | Domain | What it is |
|---|---|---|
| `healthcare.ttl` | Patient access | Appointments, patient lookup, caregiver proxy consent and prescription refill over Epic Cadence & MyChart, Cerner Millennium, MEDITECH Expanse and Surescripts; two steps declared `MANUAL_PROCEDURE` |
| `bfsi.ttl` | Banking and insurance | FIS, Fiserv and Guidewire systems; unauthenticated caller and authenticated accountholder as separate roles |
| `itsd.ttl` | IT service management | ServiceNow, SailPoint IdentityNow & Entra ID Bridge and SAP HANA EAM; a backoffice orchestrator role separate from the virtual agent |
| `hr.ttl` | Human capital | Workday, SAP SuccessFactors and Oracle PeopleSoft; a role per worker population with population-specific policies |
| `retail.ttl` | Retail support | Apex Retail Customer Support (`DRAFT`); the base graph most tests mutate for negative cases |
| `itsd-hr.ttl` | Employee IT and HR portal | A smaller dossier behind one gateway application (`DRAFT`) |
| `dadjoke.ttl` | Minimal | The smallest conforming dossier |
| `deformed.ttl` | Negative fixture | Three deliberate violations; the suite asserts exactly those three are reported |

## Conformance suite

196 tests in 15 files under `tests/`. They check that:

- every Turtle file parses, every SPARQL query compiles, and every JSON Schema is valid;
- every reference dossier conforms against the merged vocabulary and shapes, and `deformed.ttl` does not;
- each construct's shape accepts a conforming node and rejects constructed bad cases (negative cases are built by mutating a conforming dossier);
- the grammar rules (mode and mutation consistency, entity-mode and access-gate matrices, function-scoped gates) reject what they should;
- vocabulary and shapes agree (declared properties, closed enumerations, no duplicate shapes);
- the SPARQL queries run against the merged graphs;
- the CUE source and the exported JSON Schema for `UtterancePolicy` agree;
- release gating holds (the `.unreleased` marker, the CDN workflow, the 23-schema count).

```bash
uv sync --group test
uv run pytest
```

The CUE checks need the `cue` command (CI uses v0.17.1); they are skipped when it is not on `PATH`. Details, including the validation-recipe traps the suite pins, are in [`tests/README.md`](tests/README.md).

## Versioning and distribution

- **Tags are releases.** `main` can be ahead of the last tag. The last tag before 1.8.0 is `v1.6.0`; 1.7.0 was never tagged.
- **The Turtle artifacts are distributed from this repository**, by tag, under the versioned paths above. The CDN deploy publishes only `schemas/v*/` directories, and there is no `schemas/v1.8.0/`.
- **The CDN carries JSON Schema only**, at `https://schemas.domainintelligenceschema.org/dis/<version>/`. The last version published there is 1.6.0.
- **The `.unreleased` marker.** A `schemas/v<version>/` directory containing a file named `.unreleased` is skipped by the CDN sync and by CDN verification (`.github/workflows/deploy-cdn.yml`), so a version can sit on `main` without becoming a live URL. The marker is deleted only as part of tagging that version. `schemas/v1.7.0/` carries one, and `tests/test_release_gating.py` ties it to the absence of a 1.7 tag.
- Published CDN versions are append-only; automation never deletes from the bucket. `scripts/verify-cdn.sh` checks that the live CDN matches the repository.

## Legacy JSON Schema (1.6.0)

JSON Schema is deprecated as of 1.7: `schemas/v1.6.0` remains the last JSON Schema release and stays on the CDN, and no further constructs will be added there. These instructions apply to the 1.6.0 files.

### IDE Integration

Reference schemas directly for autocomplete and validation:

```json
{
  "$schema": "https://schemas.domainintelligenceschema.org/dis/1.6.0/DISDossier.schema.json",
  "dossierId": "customer-service-v1",
  "name": "Customer Service Domain",
  "disSpecificationRef": "1.6.0"
}
```

### Validation

```bash
# Using AJV with CDN
ajv validate \
  -s https://schemas.domainintelligenceschema.org/dis/1.6.0/DISDossier.schema.json \
  -d my-dossier.json

# Using local schemas
ajv validate -s schemas/v1.6.0/DISDossier.schema.json -d my-dossier.json
```

### Type Generation

```bash
# TypeScript
json-schema-to-typescript \
  https://schemas.domainintelligenceschema.org/dis/1.6.0/Entity.schema.json \
  > types/Entity.ts

# Python
datamodel-codegen \
  --url https://schemas.domainintelligenceschema.org/dis/1.6.0/Entity.schema.json \
  --output models/entity.py
```

### Schema Catalog

**23 Core Constructs** organized into 6 categories:

#### Foundation (2)
- [CommonEnums](schemas/v1.6.0/CommonEnums.schema.json) - Centralized vocabulary (31 enums)
- [DISDossier](schemas/v1.6.0/DISDossier.schema.json) - Root container and manifest

#### Identity & Structure (5)
- [Entity](schemas/v1.6.0/Entity.schema.json) - Data objects and AI agents
- [Role](schemas/v1.6.0/Role.schema.json) - Behavioral capacities
- [Application](schemas/v1.6.0/Application.schema.json) - Software systems
- [Endpoint](schemas/v1.6.0/Endpoint.schema.json) - API interfaces
- [Modes](schemas/v1.6.0/Modes.schema.json) - Mode collections

#### Behavioral Grammar (2)
- [AgenticTriplet](schemas/v1.6.0/AgenticTriplet.schema.json) - Core behavioral unit
- [ModeOfInteractionRegistryEntry](schemas/v1.6.0/ModeOfInteractionRegistryEntry.schema.json) - Mode metadata

#### Matrices (4)
- [AccessGateMatrix](schemas/v1.6.0/AccessGateMatrix.schema.json) - RBAC rules
- [EntityModeMatrix](schemas/v1.6.0/EntityModeMatrix.schema.json) - Capability mapping
- [RelationshipMatrix](schemas/v1.6.0/RelationshipMatrix.schema.json) - Construct relationships
- [TripletFunctionMatrixEntry](schemas/v1.6.0/TripletFunctionMatrixEntry.schema.json) - Execution bindings

#### Supporting Constructs (4)
- [FunctionCatalogEntry](schemas/v1.6.0/FunctionCatalogEntry.schema.json) - Reusable functions
- [KnowledgeDocument](schemas/v1.6.0/KnowledgeDocument.schema.json) - RAG artifacts
- [TagDefinition](schemas/v1.6.0/TagDefinition.schema.json) - Metadata taxonomy
- [ValidationRule](schemas/v1.6.0/ValidationRule.schema.json) - Business rules

#### Business Value & Governance (6)
- [ValueEngineeringProfile](schemas/v1.6.0/ValueEngineeringProfile.schema.json) - ROI metrics
- [DossierComparison](schemas/v1.6.0/DossierComparison.schema.json) - Version deltas
- [PrivacyManifest](schemas/v1.6.0/PrivacyManifest.schema.json) - GDPR/CCPA compliance
- [TelemetryConfiguration](schemas/v1.6.0/TelemetryConfiguration.schema.json) - Observability
- [MarketplaceEntry](schemas/v1.6.0/MarketplaceEntry.schema.json) - Publishing metadata
- [ChangeManagementRecord](schemas/v1.6.0/ChangeManagementRecord.schema.json) - ITIL change management

To validate that all 1.6.0 schemas are well-formed JSON: `./scripts/validate-schemas.sh`.

## Documentation

- [Official Website](https://domainintelligenceschema.org)
- [Documentation (`/docs`)](https://domainintelligenceschema.org/docs/)
- [DIS 1.8 specification and design record](docs/spec/DIS-1.8.md)
- [DIS 1.7 proposal](docs/spec/DIS-1.7-proposed.md) (historical; its constructs shipped in 1.8.0)
- [CHANGELOG](CHANGELOG.md)
- [Repository Documentation Map](docs/DOCUMENTATION.md), [Architecture](docs/ARCHITECTURE.md) and [Runbook](docs/RUNBOOK.md)
- JSON Schema (1.6.0): [Schema Browser](https://schemas.domainintelligenceschema.org/docs/), [Canonical URIs](https://schemas.domainintelligenceschema.org/dis/1.6.0/) and [Schema Index](https://schemas.domainintelligenceschema.org/dis/1.6.0/index.json)
- [Issue Tracker](https://github.com/nwalker85/domainintelligenceschema/issues)

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Validate your changes with `uv run pytest` (and `./scripts/validate-schemas.sh` if you touch `schemas/v1.6.0`)
4. Submit a pull request

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details

## Version history

- **1.8.0** (2026-10-09) - Six grammar fixes from the Argus trial (G1 to G6); the 1.7.0 proposal's constructs; artifacts renamed to `v1.8.0`; 196-test conformance suite; eight reference dossiers
- **1.7.0** - Absorbed into 1.8.0, never tagged
- **1.6.0+ref-fix** (2026-06-12) - Cross-schema `$ref` host corrected in place
- **1.6.0** (Q1 2026) - 23 JSON Schema constructs, CommonEnums centralization, JMESPath standardization, six governance constructs, vendor-specific references removed
