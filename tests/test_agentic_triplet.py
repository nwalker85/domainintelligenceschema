"""AgenticTripletShape: the closed grammar (§4.1). Uses a role/entity/mode
combo with a full EMM+gate already in kronos-candies (kronos-support-agent /
product / READ) so the matrix shapes never interfere with these tests."""
import pytest
from rdflib import Literal

from conftest import DIS, D, add_triplet

ROLE = D["kronos-support-agent"]
ENTITY = D.product  # READ is both EMM-supported and gate-granted for this role
MODE = DIS.READ

MODES_WITH_MATRIX_COVERAGE = {
    DIS.READ: (D["kronos-support-agent"], D.product),
    DIS.INITIATE: (D["kronos-support-agent"], D.routingdestination),
}


def test_closed_shape_rejects_extra_property_with_that_path(dossier, validate):
    g = dossier("kronos-candies")
    t = D.tx
    add_triplet(g, t, ROLE, ENTITY, MODE)
    g.add((t, DIS.foo, Literal("x")))
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "tx" and r.path == "foo" for r in report.violations())


def test_stance_maybe_rejected(dossier, validate):
    g = dossier("kronos-candies")
    t = D.tx
    add_triplet(g, t, ROLE, ENTITY, MODE, stance=DIS.MAYBE)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "tx" and r.path == "stance" for r in report.violations())


def test_actingrole_pointing_at_entity_rejected(dossier, validate):
    g = dossier("kronos-candies")
    t = D.tx
    add_triplet(g, t, ENTITY, ENTITY, MODE)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "tx" and r.path == "actingRole" for r in report.violations())


def test_targetentity_pointing_at_role_rejected(dossier, validate):
    g = dossier("kronos-candies")
    t = D.tx
    add_triplet(g, t, ROLE, ROLE, MODE)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "tx" and r.path == "targetEntity" for r in report.violations())


@pytest.mark.parametrize(
    "mode",
    [DIS.CREATE, DIS.READ, DIS.UPDATE, DIS.DELETE, DIS.INITIATE, DIS.RESPOND, DIS.NOTIFY],
)
def test_each_of_the_seven_modes_accepted_when_matrices_are_stripped(dossier, validate, mode):
    """Strip the matrices so this test is purely about mode being in the
    closed set of seven, not about matrix authority."""
    from rdflib import RDF

    g = dossier("kronos-candies")
    for cls in (DIS.EntityModeMatrix, DIS.AccessGateMatrix):
        for s in list(g.subjects(RDF.type, cls)):
            for t in list(g.triples((s, None, None))):
                g.remove(t)
    t = D.tx
    add_triplet(g, t, ROLE, ENTITY, mode)
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_mode_yeet_rejected(dossier, validate):
    g = dossier("kronos-candies")
    t = D.tx
    add_triplet(g, t, ROLE, ENTITY, DIS.YEET)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "tx" and r.path == "mode" for r in report.violations())


def test_second_name_rejected(dossier, validate):
    g = dossier("kronos-candies")
    t = D.tx
    add_triplet(g, t, ROLE, ENTITY, MODE)
    g.add((t, DIS.name, Literal("a second name")))
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "tx" and r.path == "name" for r in report.violations())


def test_second_description_rejected(dossier, validate):
    g = dossier("kronos-candies")
    t = D.tx
    add_triplet(g, t, ROLE, ENTITY, MODE)
    g.add((t, DIS.description, Literal("a second description")))
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "tx" and r.path == "description" for r in report.violations())


def test_missing_description_rejected(dossier, validate):
    from rdflib import RDF

    g = dossier("kronos-candies")
    t = D.tx
    g.add((t, RDF.type, DIS.AgenticTriplet))
    g.add((t, DIS.actingRole, ROLE))
    g.add((t, DIS.targetEntity, ENTITY))
    g.add((t, DIS.mode, MODE))
    g.add((t, DIS.stance, DIS.ACT))
    g.add((t, DIS.name, Literal("tx")))
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "tx" and r.path == "description" for r in report.violations())


def test_boundfunction_pointing_at_endpoint_rejected(dossier, validate):
    g = dossier("kronos-candies")
    t = D.tx
    add_triplet(g, t, ROLE, ENTITY, MODE, boundFunction=D["get-product-attribute"])
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "tx" and r.path == "boundFunction" for r in report.violations())
