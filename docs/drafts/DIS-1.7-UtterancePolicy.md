# DIS 1.7 — UtterancePolicy

**Status:** Proposal · **Date:** 2026-09-14 · **Author:** Nathan Walker
**Adds:** one construct · **Breaks:** nothing in 1.6.0

---

## 1. Why

DIS 1.6.0 models **structure** — who may do what to what. It has no construct for
**what an agent may say.**

`AccessGateMatrix` answers *may this Role reach this Entity*. It cannot express:

> *The consumer may read the gluten-free field — but that value must never be uttered
> without the facility disclosure attached.*

Access is **granted**. The constraint is on the **form of the utterance**. Three independent
domains hit the same wall:

| Domain | Rule with no home in 1.6.0 |
|---|---|
| Confectionery | allergen value must carry the facility disclosure |
| Benefits administration | no balance or claim detail before verification; account numbers read back as last-4 only |
| Any tool-bearing agent | when the function is unavailable, say so — never substitute generated content |

This was found empirically, by decompiling a working agent configuration into a dossier
and recording every field with no DIS construct. The homeless fields fell into exactly two
groups: **target-profile settings** (model, channel, deploy — correctly out of scope) and
**utterance rules** (persona, messages, instructions — genuinely missing).

## 2. The construct

**Required:** `policyId` · `name` · `description` · `policyType` · `requirement` · `enforcement`

```
policyType    OBLIGATION | PROHIBITION | DISCLOSURE_LIMIT | LIFECYCLE
requirement   the rule, as a condition — never copy, never steps
enforcement   STRUCTURAL | INSTRUCTED | ADVISORY
```

**Scoping** (optional; absent = domain-wide): `appliesToRoleIds` · `appliesToTripletIds` ·
`appliesToEntityIds` · `condition` · `lifecyclePhase`

**Two fields that carry the weight:**

`boundValueRefs` — for OBLIGATION, the values that must **travel with** the utterance. This is
what makes a cross-scope rule expressible: a per-entity attribute and a domain-level
disclosure are different scopes of one question, and this field binds them.

`enforcement` — where the rule is actually enforced. **STRUCTURAL** means the target *cannot*
produce a violating utterance (composed data, withheld capability). **INSTRUCTED** means it is
asked for and can be forgotten under context pressure.

> **Compilers MUST NOT silently downgrade STRUCTURAL to INSTRUCTED.** If a target cannot
> enforce structurally, the compiler reports it. This is the clause that makes the field
> load-bearing rather than documentary.

`liabilityClass` drives escalation thresholds; `onViolation` says what happens on breach.

## 3. What it deliberately excludes

**The words.** *"Hi, I'm the Kronos Candies assistant"* is copy — it belongs to the target
profile, varies by channel and language, and would make DIS non-portable. The **rule**
(*"the greeting must name scope and must not invite open-ended requests"*) is what travels.

**Procedure.** `requirement` states a condition, not steps. The moment DIS holds steps it stops
being target-agnostic — LangGraph and a voice platform sequence differently.

## 4. Representation — one model, four serialisations

| Layer | Artifact | Role |
|---|---|---|
| **CUE** | `cue/UtterancePolicy.cue` | Canonical source. Types, enums, conditionals |
| **JSON Schema** | `schemas/UtterancePolicy.schema.json` | **Generated** from CUE. The published contract |
| **Turtle** | `vocabulary/dis.ttl` | The RDF vocabulary — classes, the closed verb set, enums |
| **SHACL** | `shapes/dis-shapes.ttl` | Constraints over the graph |
| **SPARQL** | `queries/*.rq` | Views and audits |

### 4.1 Two documented fidelity gaps

Both were found by running the generators, not by reading docs.

**CUE → JSON Schema drops `format`.** A round-trip of published `Role.schema.json` agreed on
5 of 6 test instances; the divergence was `format: uuid` silently lost. Every DIS identifier
is `format: uuid`, so a naive generator would relax the identity contract across the whole spec.

**CUE → JSON Schema silently drops definitions containing `if` comprehensions.** No error — it
emits the description and nothing else. `#UtterancePolicy` is therefore kept flat and
exportable; the conditional rules live in `#UtterancePolicyStrict` (enforced by `cue vet`)
and in SHACL (enforced on the graph).

> **Consequence, stated rather than hidden: the published JSON Schema is WEAKER than the full
> contract.** SHACL carries the difference. Any implementation validating only against JSON
> Schema is doing a partial check.

## 5. Why RDF

`AgenticTriplet` is an RDF triple with three additional commitments:

| | RDF | DIS |
|---|---|---|
| Predicate | any IRI | **closed set of seven modes** |
| Subject / object | any IRI | **Role → Entity, typed** |
| Statement metadata | reification / RDF-star (RDF 1.2) | **reified from the start** |
| Stance | — | **ACT / REACT** |

Because the shape is RDF, the ecosystem applies without adapters: SHACL for constraints,
SPARQL for views and audits, triple stores, federation, reasoners.

## 6. Verification

Everything below was executed, not asserted.

| Check | Result |
|---|---|
| Vocabulary parses | ✅ 235 triples with the Kronos fixture loaded |
| CUE vets clean | ✅ |
| `OBLIGATION` without `boundValueRefs` rejected by `cue vet -c` | ✅ `bad.boundValueRefs.0: incomplete value` |
| JSON Schema generated from CUE | ✅ 17 properties · 6 required · 6 enum defs |
| Kronos fixture validates against SHACL | ✅ `Conforms: True` |
| Deformed fixture rejected | ✅ 3 violations — wrong target class, invented mode, obligation binding nothing |
| SPARQL audit — enforcement vs liability | ✅ 3 policies ranked |
| SPARQL gap finder — ungoverned triplets | ✅ empty on a fully-governed dossier |
| Graph renders | ✅ 87 nodes · 73 edges · 2 views |

### 6.1 The deformed fixture

```
Constraint Violation in ClassConstraintComponent
    Focus Node:  d:bad-target      Result Path: dis:targetEntity
    Message:     targetEntity must reference a dis:Entity — not a Role

Constraint Violation in InConstraintComponent
    Focus Node:  d:bad-mode        Value Node:  dis:YEET
    Message:     mode must be one of the seven protocol modes

Constraint Violation in OrConstraintComponent
    Focus Node:  d:bad-policy
    Message:     an OBLIGATION must bind at least one value
```

The middle one is *"do not invent verbs"* mechanised. The report locates each fault by **focus
node and path** — the error is positioned in the graph rather than thrown from a stack.

## 7. Open questions

1. **Identifier form.** Every ID is `format: uuid`. In Turtle the IRI *is* the identity, and a
   UUID IRI costs every diff and error message its legibility. Proposal: slug IRIs as the human
   handle, UUID demoted to `dis:identifier`.
2. **RDF-star.** Should `AgenticTriplet` stay reified, or become an annotated triple
   (`<< :role :READ :entity >> dis:boundFunction :fn`)? The latter is native RDF 1.2 and
   interoperable; the former is stable and already shipped.
3. **Containment.** Hierarchical IRIs express the containment tree structurally. Invariants 4
   and 5 (catalog = home ∪ ancestors, never siblings) require `sh:sparql` — SHACL Core cannot
   compare a reference against the focus node's own path. **Invariants 6 and 7 must NOT be
   enforced this way:** access is by assignment, never by tree position. The IRI names the node;
   the authority service decides. The string is never the check.

## 8. Files

```
vocabulary/dis.ttl                     RDF vocabulary — classes, 7 modes, 2 stances, 1.7 enums
cue/UtterancePolicy.cue                canonical source (+ #UtterancePolicyStrict)
schemas/UtterancePolicy.schema.json    generated
shapes/dis-shapes.ttl                  SHACL — triplet shape, policy shape, vocabulary conformance
fixtures/kronos.ttl                    3 policies across OBLIGATION / PROHIBITION / LIFECYCLE
../fixtures/deformed.ttl               3 deliberate deformities
queries/01..04.rq                      views + audits
demo/                                  Oxigraph → SPARQL → Cytoscape, 2 views
```
