from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from typing import Any, MutableMapping


DEFAULT_FILTERS: dict[str, Any] = {
    "regions": [],
    "categories": [],
    "date_range": None,
}

DEFAULT_STATE: dict[str, Any] = {
    "page": "Dashboard",
    "selected_dataset": "kosis",
    "filters": DEFAULT_FILTERS,
    "history": [],
    "cache_version": 1,
}


def _fresh_default(value: Any) -> Any:
    """Return a fresh copy for mutable defaults."""
    if isinstance(value, (dict, list, set)):
        return deepcopy(value)
    return value


def init_session_state(state: MutableMapping[str, Any]) -> None:
    """Initialize required session keys without overwriting existing values."""
    for key, value in DEFAULT_STATE.items():
        if key not in state:
            state[key] = _fresh_default(value)


def get_state(state: MutableMapping[str, Any], key: str, default: Any = None) -> Any:
    """Read a value from session state with optional fallback."""
    return state.get(key, default)


def set_state(state: MutableMapping[str, Any], key: str, value: Any) -> None:
    """Set a value in session state."""
    state[key] = value


def reset_filters(state: MutableMapping[str, Any]) -> None:
    """Reset only filter values and keep the rest of the state unchanged."""
    state["filters"] = deepcopy(DEFAULT_FILTERS)


def reset_session(state: MutableMapping[str, Any]) -> None:
    """Clear all session values and re-initialize defaults."""
    state.clear()
    init_session_state(state)


def append_history(
    state: MutableMapping[str, Any],
    action: str,
    details: dict[str, Any] | None = None,
    max_items: int = 100,
) -> None:
    """Append a history event and cap list length for bounded memory usage."""
    history = state.setdefault("history", [])
    history.append(
        {
            "timestamp": datetime.now(UTC).isoformat(),
            "action": action,
            "details": details or {},
        }
    )
    if len(history) > max_items:
        state["history"] = history[-max_items:]
