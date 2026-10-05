# DIS 1.7 — proposed specification

**Status:** Proposal · **Baseline:** 1.6.0 (published at
`schemas.domainintelligenceschema.org`) · **Author:** Nathan Walker ·
**Date:** 2026-09-15

1.7 adds three things to 1.6.0 and changes one. Each was found by building a
working agent against the 1.6 model and recording what the model could not say.

| § | Delta | Kind |
|---|---|---|
| [2](#2-utterancepolicy) | `UtterancePolicy` | **adds** one construct |
| [3](#3-the-systems-layer) | `Application` · `Endpoint` · `FunctionCatalogEntry` | **adds** three constructs |
| [4](#4-the-grammar-matrices-become-enforceable) | `EntityModeMatrix` / `AccessGateMatrix` carry modes | **changes** two constructs |
| [5](#5-the-divergence-this-resolves) | docs ⟷ canonical schema disagreement | **resolves** |

Nothing in 1.6.0 is removed. §4 is the only breaking change, and §5 explains why
it is the honest one.

---

## 1. The question 1.7 answers

DIS 1.6.0 models **structure** — who may do what to what. Scoping a use case
needs three more answers that 1.6 has no field for:

1. **What may the agent say?** Access is granted; the constraint is on the
   *form* of the utterance. (§2)
2. **What does it reach when it acts?** A triplet says a Role READs an Entity.
   Nothing says through which system, at which URL, with which fields. (§3)
3. **What is illegal?** 1.6 lets you list the triplets you thought of. It cannot
   tell you the one you wrote down is outside the grammar. (§4)

The third is the one that matters most, because **the denials are as much the
model as the permissions**, and only an enumerated cross-product produces them.

---

## 2. UtterancePolicy

Specified in full in
[`DIS-1.7-UtterancePolicy.md`](../drafts/DIS-1.7-UtterancePolicy.md)
(this repo: `cue/v1.7.0/UtterancePolicy.cue`, `schemas/v1.7.0/UtterancePolicy.schema.json`,
`queries/v1.7.0/`, `fixtures/v1.7.0/retail.ttl` + `deformed.ttl`). Summarised
here so this document stands alone.

**Required:** `policyId` · `name` · `description` · `policyType` ·
`requirement` · `enforcement`

```
policyType    OBLIGATION | PROHIBITION | DISCLOSURE_LIMIT | LIFECYCLE
requirement   the rule, as a condition — never copy, never steps
enforcement   STRUCTURAL | INSTRUCTED | ADVISORY
```

Two fields carry the weight. `boundValueRefs` (`dis:boundValue` in RDF) names the values that must
**travel with** the utterance — this is what makes a cross-scope rule
expressible, because a per-entity attribute and a domain-level disclosure are
different scopes of one question. `enforcement` says where the rule is actually
enforced, and **a compiler MUST NOT silently downgrade STRUCTURAL to
INSTRUCTED**; if the target cannot enforce structurally it reports that, which
is the clause that makes the field load-bearing rather than documentary.

It deliberately excludes **the words** (copy belongs to the target profile and
varies by channel and language) and **procedure** (`requirement` states a
condition; the moment DIS holds steps it stops being target-agnostic).

---

## 3. The Systems layer

### 3.1 Why

A triplet asserts `Support Agent —READ→ Allergen Profile`. Every target that
consumes it then has to be told, outside the model, *where allergen data lives*.
That is the layer where a demo silently becomes a lie: the model says the answer
comes from a system of record, and the agent answers from what it already
believed.

Three constructs close it, and they are deliberately the smallest set that makes
a triplet **executable**.

### 3.2 `Application`

A system that holds or serves domain data.

| Field | | |
|---|---|---|
| `name` | required | |
| `applicationType` | required | `SYSTEM_OF_RECORD` · `SAAS_PLATFORM` · `MOCK` · `KNOWLEDGE_STORE` |
| `baseUrl` | required | **must be https** — a target that cannot reach it cannot use it |
| `authMethod` | | `NONE` · `API_KEY` · `OAUTH2` · `BEARER` |

> **An Application cannot be both `MOCK` and `SYSTEM_OF_RECORD`.** Enforced by
> shape, because that confusion is exactly how a demo's provenance claim rots.

### 3.3 `Endpoint`

One callable operation on an Application.

| Field | | |
|---|---|---|
| `hostedBy` | required | → `Application` |
| `urlPath` | required | relative to `baseUrl`, **must start with `/`** |
| `httpMethod` | required | `GET` · `POST` · `PUT` · `PATCH` · `HTTP_DELETE` |
| `mutates` | required | **declared, not inferred** |

> `mutates` is required and separate from `httpMethod` because **HTTP method
> is not the answer.** A `POST /search` mutates nothing; a `GET //trigger-refund`
> exists in the wild. The model must not infer a safety property from a
> convention the target may violate.

### 3.4 `FunctionCatalogEntry`

The binding between a triplet and an endpoint — what the agent can actually
invoke.

| Field | | |
|---|---|---|
| `callsEndpoint` | required | → `Endpoint`; otherwise the entry states nothing executable |
| `readsEntity` | required | → `Entity` — the tie back to the grammar |
| `inputFields` | required | comma-separated field names the caller must supply |
| `outputFields` | required | comma-separated field names the response returns |

`dis:boundFunction` on an `AgenticTriplet` points here. That single property is
what turns *"the agent may read allergen data"* into *"and this is the call it
makes."*

### 3.5 What this is not

It is **not an API specification**. There is no schema, no auth flow, no
pagination, no error model. Those belong to OpenAPI, which already exists and is
better at it. The Systems layer records only what the *domain model* needs in
order to remain honest about provenance: which system, which operation, which
fields, and whether it changes anything.

---

## 4. The grammar matrices become enforceable

### 4.1 The change

1.6 defines `EntityModeMatrix` and `AccessGateMatrix` as constructs. 1.7 makes
their modes **structural fields**:

```turtle
dis:matrixEntity   rdfs:range dis:Entity .                                  # both matrices
dis:matrixRole     rdfs:domain dis:AccessGateMatrix ; rdfs:range dis:Role .
dis:supportedMode  rdfs:domain dis:EntityModeMatrix ; rdfs:range dis:Mode .
dis:allowedMode    rdfs:domain dis:AccessGateMatrix ; rdfs:range dis:Mode .
```

`EntityModeMatrix` says which of the seven modes an Entity supports **at all** —
the outer bound on the grammar. `AccessGateMatrix` says which Role may use which
of those modes on it — authority, *who may*.

> **Authority and utterance are different questions.** `AccessGateMatrix` governs
> reach. `UtterancePolicy` governs what may be said once reach is granted. A
> model that collapses them cannot express *"you may read this value and must
> never say it alone."*

### 4.2 The rule that makes it a grammar

> **A triplet is legal only if the target Entity supports the mode, and the
> acting Role has been granted that mode on that Entity.**
>
> A triplet outside either matrix is not merely undeclared — it is **illegal**.

Enforced by two SHACL shapes in
[`shapes/v1.7.0/dis-shapes.ttl`](../../shapes/v1.7.0/dis-shapes.ttl):
`dis:TripletWithinEntityModeShape` and `dis:TripletWithinAccessGateShape`. Both
are `sh:sparql` rather than property paths, because the constraint spans three
subjects — the triplet, the entity's mode matrix, and the role's gate — and
SHACL Core cannot compare across them.

Both carry `FILTER EXISTS { ?any a dis:…Matrix }`, so a dossier that declares no
matrices is unconstrained rather than wholly invalid. **Enumerating the
cross-product is opt-in; once you opt in, it binds.**

### 4.3 The proof

A triplet asserting that the support agent `RESPOND`s on `allergenprofile` — the
model claiming authority to answer *"is this safe for my child"* — is rejected
**twice**:

```
Conforms: False
  d:t99-assert-allergen-safety
    → this triplet's acting role has no access gate granting that mode on that
      entity — authority says who may, and nothing here says this role may
    → this triplet uses a mode the target entity does not support — declare it
      in the entity's EntityModeMatrix, or the triplet is not sayable
```

It does not fail at runtime. It **cannot be written down**, and neither
constraint is a prompt.

### 4.4 It catches the author, not only the adversary

While modelling the worked example, a triplet for *"deflect to the website"* was
declared as `INITIATE` on `Inquiry`. The matrices rejected it: `Inquiry` supports
`CREATE` and `READ`, never `INITIATE`, and no gate granted it. The model was
claiming *the agent starts an inquiry*, when in fact the caller creates one and
the agent hands it somewhere. Retargeted to `RoutingDestination`.

That is the argument for enumerating a cross-product instead of listing the six
interactions you happened to think of.

---

## 5. The divergence this resolves

The published 1.6.0 `.md` documentation and the canonical `.schema.json` files
**disagree** about these constructs. Stated plainly, because an implementer will
hit it:

| Construct | The docs say | The canonical schema says |
|---|---|---|
| `AccessGateMatrix` | has `allowedModes[]` | `{gateId, name, roleId, targetEntityId, gateCondition}` — **no modes**; `gateCondition` is a JMESPath string |
| `EntityModeMatrix` | has `supportedModes[]` | **no such field**; `modeId` is a FK to `Modes` (operational personas). The seven canonical modes appear only nested in `interactionCapabilities[].modeOfInteraction` |
| `AgenticTriplet` | Entity × Mode × Role | a **five-tuple**: `actingEntityId`, `actingRoleId`, `stance`, `modeOfInteraction`, `targetEntityId` |
| `CommonEnums` | 31 enums | defines **26** |

**1.7 resolves this in favour of the documentation's semantics, deliberately.**

The reason is not that the docs are older or more numerous. It is that a
JMESPath `gateCondition` can only be evaluated **at runtime, against a context
the schema never defines**. With it you can observe that a dangerous triplet was
blocked. You cannot *prove it is impossible*. Moving modes onto the gate makes
the constraint **statically checkable**, which is the entire difference between
§4.3 rejecting a triplet at design time and a runtime catching it on the call
that matters.

`gateCondition` is retained as an optional field for genuinely dynamic
conditions. It is no longer the only expression of the gate.

**Nothing in 1.6.0 required a triplet to be legal under both matrices.** §4.2 is
new, and it is the strongest claim in this proposal.

---

## 6. One model, five serialisations

DIS is not a file format. It is one model expressed in five layers, each doing a
job the others cannot.

| Layer | Artifact | What it is for | Enforced by |
|---|---|---|---|
| **CUE** | `cue/*.cue` | **Canonical source.** Types, enums, conditional rules | `cue vet` |
| **JSON Schema** | `schemas/*.schema.json` | **Generated** from CUE. The published contract | any validator |
| **Turtle** | `vocabulary/v1.7.0/dis.ttl`, the dossiers | The RDF vocabulary, and the model itself | parser |
| **SHACL** | `shapes/v1.7.0/dis-shapes.ttl` | **Constraints over the graph** — what may not be written | `pyshacl` |
| **SPARQL** | `queries/*.rq` | **Views and audits** — questions asked of the model | any store |

Turtle and SHACL are the same syntax; SHACL *is* RDF. The distinction is that
`dis.ttl` says what the words mean and `dis-shapes.ttl` says which sentences are
legal.

### 6.1 Why each one is load-bearing

- **CUE** can express *"an `OBLIGATION` must bind at least one value"* as a type,
  so the contract is checked before anything is serialised. JSON Schema cannot
  say it without a `dependentSchemas` contortion.
- **JSON Schema** is what other people's tooling actually consumes. It is
  generated, never hand-edited.
- **Turtle** is the model. A dossier *is* a graph, which is why views, diffs, and
  a canvas all fall out of it without a bespoke format.
- **SHACL** locates a violation by **focus node and path** — the error is
  positioned in the graph rather than thrown from a stack. This is why §4.3
  names the offending triplet instead of reporting "validation failed".
- **SPARQL** answers questions the schema was never designed for. Four exist
  today:

  | Query | Question |
  |---|---|
  | `01-full-graph.rq` | every construct and relation, for rendering |
  | `02-medical-liability.rq` | which policies carry MEDICAL liability, and how each is enforced |
  | `03-structural-audit.rq` | which rules claim STRUCTURAL enforcement — and can the target deliver it |
  | `04-ungoverned-triplets.rq` | **which triplets no policy governs** — the gap finder |

`04` is the one to run in a workshop. It returns the interactions the room
granted and then said nothing about, which is a different and more dangerous
list than the one people arrive with.

### 6.2 Two documented fidelity gaps

Both found by running the generators, not by reading docs.

**CUE → JSON Schema drops `format`.** A round-trip of the published
`Role.schema.json` agreed on 5 of 6 test instances; the divergence was
`format: uuid`, silently lost. Every DIS identifier is `format: uuid`, so a naive
generator relaxes the identity contract across the whole spec.

**CUE → JSON Schema silently drops definitions containing `if` comprehensions.**
No error — it emits the description and nothing else. `#UtterancePolicy` is
therefore kept flat and exportable, and the conditional rules live in
`#UtterancePolicyStrict` (enforced by `cue vet`) and in SHACL (enforced on the
graph).

> **Consequence, stated rather than hidden: the published JSON Schema is WEAKER
> than the full contract.** SHACL carries the difference. An implementation
> validating only against JSON Schema is doing a partial check.

### 6.3 Why RDF at all

`AgenticTriplet` is an RDF triple with three additional commitments:

| | RDF | DIS |
|---|---|---|
| Predicate | any IRI | **closed set of seven modes** |
| Subject / object | any IRI | **Role → Entity, typed** |
| Statement metadata | reification / RDF-star | **reified from the start** |
| Stance | — | **ACT / REACT** |

Because the shape is RDF, the ecosystem applies with no adapters: SHACL for
constraints, SPARQL for views and audits, triple stores, federation, reasoners.
None of that had to be built.

---

## 7. Conformance

An implementation conforms to 1.7 when:

1. It validates dossiers against [`shapes/v1.7.0/dis-shapes.ttl`](../../shapes/v1.7.0/dis-shapes.ttl)
   and reports failures by **focus node and path** — the error positioned in the
   graph, not thrown from a stack.
2. It rejects a triplet outside either matrix when matrices are declared (§4.2).
3. It does not downgrade a `STRUCTURAL` policy to `INSTRUCTED` without reporting
   it (§2).
4. It refuses an `Application` that is both `MOCK` and `SYSTEM_OF_RECORD` (§3.2).
5. It treats `mutates` as declared, never inferred from `httpMethod` (§3.3).

Point 1 matters more than it looks: **a spec whose violations are not locatable
is a style guide.**

---

## 8. Worked example

[`retail.ttl`](../../fixtures/v1.7.0/retail.ttl)
— 400 lines, conforming:

| | |
|---|---|
| Roles | 7 |
| Entities | 6 |
| Agentic triplets | 6 |
| Utterance policies | 5 |
| Applications · Endpoints · Functions | 1 · 3 · 3 |
| Entity-mode matrix rows | 6 |
| Access gate rows | **18** |

Eighteen gate rows for six triplets. **Most of the model is denial**, and that
is the point: the cross-product is enumerated, so the illegal cells are written
down rather than left to be discovered by a caller.

---

## 9. Open questions

Carried forward from the UtterancePolicy proposal, unresolved in 1.7:

1. **Identifier form.** Every ID is `format: uuid`. In Turtle the IRI *is* the
   identity, and a UUID IRI costs every diff and error message its legibility.
   Proposal: slug IRIs as the human handle, UUID demoted to `dis:identifier`.
2. **RDF-star.** Should `AgenticTriplet` stay reified, or become an annotated
   triple (`<< :role :READ :entity >> dis:boundFunction :fn`)? The latter is
   native RDF 1.2; the former is stable and already shipped.
3. **Knowledge.** `KnowledgeDocument` is declared in the vocabulary and unused in
   the worked example. Whether retrieval scope belongs in DIS at all, or is a
   target-profile concern like copy, is undecided.

---

## 10. Files

| Path | |
|---|---|
| [`vocabulary/v1.7.0/dis.ttl`](../../vocabulary/v1.7.0/dis.ttl) | vocabulary — classes, 7 modes, 2 stances, enums, Systems layer, matrices |
| [`shapes/v1.7.0/dis-shapes.ttl`](../../shapes/v1.7.0/dis-shapes.ttl) | SHACL — 352 lines, including the two `sh:sparql` grammar shapes |
| [`cue/v1.7.0/UtterancePolicy.cue`](../../cue/v1.7.0/UtterancePolicy.cue), [`schemas/v1.7.0/UtterancePolicy.schema.json`](../../schemas/v1.7.0/UtterancePolicy.schema.json) | UtterancePolicy CUE canonical source and generated JSON Schema |
| [`queries/v1.7.0/`](../../queries/v1.7.0/) | SPARQL audits — full-graph, medical-liability, structural-audit, ungoverned-triplets |
| [`fixtures/v1.7.0/`](../../fixtures/v1.7.0/) | Reference dossiers across Retail, Healthcare, BFSI, and ITSD/HR (`retail.ttl`, `healthcare.ttl`, `bfsi.ttl`, `itsd-hr.ttl`) |
| [`fixtures/v1.7.0/deformed.ttl`](../../fixtures/v1.7.0/deformed.ttl) | the negative fixture — confirms the shapes reject, not just accept |
