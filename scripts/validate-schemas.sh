#!/bin/bash
set -euo pipefail
echo "Validating DIS v1.6.0 schemas..."
ERRORS=0
for schema in schemas/v1.6.0/*.schema.json; do
  name=$(basename "$schema")
  if jq empty "$schema" 2>/dev/null; then
    echo "✅ $name"
  else
    echo "❌ $name - Invalid JSON"
    ((ERRORS++))
  fi
done
echo ""
[ $ERRORS -eq 0 ] && echo "✅ All schemas valid" || echo "❌ $ERRORS failed"
exit $ERRORS
