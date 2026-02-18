from __future__ import annotations

import pandas as pd

from src.preprocessing import (
    get_preprocess_refresh_timestamp,
    normalize_kosis_schema,
    preprocess_kosis_data,
)


def test_normalize_kosis_schema_maps_aliases_and_types() -> None:
    raw = pd.DataFrame(
        {
            "시점": ["2024-01", "2024-02"],
            "지역": ["Seoul", "Busan"],
            "항목": ["Population", "Population"],
            "값": ["100", "250"],
        }
    )

    normalized = normalize_kosis_schema(raw)

    assert list(normalized.columns) == ["date", "region", "category", "value"]
    assert str(normalized["date"].dtype).startswith("datetime64")
    assert normalized["value"].tolist() == [100.0, 250.0]


def test_preprocess_kosis_data_drops_invalid_rows_and_adds_derived_fields() -> None:
    raw = pd.DataFrame(
        {
            "date": ["2024-01-01", "invalid-date", "2024-03-01"],
            "region": ["Seoul", "Busan", None],
            "category": ["Population", None, "Population"],
            "value": ["10", "20", None],
        }
    )

    processed = preprocess_kosis_data(raw)

    assert list(processed.columns) == [
        "date",
        "region",
        "category",
        "value",
        "year",
        "month",
    ]
    assert len(processed) == 1
    assert processed.iloc[0]["region"] == "Seoul"
    assert processed.iloc[0]["category"] == "Population"
    assert processed.iloc[0]["year"] == 2024
    assert processed.iloc[0]["month"] == "01"


def test_preprocess_kosis_data_returns_stable_schema_for_mixed_inputs() -> None:
    raw = pd.DataFrame(
        {
            "period": ["2023-12", "2024-01"],
            "area": ["Incheon", "Daegu"],
            "indicator": ["Employment", "Employment"],
            "count": [300, 320],
        }
    )

    processed = preprocess_kosis_data(raw)

    assert list(processed.columns) == [
        "date",
        "region",
        "category",
        "value",
        "year",
        "month",
    ]
    assert processed["region"].tolist() == ["Incheon", "Daegu"]
    assert processed["category"].tolist() == ["Employment", "Employment"]
    assert processed["month"].tolist() == ["12", "01"]


def test_preprocess_refresh_timestamp_returns_string() -> None:
    raw = pd.DataFrame(
        {
            "date": ["2024-01-01"],
            "region": ["Seoul"],
            "category": ["Population"],
            "value": [10],
        }
    )
    ts = get_preprocess_refresh_timestamp(raw)
    assert isinstance(ts, str) and ts
