# Domain Intelligence Schema (DIS) v1.6

[![Version](https://img.shields.io/badge/version-1.6.0-blue.svg)](https://github.com/nwalker85/domainintelligenceschema/releases/tag/v1.6.0)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Schemas](https://img.shields.io/badge/schemas-23-orange.svg)](https://schemas.domainintelligenceschema.org/dis/1.6.0/)

Official JSON Schema definitions for the Domain Intelligence System - A grammar for modeling and deploying agentic AI systems in enterprise environments.

## 🎯 What is DIS?

DIS is "Terraform for Agentic AI" — a declarative specification that captures:
- **Domain structure** (entities, roles, applications)
- **Behavioral rules** (AgenticTriplets: Entity-Mode-Role)
- **Execution bindings** (functions, endpoints, workflows)
- **Governance** (RBAC, privacy, telemetry, change management)

Think of it as the **BNF for business units**, providing a formal grammar (not taxonomy) for composing valid domain models.

## 🚀 Quick Start

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

## 📚 Schema Catalog

**23 Core Constructs** organized into 6 categories:

### Foundation (2)
- [CommonEnums](schemas/v1.6.0/CommonEnums.schema.json) - Centralized vocabulary (31 enums)
- [DISDossier](schemas/v1.6.0/DISDossier.schema.json) - Root container and manifest

### Identity & Structure (5)
- [Entity](schemas/v1.6.0/Entity.schema.json) - Data objects and AI agents
- [Role](schemas/v1.6.0/Role.schema.json) - Behavioral capacities
- [Application](schemas/v1.6.0/Application.schema.json) - Software systems
- [Endpoint](schemas/v1.6.0/Endpoint.schema.json) - API interfaces
- [Modes](schemas/v1.6.0/Modes.schema.json) - Mode collections

### Behavioral Grammar (2)
- [AgenticTriplet](schemas/v1.6.0/AgenticTriplet.schema.json) - Core behavioral unit
- [ModeOfInteractionRegistryEntry](schemas/v1.6.0/ModeOfInteractionRegistryEntry.schema.json) - Mode metadata

### Matrices (4)
- [AccessGateMatrix](schemas/v1.6.0/AccessGateMatrix.schema.json) - RBAC rules
- [EntityModeMatrix](schemas/v1.6.0/EntityModeMatrix.schema.json) - Capability mapping
- [RelationshipMatrix](schemas/v1.6.0/RelationshipMatrix.schema.json) - Construct relationships
- [TripletFunctionMatrixEntry](schemas/v1.6.0/TripletFunctionMatrixEntry.schema.json) - Execution bindings

### Supporting Constructs (4)
- [FunctionCatalogEntry](schemas/v1.6.0/FunctionCatalogEntry.schema.json) - Reusable functions
- [KnowledgeDocument](schemas/v1.6.0/KnowledgeDocument.schema.json) - RAG artifacts
- [TagDefinition](schemas/v1.6.0/TagDefinition.schema.json) - Metadata taxonomy
- [ValidationRule](schemas/v1.6.0/ValidationRule.schema.json) - Business rules

### Business Value & Governance (6) — NEW in v1.6
- [ValueEngineeringProfile](schemas/v1.6.0/ValueEngineeringProfile.schema.json) - ROI metrics
- [DossierComparison](schemas/v1.6.0/DossierComparison.schema.json) - Version deltas
- [PrivacyManifest](schemas/v1.6.0/PrivacyManifest.schema.json) - GDPR/CCPA compliance
- [TelemetryConfiguration](schemas/v1.6.0/TelemetryConfiguration.schema.json) - Observability
- [MarketplaceEntry](schemas/v1.6.0/MarketplaceEntry.schema.json) - Publishing metadata
- [ChangeManagementRecord](schemas/v1.6.0/ChangeManagementRecord.schema.json) - ITIL change management

## 🎨 Key Features

### 7 Canonical Modes
The atomic verbs that force proper entity discovery:
- **CREATE** - Bring new data into existence
- **READ** - Retrieve and query data
- **UPDATE** - Modify existing data
- **DELETE** - Remove data
- **INITIATE** - Start asynchronous interactions
- **RESPOND** - Reply to initiated interactions
- **NOTIFY** - Send one-way alerts

### Zero Vendor Lock-in
v1.6 removes all proprietary references. Compile to:
- LangGraph
- CrewAI
- AWS Bedrock Agents
- Microsoft AutoGen
- Or custom platforms

### JMESPath Expressions
Standardized query and transformation language for:
- Validation rules
- Access gate conditions
- Payload transformations
- Data filtering

## 📖 Documentation

- [Live Schema Browser](https://schemas.domainintelligenceschema.org/docs/)
- [Canonical URIs](https://schemas.domainintelligenceschema.org/dis/1.6.0/)
- [Schema Index](https://schemas.domainintelligenceschema.org/dis/1.6.0/index.json)

## 🔧 Development

### Validate All Schemas

```bash
./scripts/validate-schemas.sh
```

### Sync from CDN

```bash
./scripts/sync-from-cdn.sh
```

## 📦 Distribution

**Canonical URIs:**
- Base: `https://schemas.domainintelligenceschema.org/dis/1.6.0/`
- Index: `https://schemas.domainintelligenceschema.org/dis/1.6.0/index.json`
- Docs: `https://schemas.domainintelligenceschema.org/docs/`

**Features:**
- ✅ CORS-enabled for web tools
- ✅ Immutable 1-year cache
- ✅ CDN-optimized delivery
- ✅ HTTPS with managed certificates

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Validate your changes with `./scripts/validate-schemas.sh`
4. Submit a pull request

## 📄 License

Apache License 2.0 - See [LICENSE](LICENSE) for details

## 🔗 Links

- [Official Website](https://domainintelligenceschema.org)
- [Schema Browser](https://schemas.domainintelligenceschema.org/docs/)
- [Issue Tracker](https://github.com/nwalker85/domainintelligenceschema/issues)

## 📊 Version History

- **v1.6.0** (Q1 2026) - First production-ready release
  - 23 core constructs
  - CommonEnums centralization
  - JMESPath standardization
  - 6 new governance constructs
  - Zero vendor lock-in

---

**Status:** ✅ Production Ready | **Release:** Q1 2026
