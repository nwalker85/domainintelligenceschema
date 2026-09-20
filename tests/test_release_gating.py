"""1.7's not-yet-released gating: the .unreleased marker, deploy-cdn.yml's
handling of it, the schema-count gate, and the ref-host regression check
CHANGELOG's 1.6.0+ref-fix entry promises stays fixed."""
import json
import re
import subprocess

import pytest
import yaml


def _is_git_checkout(repo):
    return (repo / ".git").exists() or subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"], cwd=repo, capture_output=True
    ).returncode == 0


@pytest.mark.skipif(
    subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True).returncode != 0,
    reason="not a git checkout",
)
def test_unreleased_marker_exists_iff_no_v17_tag(repo):
    tags = subprocess.run(["git", "tag", "-l"], cwd=repo, capture_output=True, text=True).stdout.split()
    has_v17_tag = any(t.startswith("v1.7") for t in tags)
    marker_exists = (repo / "schemas/v1.7.0/.unreleased").exists()
    assert marker_exists != has_v17_tag


def test_deploy_cdn_sync_and_verify_both_reference_unreleased_marker(repo):
    data = yaml.safe_load((repo / ".github/workflows/deploy-cdn.yml").read_text())
    steps = data["jobs"]["deploy"]["steps"]
    named = {s.get("name"): s for s in steps if "name" in s}
    sync_run = named["Sync schema versions to bucket"]["run"]
    verify_run = named["Verify live CDN matches repo"]["run"]
    assert ".unreleased" in sync_run
    assert ".unreleased" in verify_run
    assert r"\.unreleased" in sync_run  # the rsync -x exclude pattern


def test_deploy_cdn_trigger_paths_include_schemas(repo):
    data = yaml.safe_load((repo / ".github/workflows/deploy-cdn.yml").read_text())
    paths = data[True]["push"]["paths"] if True in data else data["on"]["push"]["paths"]
    assert "schemas/**" in paths


def test_validate_workflow_expects_23_and_there_are_23(repo):
    text = (repo / ".github/workflows/validate.yml").read_text()
    assert "23" in text
    count = len(list((repo / "schemas/v1.6.0").glob("*.schema.json")))
    assert count == 23


def test_changelog_170_heading_says_not_yet_released_while_marker_exists(repo):
    changelog = (repo / "CHANGELOG.md").read_text()
    assert "[1.7.0] - Proposed, not yet released" in changelog
    assert (repo / "schemas/v1.7.0/.unreleased").exists()


def test_no_v16_schema_id_or_ref_points_off_canonical_host(repo):
    """CHANGELOG 1.6.0+ref-fix: 48 $ref URIs used to point at the unregistered
    schemas.domain-intelligence.org. None should, now."""
    canonical = "schemas.domainintelligenceschema.org"
    offenders = []
    for f in (repo / "schemas/v1.6.0").glob("*.schema.json"):
        text = f.read_text()
        for m in re.finditer(r'"\$(?:id|ref)":\s*"([^"]+)"', text):
            url = m.group(1)
            if url.startswith("http") and canonical not in url:
                offenders.append((f.name, url))
    assert offenders == []


@pytest.mark.xfail(
    strict=True,
    reason="RAV-1947 gap 8: CHANGELOG deprecates all 23 v1.6.0 schemas as of "
    "1.7, but none of the .schema.json files carry a deprecated:true keyword",
)
def test_gap8_deprecated_v16_schemas_carry_deprecated_keyword(repo):
    files = list((repo / "schemas/v1.6.0").glob("*.schema.json"))
    for f in files:
        data = json.loads(f.read_text())
        assert data.get("deprecated") is True, f.name
