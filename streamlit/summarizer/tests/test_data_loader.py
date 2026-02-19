from __future__ import annotations

from pathlib import Path

import pandas as pd

from src import data_loader


def test_load_kosis_data_uses_local_when_no_api_url(tmp_path: Path) -> None:
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(
        "date,region,category,value\n2024-01-01,Seoul,Population,10\n",
        encoding="utf-8",
    )

    df, source, refresh_ts = data_loader.load_kosis_data(
        api_url=None,
        local_path=csv_path,
    )

    assert source == "local"
    assert isinstance(refresh_ts, str) and refresh_ts
    assert len(df) == 1
    assert list(df.columns) == ["date", "region", "category", "value"]


def test_load_kosis_data_falls_back_to_local_on_api_error(tmp_path: Path) -> None:
    csv_path = tmp_path / "fallback.csv"
    csv_path.write_text(
        "date,region,category,value\n2024-02-01,Busan,Population,20\n",
        encoding="utf-8",
    )

    def _raise_api_error(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("api down")

    original_fetch = data_loader.fetch_kosis_api_data
    data_loader.fetch_kosis_api_data = _raise_api_error  # type: ignore[assignment]
    try:
        df, source, refresh_ts = data_loader.load_kosis_data(
            api_url="https://example.com/kosis",
            local_path=csv_path,
        )
    finally:
        data_loader.fetch_kosis_api_data = original_fetch  # type: ignore[assignment]

    assert source == "local_fallback"
    assert isinstance(refresh_ts, str) and refresh_ts
    assert len(df) == 1
    assert df.iloc[0]["region"] == "Busan"


def test_fetch_kosis_api_data_parses_data_payload(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    class DummyResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, list[dict[str, object]]]:
            return {
                "data": [
                    {
                        "date": "2024-03-01",
                        "region": "Seoul",
                        "category": "Employment",
                        "value": 123,
                    }
                ]
            }

    class DummySession:
        def get(self, *args, **kwargs):  # type: ignore[no-untyped-def]
            return DummyResponse()

    monkeypatch.setattr(data_loader, "get_http_session", lambda: DummySession())

    df = data_loader.fetch_kosis_api_data(
        "https://example.com/kosis",
        local_only=False,
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["region"] == "Seoul"


def test_validate_kosis_api_url_allows_loopback_in_local_only_mode() -> None:
    is_valid, reason = data_loader.validate_kosis_api_url(
        "http://127.0.0.1:8000/data",
        local_only=True,
    )
    assert is_valid is True
    assert reason is None


def test_validate_kosis_api_url_blocks_external_host_in_local_only_mode() -> None:
    is_valid, reason = data_loader.validate_kosis_api_url(
        "https://example.com/kosis",
        local_only=True,
    )
    assert is_valid is False
    assert isinstance(reason, str) and "LOCAL_ONLY" in reason


def test_validate_kosis_api_url_blocks_private_and_metadata_targets() -> None:
    blocked_urls = [
        "http://169.254.169.254/latest/meta-data/",
        "http://10.0.0.8:8080/data",
        "http://192.168.1.20/data",
    ]
    for blocked_url in blocked_urls:
        is_valid, _ = data_loader.validate_kosis_api_url(blocked_url, local_only=False)
        assert is_valid is False


def test_load_kosis_data_uses_local_fallback_when_url_is_blocked(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "fallback_local_only.csv"
    csv_path.write_text(
        "date,region,category,value\n2024-03-01,Incheon,Employment,30\n",
        encoding="utf-8",
    )

    df, source, refresh_ts = data_loader.load_kosis_data(
        api_url="https://example.com/kosis",
        local_path=csv_path,
        local_only=True,
    )

    assert source == "local_fallback"
    assert isinstance(refresh_ts, str) and refresh_ts
    assert len(df) == 1
    assert df.iloc[0]["region"] == "Incheon"
