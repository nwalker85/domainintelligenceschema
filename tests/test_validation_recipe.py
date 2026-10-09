"""§7 conformance points: the canonical validation recipe, and the two traps
around it (RDFS inference, missing-vocabulary) that a naive invocation falls into.
"""
import shutil
import subprocess

import pytest


def test_recipe_a_merged_vocab_no_inference_conforms_on_retail(dossier, validate):
    report = validate(dossier("retail"), inference="none")
    assert report.conforms, report.results


def test_recipe_a_deformed_yields_exactly_the_three_expected_violations(dossier, validate):
    report = validate(dossier("deformed"), inference="none")
    assert not report.conforms
    tuples = {(r.focus, r.path, r.component) for r in report.results}
    expected = {
        ("bad-target", "targetEntity", "ClassConstraintComponent"),
        ("bad-mode", "mode", "ClassConstraintComponent"),
        ("bad-policy", None, "OrConstraintComponent"),
    }
    assert tuples == expected


def test_rdfs_inference_silently_accepts_invented_mode_never_use_it(dossier, vocab, validate):
    """Recipe B is a TRAP: rdfs:range types dis:YEET as a dis:Mode via inference,
    so bad-mode's violation disappears — and bad-target is misreported as an
    EntityShape minCount instead of the real targetEntity ClassConstraint."""
    report = validate(dossier("deformed"), inference="rdfs", ont_graph=vocab)
    assert not report.conforms
    shapes_hit = {r.shape for r in report.results}
    assert "bad-mode" not in {r.focus for r in report.results}
    # the real bad-target shape (targetEntity->Entity) is NOT what fires here
    assert not any(
        r.focus == "bad-target" and r.path == "targetEntity" for r in report.results
    )


def test_recipe_c_no_vocab_produces_false_positives_on_retail(dossier, validate):
    """Validating against the shapes alone, without the vocabulary merged in,
    cannot see the enum individuals' rdf:type -> false positives on a
    conforming dossier."""
    from rdflib import Graph
    from pathlib import Path

    g = Graph().parse(
        str(Path(__file__).resolve().parent.parent / "fixtures/v1.7.0/retail.ttl"),
        format="turtle",
    )
    report = validate(g, inference="none")
    assert not report.conforms
    assert len(report.results) >= 1


def test_deformed_report_every_violation_has_a_focus_node(dossier, validate):
    report = validate(dossier("deformed"), inference="none")
    for r in report.violations():
        assert r.focus is not None


def test_deformed_report_every_property_shape_result_has_a_result_path(dossier, validate):
    report = validate(dossier("deformed"), inference="none")
    for r in report.violations():
        # the OrConstraint (node shape, not a property shape) legitimately has no path
        if r.component == "OrConstraintComponent":
            continue
        assert r.path is not None


@pytest.mark.skipif(
    shutil.which("pyshacl") is None and shutil.which("uvx") is None,
    reason="neither pyshacl nor uvx is on PATH",
)
@pytest.mark.parametrize("fixture", ["retail.ttl", "healthcare.ttl", "bfsi.ttl", "itsd-hr.ttl", "itsd.ttl", "hr.ttl", "dadjoke.ttl"])
def test_validate_dossier_script_exits_0_on_reference_dossiers(repo, fixture):
    result = subprocess.run(
        ["bash", str(repo / "scripts/validate-dossier.sh"), f"fixtures/v1.7.0/{fixture}"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(
    shutil.which("pyshacl") is None and shutil.which("uvx") is None,
    reason="neither pyshacl nor uvx is on PATH",
)
def test_validate_dossier_script_exits_1_on_deformed(repo):
    result = subprocess.run(
        ["bash", str(repo / "scripts/validate-dossier.sh"), "fixtures/v1.7.0/deformed.ttl"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
