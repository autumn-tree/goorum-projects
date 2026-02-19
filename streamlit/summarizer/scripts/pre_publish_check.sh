#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[INFO] Running pre-publish checks..."

bash scripts/pre_push_security_scan.sh
bash scripts/check_sample_data_safety.sh

echo "[INFO] Running test suite..."
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -p no:debugging -q

tracked_artifact_hits="$(git ls-files | rg '(^|/)\.DS_Store$|(^|/)__pycache__/|(^|/)\.pytest_cache/|\.pyc$|(^|/)logs/|(^|/)\.pids/' || true)"
if [[ -n "$tracked_artifact_hits" ]]; then
  echo "[ERROR] Tracked local artifacts detected:"
  echo "$tracked_artifact_hits"
  exit 1
fi

echo "[INFO] Pre-publish checks passed."
