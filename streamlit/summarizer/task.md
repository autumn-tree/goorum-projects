# Task Plan (Based on `implementation_plan.md`)

Rule for this file: no task will be checked off until you verify.

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
