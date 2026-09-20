"""§8 worked-example counts for kronos-candies.ttl, plus gaps 1 and 7."""
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
    g = dossier("kronos-candies")
    assert len(set(g.subjects(RDF.type, cls))) == expected


def test_all_entity_instances_are_instanceof_product(dossier):
    g = dossier("kronos-candies")
    instances = list(g.subjects(RDF.type, DIS.EntityInstance))
    assert instances
    assert all((i, DIS.instanceOf, D.product) in g for i in instances)


def test_every_endpoint_mutates_false(dossier):
    g = dossier("kronos-candies")
    endpoints = list(g.subjects(RDF.type, DIS.Endpoint))
    assert endpoints
    assert all(g.value(e, DIS.mutates) == Literal(False) for e in endpoints)


def test_the_application_is_mock(dossier):
    g = dossier("kronos-candies")
    (app,) = list(g.subjects(RDF.type, DIS.Application))
    assert g.value(app, DIS.applicationType) == DIS.MOCK


def test_structural_policies_liability_classes_match_the_03_query_facts(dossier):
    """From queries/03-structural-audit.rq: p1/p2 MEDICAL, p3 REGULATORY,
    p4 STANDARD are all STRUCTURAL; p5 is STANDARD but INSTRUCTED."""
    g = dossier("kronos-candies")
    structural = {
        g.value(p, DIS.liabilityClass): None
        for p in g.subjects(RDF.type, DIS.UtterancePolicy)
        if g.value(p, DIS.enforcement) == DIS.STRUCTURAL
    }
    assert set(structural.keys()) == {DIS.MEDICAL, DIS.REGULATORY, DIS.STANDARD}
    p5 = D["p5-greeting-states-scope"]
    assert g.value(p5, DIS.enforcement) == DIS.INSTRUCTED
    assert g.value(p5, DIS.liabilityClass) == DIS.STANDARD


@pytest.mark.xfail(strict=True, reason="RAV-1947 gap 1: kronos.ttl does not conform (FunctionCatalogEntry lacks dis:name/dis:callsEndpoint)")
def test_gap1_kronos_conforms(repo, validate, vocab):
    from rdflib import Graph

    g = Graph()
    for t in vocab:
        g.add(t)
    g.parse(str(repo / "fixtures/v1.7.0/kronos.ttl"), format="turtle")
    report = validate(g, inference="none")
    assert report.conforms


@pytest.mark.xfail(strict=True, reason="RAV-1947 gap 1: dadjoke.ttl does not conform (FunctionCatalogEntry lacks dis:name/dis:callsEndpoint)")
def test_gap1_dadjoke_conforms(repo, validate, vocab):
    from rdflib import Graph

    g = Graph()
    for t in vocab:
        g.add(t)
    g.parse(str(repo / "fixtures/v1.7.0/dadjoke.ttl"), format="turtle")
    report = validate(g, inference="none")
    assert report.conforms


@pytest.mark.xfail(
    strict=True,
    reason="RAV-1947 gap 7: kronos-candies.ttl declares `d:dossier a dis:Dossier` "
    "and dis:domainName/dis:disSpecificationRef, none of which exist in dis.ttl "
    "(the vocabulary's actual design is owl:Ontology + dossierType/dossierStatus)",
)
def test_gap7_every_class_used_in_kronos_candies_is_declared_in_vocab(dossier, vocab):
    g = dossier("kronos-candies")
    used = {c for c in g.objects(None, RDF.type) if str(c).startswith(str(DIS))}
    declared = set(vocab.subjects(RDF.type, OWL.Class))
    assert used <= declared
