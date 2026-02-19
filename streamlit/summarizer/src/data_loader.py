from __future__ import annotations

import ipaddress
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pandas as pd
import requests
import streamlit as st

LOCAL_ONLY_ENV_NAME = "LOCAL_ONLY"
BLOCKED_HOSTNAMES: set[str] = {
    "localhost",
    "127.0.0.1",
    "::1",
    "0.0.0.0",
    "169.254.169.254",
}
ALLOWED_LOCAL_HOSTNAMES: set[str] = {
    "localhost",
    "127.0.0.1",
    "::1",
}


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


def _parse_bool_env(raw_value: str | None, default: bool) -> bool:
    if raw_value is None:
        return default
    normalized = raw_value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


def is_local_only_mode() -> bool:
    """Return whether external HTTP fetch should be blocked (default: enabled)."""
    return _parse_bool_env(os.getenv(LOCAL_ONLY_ENV_NAME), default=True)


def _parse_ip(hostname: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
    try:
        return ipaddress.ip_address(hostname)
    except ValueError:
        return None


def validate_kosis_api_url(
    api_url: str,
    *,
    local_only: bool | None = None,
) -> tuple[bool, str | None]:
    """
    Validate API URL safety.

    LOCAL_ONLY mode: loopback hosts only.
    Non-local mode: reject loopback/private/link-local/metadata/reserved targets.
    """
    mode_local_only = is_local_only_mode() if local_only is None else local_only
    parsed = urlparse(api_url.strip())
    hostname = (parsed.hostname or "").strip().lower()

    if parsed.scheme not in {"http", "https"}:
        return False, "Only http/https URLs are allowed."
    if not hostname:
        return False, "URL host is missing."
    if parsed.username or parsed.password:
        return False, "Credential-in-URL format is not allowed."

    parsed_ip = _parse_ip(hostname)

    if mode_local_only:
        if hostname in ALLOWED_LOCAL_HOSTNAMES:
            return True, None
        if parsed_ip and parsed_ip.is_loopback:
            return True, None
        return False, "LOCAL_ONLY mode allows localhost/loopback URLs only."

    if hostname in BLOCKED_HOSTNAMES:
        return False, "Blocked host."

    if parsed_ip and (
        parsed_ip.is_private
        or parsed_ip.is_loopback
        or parsed_ip.is_link_local
        or parsed_ip.is_reserved
        or parsed_ip.is_multicast
        or parsed_ip.is_unspecified
    ):
        return False, "Private/internal network targets are not allowed."

    return True, None


@st.cache_resource(show_spinner=False)
def get_http_session() -> requests.Session:
    """Create and reuse a long-lived HTTP session."""
    session = requests.Session()
    session.headers.update({"User-Agent": "streamlit-kosis-dashboard/1.0"})
    session.trust_env = False
    return session


@st.cache_data(show_spinner=False)
def fetch_kosis_api_data(
    api_url: str,
    params: dict[str, Any] | None = None,
    timeout: float = 10.0,
    local_only: bool | None = None,
) -> pd.DataFrame:
    """Fetch KOSIS data from an API endpoint and return DataFrame rows."""
    is_valid, reason = validate_kosis_api_url(api_url, local_only=local_only)
    if not is_valid:
        raise ValueError(reason or "Unsafe API URL.")

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
    local_only: bool | None = None,
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
    mode_local_only = is_local_only_mode() if local_only is None else local_only
    if not api_url:
        return load_local_csv(local_path), "local", refresh_timestamp

    is_valid, _ = validate_kosis_api_url(api_url, local_only=mode_local_only)
    if not is_valid:
        return load_local_csv(local_path), "local_fallback", refresh_timestamp

    try:
        return (
            fetch_kosis_api_data(
                api_url,
                params=params,
                local_only=mode_local_only,
            ),
            "api",
            refresh_timestamp,
        )
    except (requests.RequestException, ValueError):
        return load_local_csv(local_path), "local_fallback", refresh_timestamp
