"""Every checked-in artifact parses. §7 (conformance points) presupposes this."""
import json

import pytest
from jsonschema import Draft202012Validator
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery


def _ttl_files(repo):
    for sub in ("vocabulary", "shapes", "fixtures"):
        yield from (repo / sub).rglob("*.ttl")


def test_every_turtle_file_parses(repo):
    files = list(_ttl_files(repo))
    assert files, "expected at least one .ttl file under vocabulary/shapes/fixtures"
    for f in files:
        Graph().parse(str(f), format="turtle")


def test_every_sparql_query_compiles(repo):
    files = sorted((repo / "queries/v1.7.0").glob("*.rq"))
    assert len(files) == 4
    for f in files:
        prepareQuery(f.read_text())


def test_every_json_schema_is_valid_json_and_valid_draft202012(repo):
    files = list((repo / "schemas").rglob("*.schema.json"))
    assert files
    for f in files:
        data = json.loads(f.read_text())
        Draft202012Validator.check_schema(data)


def test_v16_index_lists_exactly_23_schemas(repo):
    index = json.loads((repo / "schemas/v1.6.0/index.json").read_text())
    assert index["schemaCount"] == 23
    on_disk = {p.name for p in (repo / "schemas/v1.6.0").glob("*.schema.json")}
    listed = {f["name"] for f in index["files"]}
    assert listed == on_disk
    assert len(listed) == 23
