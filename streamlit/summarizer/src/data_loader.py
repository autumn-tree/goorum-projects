from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
import requests
import streamlit as st


def _project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return Path(__file__).resolve().parents[1] / candidate


def _payload_to_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("data", "results", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    return []


@st.cache_resource(show_spinner=False)
def get_http_session() -> requests.Session:
    """Create and reuse a long-lived HTTP session."""
    session = requests.Session()
    session.headers.update({"User-Agent": "streamlit-kosis-dashboard/1.0"})
    return session


@st.cache_data(show_spinner=False)
def fetch_kosis_api_data(
    api_url: str,
    params: dict[str, Any] | None = None,
    timeout: float = 10.0,
) -> pd.DataFrame:
    """Fetch KOSIS data from an API endpoint and return DataFrame rows."""
    response = get_http_session().get(api_url, params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    records = _payload_to_records(payload)
    if not records:
        raise ValueError("API payload did not contain tabular records.")
    return pd.DataFrame(records)


@st.cache_data(show_spinner=False)
def load_local_csv(local_path: str | Path) -> pd.DataFrame:
    """Load a local CSV file for fallback/offline usage."""
    path = _project_path(local_path)
    if not path.exists():
        raise FileNotFoundError(f"Local CSV not found: {path}")
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_kosis_data(
    api_url: str | None = None,
    params: dict[str, Any] | None = None,
    local_path: str | Path = "data/raw/kosis_sample.csv",
) -> tuple[pd.DataFrame, str, str]:
    """
    Load KOSIS data with API-first strategy and local fallback.

    Returns:
        Tuple of (DataFrame, source, refresh_timestamp), where source is one of:
        - "api"
        - "local"
        - "local_fallback"
    """
    refresh_timestamp = datetime.now(UTC).isoformat()
    if not api_url:
        return load_local_csv(local_path), "local", refresh_timestamp

    try:
        return fetch_kosis_api_data(api_url, params=params), "api", refresh_timestamp
    except Exception:
        return load_local_csv(local_path), "local_fallback", refresh_timestamp
