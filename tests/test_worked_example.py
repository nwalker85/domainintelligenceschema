"""§8 worked-example counts for retail.ttl, plus gaps 1 and 7."""
import pytest
from rdflib import RDF, OWL, Literal

from conftest import DIS, D


COUNTS = {
    DIS.Role: 7,
    DIS.Entity: 6,
    DIS.AgenticTriplet: 6,
    DIS.UtterancePolicy: 5,
    DIS.Application: 1,
    DIS.Endpoint: 3,
    DIS.FunctionCatalogEntry: 3,
    DIS.EntityModeMatrix: 6,
    DIS.AccessGateMatrix: 18,
    DIS.EntityInstance: 9,
}


@pytest.mark.parametrize("cls,expected", list(COUNTS.items()), ids=[str(c).rsplit("/", 1)[-1] for c in COUNTS])
def test_worked_example_construct_counts(dossier, cls, expected):
    g = dossier("retail")
    assert len(set(g.subjects(RDF.type, cls))) == expected


def test_all_entity_instances_are_instanceof_product(dossier):
    g = dossier("retail")
    instances = list(g.subjects(RDF.type, DIS.EntityInstance))
    assert instances
    assert all((i, DIS.instanceOf, D.product) in g for i in instances)


def test_every_endpoint_mutates_false(dossier):
    g = dossier("retail")
    endpoints = list(g.subjects(RDF.type, DIS.Endpoint))
    assert endpoints
    assert all(g.value(e, DIS.mutates) == Literal(False) for e in endpoints)


def test_the_application_is_mock(dossier):
    g = dossier("retail")
    (app,) = list(g.subjects(RDF.type, DIS.Application))
    assert g.value(app, DIS.applicationType) == DIS.MOCK


def test_structural_policies_liability_classes_match_the_03_query_facts(dossier):
    """From queries/03-structural-audit.rq: p1/p4 STANDARD, p2/p3 REGULATORY
    are all STRUCTURAL; p5 is STANDARD but INSTRUCTED."""
    g = dossier("retail")
    structural = {
        g.value(p, DIS.liabilityClass): None
        for p in g.subjects(RDF.type, DIS.UtterancePolicy)
        if g.value(p, DIS.enforcement) == DIS.STRUCTURAL
    }
    assert set(structural.keys()) == {DIS.REGULATORY, DIS.STANDARD}
    p5 = D["p5-greeting-states-scope"]
    assert g.value(p5, DIS.enforcement) == DIS.INSTRUCTED
    assert g.value(p5, DIS.liabilityClass) == DIS.STANDARD


@pytest.mark.parametrize("name", ["retail", "healthcare", "bfsi", "itsd-hr", "dadjoke"])
def test_every_reference_dossier_conforms(repo, validate, vocab, name):
    from rdflib import Graph

    g = Graph()
    for t in vocab:
        g.add(t)
    g.parse(str(repo / f"fixtures/v1.7.0/{name}.ttl"), format="turtle")
    report = validate(g, inference="none")
    assert report.conforms


@pytest.mark.parametrize("name", ["retail", "healthcare", "bfsi", "itsd-hr"])
def test_gap7_every_class_used_in_reference_dossiers_is_declared_in_vocab(dossier, vocab, name):
    g = dossier(name)
    used = {c for c in g.objects(None, RDF.type) if str(c).startswith(str(DIS))}
    declared = set(vocab.subjects(RDF.type, OWL.Class))
    assert used <= declared

