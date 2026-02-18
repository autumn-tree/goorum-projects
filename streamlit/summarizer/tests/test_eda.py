from __future__ import annotations

import pandas as pd

from src.eda import (
    build_category_summary,
    build_grouped_stats,
    build_missing_value_profile,
    build_monthly_trend,
    build_region_category_pivot,
    filter_kosis_data,
    get_summary_metrics,
)


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2024-01-01", "2024-01-01", "2024-02-01", "2024-02-01"]
            ),
            "region": ["Seoul", "Busan", "Seoul", "Busan"],
            "category": ["Population", "Population", "Employment", "Employment"],
            "value": [10.0, 20.0, 30.0, 40.0],
            "year": [2024, 2024, 2024, 2024],
            "month": ["01", "01", "02", "02"],
        }
    )


def test_get_summary_metrics_returns_expected_values() -> None:
    metrics = get_summary_metrics(_sample_df())
    assert metrics["rows"] == 4
    assert metrics["regions"] == 2
    assert metrics["categories"] == 2
    assert metrics["total_value"] == 100.0
    assert metrics["avg_value"] == 25.0


def test_filter_kosis_data_applies_region_category_and_year_filters() -> None:
    df = _sample_df()
    out = filter_kosis_data(
        df,
        regions=["Seoul"],
        categories=["Employment"],
        year_range=(2024, 2024),
    )
    assert len(out) == 1
    assert out.iloc[0]["region"] == "Seoul"
    assert out.iloc[0]["category"] == "Employment"


def test_build_grouped_stats_and_monthly_trend() -> None:
    df = _sample_df()
    grouped = build_grouped_stats(df, ["region"])
    trend = build_monthly_trend(df)

    assert list(grouped.columns) == ["region", "count", "total_value", "avg_value"]
    assert grouped["total_value"].sum() == 100.0
    assert list(trend.columns) == ["date", "total_value"]
    assert trend["total_value"].tolist() == [30.0, 70.0]


def test_build_category_summary_and_pivot() -> None:
    df = _sample_df()
    category_summary = build_category_summary(df)
    pivot = build_region_category_pivot(df)

    assert set(category_summary["category"].tolist()) == {"Population", "Employment"}
    assert pivot.loc["Busan", "Employment"] == 40.0
    assert pivot.loc["Seoul", "Population"] == 10.0


def test_missing_value_profile_columns_exist() -> None:
    df = _sample_df()
    df.loc[0, "region"] = None
    profile = build_missing_value_profile(df)

    assert list(profile.columns) == ["column", "missing_count", "missing_ratio"]
    assert profile["missing_count"].sum() >= 1
