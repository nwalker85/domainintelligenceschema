"""v1.6.0 CommonEnums vs the 1.7 Turtle vocabulary — what carried forward
unchanged, and what the CHANGELOG documents as a deliberate breaking
collision fix."""
import json

from rdflib import RDF

from conftest import DIS


def _v16_enums(repo):
    return json.loads((repo / "schemas/v1.6.0/CommonEnums.schema.json").read_text())["definitions"]


def test_v16_mode_of_interaction_equals_the_seven_1_7_modes(repo, vocab):
    enums = _v16_enums(repo)
    v16_modes = set(enums["modeOfInteraction"]["enum"])
    v17_modes = {str(m).rsplit("/", 1)[-1] for m in vocab.subjects(RDF.type, DIS.Mode)}
    assert v16_modes == v17_modes


def test_v16_stance_equals_act_react(repo, vocab):
    enums = _v16_enums(repo)
    assert set(enums["stance"]["enum"]) == {"ACT", "REACT"}
    v17_stances = {str(s).rsplit("/", 1)[-1] for s in vocab.subjects(RDF.type, DIS.Stance)}
    assert v17_stances == {"ACT", "REACT"}


def test_v16_http_method_has_7_values_1_7_vocab_has_5_documented_breaking_fix(repo, vocab):
    enums = _v16_enums(repo)
    v16 = set(enums["httpMethod"]["enum"])
    assert v16 == {"GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"}
    assert len(v16) == 7
    v17 = {str(m).rsplit("/", 1)[-1] for m in vocab.subjects(RDF.type, DIS.HttpMethod)}
    assert len(v17) == 5
    assert v16 != v17


def test_v16_and_1_7_application_type_differ_documented(repo, vocab):
    """CHANGELOG 1.7.0: applicationType collided in name only — v1.6's was an
    unused technology-shape enum, v1.7's is a domain-role enum. They must NOT
    be the same set."""
    enums = _v16_enums(repo)
    v16 = set(enums["applicationType"]["enum"])
    v17 = {str(m).rsplit("/", 1)[-1] for m in vocab.subjects(RDF.type, DIS.ApplicationType)}
    assert v16 != v17
    assert v17 == {"SYSTEM_OF_RECORD", "SAAS_PLATFORM", "MOCK", "KNOWLEDGE_STORE"}
