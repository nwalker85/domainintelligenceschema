"""dis.ttl <-> dis-shapes.ttl integrity: enums, sh:in/sh:class/sh:path
closure, palette metadata, views, and the shared-enum-collision inventory.

NOTE on a corrected baseline fact: the brief asserted the individuals with
more than one rdf:type among the enum classes are exactly {NONE, APPROVED}.
Verified against the live vocabulary this is wrong: dis:APPROVED is typed
ONLY as dis:ChangeManagementStatus. dis.ttl's own comment above
DossierStatus says APPROVED is "declared once, below, and shared with
ChangeManagementRecord" but no triple actually types dis:APPROVED as
dis:DossierStatus — the sharing described in prose was never encoded. This
test asserts the real set {NONE} and is not "fixing" the vocabulary.
"""
import json
import re
from collections import Counter, defaultdict

import pytest
from rdflib import RDF, RDFS, OWL, Literal
from rdflib.collection import Collection

from conftest import DIS, SH


def _local(iri) -> str:
    s = str(iri)
    return s.rsplit("/", 1)[-1] if "/" in s else s.rsplit("#", 1)[-1]


def test_exactly_seven_modes(vocab):
    modes = {_local(m) for m in vocab.subjects(RDF.type, DIS.Mode)}
    assert modes == {"CREATE", "READ", "UPDATE", "DELETE", "INITIATE", "RESPOND", "NOTIFY"}


def test_exactly_two_stances(vocab):
    stances = {_local(m) for m in vocab.subjects(RDF.type, DIS.Stance)}
    assert stances == {"ACT", "REACT"}


def test_http_method_is_five_values_no_delete_options_head(vocab):
    """CHANGELOG 1.7.0: DELETE -> HTTP_DELETE (dodges SPARQL's DELETE keyword);
    OPTIONS/HEAD dropped as not agent-invokable actions."""
    methods = {_local(m) for m in vocab.subjects(RDF.type, DIS.HttpMethod)}
    assert methods == {"GET", "POST", "PUT", "PATCH", "HTTP_DELETE"}
    assert "DELETE" not in methods
    assert "OPTIONS" not in methods
    assert "HEAD" not in methods


def test_application_type_has_four_values(vocab):
    types = {_local(m) for m in vocab.subjects(RDF.type, DIS.ApplicationType)}
    assert len(types) == 4
    assert types == {"SYSTEM_OF_RECORD", "SAAS_PLATFORM", "MOCK", "KNOWLEDGE_STORE"}


def test_every_sh_in_member_iri_has_a_type_in_the_vocab(vocab, shapes):
    for row in shapes.query("PREFIX sh: <http://www.w3.org/ns/shacl#> SELECT ?list WHERE { ?ps sh:in ?list }"):
        for item in Collection(shapes, row["list"]):
            if isinstance(item, Literal):
                continue  # e.g. RoleShape's "human"/"agent"/"system" string enum
            assert list(vocab.objects(item, RDF.type)), f"{item} has no rdf:type in vocab"


def test_every_sh_class_object_is_an_owl_class_in_the_vocab(vocab, shapes):
    q = "PREFIX sh: <http://www.w3.org/ns/shacl#> SELECT DISTINCT ?c WHERE { ?ps sh:class ?c }"
    seen = list(shapes.query(q))
    assert seen
    for row in seen:
        assert (row["c"], RDF.type, OWL.Class) in vocab, f"{row['c']} is not owl:Class"


def _undeclared_sh_paths(vocab, shapes):
    q = "PREFIX sh: <http://www.w3.org/ns/shacl#> SELECT DISTINCT ?p WHERE { ?ps sh:path ?p }"
    prop_types = {OWL.ObjectProperty, OWL.DatatypeProperty, RDF.Property}
    undeclared = []
    for row in shapes.query(q):
        p = row["p"]
        types = set(vocab.objects(p, RDF.type)) | set(shapes.objects(p, RDF.type))
        if not (types & prop_types):
            undeclared.append(_local(p))
    return set(undeclared)


def test_gap4_every_sh_path_is_declared_as_a_property_in_vocab_or_shapes(vocab, shapes):
    """Documents the exact, current gap-4 set directly (not xfail) because it
    enumerates ALL undeclared paths -- if the set ever grows this test's
    failure message says exactly what changed."""
    assert _undeclared_sh_paths(vocab, shapes) == {"roleType", "entityType"}


@pytest.mark.xfail(
    strict=True,
    reason="RAV-1947 gap 4: dis:roleType and dis:entityType are used as "
    "sh:path but never declared as a property anywhere",
)
def test_gap4_no_sh_path_is_left_undeclared(vocab, shapes):
    assert _undeclared_sh_paths(vocab, shapes) == set()


def _construct_subclasses_without_a_targeting_nodeshape(vocab, shapes):
    subclasses = set(vocab.subjects(RDFS.subClassOf, DIS.Construct))
    targeted = set(shapes.objects(None, SH.targetClass))
    return subclasses - targeted


def test_gap5_the_exact_construct_subclasses_missing_a_nodeshape(vocab, shapes):
    expected = {
        DIS.TagDefinition,
        DIS.PrivacyManifest,
        DIS.TelemetryConfiguration,
        DIS.MarketplaceEntry,
        DIS.ChangeManagementRecord,
        DIS.ValueEngineeringProfile,
        DIS.DossierComparison,
        DIS.KnowledgeDocument,
        DIS.AccessGate,
    }
    assert _construct_subclasses_without_a_targeting_nodeshape(vocab, shapes) == expected


@pytest.mark.xfail(
    strict=True,
    reason="RAV-1947 gap 5: nine rdfs:subClassOf dis:Construct classes have "
    "no NodeShape sh:targetClass -- a class declared only in the vocabulary "
    "is invisible to anything generated from the shapes",
)
def test_gap5_every_construct_subclass_has_a_targeting_nodeshape(vocab, shapes):
    assert _construct_subclasses_without_a_targeting_nodeshape(vocab, shapes) == set()


def _duplicated_nodeshape_names(repo):
    text = (repo / "shapes/v1.7.0/dis-shapes.ttl").read_text()
    names = re.findall(r"^(dis:\w+Shape)\s+a\s+sh:NodeShape", text, re.MULTILINE)
    return {name for name, count in Counter(names).items() if count > 1}


def test_gap2_the_exact_nodeshapes_declared_twice(repo):
    assert _duplicated_nodeshape_names(repo) == {
        "dis:VocabularyBoundShape",
        "dis:LifecycleNeedsPhaseShape",
        "dis:StructuralMedicalShape",
    }


@pytest.mark.xfail(
    strict=True,
    reason="RAV-1947 gap 2: VocabularyBoundShape, LifecycleNeedsPhaseShape "
    "and StructuralMedicalShape are each declared twice (text-level, "
    "~lines 107-133 and 160-187) -- harmless under SHACL semantics "
    "(shape merge) but a maintenance trap",
)
def test_gap2_no_nodeshape_iri_declared_twice_at_text_level(repo):
    assert _duplicated_nodeshape_names(repo) == set()


def test_every_palette_shape_has_name_description_order_and_a_declared_group(shapes):
    palette_shapes = list(shapes.subjects(DIS.paletteConstruct, Literal(True)))
    assert len(palette_shapes) == 9
    for s in palette_shapes:
        assert shapes.value(s, SH.name) is not None, s
        assert shapes.value(s, SH.description) is not None, s
        assert shapes.value(s, SH.order) is not None, s
        group = shapes.value(s, SH.group)
        assert group is not None, s
        assert (group, RDF.type, SH.PropertyGroup) in shapes, group


def test_palette_order_unique_within_each_group(shapes):
    palette_shapes = list(shapes.subjects(DIS.paletteConstruct, Literal(True)))
    by_group = defaultdict(list)
    for s in palette_shapes:
        by_group[shapes.value(s, SH.group)].append(shapes.value(s, SH.order))
    for group, orders in by_group.items():
        assert len(orders) == len(set(orders)), f"duplicate sh:order in {group}: {orders}"


def test_every_showsconstruct_is_a_declared_class(vocab, shapes):
    shown = set(shapes.objects(None, DIS.showsConstruct))
    assert shown
    for c in shown:
        assert (c, RDF.type, OWL.Class) in vocab, c


def _palette_targets_missing_from_fullview(shapes):
    palette_targets = {
        shapes.value(s, SH.targetClass)
        for s in shapes.subjects(DIS.paletteConstruct, Literal(True))
    }
    full_view_shows = set(shapes.objects(DIS.FullView, DIS.showsConstruct))
    return palette_targets - full_view_shows


def test_gap6_the_exact_palette_constructs_fullview_omits(shapes):
    expected = {DIS.AccessGateMatrix, DIS.Application, DIS.Endpoint, DIS.EntityModeMatrix, DIS.FunctionCatalogEntry}
    assert _palette_targets_missing_from_fullview(shapes) == expected


@pytest.mark.xfail(
    strict=True,
    reason="RAV-1947 gap 6: dis:FullView ('Everything') shows only Role/"
    "Entity/AgenticTriplet/UtterancePolicy, not the Systems-layer or matrix "
    "palette constructs added since",
)
def test_gap6_fullview_shows_every_palette_constructs_target_class(shapes):
    assert _palette_targets_missing_from_fullview(shapes) == set()


def test_shared_enum_individuals_is_exactly_none(vocab):
    """Corrected baseline (see module docstring): only dis:NONE is genuinely
    multi-typed (AuthMethod + TelemetryLogLevel). dis:APPROVED, despite the
    prose comment, is only ever typed as dis:ChangeManagementStatus."""
    construct_subclasses = set(vocab.subjects(RDFS.subClassOf, DIS.Construct)) | {DIS.Construct}
    non_enum = construct_subclasses | {DIS.AgenticTriplet, DIS.UtterancePolicy}
    enum_classes = set(vocab.subjects(RDF.type, OWL.Class)) - non_enum

    type_count = defaultdict(set)
    for cls in enum_classes:
        for ind in vocab.subjects(RDF.type, cls):
            type_count[ind].add(cls)
    multi = {ind for ind, types in type_count.items() if len(types) > 1}
    assert multi == {DIS.NONE}

    # documented-deliberate check: NONE's comment exists somewhere near its declarations
    assert (DIS.NONE, RDF.type, DIS.AuthMethod) in vocab
    assert (DIS.NONE, RDF.type, DIS.TelemetryLogLevel) in vocab

    # and record that APPROVED is NOT (contra the brief) multiply typed
    approved_types = set(vocab.objects(DIS.APPROVED, RDF.type))
    assert approved_types == {DIS.ChangeManagementStatus}


ENUM_PARITY_CASES = [
    # (vocab class local name, cue #Name, json $defs key, shacl sh:in path local name)
    ("PolicyType", "PolicyType", "PolicyType", "policyType"),
    ("Enforcement", "Enforcement", "Enforcement", "enforcement"),
    ("LiabilityClass", "LiabilityClass", "LiabilityClass", "liabilityClass"),
    ("ViolationAction", "Violation", "Violation", "onViolation"),
    ("LifecyclePhase", "Lifecycle", "Lifecycle", "lifecyclePhase"),
]


@pytest.fixture(scope="module")
def cue_disjunctions(repo):
    text = (repo / "cue/v1.7.0/UtterancePolicy.cue").read_text()
    out = {}
    for m in re.finditer(r"#(\w+):\s*(\".+)", text):
        name, rhs = m.groups()
        out[name] = set(re.findall(r'"([^"]+)"', rhs))
    return out


@pytest.fixture(scope="module")
def json_schema_defs(repo):
    data = json.loads((repo / "schemas/v1.7.0/UtterancePolicy.schema.json").read_text())
    return {k: set(v["enum"]) for k, v in data["$defs"].items() if "enum" in v}


@pytest.mark.parametrize("vocab_cls,cue_name,json_key,shacl_path", ENUM_PARITY_CASES)
def test_enum_parity_across_vocab_cue_json_shacl(
    vocab, shapes, cue_disjunctions, json_schema_defs, vocab_cls, cue_name, json_key, shacl_path
):
    vocab_set = {_local(x) for x in vocab.subjects(RDF.type, DIS[vocab_cls])}
    assert vocab_set == cue_disjunctions[cue_name], f"{vocab_cls} vs CUE #{cue_name}"
    assert vocab_set == json_schema_defs[json_key], f"{vocab_cls} vs JSON $defs.{json_key}"

    shacl_set = None
    for row in shapes.query(
        "PREFIX sh: <http://www.w3.org/ns/shacl#> PREFIX dis: <https://schemas.domainintelligenceschema.org/dis/1.7.0/> "
        "SELECT ?list WHERE { dis:UtterancePolicyShape sh:property ?ps . ?ps sh:path dis:%s ; sh:in ?list }" % shacl_path
    ):
        shacl_set = {_local(x) for x in Collection(shapes, row["list"])}
    assert shacl_set == vocab_set, f"{vocab_cls} vs UtterancePolicyShape sh:in on {shacl_path}"


def test_ontology_version_and_namespace(vocab):
    from rdflib import URIRef

    ontology_iri = URIRef(str(DIS))
    version = vocab.value(ontology_iri, OWL.versionInfo)
    assert str(version) == "1.7.0"
    assert str(DIS).endswith("/1.7.0/")
