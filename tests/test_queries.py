"""queries/v1.8.0/*.rq against the merged vocab+reference dossier graphs."""
from rdflib.plugins.sparql import prepareQuery

from conftest import DIS


def _local(iri) -> str:
    s = str(iri)
    return s.rsplit("/", 1)[-1] if "/" in s else s.rsplit("#", 1)[-1]


def _run(g, repo, filename):
    text = (repo / "queries/v1.8.0" / filename).read_text()
    return g.query(prepareQuery(text))


def test_04_ungoverned_triplets_returns_exactly_t4_and_t5(dossier, repo):
    g = dossier("retail")
    rows = list(_run(g, repo, "04-ungoverned-triplets.rq"))
    names = {_local(r["triplet"]) for r in rows}
    assert names == {"t4-route-to-human-support", "t5-route-to-store-associate"}


def test_03_structural_audit_returns_5_rows_only_p5_instructed(dossier, repo):
    g = dossier("retail")
    rows = list(_run(g, repo, "03-structural-audit.rq"))
    assert len(rows) == 5
    instructed = [r for r in rows if _local(r["enforcement"]) == "INSTRUCTED"]
    assert len(instructed) == 1
    assert _local(instructed[0]["policy"]) == "p5-greeting-states-scope"


def test_02_medical_liability_construct_scopes_to_medical_policies_in_healthcare(dossier, repo):
    g = dossier("healthcare")
    result_graph = _run(g, repo, "02-medical-liability.rq").graph
    subjects = {_local(s) for s in result_graph.subjects()}
    assert {
        "p1-clinical-advice-prohibition",
        "p2-emergency-symptom-escalation",
        "t4-escalate-symptom-triage",
        "t5-dispatch-emergency-crisis",
    } <= subjects
    assert "p3-hipaa-phi-notice" not in subjects
    assert "p4-cancellation-notice" not in subjects
    assert "p5-greeting-scope" not in subjects


def test_01_full_graph_strips_prose_and_labels_named_subjects(dossier, repo):
    g = dossier("retail")
    result_graph = _run(g, repo, "01-full-graph.rq").graph
    preds = {_local(p) for p in result_graph.predicates()}
    assert "description" not in preds
    assert "requirement" not in preds
    assert "__label" in preds

