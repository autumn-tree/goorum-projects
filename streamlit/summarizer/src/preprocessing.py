from __future__ import annotations

from datetime import UTC, datetime
from typing import Final

import pandas as pd
import streamlit as st


CANONICAL_COLUMNS: Final[list[str]] = ["date", "region", "category", "value"]

_ALIASES: Final[dict[str, tuple[str, ...]]] = {
    "date": ("date", "period", "year_month", "time", "시점", "기준시점"),
    "region": ("region", "area", "location", "지역", "시도", "시군구"),
    "category": ("category", "indicator", "item", "항목", "지표"),
    "value": ("value", "val", "amount", "count", "값", "수치"),
}


def _standardize_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


@st.cache_data(show_spinner=False)
def normalize_kosis_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Map diverse KOSIS-style column names into a canonical schema."""
    renamed = df.copy()
    renamed.columns = [_standardize_name(column) for column in renamed.columns]

    column_map: dict[str, str] = {}
    existing = set(renamed.columns)
    for canonical, aliases in _ALIASES.items():
        for alias in aliases:
            normalized_alias = _standardize_name(alias)
            if normalized_alias in existing:
                column_map[normalized_alias] = canonical
                break

    normalized = renamed.rename(columns=column_map)
    for required in CANONICAL_COLUMNS:
        if required not in normalized.columns:
            normalized[required] = pd.NA

    normalized = normalized[CANONICAL_COLUMNS].copy()
    normalized["date"] = pd.to_datetime(normalized["date"], errors="coerce")
    normalized["value"] = pd.to_numeric(normalized["value"], errors="coerce")
    normalized["region"] = normalized["region"].astype("string").str.strip()
    normalized["category"] = normalized["category"].astype("string").str.strip()

    return normalized


@st.cache_data(show_spinner=False)
def preprocess_kosis_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean normalized KOSIS data and add derived columns for dashboard usage."""
    normalized = normalize_kosis_schema(df)

    cleaned = normalized.dropna(subset=["date", "value"]).copy()
    cleaned["region"] = cleaned["region"].fillna("Unknown")
    cleaned["category"] = cleaned["category"].fillna("Unknown")
    cleaned["year"] = cleaned["date"].dt.year.astype(int)
    cleaned["month"] = cleaned["date"].dt.month.astype(int).astype(str).str.zfill(2)

    cleaned = cleaned.sort_values(["date", "region", "category"]).reset_index(drop=True)
    return cleaned[["date", "region", "category", "value", "year", "month"]]


@st.cache_data(show_spinner=False)
def get_preprocess_refresh_timestamp(df: pd.DataFrame) -> str:
    """Return a cached timestamp to expose preprocessing cache behavior."""
    return datetime.now(UTC).isoformat()
