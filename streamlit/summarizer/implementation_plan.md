# Implementation Plan

## 1. Goal

Implement a Streamlit project with four integrated capabilities:

1. Reliable session state management with `st.session_state`.
2. A Statistics Korea (KOSIS) dashboard using the flow: preprocessing -> EDA -> Plotly visualization.
3. Clear caching architecture using `st.cache_data` and `st.cache_resource`.
4. A YouTube thumbnail extractor app (videos and shorts only).

## 2. Execution Strategy

Work in vertical slices so each phase produces a runnable result.  
Recommended order:

1. Core app structure and session state base.
2. KOSIS data ingestion + preprocessing.
3. EDA and Plotly dashboard UI.
4. Caching integration and cache-control UI.
5. Thumbnail extractor module.
6. Final QA, performance checks, and documentation polish.

## 3. Work Breakdown by Phase

## Phase 1: Foundation and Session Management

Target files:
- `app.py`
- `src/session_manager.py`

Tasks:
1. Create navigation structure (`Dashboard`, `Thumbnail Extractor`, `Debug`).
2. Implement `init_session_state()` with default keys:
   - `page`
   - `selected_dataset`
   - `filters`
   - `history`
   - `cache_version`
3. Add state helpers:
   - `get_state`
   - `set_state`
   - `reset_filters`
   - `reset_session`
4. Add sidebar actions for controlled state reset.

Exit criteria:
1. No missing-key exceptions after reruns.
2. State persists across widget interactions.
3. Reset actions behave predictably.

## Phase 2: KOSIS Data Layer (Load + Preprocess)

Target files:
- `src/data_loader.py`
- `src/preprocessing.py`
- `data/raw/`
- `data/processed/`

Tasks:
1. Implement loader with two paths:
   - KOSIS API fetch
   - Local CSV fallback
2. Normalize schema:
   - standard column names
   - datetime parsing
   - numeric type coercion
3. Add preprocessing pipeline:
   - null handling
   - outlier-safe numeric conversion
   - derived metrics required by dashboard

Exit criteria:
1. Pipeline returns consistent DataFrame schema.
2. API failure falls back to local data without app crash.
3. Preprocessed data is ready for EDA/Plotly without manual fixes.

## Phase 3: EDA and Visualization

Target files:
- `src/eda.py`
- `src/charts.py`
- `app.py`

Tasks:
1. Implement EDA summary functions:
   - row/column stats
   - missing-value profile
   - grouped stats by time/region/category
2. Build Plotly chart functions:
   - trend line chart
   - category comparison bar chart
   - optional heatmap or scatter
3. Connect UI filters to chart and table outputs.
4. Add KPI cards for headline metrics.

Exit criteria:
1. Filters update all relevant visuals.
2. Charts and tables show consistent numbers.
3. Dashboard remains usable on rerun.

## Phase 4: Caching Design (`st.cache_data` vs `st.cache_resource`)

Target files:
- `src/data_loader.py`
- `src/preprocessing.py`
- `app.py`

Tasks:
1. Apply `@st.cache_data` to:
   - API/CSV fetch functions
   - preprocessing functions
   - EDA aggregate helpers
2. Apply `@st.cache_resource` to:
   - persistent connection/resource object (for example `requests.Session`)
3. Add cache control UI:
   - clear data cache
   - clear resource cache
4. Expose cache behavior in debug panel:
   - last refresh timestamp
   - cache version value from session state

Exit criteria:
1. Repeated reruns do not re-fetch/recompute unnecessarily.
2. Clearing data cache triggers recomputation only for cached data functions.
3. Clearing resource cache reinitializes resource object lifecycle.

## Phase 5: Thumbnail Extractor

Target files:
- `src/thumbnail.py`
- `app.py`

Tasks:
1. Implement URL parser:
   - validate YouTube URL format (videos and shorts only)
   - support `watch`, `youtu.be`, and `shorts` URL patterns
2. Implement thumbnail resolver:
   - extract video ID from URL
   - build candidate thumbnail URLs (`maxresdefault`, `hqdefault`, `mqdefault`, `default`)
   - select best available thumbnail by HTTP availability check
3. Build extraction UI:
   - input field
   - fetch button
   - image preview
   - download link
4. Add error handling for invalid YouTube URLs, missing thumbnails, and network failures.

Exit criteria:
1. Valid YouTube URLs return thumbnail URLs reliably.
2. Invalid/unsupported URLs fail with clear user-facing messages.
3. Thumbnail preview and download work end to end.

## Phase 6: Verification and Hardening

Target files:
- `task.md` (or equivalent review notes)
- `README` updates if needed

Tasks:
1. Functional checks:
   - session persistence
   - filter interactions
   - cache behavior
   - thumbnail extraction paths
2. Performance checks:
   - first load vs rerun timing comparison
3. Reliability checks:
   - API failure fallback behavior
   - invalid-input handling
4. Final cleanup:
   - remove dead code
   - ensure clear user messages

Exit criteria:
1. All major flows complete without runtime errors.
2. Caching behavior is demonstrable and correct.
3. Documentation matches implemented behavior.

## 4. Verification Matrix

1. Session state:
   - expected: selections persist across reruns.
2. Data pipeline:
   - expected: normalized schema and stable metrics.
3. Dashboard:
   - expected: visuals update correctly with filters.
4. Cache data:
   - expected: repeated calls reuse cached values.
5. Cache resource:
   - expected: resource object reused until resource cache clear.
6. Thumbnail extractor:
   - expected: supported URL -> thumbnail preview + download.

## 5. Risks and Controls

1. External API instability:
   - control: CSV fallback and retry with timeout.
2. Heavy plotting on large data:
   - control: pre-aggregation + cached transformations.
3. URL pattern changes on platforms:
   - control: platform handlers isolated in `src/thumbnail.py`.

## 6. Definition of Done

Project is done when:

1. All phases meet their exit criteria.
2. App demonstrates both cache decorators with observable differences.
3. KOSIS dashboard follows preprocessing -> EDA -> Plotly workflow.
4. YouTube thumbnail extractor works for `watch`, `youtu.be`, and `shorts` URLs.
5. Session management is stable and reset-safe.
