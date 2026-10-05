"""§2 UtterancePolicy + UtterancePolicyShape/VocabularyBoundShape/
LifecycleNeedsPhaseShape/StructuralMedicalShape."""
from rdflib import Literal, URIRef

from conftest import DIS, D, add_node

BASE_OK = dict(
    name=Literal("ok policy"),
    description=Literal("ok description"),
    requirement=Literal("must do the thing"),
    enforcement=DIS.STRUCTURAL,
    policyType=DIS.PROHIBITION,
)


def _policy(g, iri, **overrides):
    props = dict(BASE_OK)
    props.update(overrides)
    return add_node(g, iri, DIS.UtterancePolicy, **props)


def test_obligation_without_bound_value_rejected(dossier, validate):
    g = dossier("retail")
    _policy(g, D.px, policyType=DIS.OBLIGATION, boundValue=None)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "px" and r.component == "OrConstraintComponent" for r in report.results)


def test_obligation_with_one_bound_value_accepted(dossier, validate):
    g = dossier("retail")
    _policy(g, D.px, policyType=DIS.OBLIGATION, boundValue=D.some_value)
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_lifecycle_without_phase_rejected(dossier, validate):
    g = dossier("retail")
    _policy(g, D.px, policyType=DIS.LIFECYCLE)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.shape == "LifecycleNeedsPhaseShape" for r in report.results)


def test_lifecycle_with_phase_accepted(dossier, validate):
    g = dossier("retail")
    _policy(g, D.px, policyType=DIS.LIFECYCLE, lifecyclePhase=DIS.GREETING)
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_medical_instructed_warns_but_conforms_with_allow_warnings(dossier, validate):
    g = dossier("retail")
    _policy(g, D.px, enforcement=DIS.INSTRUCTED, liabilityClass=DIS.MEDICAL)
    report = validate(g, inference="none")
    assert not report.conforms
    warns = [r for r in report.results if r.shape == "StructuralMedicalShape"]
    assert warns and all(r.severity == "Warning" for r in warns)
    assert not any(r.severity == "Violation" for r in report.results)
    report2 = validate(g, inference="none", allow_warnings=True)
    assert report2.conforms


def test_missing_enforcement_rejected(dossier, validate):
    g = dossier("retail")
    _policy(g, D.px, enforcement=None)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "px" and r.path == "enforcement" for r in report.violations())


def test_enforcement_magic_rejected(dossier, validate):
    g = dossier("retail")
    _policy(g, D.px, enforcement=DIS.MAGIC)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "px" and r.path == "enforcement" for r in report.violations())


def test_missing_requirement_rejected(dossier, validate):
    g = dossier("retail")
    _policy(g, D.px, requirement=None)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "px" and r.path == "requirement" for r in report.violations())


def test_liability_class_pii_wrong_class_rejected(dossier, validate):
    """dis:PII is a real IRI in the vocab, but it's a DataCategory, not a
    LiabilityClass -- VocabularyBoundShape's sh:class must catch it even
    though it isn't sh:in-listed at all."""
    g = dossier("retail")
    _policy(g, D.px, liabilityClass=DIS.PII)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "px" and r.path == "liabilityClass" for r in report.violations())


def test_bound_value_literal_rejected_wrong_nodekind(dossier, validate):
    g = dossier("retail")
    _policy(g, D.px, policyType=DIS.OBLIGATION, boundValue=Literal("a literal"))
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "px" and r.path == "boundValue" for r in report.violations())


def test_two_lifecycle_phases_rejected(dossier, validate):
    g = dossier("retail")
    _policy(
        g,
        D.px,
        policyType=DIS.LIFECYCLE,
        lifecyclePhase=[DIS.GREETING, DIS.CLOSING],
    )
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "px" and r.path == "lifecyclePhase" for r in report.violations())


def test_applies_to_triplet_pointing_at_role_rejected(dossier, validate):
    g = dossier("retail")
    _policy(g, D.px, appliesToTriplet=D["retail-support-agent"])
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "px" and r.path == "appliesToTriplet" for r in report.violations())


def test_applies_to_role_pointing_at_entity_rejected(dossier, validate):
    g = dossier("retail")
    _policy(g, D.px, appliesToRole=D.product)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "px" and r.path == "appliesToRole" for r in report.violations())
