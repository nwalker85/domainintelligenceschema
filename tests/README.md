# DIS 1.7 conformance suite

## Running

```
uv sync --group test
uv run pytest
```

(or in one line: `uv sync --group test && uv run pytest`). `uv run pytest --co -q`
lists every collected test without running it.

## The recipe

Validate a dossier by merging `vocabulary/v1.7.0/dis.ttl` into the dossier's own
graph and running SHACL with **no** `-i`/inference flag against
`shapes/v1.7.0/dis-shapes.ttl` — that is `scripts/validate-dossier.sh`. Skipping
the vocabulary merge produces false positives (the shapes can't see the enum
individuals' types); adding `-i rdfs` is worse than skipping validation, because
`rdfs:range` silently types an invented value as legitimate instead of catching it.

## The xfail convention

A test marked `@pytest.mark.xfail(strict=True, reason="RAV-1947 gap N: ...")`
asserts the **ideal** behavior and is expected to currently fail — `xfail_strict`
turns an unexpected pass (XPASS) into a hard failure, so the day a gap is
actually closed this suite tells you immediately. Never "fix" a gap by editing
`vocabulary/`, `shapes/`, `fixtures/`, `cue/`, or `schemas/` to make an xfail
test pass — that decision belongs to whoever owns those files.

## The 8 known gaps

| # | What | Test(s) |
|---|------|---------|
| 1 | `kronos.ttl` / `dadjoke.ttl` don't conform (FunctionCatalogEntry lacks `dis:name`/`dis:callsEndpoint`) | `test_worked_example.py::test_gap1_kronos_conforms`, `::test_gap1_dadjoke_conforms` |
| 2 | `VocabularyBoundShape`, `LifecycleNeedsPhaseShape`, `StructuralMedicalShape` each declared twice at text level | `test_vocabulary_integrity.py::test_gap2_no_nodeshape_iri_declared_twice_at_text_level` |
| 3 | Spec says required, shapes say optional: `Application.baseUrl`, `Endpoint.mutates`, `FunctionCatalogEntry.readsEntity`/`inputFields`/`outputFields` | `test_systems_layer.py::test_gap3_*` (5 tests) |
| 4 | `dis:roleType`, `dis:entityType` used as `sh:path` but never declared as a property | `test_vocabulary_integrity.py::test_gap4_no_sh_path_is_left_undeclared` |
| 5 | Nine `rdfs:subClassOf dis:Construct` classes have no targeting NodeShape | `test_vocabulary_integrity.py::test_gap5_every_construct_subclass_has_a_targeting_nodeshape` |
| 6 | `dis:FullView` doesn't show the Systems-layer or matrix palette constructs | `test_vocabulary_integrity.py::test_gap6_fullview_shows_every_palette_constructs_target_class` |
| 7 | `kronos-candies.ttl`/`dadjoke.ttl` use `dis:Dossier`/`dis:domainName`/`dis:disSpecificationRef`, none of which exist in `dis.ttl` | `test_worked_example.py::test_gap7_every_class_used_in_kronos_candies_is_declared_in_vocab` |
| 8 | None of the 23 deprecated v1.6.0 JSON Schemas carry a `deprecated: true` keyword | `test_release_gating.py::test_gap8_deprecated_v16_schemas_carry_deprecated_keyword` |

Gaps 2/4/5/6 also have a companion non-xfail test in the same file that pins
the *exact current* bad set (not just "some gap exists") — if that set ever
changes, that test's failure message says precisely what moved, even before
anyone marks the gap closed.

## One corrected baseline fact

`test_vocabulary_integrity.py::test_shared_enum_individuals_is_exactly_none`
corrects one fact asserted by the implementation brief: the set of individuals
with more than one `rdf:type` among the vocabulary's enum classes is `{NONE}`,
not `{NONE, APPROVED}`. `dis:APPROVED` is typed only as
`dis:ChangeManagementStatus` — the `DossierStatus` block's comment claims it is
"shared", but no triple actually types `dis:APPROVED` as `dis:DossierStatus`.
