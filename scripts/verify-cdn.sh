#!/bin/bash
# Verify the live CDN matches the repo (repo is the source of truth;
# the bucket is deployed by .github/workflows/deploy-cdn.yml on merge).
set -euo pipefail
BASE_URL="https://schemas.domainintelligenceschema.org/dis"
fail=0
for d in schemas/v*/; do
  ver="${d#schemas/v}"; ver="${ver%/}"
  for f in "$d"*.json; do
    name="$(basename "$f")"
    if curl -fsS "$BASE_URL/${ver}/${name}" | diff -q - "$f" >/dev/null; then
      echo "  ✅ dis/${ver}/${name}"
    else
      echo "  ❌ dis/${ver}/${name} differs from repo"; fail=1
    fi
  done
done
[ "$fail" -eq 0 ] && echo "✅ CDN matches repo" || echo "❌ CDN drift detected"
exit $fail
