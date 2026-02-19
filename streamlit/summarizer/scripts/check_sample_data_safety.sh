#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

DATA_FILE="data/raw/kosis_sample.csv"
if [[ ! -f "$DATA_FILE" ]]; then
  echo "[ERROR] Sample data file not found: $DATA_FILE"
  exit 1
fi

echo "[INFO] Checking sample data safety: $DATA_FILE"

header="$(head -n 1 "$DATA_FILE" | tr '[:upper:]' '[:lower:]')"
if echo "$header" | rg -q '(name|email|phone|address|ssn|password|birth|birthday|resident)'; then
  echo "[ERROR] Header suggests potentially sensitive columns:"
  echo "$header"
  exit 1
fi

pii_pattern='([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|(\+?\d{1,3}[ -]?)?0\d{1,2}[ -]\d{3,4}[ -]\d{4})'
pii_hits="$(tail -n +2 "$DATA_FILE" | rg -n "$pii_pattern" || true)"
if [[ -n "$pii_hits" ]]; then
  echo "[ERROR] Potential PII-like values found in sample data:"
  echo "$pii_hits"
  exit 1
fi

echo "[INFO] Sample data safety check passed."
