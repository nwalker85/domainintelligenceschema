"""§4.2/§4.3/§4.4: the grammar matrices, mechanised as sh:sparql shapes.

A triplet is legal only if the target Entity supports the mode
(EntityModeMatrix) AND the acting Role has been granted that mode on that
Entity (AccessGateMatrix). Opt-in: a dossier declaring no matrices is
unconstrained (the FILTER EXISTS guard in each shape).
"""
from rdflib import RDF

from conftest import DIS, D, add_triplet


def _remove_all(g, cls):
    for s in list(g.subjects(RDF.type, cls)):
        for t in list(g.triples((s, None, None))):
            g.remove(t)


def test_t99_respond_on_allergenprofile_rejected_by_exactly_both_matrix_shapes(dossier, validate):
    """§4.3: RESPOND on allergenprofile by the support agent — that role's gate
    only grants READ, and the entity's EMM only supports READ."""
    g = dossier("kronos-candies")
    add_triplet(g, D.t99, D["kronos-support-agent"], D.allergenprofile, DIS.RESPOND, DIS.ACT)
    report = validate(g, inference="none")
    assert not report.conforms
    fired = {r.shape for r in report.results if r.focus == "t99"}
    assert fired == {"TripletWithinAccessGateShape", "TripletWithinEntityModeShape"}


def test_initiate_on_inquiry_by_support_agent_rejected_both_shapes(dossier, validate):
    """§4.4 author case: inquiry supports CREATE/READ, and no gate grants
    INITIATE to the support agent on inquiry."""
    g = dossier("kronos-candies")
    add_triplet(g, D.tX, D["kronos-support-agent"], D.inquiry, DIS.INITIATE, DIS.ACT)
    report = validate(g, inference="none")
    assert not report.conforms
    fired = {r.shape for r in report.results if r.focus == "tX"}
    assert fired == {"TripletWithinAccessGateShape", "TripletWithinEntityModeShape"}


def test_mode_supported_but_no_gate_rejected_by_access_gate_shape_only(dossier, validate):
    """distribution-partner READ productattribute: EMM supports READ, but no
    gate grants the distribution partner READ on productattribute."""
    g = dossier("kronos-candies")
    add_triplet(g, D.tY, D["distribution-partner"], D.productattribute, DIS.READ, DIS.ACT)
    report = validate(g, inference="none")
    assert not report.conforms
    fired = {r.shape for r in report.results if r.focus == "tY"}
    assert fired == {"TripletWithinAccessGateShape"}


def test_gate_present_but_entity_does_not_support_rejected_by_entity_mode_shape_only(
    dossier, validate
):
    """Grant consumer UPDATE on product (a gate that did not exist before),
    but product's EMM only supports READ."""
    g = dossier("kronos-candies")
    from rdflib import Literal

    gate = D["gate-consumer-product-update"]
    g.add((gate, RDF.type, DIS.AccessGateMatrix))
    g.add((gate, DIS.matrixRole, D.consumer))
    g.add((gate, DIS.matrixEntity, D.product))
    g.add((gate, DIS.allowedMode, DIS.UPDATE))
    g.add((gate, DIS.name, Literal("consumer -> product: UPDATE")))
    g.add((gate, DIS.description, Literal("granted for this test only")))
    add_triplet(g, D.tZ, D.consumer, D.product, DIS.UPDATE, DIS.ACT)
    report = validate(g, inference="none")
    assert not report.conforms
    fired = {r.shape for r in report.results if r.focus == "tZ"}
    assert fired == {"TripletWithinEntityModeShape"}


def test_removing_all_matrices_makes_the_grammar_unconstrained(dossier, validate):
    """§4.2 last paragraph: opt-in. No matrices declared -> no matrix shape fires."""
    g = dossier("kronos-candies")
    _remove_all(g, DIS.EntityModeMatrix)
    _remove_all(g, DIS.AccessGateMatrix)
    add_triplet(g, D.t99, D["kronos-support-agent"], D.allergenprofile, DIS.RESPOND, DIS.ACT)
    report = validate(g, inference="none")
    assert report.conforms


def test_removing_only_entity_mode_matrices_leaves_access_gate_shape_active(dossier, validate):
    g = dossier("kronos-candies")
    _remove_all(g, DIS.EntityModeMatrix)
    add_triplet(g, D.t99, D["kronos-support-agent"], D.allergenprofile, DIS.RESPOND, DIS.ACT)
    report = validate(g, inference="none")
    assert not report.conforms
    fired = {r.shape for r in report.results if r.focus == "t99"}
    assert fired == {"TripletWithinAccessGateShape"}


def test_every_fixture_triplet_has_a_satisfying_emm_row_and_gate_row(dossier):
    """Compute, in plain Python, what the shapes enforce declaratively: every
    one of the six kronos-candies AgenticTriplets has a matching supportedMode
    on its target entity's EMM, and a matching allowedMode on an AccessGateMatrix
    for its acting role + target entity."""
    g = dossier("kronos-candies")

    supported = set()
    for matrix in g.subjects(RDF.type, DIS.EntityModeMatrix):
        entity = g.value(matrix, DIS.matrixEntity)
        for mode in g.objects(matrix, DIS.supportedMode):
            supported.add((entity, mode))

    allowed = set()
    for gate in g.subjects(RDF.type, DIS.AccessGateMatrix):
        role = g.value(gate, DIS.matrixRole)
        entity = g.value(gate, DIS.matrixEntity)
        for mode in g.objects(gate, DIS.allowedMode):
            allowed.add((role, entity, mode))

    triplets = list(g.subjects(RDF.type, DIS.AgenticTriplet))
    assert len(triplets) == 6
    for t in triplets:
        role = g.value(t, DIS.actingRole)
        entity = g.value(t, DIS.targetEntity)
        mode = g.value(t, DIS.mode)
        assert (entity, mode) in supported, f"{t} not within its entity's EMM"
        assert (role, entity, mode) in allowed, f"{t} not granted by an access gate"
