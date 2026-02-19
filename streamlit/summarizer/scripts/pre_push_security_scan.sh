#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[INFO] Running pre-push security scan..."

tracked_artifact_hits="$(git ls-files | rg '(^|/)\.DS_Store$|(^|/)__pycache__/|(^|/)\.pytest_cache/|\.pyc$|(^|/)logs/|(^|/)\.pids/' || true)"
if [[ -n "$tracked_artifact_hits" ]]; then
  echo "[ERROR] Tracked local artifacts detected:"
  echo "$tracked_artifact_hits"
  exit 1
fi

if command -v gitleaks >/dev/null 2>&1; then
  echo "[INFO] gitleaks detected. Running gitleaks..."
  gitleaks detect --source "$ROOT_DIR" --redact --no-banner
else
  echo "[INFO] gitleaks not installed. Running regex-based lightweight scan..."
  secret_pattern='(BEGIN (RSA|OPENSSH) PRIVATE KEY|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]+|sk-[A-Za-z0-9]{20,}|(OPENAI_API_KEY|DATABASE_URL)\s*=|api[_-]?key\s*[:=]\s*["'"'"'][^"'"'"']+["'"'"']|password\s*[:=]\s*["'"'"'][^"'"'"']+["'"'"'])'
  tracked_files="$(git ls-files)"
  if [[ -n "$tracked_files" ]]; then
    secret_hits="$(git ls-files | xargs rg -n -S -i -- "$secret_pattern" || true)"
    if [[ -n "$secret_hits" ]]; then
      echo "[ERROR] Potential secret patterns found:"
      echo "$secret_hits"
      exit 1
    fi
  fi
fi

echo "[INFO] Pre-push security scan passed."
