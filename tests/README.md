# DIS 1.7 conformance suite

## Running

```
uv sync --group test
uv run pytest
```

(or in one line: `uv sync --group test && uv run pytest`). `uv run pytest --co -q`
lists every collected test without running it.

## The recipe

Validate a dossier by merging `vocabulary/v1.8.0/dis.ttl` into the dossier's own
graph and running SHACL with **no** `-i`/inference flag against
`shapes/v1.8.0/dis-shapes.ttl` — that is `scripts/validate-dossier.sh`. Skipping
the vocabulary merge produces false positives (the shapes can't see the enum
individuals' types); adding `-i rdfs` is worse than skipping validation, because
`rdfs:range` silently types an invented value as legitimate instead of catching it.

## The xfail convention

A test marked `@pytest.mark.xfail(strict=True, reason="RAV-1947 gap N: ...")`
asserts the **ideal** behavior and is expected to currently fail — `xfail_strict`
turns an unexpected pass (XPASS) into a hard failure, so the day a gap is
actually closed this suite tells you immediately. All 13 such markers from
RAV-1947 phase 1 are gone as of phase 2 — every gap below is closed and its
test now passes for real, unmarked.

## Eight gaps found and closed in RAV-1947

| # | What | What changed | Test(s) |
|---|------|---------------|---------|
| 1 | Reference fixtures / `dadjoke.ttl` don't conform (FunctionCatalogEntry lacks `dis:name`/`dis:callsEndpoint`) | Ported to the Systems layer: an `Application` and `Endpoint` each, `dis:name`/`dis:callsEndpoint`/`dis:readsEntity`/`dis:inputFields`/`dis:outputFields` on each `FunctionCatalogEntry`, `dis:mutates` moved onto the Endpoint | `test_worked_example.py::test_every_reference_dossier_conforms`, `::test_gap1_dadjoke_conforms` |
| 2 | `VocabularyBoundShape`, `LifecycleNeedsPhaseShape`, `StructuralMedicalShape` each declared twice at text level | Removed the second, byte-identical copies | `test_vocabulary_integrity.py::test_gap2_no_nodeshape_iri_declared_twice_at_text_level` |
| 3 | Spec says required, shapes say optional: `Application.baseUrl`, `Endpoint.mutates`, `FunctionCatalogEntry.readsEntity`/`inputFields`/`outputFields` | Added `sh:minCount 1` to each | `test_systems_layer.py::test_gap3_*` (5 tests) |
| 4 | `dis:roleType`, `dis:entityType` used as `sh:path` but never declared as a property | Declared both as `owl:DatatypeProperty` in `dis.ttl` | `test_vocabulary_integrity.py::test_gap4_no_sh_path_is_left_undeclared` |
| 5 | Nine `rdfs:subClassOf dis:Construct` classes have no targeting NodeShape | Added NodeShapes for the eight real ones (TagDefinition, PrivacyManifest, TelemetryConfiguration, MarketplaceEntry, ChangeManagementRecord, ValueEngineeringProfile, DossierComparison, KnowledgeDocument); `dis:AccessGate` — the ninth, a leftover duplicate of `dis:AccessGateMatrix` — was removed from the vocabulary instead | `test_vocabulary_integrity.py::test_gap5_every_construct_subclass_has_a_targeting_nodeshape`, `tests/test_governance_constructs.py` |
| 6 | `dis:FullView` doesn't show the Systems-layer or matrix palette constructs | `FullView` now shows every `dis:paletteConstruct true` target class; added `dis:SystemsView` and `dis:GrammarView` | `test_vocabulary_integrity.py::test_gap6_fullview_shows_every_palette_constructs_target_class`, `::test_gap6_systems_view_and_grammar_view_exist` |
| 7 | Early drafts / `dadjoke.ttl` use `dis:Dossier`/`dis:domainName`/`dis:disSpecificationRef`, none of which exist in `dis.ttl` | Replaced with the vocabulary's own `owl:Ontology`/`dis:dossierType`/`dis:dossierStatus`/`owl:versionInfo` header, now constrained by `DossierMetadataShape`/`DossierStatusMetadataShape` | `test_worked_example.py::test_gap7_every_class_used_in_reference_dossiers_is_declared_in_vocab`, `tests/test_governance_constructs.py` |
| 8 | None of the 23 deprecated v1.6.0 JSON Schemas carry a `deprecated: true` keyword | Added `"deprecated": true` to each `.schema.json`, plus `"supersededBy": "1.7.0"` on `index.json` | `test_release_gating.py::test_gap8_deprecated_v16_schemas_carry_deprecated_keyword` |

## One corrected-then-closed baseline fact

`test_vocabulary_integrity.py::test_shared_enum_individuals_are_exactly_none_and_approved`
(formerly `test_shared_enum_individuals_is_exactly_none`) tracked a fact the
phase-1 implementation brief got wrong: the set of individuals with more than
one `rdf:type` among the vocabulary's enum classes was `{NONE}`, not
`{NONE, APPROVED}` — `dis:APPROVED` was typed only as
`dis:ChangeManagementStatus`, though the `DossierStatus` block's comment
claimed it was "shared". Gap 5's fix adds the missing
`dis:APPROVED a dis:DossierStatus` triple, so the prose and the graph now
agree and the real set is `{NONE, APPROVED}`.
