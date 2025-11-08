# KnowledgeDocument

# KnowledgeDocument v1.6

## Purpose

Defines a knowledge artifact (FAQ, manual, policy, guide) that can be referenced by agents for context. Enables RAG (Retrieval Augmented Generation) patterns by linking declarative knowledge to agent behaviors.

## v1.6 Changes

- **MIGRATED:** documentType enum abstracted to CommonEnums
- **STABLE:** Core structure unchanged from v1.5

## Relationships

- Referenced by AgenticTriplet via knowledgeDocumentIds
- Can be tagged via appliedTags (references TagDefinition)
- Used to provide context for agent decision-making

## Required Fields

knowledgeDocumentId, title, documentType

## Properties (high level)

- knowledgeDocumentId (uuid) — Primary key
- title (string) — Document title
- description (string) — Document summary
- documentType (enum) — FAQ, Manual, Policy, Article, Guide, WebsiteContent, ProductSheet, TechnicalSpecification, Tutorial, CaseStudy, Other
- content (string) — Full document content or reference
- sourceUrl (string, uri) — External source URL
- tags (array<string>) — Searchable keywords
- version (string) — Document version
- lastUpdated (date-time) — Last modification timestamp

## Validation & Invariants

- documentType must be valid enum from CommonEnums
- Either content or sourceUrl should be provided

## Examples

### Example 1: FAQ Document

`````json
{
  "knowledgeDocumentId": "kd-billing-faq",
  "title": "Billing FAQ",
  "description": "Frequently asked questions about billing processes",
  "documentType": "FAQ",
  "content": "Q: How do I create an invoice? A: Navigate to Billing > New Invoice...",
  "tags": ["billing", "invoices", "faq"],
  "version": "1.0"
}
```

## JSON Schema

**URI:** [`https://schemas.domainintelligenceschema.org/dis/1.6.0/KnowledgeDocument.schema.json`](https://schemas.domainintelligenceschema.org/dis/1.6.0/KnowledgeDocument.schema.json)

`````json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "$id": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/KnowledgeDocument.schema.json](https://schemas.domainintelligenceschema.org/dis/1.6.0/KnowledgeDocument.schema.json)",
  "title": "KnowledgeDocument (v1.6)",
  "type": "object",
  "properties": {
    "knowledgeDocumentId": {"type": "string", "format": "uuid"},
    "title": {"type": "string"},
    "description": {"type": "string"},
    "documentType": {"$ref": "[https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/documentType](https://schemas.domainintelligenceschema.org/dis/1.6.0/CommonEnums.schema.json#/definitions/documentType)"},
    "content": {"type": "string"},
    "sourceUrl": {"type": "string", "format": "uri"}
  },
  "required": ["knowledgeDocumentId", "title", "documentType"]
}
```