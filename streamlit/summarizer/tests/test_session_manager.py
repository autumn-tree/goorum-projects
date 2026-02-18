from src.session_manager import (
    append_history,
    get_state,
    init_session_state,
    reset_filters,
    reset_session,
    set_state,
)


def test_init_session_state_sets_expected_defaults() -> None:
    state: dict = {}
    init_session_state(state)

    assert state["page"] == "Dashboard"
    assert state["selected_dataset"] == "kosis"
    assert state["cache_version"] == 1
    assert state["filters"] == {"regions": [], "categories": [], "date_range": None}
    assert state["history"] == []


def test_init_session_state_does_not_override_existing_values() -> None:
    state = {"page": "Debug", "cache_version": 9}
    init_session_state(state)

    assert state["page"] == "Debug"
    assert state["cache_version"] == 9


def test_get_and_set_state_helpers_work() -> None:
    state: dict = {}
    init_session_state(state)

    set_state(state, "page", "Thumbnail Extractor")
    assert get_state(state, "page") == "Thumbnail Extractor"
    assert get_state(state, "missing_key", "fallback") == "fallback"


def test_reset_filters_only_resets_filter_values() -> None:
    state = {
        "page": "Debug",
        "selected_dataset": "kosis",
        "cache_version": 2,
        "filters": {"regions": ["Seoul"], "categories": ["Population"], "date_range": None},
        "history": [],
    }

    reset_filters(state)

    assert state["filters"] == {"regions": [], "categories": [], "date_range": None}
    assert state["page"] == "Debug"
    assert state["cache_version"] == 2


def test_reset_session_restores_defaults() -> None:
    state = {
        "page": "Debug",
        "selected_dataset": "custom",
        "cache_version": 8,
        "filters": {"regions": ["Busan"], "categories": [], "date_range": None},
        "history": [{"action": "changed"}],
    }

    reset_session(state)

    assert state["page"] == "Dashboard"
    assert state["selected_dataset"] == "kosis"
    assert state["cache_version"] == 1
    assert state["filters"] == {"regions": [], "categories": [], "date_range": None}
    assert state["history"] == []


def test_append_history_respects_max_items() -> None:
    state: dict = {}
    init_session_state(state)

    for i in range(105):
        append_history(state, action=f"evt-{i}", details={"index": i}, max_items=100)

    assert len(state["history"]) == 100
    assert state["history"][0]["action"] == "evt-5"
    assert state["history"][-1]["action"] == "evt-104"
