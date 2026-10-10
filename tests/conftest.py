"""Shared fixtures for the DIS 1.8 conformance suite.

`dossier(name)` returns a FRESH merged graph each call (vocab + one fixture)
so tests can mutate it (add_triplet / add_node) without bleeding state into
other tests. `validate(graph, **kw)` wraps pyshacl.validate and returns a
small, readable Report instead of the raw results graph.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest
from rdflib import Graph, Namespace, RDF
from pyshacl import validate as _pyshacl_validate

DIS = Namespace("https://schemas.domainintelligenceschema.org/dis/1.8.0/")
D = Namespace("https://dossier.ravenhelm.dev/retail/")
SH = Namespace("http://www.w3.org/ns/shacl#")

REPO = Path(__file__).resolve().parent.parent
VOCAB_PATH = REPO / "vocabulary/v1.8.0/dis.ttl"
SHAPES_PATH = REPO / "shapes/v1.8.0/dis-shapes.ttl"
FIXTURES_DIR = REPO / "fixtures/v1.8.0"


def _local(iri) -> str:
    """Shorten an IRI/Literal to its local name (or the literal's own repr)."""
    s = str(iri)
    if "#" in s:
        return s.rsplit("#", 1)[-1]
    return s.rsplit("/", 1)[-1]


@dataclass(frozen=True)
class Result:
    focus: str | None
    shape: str | None
    severity: str | None
    path: str | None
    component: str | None
    message: str | None


@dataclass
class Report:
    conforms: bool
    results: list[Result] = field(default_factory=list)

    def violations(self) -> list[Result]:
        return [r for r in self.results if r.severity == "Violation"]

    def warnings(self) -> list[Result]:
        return [r for r in self.results if r.severity == "Warning"]

    def by_shape(self, name: str) -> list[Result]:
        return [r for r in self.results if r.shape == name]


@pytest.fixture(scope="session")
def repo() -> Path:
    return REPO


@pytest.fixture(scope="session")
def vocab() -> Graph:
    return Graph().parse(str(VOCAB_PATH), format="turtle")


@pytest.fixture(scope="session")
def shapes() -> Graph:
    return Graph().parse(str(SHAPES_PATH), format="turtle")


@pytest.fixture
def dossier(vocab):
    """Factory: dossier("retail") -> a NEW merged Graph each call."""

    def _make(name: str) -> Graph:
        g = Graph()
        for triple in vocab:
            g.add(triple)
        g.parse(str(FIXTURES_DIR / f"{name}.ttl"), format="turtle")
        return g

    return _make


@pytest.fixture
def validate():
    """validate(graph, **kw) -> Report. kw forwarded to pyshacl.validate."""

    def _validate(graph: Graph, shapes_graph: Graph | None = None, **kw) -> Report:
        if shapes_graph is None:
            shapes_graph = Graph().parse(str(SHAPES_PATH), format="turtle")
        conforms, results_graph, _text = _pyshacl_validate(
            graph, shacl_graph=shapes_graph, **kw
        )
        results = []
        for r in results_graph.subjects(RDF.type, SH.ValidationResult):
            focus = results_graph.value(r, SH.focusNode)
            shape = results_graph.value(r, SH.sourceShape)
            severity = results_graph.value(r, SH.resultSeverity)
            path = results_graph.value(r, SH.resultPath)
            component = results_graph.value(r, SH.sourceConstraintComponent)
            message = results_graph.value(r, SH.resultMessage)
            results.append(
                Result(
                    focus=_local(focus) if focus is not None else None,
                    shape=_local(shape) if shape is not None else None,
                    severity=_local(severity) if severity is not None else None,
                    path=_local(path) if path is not None else None,
                    component=_local(component) if component is not None else None,
                    message=str(message) if message is not None else None,
                )
            )
        return Report(conforms=conforms, results=results)

    return _validate


def add_triplet(g: Graph, iri, role, entity, mode, stance=DIS.ACT, **extra):
    """Build a minimal, valid AgenticTriplet node for negative-case fixtures."""
    from rdflib import Literal

    g.add((iri, RDF.type, DIS.AgenticTriplet))
    g.add((iri, DIS.actingRole, role))
    g.add((iri, DIS.targetEntity, entity))
    g.add((iri, DIS.mode, mode))
    g.add((iri, DIS.stance, stance))
    g.add((iri, DIS.name, Literal(_local(iri))))
    g.add((iri, DIS.description, Literal(f"{_local(iri)} description")))
    for key, value in extra.items():
        g.add((iri, DIS[key], value))
    return iri


def add_node(g: Graph, iri, cls, **props):
    """Build an arbitrary typed node with the given dis:-namespaced properties.

    A value of None removes/skips that property. A list value adds each item
    as a separate triple (for multi-valued properties in negative cases).
    """
    g.add((iri, RDF.type, cls))
    for key, value in props.items():
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            for v in value:
                g.add((iri, DIS[key], v))
        else:
            g.add((iri, DIS[key], value))
    return iri
