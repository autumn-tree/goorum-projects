from __future__ import annotations

from typing import Any, Iterable

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def get_summary_metrics(df: pd.DataFrame) -> dict[str, Any]:
    """Return high-level KPI metrics used in the dashboard header."""
    if df.empty:
        return {
            "rows": 0,
            "regions": 0,
            "categories": 0,
            "total_value": 0.0,
            "avg_value": 0.0,
        }
    return {
        "rows": int(len(df)),
        "regions": int(df["region"].nunique()),
        "categories": int(df["category"].nunique()),
        "total_value": float(df["value"].sum()),
        "avg_value": float(df["value"].mean()),
    }


@st.cache_data(show_spinner=False)
def build_missing_value_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Build a missing-value profile by column."""
    if df.empty:
        return pd.DataFrame(columns=["column", "missing_count", "missing_ratio"])
    missing_count = df.isna().sum()
    missing_ratio = (missing_count / len(df)).round(4)
    return (
        pd.DataFrame(
            {
                "column": missing_count.index,
                "missing_count": missing_count.values,
                "missing_ratio": missing_ratio.values,
            }
        )
        .sort_values("missing_count", ascending=False)
        .reset_index(drop=True)
    )


@st.cache_data(show_spinner=False)
def build_grouped_stats(df: pd.DataFrame, group_by: Iterable[str]) -> pd.DataFrame:
    """Build count/sum/mean stats grouped by one or more columns."""
    group_keys = [key for key in group_by if key in df.columns]
    if not group_keys or df.empty:
        return pd.DataFrame(columns=[*group_keys, "count", "total_value", "avg_value"])
    grouped = (
        df.groupby(group_keys, dropna=False)["value"]
        .agg(count="count", total_value="sum", avg_value="mean")
        .reset_index()
    )
    grouped["avg_value"] = grouped["avg_value"].round(2)
    return grouped.sort_values(group_keys).reset_index(drop=True)


def filter_kosis_data(
    df: pd.DataFrame,
    regions: list[str] | None = None,
    categories: list[str] | None = None,
    year_range: tuple[int, int] | None = None,
) -> pd.DataFrame:
    """Apply dashboard filters and return filtered data."""
    filtered = df.copy()
    if regions:
        filtered = filtered[filtered["region"].isin(regions)]
    if categories:
        filtered = filtered[filtered["category"].isin(categories)]
    if year_range:
        start, end = year_range
        filtered = filtered[(filtered["year"] >= start) & (filtered["year"] <= end)]
    return filtered.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def build_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate monthly totals for trend visualization."""
    if df.empty:
        return pd.DataFrame(columns=["date", "total_value"])
    trend = (
        df.groupby("date", as_index=False)["value"]
        .sum()
        .rename(columns={"value": "total_value"})
        .sort_values("date")
    )
    return trend.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def build_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate totals by category for category comparison chart."""
    if df.empty:
        return pd.DataFrame(columns=["category", "total_value"])
    summary = (
        df.groupby("category", as_index=False)["value"]
        .sum()
        .rename(columns={"value": "total_value"})
        .sort_values("total_value", ascending=False)
    )
    return summary.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def build_region_category_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Build a region-category matrix for heatmap-style visualization."""
    if df.empty:
        return pd.DataFrame()
    pivot = pd.pivot_table(
        df,
        index="region",
        columns="category",
        values="value",
        aggfunc="sum",
        fill_value=0,
    )
    return pivot.sort_index().sort_index(axis=1)
