# Project Plan 2: Streamlit Session, KOSIS Dashboard, Caching, and Thumbnail Extractor

## 1. Objective

Build a multi-feature Streamlit project that demonstrates:

1. Practical `st.session_state` usage and robust session management.
2. A dashboard based on Statistics Korea (KOSIS) data.
3. Correct use of `st.cache_data` and `st.cache_resource`.
4. A thumbnail extraction app (non-YouTube platform recommended, YouTube optional).

---

## 2. Scope and Deliverables

### Deliverable A: Session State Management Module

- Initialize required session keys on first load.
- Persist UI filters, selected dataset, and user preferences across reruns.
- Provide session reset controls (partial reset and full reset).
- Track user actions in session history (for debugging and learning).

### Deliverable B: Statistics Korea Data Dashboard

- Data source: KOSIS API or pre-downloaded KOSIS CSV files.
- Workflow:
  1. Data preprocessing
  2. Exploratory Data Analysis (EDA)
  3. Data visualization with Plotly
- Interactive filtering by period, region, and category.
- KPI cards + trend charts + distribution charts + table view.

### Deliverable C: Caching Demonstration

- `st.cache_data` for data-fetch and preprocessing functions.
- `st.cache_resource` for long-lived resources (for example API client/session object).
- Include cache invalidation controls and timestamp indicators.

### Deliverable D: Thumbnail Extractor App

- Primary recommendation: support a non-YouTube platform (for example Vimeo via oEmbed).
- Optional: YouTube fallback support.
- Parse URL, validate platform, fetch thumbnail URL, preview image, and allow download.

---

## 3. Proposed App Structure

```text
streamlit/
  app.py
  plan.md
  plan2.md
  requirements.txt
  data/
    raw/
    processed/
  src/
    session_manager.py
    data_loader.py
    preprocessing.py
    eda.py
    charts.py
    thumbnail.py
```

---

## 4. Detailed Implementation Plan

## Phase 1: Session State Foundations

### Tasks

1. Create `init_session_state()` to define all keys with defaults:
   - `selected_dataset`
   - `filters`
   - `theme`
   - `history`
   - `cache_version`
2. Build helper functions:
   - `get_state(key, default)`
   - `set_state(key, value)`
   - `reset_filters()`
   - `reset_all_state()`
3. Add sidebar controls for state debugging and reset actions.

### Acceptance Criteria

- State values persist between reruns.
- Reset buttons work predictably.
- No `KeyError` from missing session keys.

---

## Phase 2: KOSIS Data Pipeline (Preprocessing -> EDA -> Visualization)

### Tasks

1. Data ingestion:
   - Implement API/CSV loader.
   - Normalize column names and data types.
2. Data preprocessing:
   - Handle missing values.
   - Convert date fields to datetime.
   - Ensure numeric metrics are clean and comparable.
3. EDA:
   - Summary statistics.
   - Missing-value report.
   - Grouped comparisons (region/category/time).
4. Visualization (Plotly):
   - Time-series line chart.
   - Category bar chart.
   - Optional heatmap/scatter for deeper insights.
5. UI:
   - Sidebar filters.
   - KPI cards for headline metrics.
   - Expanders for raw data and methodology.

### Acceptance Criteria

- User can filter data interactively.
- Charts respond correctly to filter changes.
- Dashboard remains responsive on rerun.

---

## Phase 3: Caching Architecture

### Tasks

1. Use `@st.cache_data` for:
   - Data fetch functions.
   - Preprocessing functions.
   - EDA result calculations.
2. Use `@st.cache_resource` for:
   - Long-lived connection/resource objects (for example `requests.Session()` client).
3. Add UI controls:
   - `Clear cached data`
   - `Reinitialize resources`
4. Add clear comments that explain:
   - `st.cache_data`: caches return values based on function inputs.
   - `st.cache_resource`: caches expensive singleton-like resources.

### Acceptance Criteria

- Repeated reruns avoid redundant data work.
- Cache clear actions visibly trigger recomputation/reinitialization.
- Team can observe behavioral difference between the two cache decorators.

---

## Phase 4: Thumbnail Extractor App

### Tasks

1. URL parser and validator:
   - Identify platform (`vimeo`, `youtube`, or unsupported).
2. Thumbnail retrieval:
   - Vimeo first (recommended).
   - YouTube fallback if enabled.
3. UI:
   - Input URL field.
   - Fetch button.
   - Thumbnail preview and download link.
4. Error handling:
   - Invalid URL.
   - Unsupported platform.
   - Missing thumbnail or network failures.

### Acceptance Criteria

- Valid URLs return thumbnails reliably.
- Unsupported inputs show clear errors.
- User can preview and download thumbnail image.

---

## 5. Tech Stack and Dependencies

- Streamlit
- Pandas
- Plotly
- Requests

Optional:
- Pydantic (URL validation)
- Tenacity (retry logic for API calls)

---

## 6. Testing and Verification Plan

1. Unit checks:
   - Session helper functions.
   - URL parsing logic.
   - Data preprocessing transformations.
2. Manual app checks:
   - Filter state persistence.
   - Cache hit/miss behavior.
   - Chart correctness after filter changes.
   - Thumbnail extraction success/failure paths.
3. Performance checks:
   - Compare first load vs cached rerun.
   - Validate no unnecessary recomputation.

---

## 7. Risks and Mitigation

1. KOSIS API availability/format changes:
   - Mitigation: keep CSV fallback dataset.
2. Slow large-data plotting:
   - Mitigation: pre-aggregate and cache transformed outputs.
3. Thumbnail endpoint changes:
   - Mitigation: isolate platform logic in dedicated parser/fetch functions.

---

## 8. Completion Definition

This plan is complete when:

1. Session state logic is stable and resettable.
2. KOSIS dashboard supports preprocess -> EDA -> Plotly visualization flow.
3. `st.cache_data` and `st.cache_resource` are both implemented and demonstrably different.
4. Thumbnail extractor works for at least one non-YouTube platform, with optional YouTube support.
