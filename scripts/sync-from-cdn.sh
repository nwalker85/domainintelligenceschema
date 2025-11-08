#!/bin/bash
set -euo pipefail
BASE_URL="https://schemas.domainintelligenceschema.org/dis/1.6.0"
echo "Syncing schemas from CDN..."
INDEX=$(curl -sS "$BASE_URL/index.json")
echo "$INDEX" | jq -r '.files[].name' | while read -r schema; do
  echo "  📥 $schema"
  curl -sS "$BASE_URL/$schema" -o "schemas/v1.6.0/$schema"
done
echo "✅ Sync complete"
