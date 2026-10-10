"""cue/v1.8.0/UtterancePolicy.cue <-> schemas/v1.7.0/UtterancePolicy.schema.json.

§6.2's documented fidelity gap: the exported JSON Schema is WEAKER than
#UtterancePolicyStrict — the OBLIGATION-needs-boundValueRefs and
LIFECYCLE-needs-lifecyclePhase conditionals live only in CUE (and SHACL's
sh:or on the graph side), because CUE's JSON-Schema exporter silently drops
`if` comprehensions. These tests keep that gap honest rather than papering
over it.
"""
import json
import shutil
import subprocess

import pytest
from jsonschema import Draft202012Validator

CUE_MISSING = shutil.which("cue") is None
pytestmark = pytest.mark.skipif(CUE_MISSING, reason="cue is not on PATH")

VALID_BASE = {
    "policyId": "550e8400-e29b-41d4-a716-446655440000",
    "name": "n",
    "description": "d",
    "policyType": "OBLIGATION",
    "requirement": "r",
    "enforcement": "STRUCTURAL",
    "boundValueRefs": ["x"],
}


def _cue_vet(repo, instance, definition="#UtterancePolicy", tmp_path=None):
    tmp_path = tmp_path or (repo / "tests")
    instance_file = tmp_path / "_cue_probe_instance.json"
    instance_file.write_text(json.dumps(instance))
    try:
        result = subprocess.run(
            ["cue", "vet", str(repo / "cue/v1.8.0/UtterancePolicy.cue"), str(instance_file), "-d", definition],
            capture_output=True,
            text=True,
        )
        return result
    finally:
        instance_file.unlink(missing_ok=True)


def test_cue_vet_the_source_file_passes(repo):
    result = subprocess.run(["cue", "vet", str(repo / "cue/v1.8.0/UtterancePolicy.cue")], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_cue_export_json_equals_checked_in_schema(repo, tmp_path):
    result = subprocess.run(
        ["cue", "def", str(repo / "cue/v1.8.0/UtterancePolicy.cue"), "-e", "#UtterancePolicy", "--out", "jsonschema"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    exported = json.loads(result.stdout)
    checked_in = json.loads((repo / "schemas/v1.7.0/UtterancePolicy.schema.json").read_text())
    assert json.dumps(exported, sort_keys=True) == json.dumps(checked_in, sort_keys=True)


def test_complete_valid_instance_passes_json_schema_and_cue_vet_strict(repo, tmp_path):
    schema = json.loads((repo / "schemas/v1.7.0/UtterancePolicy.schema.json").read_text())
    Draft202012Validator(schema).validate(VALID_BASE)
    result = _cue_vet(repo, VALID_BASE, "#UtterancePolicyStrict", tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_missing_enforcement_fails_json_schema(repo):
    schema = json.loads((repo / "schemas/v1.7.0/UtterancePolicy.schema.json").read_text())
    instance = {k: v for k, v in VALID_BASE.items() if k != "enforcement"}
    errors = list(Draft202012Validator(schema).iter_errors(instance))
    assert errors


def test_unknown_key_fails_json_schema_additional_properties_false(repo):
    schema = json.loads((repo / "schemas/v1.7.0/UtterancePolicy.schema.json").read_text())
    instance = dict(VALID_BASE, bogus="z")
    errors = list(Draft202012Validator(schema).iter_errors(instance))
    assert errors


def test_gap_obligation_without_bound_values_passes_json_schema_but_fails_cue_strict(repo, tmp_path):
    """§6.2: the published JSON Schema cannot express this conditional."""
    schema = json.loads((repo / "schemas/v1.7.0/UtterancePolicy.schema.json").read_text())
    instance = {k: v for k, v in VALID_BASE.items() if k != "boundValueRefs"}
    Draft202012Validator(schema).validate(instance)  # passes
    result = _cue_vet(repo, instance, "#UtterancePolicyStrict", tmp_path)
    assert result.returncode != 0


def test_gap_lifecycle_without_phase_passes_json_schema_but_fails_cue_strict(repo, tmp_path):
    schema = json.loads((repo / "schemas/v1.7.0/UtterancePolicy.schema.json").read_text())
    instance = dict(VALID_BASE, policyType="LIFECYCLE")
    Draft202012Validator(schema).validate(instance)  # passes
    result = _cue_vet(repo, instance, "#UtterancePolicyStrict", tmp_path)
    assert result.returncode != 0


def test_non_uuid_policyid_fails_json_schema_pattern_survived_export(repo):
    schema = json.loads((repo / "schemas/v1.7.0/UtterancePolicy.schema.json").read_text())
    instance = dict(VALID_BASE, policyId="not-a-uuid")
    errors = list(Draft202012Validator(schema).iter_errors(instance))
    assert errors
