# Task Plan (Based on `implementation_plan.md`)

Rule for this file: tasks are checked after implementation and verification runs.

## Phase 1: Foundation and Session Management

- [x] Build app navigation (`Dashboard`, `Thumbnail Extractor`, `Debug`).
- [x] Implement session defaults and state helper utilities.
- [x] Add sidebar controls for session reset behavior.
- [x] Add baseline tests for session helpers.
- [x] Verification request to user before Phase 2.

## Phase 2: KOSIS Data Layer (Load + Preprocess)

- [x] Implement dual-path loader (API + local CSV fallback).
- [x] Normalize schema and preprocess data.
- [x] Add local sample dataset.
- [x] Add tests for loader fallback and preprocessing outputs.
- [x] Verification request to user before Phase 3.

## Phase 3: EDA and Visualization

- [x] Implement EDA summary/grouping helpers.
- [x] Implement Plotly chart builders.
- [x] Connect dashboard filters, KPIs, charts, and table.
- [x] Add tests for EDA utilities.
- [x] Verification request to user before Phase 4.

## Phase 4: Caching Architecture

- [x] Apply `st.cache_data` to data/processing/aggregate functions.
- [x] Apply `st.cache_resource` to long-lived resource object.
- [x] Add cache controls and cache debug panel.
- [x] Keep cache behavior details out of the main dashboard view.
- [x] Add `Show cache diagnostics` toggle (default off) in `Debug`.
- [x] Keep session state details out of the main dashboard view.
- [x] Add `Show session state diagnostics` toggle (default off) in `Debug`.
- [x] Verify cache behavior in app.
- [x] Verification request to user before Phase 5.

## Phase 5: YouTube Thumbnail Extractor (Videos + Shorts Only)

- [x] Implement YouTube-only URL parser (`watch`, `youtu.be`, `shorts`) and strict validation.
- [x] Implement video ID extractor with deterministic parsing rules.
- [x] Implement thumbnail resolver with fallback order:
  - [x] `maxresdefault`
  - [x] `hqdefault`
  - [x] `mqdefault`
  - [x] `default`
- [x] Implement thumbnail availability check (HTTP status) to choose best candidate.
- [x] Build extractor UI in `Thumbnail Extractor` page:
  - [x] URL input
  - [x] fetch action
  - [x] thumbnail preview
  - [x] download button/link
- [x] Add tests for:
  - [x] valid URL parsing by pattern type
  - [x] invalid URL handling
  - [x] fallback selection behavior
  - [x] missing thumbnail/network failure paths
- [x] Verification request to user before Phase 6.

## Phase 6: Verification and Hardening

- [x] Run full tests and syntax checks.
- [x] Validate main app flows manually.
- [x] Clean up edge-case handling and messages.
- [x] Prepare final verification request and handoff.

## Plan V2: Service Separation (Cache + Session)

Rule: restarted from `planv2.md`; keep unchecked until you verify.

### Phase A: Foundation

- [ ] Remove unreachable `Debug` page function from `app.py`.
- [ ] Create `services/common/logging_config.py` with INFO console + rotating file logging.
- [ ] Create `services/common/config.py` for host/port/log settings.
- [ ] Create `services/common/models.py` for shared response schemas.
- [ ] Create `services/cache_service.py` with health endpoint.
- [ ] Create `services/session_service.py` with health endpoint.
- [ ] Verify both services can run at the same time.

### Phase B: Cache Service Functionality

- [ ] Implement cache store (`get`, `set`, `clear`, `status`) with thread safety.
- [ ] Expose HTTP endpoints (`/health`, `/cache/status`, `/cache/get`, `/cache/set`, `/cache/clear`).
- [ ] Add INFO logs for startup and each cache operation.
- [ ] Add unit tests for cache store behavior.
- [ ] Verification request to user before Phase C.

### Phase C: Session Service Functionality

- [ ] Implement session store (`init`, `get`, `set`, `reset`, `history append`) with thread safety.
- [ ] Expose HTTP endpoints (`/health`, `/session/init`, `/session/get`, `/session/set`, `/session/reset`, `/session/history/append`).
- [ ] Add INFO logs for startup and session mutations.
- [ ] Add unit tests for session store behavior.
- [ ] Verification request to user before Phase D.

### Phase D: Concurrent Run Scripts

- [ ] Add `scripts/run_all.sh` to start cache, session, and Streamlit together.
- [ ] Add `scripts/stop_all.sh` to stop spawned services cleanly.
- [ ] Ensure logs are written to `logs/cache_service.log` and `logs/session_service.log`.
- [ ] Verification request to user before Phase E.

### Phase E: Streamlit Integration (Service-backed)

- [ ] Replace direct in-app cache/session logic with service calls.
- [ ] Add graceful fallback when a service is unavailable.
- [ ] Validate parity for dashboard and thumbnail flows.
- [ ] Final verification request and handoff.
