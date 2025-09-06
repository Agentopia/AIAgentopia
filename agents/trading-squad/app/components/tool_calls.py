"""
Tool Calls Panel Component
Renders a collapsible panel showing recent tool calls captured during analysis.
"""

from __future__ import annotations

from typing import Deque, Iterable
import streamlit as st


def _as_rows(items: Iterable[str]) -> list[dict]:
    """Convert a list/deque of string entries into table-like rows.

    Each item is expected to be a short string like:
    "HH:MM:SS [Tool] <name>: <args-preview>..."
    """
    rows: list[dict] = []
    for i, entry in enumerate(items, start=1):
        rows.append({"#": i, "Entry": str(entry)})
    return rows


def render_tool_calls_panel(
    title: str = "\U0001F6E0\uFE0F Tool Calls (Debug)", *, expanded: bool = False
) -> None:
    """Render a collapsible panel for tool calls stored in st.session_state.tool_calls.

    - Shows a compact count badge
    - Displays the most recent entries first (as they are usually appended left)
    - Graceful empty state
    """
    tool_calls = st.session_state.get("tool_calls")

    with st.expander(title, expanded=expanded):
        if not tool_calls:
            st.info("No tool calls have been recorded yet.")
            return

        # Show a compact count and quick preview
        count = len(tool_calls)
        st.caption(f"Recent tool calls: {count}")

        # Render as a simple table for readability
        try:
            rows = _as_rows(tool_calls)
            st.dataframe(rows, hide_index=True, use_container_width=True)
        except Exception:
            # Fallback: raw list
            for entry in list(tool_calls)[:20]:
                st.markdown(f"- {entry}")


def render_tool_calls_sidebar(title: str = "\U0001F6E0\uFE0F Tool Calls (Debug)", *, expanded: bool = False) -> None:
    """Render Tool Calls as a non-invasive sidebar expander.

    Intended to be used when Debug Mode is ON so it does not distract from main content.
    """
    tool_calls = st.session_state.get("tool_calls")

    with st.sidebar.expander(title, expanded=expanded):
        if not tool_calls:
            st.info("No tool calls have been recorded yet.")
            return

        count = len(tool_calls)
        st.caption(f"Recent tool calls: {count}")

        try:
            rows = _as_rows(tool_calls)
            st.dataframe(rows, hide_index=True, use_container_width=True)
        except Exception:
            for entry in list(tool_calls)[:20]:
                st.markdown(f"- {entry}")
