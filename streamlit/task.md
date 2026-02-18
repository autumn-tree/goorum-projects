# Security Review (Local-Only Distribution)

Date: 2026-02-18  
Scope: `app.py`, `requirements.txt`, `.gitpod.yml`  
Assumption: The app is run locally by each user after cloning/downloading; no public internet deployment.

## Open Findings Count (After Remediation)

- Critical: 0
- High: 0
- Medium: 0
- Low: 0
- Informational: 0
- Resolved: 2

## Resolved Findings

### 1) Low - Unpinned dependencies created supply-chain drift (Resolved)

- Original evidence: `requirements.txt:1`, `requirements.txt:2`, `.gitpod.yml:4`
- Remediation applied: pinned exact versions in `requirements.txt`.
- Current evidence: `requirements.txt:1`, `requirements.txt:2`
- Verification:
- [x] `requirements.txt` now uses `streamlit==1.45.1`.
- [x] `requirements.txt` now uses `pandas==2.2.3`.

### 2) Informational - Unbounded session data growth could freeze local app (Resolved)

- Original evidence: `app.py:77`, `app.py:88`, `app.py:52`
- Remediation applied: added max length limits and capped stored rows.
- Current evidence: `app.py:6`, `app.py:7`, `app.py:8`, `app.py:49`, `app.py:63`, `app.py:90`, `app.py:100`, `app.py:107`
- Verification:
- [x] Name input in basic section is bounded via `max_chars`.
- [x] Expense item input is bounded via `max_chars`.
- [x] Expense row storage is capped with `tail(MAX_EXPENSE_ROWS)`.
- [x] Python compile check passed (`python -m py_compile app.py`).

## Checklist Coverage (Security-Review Skill)

- Secrets hardcoded: Not found.
- Input validation: Improved with explicit length and positive amount checks.
- SQL injection: Not applicable (no DB/SQL usage).
- AuthN/AuthZ: Not applicable (no authentication layer).
- XSS: No unsafe HTML rendering detected.
- CSRF: Not applicable (no authenticated state-changing HTTP API).
- Rate limiting: Not applicable for local interactive app usage.
- Sensitive data logging: No sensitive logging found.

## Residual Gaps

- Automated security scanners were not executed in this environment (`bandit` and `pip-audit` unavailable).
- No automated security tests are present.
