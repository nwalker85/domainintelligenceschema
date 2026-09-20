#!/bin/bash
# Canonical DIS validation recipe: merge vocab+dossier, validate with NO -i.
# Two traps to avoid: `-i rdfs` lets rdfs:range silently type an invented mode
# as legitimate (never use it), and validating the dossier against the shapes
# WITHOUT the vocabulary merged in produces false positives (missing types).
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "usage: $0 <dossier.ttl> [more.ttl ...]" >&2
  exit 2
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VOCAB="$REPO_ROOT/vocabulary/v1.7.0/dis.ttl"
SHAPES="$REPO_ROOT/shapes/v1.7.0/dis-shapes.ttl"

command -v pyshacl >/dev/null 2>&1 && PYSHACL=(pyshacl) || PYSHACL=(uvx pyshacl)
command -v uv >/dev/null 2>&1 && PYRUN=(uv run --group test python -) || PYRUN=(uvx --from rdflib python -)

MERGED="$(mktemp -t dis-merged-XXXXXX.ttl)"
trap 'rm -f "$MERGED"' EXIT

"${PYRUN[@]}" "$VOCAB" "$@" > "$MERGED" << 'PYEOF'
import sys
from rdflib import Graph
g = Graph()
for path in sys.argv[1:]:
    g.parse(path, format="turtle")
print(g.serialize(format="turtle"))
PYEOF

exec "${PYSHACL[@]}" -s "$SHAPES" -f human "$MERGED"
