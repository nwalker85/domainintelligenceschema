"""EntityInstanceShape / InstanceNotSelfConfusableShape — the closed
instance-set construct (1.7)."""
from rdflib import Literal

from conftest import DIS, D, add_node

INSTANCE_OK = dict(
    instanceOf=D.product,
    spokenForm=Literal("The Thing"),
    systemKey=Literal("the-thing"),
)


def _instance(g, iri, **overrides):
    props = dict(INSTANCE_OK)
    props.update(overrides)
    return add_node(g, iri, DIS.EntityInstance, **props)


def test_missing_instanceof_rejected(dossier, validate):
    g = dossier("retail")
    _instance(g, D.ix, instanceOf=None)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "ix" and r.path == "instanceOf" for r in report.violations())


def test_instanceof_pointing_at_role_rejected(dossier, validate):
    g = dossier("retail")
    _instance(g, D.ix, instanceOf=D["retail-support-agent"])
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "ix" and r.path == "instanceOf" for r in report.violations())


def test_missing_spokenform_rejected(dossier, validate):
    g = dossier("retail")
    _instance(g, D.ix, spokenForm=None)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "ix" and r.path == "spokenForm" for r in report.violations())


def test_missing_systemkey_rejected(dossier, validate):
    g = dossier("retail")
    _instance(g, D.ix, systemKey=None)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "ix" and r.path == "systemKey" for r in report.violations())


def test_two_systemkeys_rejected(dossier, validate):
    g = dossier("retail")
    _instance(g, D.ix, systemKey=[Literal("a"), Literal("b")])
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "ix" and r.path == "systemKey" for r in report.violations())


def test_confusablewith_pointing_at_entity_rejected(dossier, validate):
    g = dossier("retail")
    _instance(g, D.ix, confusableWith=D.product)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "ix" and r.path == "confusableWith" for r in report.violations())


def test_self_confusable_rejected(dossier, validate):
    g = dossier("retail")
    _instance(g, D.ix, confusableWith=D.ix)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(
        r.focus == "ix" and r.shape == "InstanceNotSelfConfusableShape"
        for r in report.violations()
    )


def test_two_instances_with_same_spokenform_accepted(dossier, validate):
    g = dossier("retail")
    _instance(g, D.ix1, spokenForm=Literal("Same Name"), systemKey=Literal("key-1"))
    _instance(g, D.ix2, spokenForm=Literal("Same Name"), systemKey=Literal("key-2"))
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_fixture_earbuds_confusable_pair_present_and_one_directional(dossier):
    g = dossier("retail")
    a, b = D["p-wireless-earbuds-pro"], D["p-wireless-earbuds"]
    assert (a, DIS.confusableWith, b) in g
    assert (b, DIS.confusableWith, a) not in g
