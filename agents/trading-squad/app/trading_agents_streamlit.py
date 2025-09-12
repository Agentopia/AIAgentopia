"""
TradingAgents Streamlit Interface - Clean Rebuild
A modern web UI for multi-agent trading analysis
"""

import json
import os
import sys
import time
from collections import deque
from datetime import date, datetime, timedelta
import urllib.request
import urllib.parse
import re

import streamlit as st

# Add the parent directory to the path to import tradingagents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TradingAgents - Multi-Agent Trading Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import components (with fallback if they don't exist)
try:
    # from components.agent_status import render_agent_card  # Not used currently
    from components.analysis_params import (
        render_analysis_controls,
        render_analysis_parameters,
    )
    from components.css_loader import load_css
    from components.header_component import render_header
    from components.report_components import render_analysis_report, build_partial_report_md
    from components.sidebar_config import render_sidebar_configuration
    from components.tool_calls import render_tool_calls_sidebar

    COMPONENTS_AVAILABLE = True
except ImportError:
    COMPONENTS_AVAILABLE = False
    st.warning("⚠️ Component modules not found. Using fallback UI.")

# Apply custom styling
if COMPONENTS_AVAILABLE:
    load_css()

# Add agent status button CSS
st.markdown(
    """
<style>
/* Agent Status Button Styling - Updated selectors for actual Streamlit buttons */

/* Running agents (type="primary") - Enhanced visibility */
button[kind="primary"] {
    background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    border: 2px solid #38bdf8 !important;
    box-shadow: 0 4px 20px rgba(14, 165, 233, 0.4) !important;
    animation: agentPulse 2s infinite !important;
}

/* High-contrast focus state for primary buttons (keyboard accessibility) */
button[kind="primary"]:focus-visible {
    outline: 3px solid #f59e0b !important; /* amber ring */
    outline-offset: 3px !important;
    box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.35), 0 4px 20px rgba(14, 165, 233, 0.4) !important;
}

/* Team expander titles: increase size so they are larger than sub-agent buttons */
.stExpander summary,
.stExpander > div[role="button"] {
    font-size: 1.0625rem !important; /* ~17px */
    font-weight: 700 !important;
}

/* Agent status buttons - ONLY inside expanders (team sections) */
.stExpander button[kind="secondary"] {
    background-color: #1f2937 !important; /* slate-800 */
    color: #ffffff !important;
    border: 1px solid transparent !important; /* de-emphasized border */
    box-shadow: none !important; /* remove heavy outline look */
    font-size: 0.875rem !important; /* 14px: smaller than expander title */
    padding: 0.35rem 0.75rem !important; /* slightly tighter */
}

/* High-contrast focus state for secondary buttons */
.stExpander button[kind="secondary"]:focus-visible {
    outline: 3px solid #f59e0b !important; /* amber ring */
    outline-offset: 3px !important;
    box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.35) !important;
}

/* Enhanced pulsing animation for running agents */
@keyframes agentPulse {
    0% {
        transform: scale(1.0);
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.4), 0 0 0 0 rgba(14, 165, 233, 0.7);
    }
    50% {
        transform: scale(1.08);
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.6), 0 0 0 15px rgba(14, 165, 233, 0);
    }
    100% {
        transform: scale(1.0);
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.4), 0 0 0 0 rgba(14, 165, 233, 0);
    }
}

/* Export button styling - remove pulsing from download buttons */
.stDownloadButton > button {
    animation: none !important;
}

/* Color-coded export buttons - targeting actual download buttons */
/* First, override the default gray styling for download buttons */
.stDownloadButton > button[kind="secondary"] {
    background-color: transparent !important;
    border: 1px solid #666666 !important;
}

/* Target download buttons by their text content */
.stDownloadButton > button[kind="secondary"]:has-text("📄 Full Report") {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
    color: white !important;
    border: 1px solid #3b82f6 !important;
}

.stDownloadButton > button[kind="secondary"]:has-text("📋 Execution Log") {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
    color: white !important;
    border: 1px solid #8b5cf6 !important;
}

/* Target regular button for Quick Summary */
button[kind="secondary"]:has-text("🎯 Quick Summary") {
    background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%) !important;
    color: white !important;
    border: 1px solid #06b6d4 !important;
}


/* Alternative selectors in case the above don't work */
.stButton > button[data-testid="baseButton-primary"],
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    border: 2px solid #38bdf8 !important;
    box-shadow: 0 4px 20px rgba(14, 165, 233, 0.4) !important;
    animation: agentPulse 2s infinite !important;
}

/* Focus state fallback for alternative selectors */
.stButton > button[data-testid="baseButton-primary"]:focus-visible,
div[data-testid="stButton"] > button[kind="primary"]:focus-visible {
    outline: 3px solid #f59e0b !important;
    outline-offset: 3px !important;
    box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.35), 0 4px 20px rgba(14, 165, 233, 0.4) !important;
}

</style>""",
    unsafe_allow_html=True,
)


# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if "analysis_running" not in st.session_state:
        st.session_state.analysis_running = False
        
    if "agent_panel_visible" not in st.session_state:
        st.session_state.agent_panel_visible = True

    if "progress_messages" not in st.session_state:
        st.session_state.progress_messages = deque(maxlen=100)

    if "tool_calls" not in st.session_state:
        st.session_state.tool_calls = deque(maxlen=100)

    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None

    if "last_error" not in st.session_state:
        st.session_state.last_error = None

    # Initialize agent status - matching CLI exactly
    if "agent_status" not in st.session_state:
        st.session_state.agent_status = {
            # Analyst Team
            "Market Analyst": "pending",
            "Social Analyst": "pending",
            "News Analyst": "pending",
            "Fundamentals Analyst": "pending",
            # Research Team
            "Bull Researcher": "pending",
            "Bear Researcher": "pending",
            "Research Manager": "pending",
            # Trading Team
            "Trader": "pending",
            # Risk Management Team
            "Risky Analyst": "pending",
            "Neutral Analyst": "pending",
            "Safe Analyst": "pending",
            # Portfolio Management Team
            "Portfolio Manager": "pending",
        }
    # Initialize report sections - matching CLI exactly
    if "report_sections" not in st.session_state:
        st.session_state.report_sections = {
            "market_report": None,
            "sentiment_report": None,
            "news_report": None,
            "fundamentals_report": None,
            "investment_plan": None,
            "trader_investment_plan": None,
            "final_trade_decision": None,
        }

    # Preflight symbol resolution states
    if "preflight_pending" not in st.session_state:
        st.session_state.preflight_pending = False
    if "preflight_profile" not in st.session_state:
        st.session_state.preflight_profile = None
    if "resolved_profile" not in st.session_state:
        st.session_state.resolved_profile = None
    if "pending_symbol" not in st.session_state:
        st.session_state.pending_symbol = None
    if "mismatch_warned_sections" not in st.session_state:
        st.session_state.mismatch_warned_sections = set()


# Fallback UI components
def fallback_render_header():
    """Fallback header component"""
    st.title("📈 TradingAgents - Multi-Agent Trading Analysis")
    st.markdown(
        "*Powered by collaborative AI agents for comprehensive market analysis*"
    )


def fallback_render_sidebar():
    """Fallback sidebar configuration"""
    st.header("🔧 Configuration")

    # API Status
    with st.expander("🔑 API Status", expanded=True):
        openai_key = os.getenv("OPENAI_API_KEY", "")
        finnhub_key = os.getenv("FINNHUB_API_KEY", "")

        if openai_key:
            st.success("✅ OpenAI API Key: Configured")
        else:
            st.error("❌ OpenAI API Key: Missing")

        if finnhub_key:
            st.success("✅ Finnhub API Key: Configured")
        else:
            st.error("❌ Finnhub API Key: Missing")

    # LLM Configuration
    with st.expander("🧠 LLM Configuration", expanded=True):
        provider = st.selectbox("Provider", ["OpenAI"], index=0)
        model = st.selectbox(
            "Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0
        )
        backend_url = st.text_input(
            "Backend URL (optional)", value=os.getenv("OPENAI_API_BASE_URL", "")
        )

    # Analyst Selection
    with st.expander("👥 Analyst Selection", expanded=False):
        analysts = ["market", "social", "news", "fundamentals"]
        selected = st.multiselect("Select Analysts", analysts, default=analysts)

    return {
        "llm_config": {
            "provider": provider,
            "model": model,
            "backend_url": backend_url,
        },
        "selected_analysts": selected,
    }


def fallback_render_analysis_params():
    """Fallback analysis parameters"""
    st.subheader("📊 Analysis Parameters")

    col1, col2 = st.columns(2)
    with col1:
        stock_symbol = st.text_input(
            "Stock Symbol", value="NVDA", placeholder="e.g., AAPL, TSLA"
        )
        analysis_date = st.date_input(
            "Analysis Date", value=date.today() - timedelta(days=1)
        )

    with col2:
        max_debate_rounds = st.slider("Debate Rounds", 1, 5, 2)
        max_risk_rounds = st.slider("Risk Rounds", 1, 3, 2)

    online_tools = st.checkbox("Enable Online Tools", value=True)
    debug_mode = st.checkbox("Debug Mode", value=False)

    return {
        "stock_symbol": stock_symbol,
        "analysis_date": analysis_date,
        "max_debate_rounds": max_debate_rounds,
        "max_risk_rounds": max_risk_rounds,
        "online_tools": online_tools,
        "debug_mode": debug_mode,
    }


def fallback_render_analysis_controls():
    """Fallback analysis controls"""
    if st.session_state.analysis_running:
        if st.button("⏹️ Stop Analysis", type="secondary", use_container_width=True):
            st.session_state.analysis_running = False
            # Clear any stored run configuration tooltip to avoid stale info
            if "current_run_config_tip" in st.session_state:
                del st.session_state["current_run_config_tip"]
            # Debug logging for stop button
            if st.session_state.get("debug_mode", False):
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.progress_messages.appendleft(
                    f"{timestamp} [DEBUG] Stop Analysis button clicked"
                )
            st.rerun()

    # Show Start button when not running
    if not st.session_state.analysis_running:
        started = st.button("🚀 Start Analysis", type="primary", use_container_width=True)
        # Always show a persistent Live Analysis Feed (History) below controls
        render_live_feed_history()
        return started
    # If running, we already returned above after handling Stop
    # Keep feed visible even when running
    render_live_feed_history()
    return False


def fallback_render_agent_card(placeholder, agent, status):
    """Fallback agent status card"""
    if status == "complete":
        placeholder.success(f"✅ {agent}")
    elif status == "running":
        placeholder.info(f"🔄 {agent}")
    elif status == "error":
        placeholder.error(f"❌ {agent}")
    else:
        placeholder.warning(f"⏳ {agent}")


def get_agent_display_text(agent, status):
    """Get dynamic display text based on agent name and status"""
    # Map agent names to their working activity
    agent_activities = {
        "Market Analyst": "Market Analysis",
        "Social Analyst": "Social Analysis",
        "News Analyst": "News Analysis",
        "Fundamentals Analyst": "Fundamentals Analysis",
        "Bull Researcher": "Bull Research",
        "Bear Researcher": "Bear Research",
        "Research Manager": "Research Management",
        "Trader": "Trading Analysis",
        "Risky Analyst": "Risk Analysis",
        "Neutral Analyst": "Neutral Analysis",
        "Safe Analyst": "Safety Analysis",
        "Portfolio Manager": "Portfolio Management",
    }


    activity = agent_activities.get(agent, f"{agent} Work")


    if status == "in_progress":
        return f"🔄 {activity} is Working"
    elif status == "completed":
        # If we have a recorded duration for research sub-agents, append it in brackets
        duration_text = ""
        try:
            durations = st.session_state.get("agent_durations", {})
            # Only show for research sub-agents
            if agent in {"Bull Researcher", "Bear Researcher", "Research Manager"}:
                dur = durations.get(agent)
                if dur is not None:
                    duration_text = f" [{dur:.1f}s]"
        except Exception:
            pass
        return f"✅ {agent} Done{duration_text}"
    elif status == "error":
        return f"❌ {agent} Error"
    else:  # pending
        return f"⏳ {agent} - Waiting"


def render_agent_button(placeholder, agent, status):
    """Render agent button with proper styling based on status"""
    # Use session state counter for unique keys
    if "button_counter" not in st.session_state:
        st.session_state.button_counter = 0
    st.session_state.button_counter += 1
    unique_id = st.session_state.button_counter

    # Get dynamic display text
    display_text = get_agent_display_text(agent, status)

    with placeholder.container():
        if status == "in_progress":
            st.button(
                display_text,
                key=f"agent_{agent}_{status}_{unique_id}",
                disabled=True,
                help=f"Button. {agent} status: in progress. This indicates the agent is actively working.",
                type="primary",
            )
        elif status == "completed":
            st.button(
                display_text,
                key=f"agent_{agent}_{status}_{unique_id}",
                disabled=True,
                help=f"Button. {agent} status: completed. Analysis has finished successfully.",
                type="secondary",
            )
        elif status == "error":
            st.button(
                display_text,
                key=f"agent_{agent}_{status}_{unique_id}",
                disabled=True,
                help=f"Button. {agent} status: error. The agent encountered an issue during analysis.",
                type="secondary",
            )
        else:  # pending
            st.button(
                display_text,
                key=f"agent_{agent}_{status}_{unique_id}",
                disabled=True,
                help=f"Button. {agent} status: pending. Waiting to start.",
                type="secondary",
            )


def update_agent_status(agent: str, status: str):
    """Update agent status and refresh UI placeholder"""
    if agent in st.session_state.agent_status:
        # --- Lightweight timing for research sub-agents ---
        # Initialize timing dicts if needed
        if "agent_start_times" not in st.session_state:
            st.session_state.agent_start_times = {}
        if "agent_durations" not in st.session_state:
            st.session_state.agent_durations = {}

        monitored = {"Bull Researcher", "Bear Researcher", "Research Manager"}
        # On start: record start time
        if status == "in_progress" and agent in monitored:
            # Only set start time if not already set to avoid overwriting
            if st.session_state.agent_start_times.get(agent) is None:
                st.session_state.agent_start_times[agent] = time.time()
        # On complete: compute duration if we have a start time
        if status == "completed" and agent in monitored:
            t0 = st.session_state.agent_start_times.get(agent)
            if t0:
                elapsed = max(0.0, time.time() - t0)
                st.session_state.agent_durations[agent] = elapsed
                # Also push a concise timing line into the live feed
                try:
                    ts = datetime.now().strftime("%H:%M:%S")
                    st.session_state.progress_messages.appendleft(
                        f"{ts} [Timing] {agent} turn completed in {elapsed:.1f}s"
                    )
                except Exception:
                    pass

        # Update status value
        st.session_state.agent_status[agent] = status
        # Update the placeholder if it exists
        if (
            hasattr(st.session_state, "agent_placeholders")
            and agent in st.session_state.agent_placeholders
        ):
            render_agent_button(
                st.session_state.agent_placeholders[agent], agent, status
            )
        # Also refresh the dynamic header counts immediately if available
        header_ph = st.session_state.get("progress_header_placeholder")
        if header_ph is not None:
            try:
                render_progress_header(header_ph)
            except Exception:
                pass


def get_analyst_progress_counts() -> tuple[int, int]:
    """Return (completed_count, total_count) for agent statuses."""
    status = st.session_state.get("agent_status", {})
    total = len(status)
    done = 0
    if status:
        for s in status.values():
            if s in ("completed", "complete"):
                done += 1
    return done, total


def render_progress_header(header_placeholder):
    """Render the 'Analysis in Progress' header with dynamic completion counts.

    Also shows a compact gear icon on the right; hovering reveals the current run
    configuration (provider/model/base URL) as a native tooltip.
    """
    done, total = get_analyst_progress_counts()
    # Build optional tooltip for run configuration
    tip = st.session_state.get("current_run_config_tip")
    # Escape quotes for HTML title attribute
    def _escape_title(s: str) -> str:
        return (
            s.replace("&", "&amp;")
            .replace("\"", "&quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
    tip_html = (
        f'<span title="{_escape_title(tip)}" '
        'style="cursor:help; font-size:0.95rem; color:#9ca3af; white-space:pre-line" aria-label="Run configuration">⚙️\u00A0Run Configuration</span>'
        if tip
        else ""
    )

    # Render header row with counts and right-aligned gear icon
    html = (
        "<div style=\"display:flex; align-items:flex-end; justify-content:space-between;\">"
        "  <div>"
        "    <h3 class=\"section-title-progress\" style=\"margin:0 0 0.25rem 0;\">🔄 Analysis in Progress...</h3>"
        f"    <div style=\"font-size:0.875rem; color:#9ca3af; margin-top:0.1rem\">({done}/{total} analysts completed)</div>"
        "  </div>"
        f"  <div style=\"padding-left:0.5rem\">{tip_html}</div>"
        "</div>"
    )
    header_placeholder.markdown(html, unsafe_allow_html=True)


def render_live_feed_history():
    """Render a persistent, collapsible Live Analysis Feed (History)."""
    try:
        with st.expander("💬 Live Analysis Feed (History)", expanded=False):
            # Render up to the last 400 messages in a scrollable div
            history_msgs = list(st.session_state.get("progress_messages", []))
            history_html = "<div style='max-height: 360px; overflow-y: auto; font-size: 0.9rem;'>"
            for msg in history_msgs[:400]:
                history_html += f"<div>- {msg}</div>"
            history_html += "</div>"
            st.markdown(history_html, unsafe_allow_html=True)
    except Exception:
        pass


# --- Event-driven progress tracking helpers ---
def _init_progress_tracker(progress_bar_obj):
    """Initialize event-driven progress tracker in session state.

    We map key analysis milestones to a set of unique events. Each first-time
    event increases the progress floor, creating a steady, real-time feeling.
    """
    st.session_state["progress_bar"] = progress_bar_obj
    st.session_state["progress_events_done"] = set()
    # Define the ordered set of events we'll count toward progress
    st.session_state["progress_events_list"] = [
        # Initialization
        "init_start",
        "framework_ready",
        "first_analyst_started",
        # Analyst reports
        "market_report",
        "sentiment_report",
        "news_report",
        "fundamentals_report",
        # Research debate milestones
        "research_bull",
        "research_bear",
        "research_manager_decision",
        # Trader plan
        "trader_plan",
        # Risk debate milestones
        "risk_risky",
        "risk_safe",
        "risk_neutral",
        # Portfolio manager
        "portfolio_judge",
        # Finalization
        "finalized",
    ]
    st.session_state["progress_total_events"] = len(
        st.session_state["progress_events_list"]
    )


def _mark_progress(event_name: str):
    """Record an analysis event and bump the progress floor proportionally."""
    bar = st.session_state.get("progress_bar")
    if bar is None:
        return
    events_done = st.session_state.get("progress_events_done")
    all_events = st.session_state.get("progress_events_list")
    if not isinstance(events_done, set) or not isinstance(all_events, list):
        return
    if event_name in events_done:
        return
    events_done.add(event_name)
    # Compute target progress: start at ~2% and linearly approach ~99%
    total = max(1, st.session_state.get("progress_total_events", len(all_events)))
    fraction = len(events_done) / total
    target = min(0.99, 0.02 + 0.97 * fraction)
    # Prevent regression
    target = max(target, st.session_state.get("last_progress", 0.0))
    try:
        bar.progress(target)
        st.session_state["last_progress"] = target
    except Exception:
        pass


def extract_content_string(content):
    """Extract string content from various message formats - matching CLI"""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # Handle Anthropic's list format
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
                elif item.get("type") == "tool_use":
                    text_parts.append(f"[Tool: {item.get('name', 'unknown')}]")
            else:
                text_parts.append(str(item))
        return " ".join(text_parts)
    else:
        return str(content)


def update_research_team_status(status):
    """Update status for all research team members and trader - matching CLI"""
    research_team = ["Bull Researcher", "Bear Researcher", "Research Manager", "Trader"]
    for agent in research_team:
        update_agent_status(agent, status)


def generate_markdown_report(analysis_results: dict) -> str:
    """Generate a comprehensive Markdown report from analysis results"""
    results = analysis_results
    result_data = results.get("result", {})

    # Header
    markdown_content = f"""# Trading Analysis Report

**Symbol:** {results.get("symbol", "N/A")}
**Analysis Date:** {results.get("date", "N/A")}
**Generated:** {results.get("timestamp", "N/A")}
**Final Decision:** {results.get("decision", "N/A")}

---

"""

    # Add each report section
    section_mapping = {
        "market_report": "## 📈 Market Analysis",
        "sentiment_report": "## 👥 Social Sentiment Analysis",
        "news_report": "## 📰 News Analysis",
        "fundamentals_report": "## 💼 Fundamentals Analysis",
        "investment_plan": "## 🔍 Research Team Analysis",
        "trader_investment_plan": "## 💰 Trading Team Plan",
        "final_trade_decision": "## ⚖️ Portfolio Management Decision",
    }

    for section_key, section_title in section_mapping.items():
        if result_data.get(section_key):
            markdown_content += (
                f"{section_title}\n\n{result_data[section_key]}\n\n---\n\n"
            )

    # Add metadata footer
    markdown_content += f"""
## Analysis Metadata

- **Analysis Framework:** TradingAgents Multi-Agent System
- **Report Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Configuration:** {results.get("symbol", "N/A")} analysis for {results.get("date", "N/A")}

*This report was generated by the TradingAgents collaborative AI framework.*
"""

    return markdown_content


def generate_jsonl_log(
    analysis_results: dict, progress_messages: deque, tool_calls: deque
) -> str:
    """Generate JSONL log with run metadata, progress messages, and tool calls"""
    jsonl_lines = []

    # Add run metadata
    metadata = {
        "type": "run_metadata",
        "timestamp": datetime.now().isoformat(),
        "symbol": analysis_results.get("symbol", "N/A"),
        "analysis_date": analysis_results.get("date", "N/A"),
        "decision": analysis_results.get("decision", "N/A"),
        "generated_at": analysis_results.get("timestamp", "N/A"),
    }
    jsonl_lines.append(json.dumps(metadata))

    # Add progress messages
    for message in progress_messages:
        log_entry = {
            "type": "progress_message",
            "timestamp": datetime.now().isoformat(),
            "content": str(message),
        }
        jsonl_lines.append(json.dumps(log_entry))

    # Add tool calls
    for tool_call in tool_calls:
        log_entry = {
            "type": "tool_call",
            "timestamp": datetime.now().isoformat(),
            "content": str(tool_call),
        }
        jsonl_lines.append(json.dumps(log_entry))

    # Add final results summary
    summary = {
        "type": "analysis_summary",
        "timestamp": datetime.now().isoformat(),
        "total_progress_messages": len(progress_messages),
        "total_tool_calls": len(tool_calls),
        "analysis_completed": True,
    }
    jsonl_lines.append(json.dumps(summary))

    return "\n".join(jsonl_lines)


def get_decision_summary(analysis_results: dict) -> str:
    """Extract a concise decision summary for copy-to-clipboard"""
    symbol = analysis_results.get("symbol", "N/A")
    date = analysis_results.get("date", "N/A")
    decision = analysis_results.get("decision", "N/A")

    # Try to extract key reasoning from final decision
    result_data = analysis_results.get("result", {})
    final_decision_text = result_data.get("final_trade_decision", "")

    # Extract first few sentences as reasoning
    reasoning = "Analysis completed"
    if final_decision_text:
        sentences = final_decision_text.split(".")[:2]  # First 2 sentences
        reasoning = ".".join(sentences).strip()
        if reasoning and not reasoning.endswith("."):
            reasoning += "."

    summary = f"""TradingAgents Analysis Summary
Symbol: {symbol}
Date: {date}
Decision: {decision}
Reasoning: {reasoning}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""

    return summary


def fetch_company_profile(symbol: str) -> dict:
    """Fetch company profile for a ticker using Finnhub if configured.

    Returns a dict with keys like: name, ticker, exchange, country, finnhubIndustry, weburl, ipo, logo, marketCapitalization, shareOutstanding.
    If no API key configured or request fails, returns an empty dict.
    """
    token = os.getenv("FINNHUB_API_KEY", "").strip()
    if not token or not symbol:
        return {}
    try:
        base = "https://finnhub.io/api/v1/stock/profile2"
        params = urllib.parse.urlencode({"symbol": symbol.upper(), "token": token})
        url = f"{base}?{params}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            # Finnhub returns {} for unknown symbols
            if isinstance(data, dict) and data:
                return data
            return {}
    except Exception:
        return {}


def validate_and_correct_section(text: str, company_name: str | None, symbol: str) -> tuple[str, bool]:
    """Validate section text mentions the resolved company; lightly correct common header formats.

    Returns (corrected_text, is_consistent).
    is_consistent is True if the text likely refers to the resolved company.
    """
    if not text:
        return text, True
    if not company_name:
        return text, True

    lower = text.lower()
    consistent = company_name.lower() in lower

    # Try to fix a common header like: "Comprehensive Report on CRCL (Other Name)"
    # Replace parenthetical company with the resolved one when symbol matches
    header_pattern = rf"^(.*?\b{re.escape(symbol)}\s*\()(.*?)(\))"
    def _repl(m):
        return f"{m.group(1)}{company_name}{m.group(3)}"

    corrected = re.sub(header_pattern, _repl, text, count=1, flags=re.IGNORECASE | re.MULTILINE)
    # After correction, deem consistent if company name now present
    if company_name.lower() in corrected.lower():
        consistent = True
    return corrected, consistent


def run_real_analysis(
    stock_symbol: str,
    analysis_date: date,
    analysis_params: dict,
    llm_config: dict,
    selected_analysts: list,
    debug_mode: bool,
):
    """Run real TradingAgents analysis - matching CLI streaming behavior exactly"""

    # Import TradingAgents
    try:
        from tradingagents.default_config import DEFAULT_CONFIG
        from tradingagents.graph.trading_graph import TradingAgentsGraph
    except ImportError as e:
        st.error(f"Failed to import TradingAgents: {e}")
        st.error("Please ensure TradingAgents is properly installed.")
        st.session_state.analysis_running = False
        return

    # Create progress placeholders
    progress_container = st.container()
    with progress_container:
        header_placeholder = st.empty()
        # Persist header placeholder so status updates can refresh counts immediately
        st.session_state["progress_header_placeholder"] = header_placeholder
        render_progress_header(header_placeholder)
        progress_bar = st.progress(0)
        # Initialize a progress floor to prevent regressions in early phases
        st.session_state["last_progress"] = 0.0
        # Initialize event-driven progress tracker and mark init start
        _init_progress_tracker(progress_bar)
        _mark_progress("init_start")
        # Show an immediate small progress indicator so users see activity right away
        try:
            progress = 0.02
            progress_bar.progress(progress)
            st.session_state["last_progress"] = max(st.session_state["last_progress"], progress)
        except Exception:
            pass
        status_text = st.empty()

        st.markdown('<h3 class="section-title-info">💬 Live Analysis Feed</h3>', unsafe_allow_html=True)
        # Systematic CSS definitions for different text types
        st.markdown("""
        <style>
        /* === SYSTEMATIC FONT SIZE DEFINITIONS === */
        
        /* Main Section Titles */
        .section-title-primary {
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            color: #22c55e !important;
            margin-bottom: 1rem !important;
        }
        
        /* Progress Section Titles */
        .section-title-progress {
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            color: #e74c3c !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Info Section Titles */
        .section-title-info {
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            color: #1f77b4 !important;
            margin-bottom: 1rem !important;
        }
        
        /* Content Text */
        .content-text {
            font-size: 0.875rem !important;
            line-height: 1.4 !important;
            font-weight: normal !important;
        }
        
        /* Feed Messages */
        .feed-message {
            font-size: 0.875rem !important;
            line-height: 1.4 !important;
            font-weight: normal !important;
        }
        
        /* Status Text */
        .status-text {
            font-size: 0.875rem !important;
            color: #9ca3af !important;
            font-weight: normal !important;
        }
        
        /* === APPLY TO STREAMLIT ELEMENTS === */
        
        /* Target all markdown content by default */
        .stMarkdown p, .stMarkdown div, .stMarkdown span, .stMarkdown li {
            font-size: 0.875rem !important;
            line-height: 1.4 !important;
            font-weight: normal !important;
        }
        
        /* Override unwanted large headers in content areas */
        .stMarkdown h1:not(.section-title-primary):not(.section-title-progress):not(.section-title-info),
        .stMarkdown h2:not(.section-title-primary):not(.section-title-progress):not(.section-title-info),
        .stMarkdown h4:not(.section-title-primary):not(.section-title-progress):not(.section-title-info) {
            font-size: 0.875rem !important;
            font-weight: normal !important;
        }
        </style>
        <script>
        // JavaScript to fix oversized content while preserving section titles
        function resizeAnalysisFeed() {
            // Target content elements but preserve section titles
            const allElements = document.querySelectorAll('p, div, span, li');
            allElements.forEach(el => {
                // Skip section titles but target content
                if (el.textContent && 
                    !el.textContent.includes('💬 Live Analysis Feed') &&
                    !el.textContent.includes('🔄 Analysis in Progress') &&
                    !el.closest('h3') && // Don't target elements inside h3 tags
                    (el.textContent.includes('Total records') || 
                     el.textContent.includes('Data retrieved') ||
                     el.textContent.includes('Market Analyst') ||
                     el.textContent.includes('Social Analyst') ||
                     el.textContent.includes('News Analyst') ||
                     el.textContent.includes('Fundamentals Analyst') ||
                     el.textContent.includes('Provider:') ||
                     el.textContent.includes('Model:') ||
                     el.textContent.includes('Base URL:') ||
                     el.textContent.includes('Selected') ||
                     /\\d{2}:\\d{2}:\\d{2}/.test(el.textContent))) {
                    
                    // Only resize content, not titles
                    el.style.setProperty('font-size', '0.875rem', 'important');
                    el.style.setProperty('font-weight', 'normal', 'important');
                    el.style.setProperty('line-height', '1.4', 'important');
                }
            });
            
            // Specifically target problem elements but preserve titles
            const problemTexts = ['Total records:', 'Data retrieved on:'];
            problemTexts.forEach(text => {
                const elements = Array.from(document.querySelectorAll('*')).filter(el => 
                    el.textContent && 
                    el.textContent.includes(text) &&
                    !el.closest('h3') // Don't target if inside h3
                );
                elements.forEach(el => {
                    el.style.setProperty('font-size', '0.875rem', 'important');
                    el.style.setProperty('font-weight', 'normal', 'important');
                });
            });
            
            // Ensure section titles remain large
            const sectionTitles = document.querySelectorAll('h3');
            sectionTitles.forEach(title => {
                if (title.textContent && 
                    (title.textContent.includes('💬 Live Analysis Feed') ||
                     title.textContent.includes('🔄 Analysis in Progress'))) {
                    title.style.setProperty('font-size', '1.5rem', 'important');
                    title.style.setProperty('font-weight', '700', 'important');
                }
            });
        }
        
        // Run more frequently to catch dynamic content
        setTimeout(resizeAnalysisFeed, 50);
        setTimeout(resizeAnalysisFeed, 200);
        setTimeout(resizeAnalysisFeed, 500);
        setInterval(resizeAnalysisFeed, 500);
        </script>
        """, unsafe_allow_html=True)
        messages_container = st.empty()

        # Initialize with a placeholder message to verify container works
        messages_container.markdown("- Waiting for analysis to start...")

        # (Removed main-area Tooling section; Tool Calls now lives in sidebar)
        # (Removed Current Report section; moved to Agent Status side pane)

    # Configure TradingAgents - matching CLI config
    config = DEFAULT_CONFIG.copy()

    # Determine model selection based on depth and sidebar choices
    depth_choice = analysis_params.get("depth_choice", "Standard")
    quick_model = llm_config.get("quick_think_model")
    deep_model = llm_config.get("deep_think_model")
    chosen_model = (
        deep_model
        if depth_choice == "Deep"
        else (quick_model or deep_model or llm_config.get("model", "gpt-4o"))
    )

    backend_url = llm_config.get("backend_url") or None

    config["llm_config"] = {
        "provider": llm_config.get("provider", "OpenAI").lower(),
        "config_list": [
            {
                "model": chosen_model,
                "base_url": backend_url,
            }
        ],
        "temperature": 0.1,
    }

    # Map UI depth to backend research depth
    depth_map = {"Beginner": "shallow", "Standard": "balanced", "Deep": "deep"}
    if depth_choice == "Custom":
        total_rounds = (
            int(analysis_params.get("max_debate_rounds", 2))
            + int(analysis_params.get("max_risk_rounds", 2))
        )
        research_depth = "deep" if total_rounds >= 5 else "balanced"
    else:
        research_depth = depth_map.get(depth_choice, "balanced")
    config["research_depth"] = research_depth
    # Honor Online Tools toggle from Analysis Parameters
    config["online_tools"] = bool(analysis_params.get("online_tools", True))
    # Wire debate/risk rounds from Analysis Parameters (used by ConditionalLogic)
    try:
        config["max_debate_rounds"] = int(analysis_params.get("max_debate_rounds", 1))
    except Exception:
        config["max_debate_rounds"] = 1
    try:
        # Note: UI uses 'max_risk_rounds'; backend expects 'max_risk_discuss_rounds'
        config["max_risk_discuss_rounds"] = int(analysis_params.get("max_risk_rounds", 1))
    except Exception:
        config["max_risk_discuss_rounds"] = 1

    # Fetch a fresh company profile for this run only (no session coupling)
    local_profile = fetch_company_profile(stock_symbol)
    if local_profile:
        config["company_profile"] = local_profile

    # Map selected analysts to TradingAgents format
    analyst_mapping = {
        "market": "market",
        "social": "social",
        "news": "news",
        "fundamentals": "fundamentals",
    }

    if selected_analysts:
        mapped_analysts = [analyst_mapping.get(key, key) for key in selected_analysts]
    else:
        mapped_analysts = ["market", "social", "news", "fundamentals"]

    try:
        # Initialize TradingAgents
        status_text.text("🔧 Initializing TradingAgents framework...")
        ta = TradingAgentsGraph(
            selected_analysts=mapped_analysts, debug=debug_mode, config=config
        )
        # Bump progress slightly after framework initialization
        try:
            progress = 0.08
            progress_bar.progress(progress)
            st.session_state["last_progress"] = max(st.session_state["last_progress"], progress)
        except Exception:
            pass
        # Event milestone: framework ready
        _mark_progress("framework_ready")

        # Run configuration summary (condensed into header tooltip)
        provider = config.get("llm_config", {}).get("provider")
        model = (config.get("llm_config", {}).get("config_list") or [{}])[0].get("model")
        base_url = (config.get("llm_config", {}).get("config_list") or [{}])[0].get("base_url")
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.progress_messages.appendleft(
            f"{timestamp} - Provider: {provider} | Model: {model} | Base URL: {base_url or 'default'}"
        )
        # Store a compact run configuration string for the header tooltip
        st.session_state["current_run_config_tip"] = (
            f"Provider: {provider}\nModel: {model}\nBase URL: {base_url or 'default'}"
        )
        # Refresh the header to ensure the gear icon + tooltip appear immediately
        render_progress_header(header_placeholder)

        status_text.text("🚀 Starting analysis...")
        date_str = analysis_date.strftime("%Y-%m-%d")

        # Lifecycle log: AnalysisStart
        if st.session_state.get("ui_debug_mode"):
            ts = datetime.now().strftime("%H:%M:%S")
            st.session_state.tool_calls.appendleft(
                f"{ts} [Tool] AnalysisStart: {stock_symbol} @ {date_str}"
            )
            if "tool_calls_sidebar_placeholder" in st.session_state:
                with st.session_state.tool_calls_sidebar_placeholder.container():
                    render_tool_calls_sidebar(expanded=False)

        # Initialize state and get graph args - matching CLI exactly
        init_agent_state = ta.propagator.create_initial_state(stock_symbol, date_str)
        args = ta.propagator.get_graph_args()

        # Add initial system messages
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.progress_messages.appendleft(
            f"{timestamp} - Selected ticker: {stock_symbol}"
        )
        st.session_state.progress_messages.appendleft(
            f"{timestamp} - Analysis date: {date_str}"
        )
        st.session_state.progress_messages.appendleft(
            f"{timestamp} - Selected analysts: {', '.join(mapped_analysts)}"
        )

        # Debug-only: no longer mirroring initial progress lines to avoid duplication with Live Feed

        # Show the most recent messages immediately (before streaming starts)
        initial_msgs = []
        for msg in list(st.session_state.progress_messages)[:10]:
            initial_msgs.append(f"- {msg}")
        messages_container.markdown("\n".join(initial_msgs))

        # Set first analyst to in_progress
        if mapped_analysts:
            first_analyst = f"{mapped_analysts[0].capitalize()} Analyst"
            update_agent_status(first_analyst, "in_progress")
            # Refresh dynamic header counts
            render_progress_header(header_placeholder)
            # Provide an immediate visual bump to indicate analyst work has started
            try:
                progress = 0.18
                progress_bar.progress(progress)
                st.session_state["last_progress"] = max(st.session_state["last_progress"], progress)
            except Exception:
                pass
            # Event milestone: first analyst started
            _mark_progress("first_analyst_started")

        # Debug: Show which analysts are selected
        if debug_mode:
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.progress_messages.appendleft(
                f"{timestamp} [DEBUG] Starting analysis with analysts: {mapped_analysts}"
            )

        # Stream the analysis - matching CLI exactly
        trace = []
        try:
            # Debug: Log streaming start
            if debug_mode:
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.progress_messages.appendleft(
                    f"{timestamp} [DEBUG] Starting streaming loop"
                )
                messages_container.markdown(
                    f"- {timestamp} [DEBUG] Starting streaming loop"
                )
                # Bump progress when the first stream starts arriving
                try:
                    progress = 0.15
                    progress_bar.progress(progress)
                    st.session_state["last_progress"] = max(st.session_state["last_progress"], progress)
                except Exception:
                    pass

            for chunk in ta.graph.stream(init_agent_state, **args):
                if not st.session_state.analysis_running:
                    break

                # Debug: Log each chunk received
                if debug_mode:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    chunk_keys = list(chunk.keys())
                    st.session_state.progress_messages.appendleft(
                        f"{timestamp} [DEBUG] Received chunk with keys: {chunk_keys}"
                    )

                    # Check if this chunk should trigger Social Analyst
                    if "sentiment_report" in chunk_keys:
                        st.session_state.progress_messages.appendleft(
                            f"{timestamp} [DEBUG] Found sentiment_report in chunk!"
                        )
                    elif any(key.startswith("social") for key in chunk_keys):
                        st.session_state.progress_messages.appendleft(
                            f"{timestamp} [DEBUG] Found social-related key in chunk: {[k for k in chunk_keys if 'social' in k.lower()]}"
                        )

                    # Update UI immediately with debug info
                    all_debug_messages = []
                    for msg in list(st.session_state.progress_messages)[:15]:
                        all_debug_messages.append(f"- {msg}")
                    messages_container.markdown("\n".join(all_debug_messages))

                if len(chunk.get("messages", [])) > 0:
                    # Get the last message from the chunk
                    last_message = chunk["messages"][-1]

                    # Extract message content and type
                    if hasattr(last_message, "content"):
                        content = extract_content_string(last_message.content)
                        msg_type = "Reasoning"
                    else:
                        content = str(last_message)
                        msg_type = "System"

                    # Add full message to buffer (no truncation; history is scrollable)
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.progress_messages.appendleft(
                        f"{timestamp} [{msg_type}] {content}"
                    )

                    # Debug-only: do not mirror streamed messages into Tool Calls (keeps panel focused)

                    # If it's a tool call, add it to tool calls and refresh the sidebar panel
                    if hasattr(last_message, "tool_calls"):
                        for tool_call in last_message.tool_calls:
                            if isinstance(tool_call, dict):
                                st.session_state.tool_calls.appendleft(
                                    f"{timestamp} [Tool] {tool_call['name']}: {str(tool_call['args'])}"
                                )
                            else:
                                st.session_state.tool_calls.appendleft(
                                    f"{timestamp} [Tool] {tool_call.name}: {str(tool_call.args)}"
                                )
                        # Refresh sidebar panel if debug mode is on
                        if analysis_params.get("debug_mode", False):
                            if "tool_calls_sidebar_placeholder" not in st.session_state:
                                st.session_state.tool_calls_sidebar_placeholder = st.sidebar.empty()
                            with st.session_state.tool_calls_sidebar_placeholder.container():
                                render_tool_calls_sidebar(expanded=False)

                    # Update UI displays immediately after adding messages
                    all_messages = []
                    for msg in list(st.session_state.progress_messages)[:10]:
                        all_messages.append(f"- {msg}")
                    for tool in list(st.session_state.tool_calls)[:5]:
                        all_messages.append(f"- {tool}")

                    messages_container.markdown("\n".join(all_messages[:15]))

                # Update reports and agent status based on chunk content - EXACTLY matching CLI

                # Analyst Team Reports
                if "market_report" in chunk and chunk["market_report"]:
                    content = chunk["market_report"]
                    # Use the local per-run profile's company name if available
                    company_name = local_profile.get("name") if local_profile else None
                    corrected, ok = validate_and_correct_section(
                        content, company_name, stock_symbol
                    ) if company_name else (content, True)
                    st.session_state.report_sections["market_report"] = corrected
                    if not ok and "market_report" not in st.session_state.mismatch_warned_sections:
                        ts = datetime.now().strftime("%H:%M:%S")
                        st.session_state.progress_messages.appendleft(
                            f"{ts} [WARN] Company identity mismatch detected in Market Analysis — adjusted header."
                        )
                        st.session_state.mismatch_warned_sections.add("market_report")
                    update_agent_status("Market Analyst", "completed")
                    # Event milestone: market report ready
                    _mark_progress("market_report")
                    # Set next analyst to in_progress
                    # Check if social analyst is selected using correct format
                    selected_analyst_names = [
                        f"{analyst.lower()}" for analyst in mapped_analysts
                    ]
                    if "social" in selected_analyst_names:
                        update_agent_status("Social Analyst", "in_progress")
                        if debug_mode:
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            st.session_state.progress_messages.appendleft(
                                f"{timestamp} [DEBUG] Starting Social Analyst after Market completion"
                            )

                if "sentiment_report" in chunk and chunk["sentiment_report"]:
                    if debug_mode:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        st.session_state.progress_messages.appendleft(
                            f"{timestamp} [DEBUG] Received sentiment_report chunk"
                        )
                    content = chunk["sentiment_report"]
                    # Use the local per-run profile's company name if available
                    company_name = local_profile.get("name") if local_profile else None
                    corrected, ok = validate_and_correct_section(
                        content, company_name, stock_symbol
                    ) if company_name else (content, True)
                    st.session_state.report_sections["sentiment_report"] = corrected
                    if not ok and "sentiment_report" not in st.session_state.mismatch_warned_sections:
                        ts = datetime.now().strftime("%H:%M:%S")
                        st.session_state.progress_messages.appendleft(
                            f"{ts} [WARN] Company identity mismatch detected in Social Sentiment — adjusted header."
                        )
                        st.session_state.mismatch_warned_sections.add("sentiment_report")
                    update_agent_status("Social Analyst", "completed")
                    # Event milestone: sentiment report ready
                    _mark_progress("sentiment_report")
                    # Set next analyst to in_progress
                    selected_analyst_names = [
                        f"{analyst.lower()}" for analyst in mapped_analysts
                    ]
                    if "news" in selected_analyst_names:
                        update_agent_status("News Analyst", "in_progress")
                        if debug_mode:
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            st.session_state.progress_messages.appendleft(
                                f"{timestamp} [DEBUG] Starting News Analyst"
                            )

                if "news_report" in chunk and chunk["news_report"]:
                    content = chunk["news_report"]
                    # Use the local per-run profile's company name if available
                    company_name = local_profile.get("name") if local_profile else None
                    corrected, ok = validate_and_correct_section(
                        content, company_name, stock_symbol
                    ) if company_name else (content, True)
                    st.session_state.report_sections["news_report"] = corrected
                    if not ok and "news_report" not in st.session_state.mismatch_warned_sections:
                        ts = datetime.now().strftime("%H:%M:%S")
                        st.session_state.progress_messages.appendleft(
                            f"{ts} [WARN] Company identity mismatch detected in News Analysis — adjusted header."
                        )
                        st.session_state.mismatch_warned_sections.add("news_report")
                    update_agent_status("News Analyst", "completed")
                    # Event milestone: news report ready
                    _mark_progress("news_report")
                    # Set next analyst to in_progress
                    selected_analyst_names = [
                        f"{analyst.lower()}" for analyst in mapped_analysts
                    ]
                    if "fundamentals" in selected_analyst_names:
                        update_agent_status("Fundamentals Analyst", "in_progress")

                if "fundamentals_report" in chunk and chunk["fundamentals_report"]:
                    content = chunk["fundamentals_report"]
                    # Use the local per-run profile's company name if available
                    company_name = local_profile.get("name") if local_profile else None
                    corrected, ok = validate_and_correct_section(
                        content, company_name, stock_symbol
                    ) if company_name else (content, True)
                    st.session_state.report_sections["fundamentals_report"] = corrected
                    if not ok and "fundamentals_report" not in st.session_state.mismatch_warned_sections:
                        ts = datetime.now().strftime("%H:%M:%S")
                        st.session_state.progress_messages.appendleft(
                            f"{ts} [WARN] Company identity mismatch detected in Fundamentals — adjusted header."
                        )
                        st.session_state.mismatch_warned_sections.add("fundamentals_report")
                    update_agent_status("Fundamentals Analyst", "completed")
                    # Start Research phase: only Bull Researcher should be in progress first
                    update_agent_status("Bull Researcher", "in_progress")
                    update_agent_status("Bear Researcher", "pending")
                    update_agent_status("Research Manager", "pending")
                    # Event milestone: fundamentals report ready
                    _mark_progress("fundamentals_report")

                # Update partial report after any analyst section change
                if "report_container" in st.session_state:
                    st.session_state.report_container.markdown(
                        build_partial_report_md(st.session_state.report_sections)
                    )

                # Update progress (reflect in-progress work for better UX)
                completed_count = sum(
                    1 for s in st.session_state.agent_status.values() if s == "completed"
                )
                in_progress_count = sum(
                    1 for s in st.session_state.agent_status.values() if s == "in_progress"
                )
                total_agents = len(st.session_state.agent_status)
                if total_agents > 0:
                    progress_val = (completed_count + 0.3 * in_progress_count) / total_agents
                    # Avoid showing full bar until completion
                    progress_val = min(progress_val, 0.99)
                else:
                    progress_val = 0
                # Prevent regression: never drop below last_progress
                progress_val = max(progress_val, st.session_state.get("last_progress", 0.0))
                progress_bar.progress(progress_val)
                st.session_state["last_progress"] = progress_val

                # Update status text
                in_progress_agents = [
                    agent
                    for agent, status in st.session_state.agent_status.items()
                    if status == "in_progress"
                ]
                if in_progress_agents:
                    status_text.text(f"🔄 {in_progress_agents[0]} is working...")
                else:
                    status_text.text("🔄 Processing...")

                trace.append(chunk)
                time.sleep(0.1)  # Small delay for UI responsiveness

            # Initialize progress tracker at analysis start
            if not st.session_state.get("progress_tracker"):
                st.session_state.progress_tracker = {
                    "milestones": [],
                    "completed": 0,
                    "total": 0,
                }

            # Research Team - Handle Investment Debate State
            if "investment_debate_state" in chunk and chunk["investment_debate_state"]:
                debate_state = chunk["investment_debate_state"]

                # Seed timing for current speaker if available
                try:
                    current = (debate_state.get("current_response") or "").lower()
                except Exception:
                    current = ""
                if current:
                    if "bull" in current:
                        if "agent_start_times" not in st.session_state:
                            st.session_state.agent_start_times = {}
                        if st.session_state.agent_start_times.get("Bull Researcher") is None:
                            st.session_state.agent_start_times["Bull Researcher"] = time.time()
                    elif "bear" in current:
                        if "agent_start_times" not in st.session_state:
                            st.session_state.agent_start_times = {}
                        if st.session_state.agent_start_times.get("Bear Researcher") is None:
                            st.session_state.agent_start_times["Bear Researcher"] = time.time()

                # Initialize debate history trackers
                if "debate_seen" not in st.session_state:
                    st.session_state.debate_seen = {"bull": 0, "bear": 0, "judge": ""}

                # Update Bull Researcher status and report (per-agent status)
                if "bull_history" in debate_state and debate_state["bull_history"]:
                    # Only handle completion if bull history grew
                    bull_lines = [l for l in debate_state["bull_history"].split("\n") if l.strip()]
                    if len(bull_lines) > st.session_state.debate_seen.get("bull", 0):
                        # Bull's turn content has arrived => Bull completes now
                        update_agent_status("Bull Researcher", "completed")
                        # Start Bear's timing/turn
                        update_agent_status("Bear Researcher", "in_progress")
                        st.session_state.debate_seen["bull"] = len(bull_lines)
                    update_agent_status("Research Manager", "pending")
                    bull_responses = debate_state["bull_history"].split("\n")
                    latest_bull = bull_responses[-1] if bull_responses else ""
                    if latest_bull:
                        st.session_state.report_sections["investment_plan"] = (
                            f"### Bull Researcher Analysis\n{latest_bull}"
                        )
                        # Event milestone: research bull contribution
                        _mark_progress("research_bull")
                    st.session_state.progress_tracker["milestones"].append("bull_history")
                    st.session_state.progress_tracker["completed"] += 1
                    st.session_state.progress_tracker["total"] += 1

                # Update Bear Researcher status and report (per-agent status)
                if "bear_history" in debate_state and debate_state["bear_history"]:
                    # Only handle completion if bear history grew
                    bear_lines = [l for l in debate_state["bear_history"].split("\n") if l.strip()]
                    if len(bear_lines) > st.session_state.debate_seen.get("bear", 0):
                        # Bear's turn content has arrived => Bear completes now
                        update_agent_status("Bear Researcher", "completed")
                        st.session_state.debate_seen["bear"] = len(bear_lines)
                    # Begin Research Manager's turn so we can measure timing before decision arrives
                    update_agent_status("Research Manager", "in_progress")
                    bear_responses = debate_state["bear_history"].split("\n")
                    latest_bear = bear_responses[-1] if bear_responses else ""
                    if latest_bear:
                        # Append or replace investment plan preview with Bear section
                        st.session_state.report_sections["investment_plan"] = (
                            f"### Bear Researcher Analysis\n{latest_bear}"
                        )
                        # Event milestone: research bear contribution
                        _mark_progress("research_bear")

                # Research Manager (judge) takes over after debate rounds
                if (
                    "judge_decision" in debate_state
                    and debate_state["judge_decision"]
                ):
                    # Judge has produced a decision: mark debaters completed,
                    # mark Research Manager completed, and move Trader to in_progress
                    st.session_state.report_sections["investment_plan"] = (
                        f"### Research Manager Decision\n{debate_state['judge_decision']}"
                    )
                    update_agent_status("Bull Researcher", "completed")
                    update_agent_status("Bear Researcher", "completed")
                    update_agent_status("Research Manager", "completed")
                    update_agent_status("Trader", "in_progress")
                    _mark_progress("research_manager_decision")

                # ... (rest of the code remains the same)

                if "trader_investment_plan" in chunk and chunk["trader_investment_plan"]:
                    # Trader has produced a plan: mark Trader completed and advance to Risk phase
                    st.session_state.report_sections["trader_investment_plan"] = chunk[
                        "trader_investment_plan"
                    ]
                    update_agent_status("Trader", "completed")
                    update_agent_status("Risky Analyst", "in_progress")
                    _mark_progress("trader_plan")

                # Risk Management Team - Handle Risk Debate State (proper scope)
                if "risk_debate_state" in chunk and chunk["risk_debate_state"]:
                    risk_state = chunk["risk_debate_state"]

                    # Update Risky Analyst status and report
                    if (
                        "current_risky_response" in risk_state
                        and risk_state["current_risky_response"]
                    ):
                        update_agent_status("Risky Analyst", "in_progress")
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        st.session_state.progress_messages.appendleft(
                            f"{timestamp} [Reasoning] Risky Analyst: {risk_state['current_risky_response'][:100]}..."
                        )
                        st.session_state.report_sections["final_trade_decision"] = (
                            f"### Risky Analyst Analysis\n{risk_state['current_risky_response']}"
                        )
                        # Event milestone: risk (risky) contribution
                        _mark_progress("risk_risky")

                    # Update Safe Analyst status and report
                    if (
                        "current_safe_response" in risk_state
                        and risk_state["current_safe_response"]
                    ):
                        update_agent_status("Safe Analyst", "in_progress")
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        st.session_state.progress_messages.appendleft(
                            f"{timestamp} [Reasoning] Safe Analyst: {risk_state['current_safe_response'][:100]}..."
                        )
                        st.session_state.report_sections["final_trade_decision"] = (
                            f"### Safe Analyst Analysis\n{risk_state['current_safe_response']}"
                        )
                        # Event milestone: risk (safe) contribution
                        _mark_progress("risk_safe")

                    # Update Neutral Analyst status and report
                    if (
                        "current_neutral_response" in risk_state
                        and risk_state["current_neutral_response"]
                    ):
                        update_agent_status("Neutral Analyst", "in_progress")
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        st.session_state.progress_messages.appendleft(
                            f"{timestamp} [Reasoning] Neutral Analyst: {risk_state['current_neutral_response'][:100]}..."
                        )
                        st.session_state.report_sections["final_trade_decision"] = (
                            f"### Neutral Analyst Analysis\n{risk_state['current_neutral_response']}"
                        )
                        # Event milestone: risk (neutral) contribution
                        _mark_progress("risk_neutral")

                    # Update Portfolio Manager status and final decision
                    if "judge_decision" in risk_state and risk_state["judge_decision"]:
                        update_agent_status("Portfolio Manager", "in_progress")
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        st.session_state.progress_messages.appendleft(
                            f"{timestamp} [Reasoning] Portfolio Manager: {risk_state['judge_decision'][:100]}..."
                        )
                        st.session_state.report_sections["final_trade_decision"] = (
                            f"### Portfolio Manager Decision\n{risk_state['judge_decision']}"
                        )
                        # Mark risk analysts as completed
                        update_agent_status("Risky Analyst", "completed")
                        update_agent_status("Safe Analyst", "completed")
                        update_agent_status("Neutral Analyst", "completed")
                        update_agent_status("Portfolio Manager", "completed")
                        # Event milestone: portfolio judge decision
                        _mark_progress("portfolio_judge")

                # Update UI displays inside the streaming loop
                # Display combined messages and tool calls
                all_messages = []
                for msg in list(st.session_state.progress_messages)[:10]:
                    all_messages.append(f"- {msg}")
                for tool in list(st.session_state.tool_calls)[:5]:
                    all_messages.append(f"- {tool}")

                messages_container.markdown("\n".join(all_messages[:15]))

                # Update partial report during risk/research updates
                if "report_container" in st.session_state:
                    st.session_state.report_container.markdown(
                        build_partial_report_md(st.session_state.report_sections)
                    )

            # Update partial report at the end of the loop iteration as well
            if "report_container" in st.session_state:
                st.session_state.report_container.markdown(
                    build_partial_report_md(st.session_state.report_sections)
                )

            # Render persistent Live Analysis Feed (History) during streaming
            render_live_feed_history()

            # Update progress (reflect in-progress work for better UX)
            completed_count = sum(
                1 for s in st.session_state.agent_status.values() if s == "completed"
            )
            in_progress_count = sum(
                1 for s in st.session_state.agent_status.values() if s == "in_progress"
            )
            total_agents = len(st.session_state.agent_status)
            if total_agents > 0:
                progress_val = (completed_count + 0.3 * in_progress_count) / total_agents
                progress_val = min(progress_val, 0.99)
            else:
                progress_val = 0
            # Prevent regression: never drop below last_progress
            progress_val = max(progress_val, st.session_state.get("last_progress", 0.0))
            progress_bar.progress(progress_val)
            st.session_state["last_progress"] = progress_val

            # Update status text
            in_progress_agents = [
                agent
                for agent, status in st.session_state.agent_status.items()
                if status == "in_progress"
            ]
            if in_progress_agents:
                status_text.text(f"🔄 {in_progress_agents[0]} is working...")
            else:
                status_text.text("🔄 Processing...")

            trace.append(chunk)
            time.sleep(0.1)  # Small delay for UI responsiveness

            # Debug: Log when streaming loop exits
            if debug_mode:
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.progress_messages.appendleft(
                    f"{timestamp} [DEBUG] Streaming loop completed normally"
                )

        except Exception as streaming_error:
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.progress_messages.appendleft(
                f"{timestamp} [ERROR] Streaming failed: {str(streaming_error)}"
            )
            if debug_mode:
                st.exception(streaming_error)
            # Mark current running agents as error
            for agent, status in st.session_state.agent_status.items():
                if status == "in_progress":
                    update_agent_status(agent, "error")
            raise streaming_error

        # Get final state and complete analysis
        if trace:
            final_state = trace[-1]

            # Process final decision - extract from text
            decision = None
            if (
                "final_trade_decision" in final_state
                and final_state["final_trade_decision"]
            ):
                decision_text = str(final_state["final_trade_decision"]).upper()
                if "BUY" in decision_text:
                    decision = "BUY"
                elif "SELL" in decision_text:
                    decision = "SELL"
                elif "HOLD" in decision_text:
                    decision = "HOLD"
                else:
                    decision = "ANALYZE"

            # Update all agent statuses to completed
            for agent in st.session_state.agent_status:
                update_agent_status(agent, "completed")

            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.progress_messages.appendleft(
                f"{timestamp} [Analysis] Completed analysis for {date_str}"
            )

            # Update final report sections
            for section in st.session_state.report_sections.keys():
                if section in final_state:
                    st.session_state.report_sections[section] = final_state[section]

            # Store results with decision
            st.session_state.analysis_results = {
                "symbol": stock_symbol,
                "date": date_str,
                "result": final_state,
                "decision": decision,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            st.session_state.analysis_running = False
            # Clear run configuration tooltip after completion
            if "current_run_config_tip" in st.session_state:
                del st.session_state["current_run_config_tip"]
            # Event milestone: finalized
            _mark_progress("finalized")
            # Ensure progress is full and reset last_progress for next run
            try:
                progress_bar.progress(1.0)
            except Exception:
                pass
            # Clear tracker state for next run
            st.session_state.pop("last_progress", None)
            st.session_state.pop("progress_bar", None)
            st.session_state.pop("progress_events_done", None)
            st.session_state.pop("progress_events_list", None)
            st.session_state.pop("progress_total_events", None)
            status_text.text("✅ Analysis complete!")
            st.success("🎉 Real analysis completed successfully!")
            # Lifecycle log: AnalysisComplete
            if st.session_state.get("ui_debug_mode"):
                ts = datetime.now().strftime("%H:%M:%S")
                st.session_state.tool_calls.appendleft(
                    f"{ts} [Tool] AnalysisComplete: {stock_symbol} @ {date_str}"
                )
                if "tool_calls_sidebar_placeholder" in st.session_state:
                    with st.session_state.tool_calls_sidebar_placeholder.container():
                        render_tool_calls_sidebar(expanded=False)
            st.rerun()

    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        st.session_state.analysis_running = False
        # Clear run configuration tooltip on failure as well
        if "current_run_config_tip" in st.session_state:
            del st.session_state["current_run_config_tip"]
        # Reset progress floor for next run
        st.session_state.pop("last_progress", None)
        st.session_state.pop("progress_bar", None)
        st.session_state.pop("progress_events_done", None)
        st.session_state.pop("progress_events_list", None)
        st.session_state.pop("progress_total_events", None)
        st.session_state.last_error = str(e)
        if debug_mode:
            st.exception(e)
        # Lifecycle log: AnalysisFailed
        if st.session_state.get("ui_debug_mode"):
            ts = datetime.now().strftime("%H:%M:%S")
            st.session_state.tool_calls.appendleft(
                f"{ts} [Tool] AnalysisFailed: {stock_symbol}"
            )
            if "tool_calls_sidebar_placeholder" in st.session_state:
                with st.session_state.tool_calls_sidebar_placeholder.container():
                    render_tool_calls_sidebar(expanded=False)
        st.rerun()


# Initialize session state
init_session_state()

# Render header
if COMPONENTS_AVAILABLE:
    render_header()
else:
    fallback_render_header()

# Sidebar configuration
with st.sidebar:
    if COMPONENTS_AVAILABLE:
        sidebar_config = render_sidebar_configuration()
    else:
        sidebar_config = fallback_render_sidebar()

# Create main layout container with two columns
main_content_col, agent_status_col = st.columns([7, 3])

# Main content area
with main_content_col:
    st.header("🎯 Trading Analysis Dashboard")

    # Analysis parameters
    if COMPONENTS_AVAILABLE:
        analysis_params = render_analysis_parameters()
        start_analysis = render_analysis_controls(
            analysis_params,
            sidebar_config.get("llm_config", {}),
            sidebar_config.get("selected_analysts", []),
        )
    else:
        analysis_params = fallback_render_analysis_params()
        start_analysis = fallback_render_analysis_controls()

    # Ensure the Tool Calls debug panel appears in the sidebar immediately when Debug Mode is ON
    if analysis_params.get("debug_mode", False):
        # Persist UI debug flag for hooks outside this scope (e.g., preflight/profile fetch)
        st.session_state.ui_debug_mode = True
        if "tool_calls_sidebar_placeholder" not in st.session_state:
            st.session_state.tool_calls_sidebar_placeholder = st.sidebar.empty()
        with st.session_state.tool_calls_sidebar_placeholder.container():
            render_tool_calls_sidebar(expanded=False)
    else:
        st.session_state.ui_debug_mode = False

    # Handle start analysis
    if start_analysis and not st.session_state.get("preflight_pending", False):
        # Validate inputs
        if not analysis_params["stock_symbol"]:
            st.error("Please enter a stock symbol")
            st.stop()

        # Check API keys
        openai_key = os.getenv("OPENAI_API_KEY", "")
        finnhub_key = os.getenv("FINNHUB_API_KEY", "")
        backend_url = sidebar_config.get("llm_config", {}).get("backend_url", "")
        if not openai_key and not backend_url:
            st.error("Please provide OpenAI API key or backend URL")
        elif not analysis_params["stock_symbol"]:
            st.error("Please enter a stock symbol")
        else:
            # Preflight: resolve ticker to company profile
            symbol = analysis_params["stock_symbol"].strip().upper()
            profile = fetch_company_profile(symbol)
            st.session_state.preflight_profile = profile
            st.session_state.pending_symbol = symbol
            st.session_state.preflight_pending = True
            # Debug-only: log that run is initiated (preflight about to rerun)
            if st.session_state.get("ui_debug_mode"):
                ts = datetime.now().strftime("%H:%M:%S")
                st.session_state.tool_calls.appendleft(
                    f"{ts} [Tool] RunInitiated: {symbol}"
                )
                if "tool_calls_sidebar_placeholder" in st.session_state:
                    with st.session_state.tool_calls_sidebar_placeholder.container():
                        render_tool_calls_sidebar(expanded=False)
            st.rerun()

    # If preflight pending, show confirmation card and gate run start
    # Only show when analysis is not running to avoid a greyed-out card lingering
    if st.session_state.get("preflight_pending", False) and not st.session_state.get("analysis_running", False):
        preflight_placeholder = st.empty()
        with preflight_placeholder.container(border=True):
            prof = st.session_state.get("preflight_profile") or {}
            symbol = st.session_state.get("pending_symbol") or analysis_params.get("stock_symbol", "").upper()
            st.markdown("#### 🔎 Ticker Resolution")
            if prof:
                st.markdown(
                    f"**Ticker:** {symbol}  ")
                st.markdown(
                    f"**Company:** {prof.get('name', 'N/A')}  ")
                st.markdown(
                    f"**Exchange:** {prof.get('exchange', 'N/A')} · **Country:** {prof.get('country', 'N/A')}  ")
                st.markdown(
                    f"**Industry:** {prof.get('finnhubIndustry', 'N/A')}  ")
                if prof.get("weburl"):
                    st.markdown(f"**Website:** {prof.get('weburl')}")
            else:
                st.warning("Could not resolve company profile automatically. You can still proceed or change the symbol.")

            col_ok, col_change = st.columns([1, 1])
            with col_ok:
                if st.button("✅ Looks right — Proceed", use_container_width=True):
                    # Lock in the resolved profile (possibly empty if not found)
                    st.session_state.resolved_profile = prof if prof else {"ticker": symbol}
                    # Reset UI state to avoid stale content
                    st.session_state.progress_messages = deque(maxlen=50)
                    st.session_state.tool_calls = deque(maxlen=100)
                    st.session_state.analysis_results = None
                    st.session_state.last_error = None
                    st.session_state.report_sections = {
                        "market_report": None,
                        "sentiment_report": None,
                        "news_report": None,
                        "fundamentals_report": None,
                        "investment_plan": None,
                        "trader_investment_plan": None,
                        "final_trade_decision": None,
                    }
                    for agent in [
                        "Market Analyst",
                        "Social Analyst",
                        "News Analyst",
                        "Fundamentals Analyst",
                    ]:
                        update_agent_status(agent, "pending")
                    # Proceed to start analysis and clear preflight UI
                    st.session_state.preflight_pending = False
                    st.session_state.analysis_running = True
                    preflight_placeholder.empty()
                    st.rerun()
            with col_change:
                if st.button("✏️ Change Symbol", type="secondary", use_container_width=True):
                    st.session_state.preflight_pending = False
                    st.session_state.preflight_profile = None
                    st.session_state.pending_symbol = None
                    st.session_state.resolved_profile = None
                    st.rerun()

    st.divider()

    # Show analysis progress if running
    if st.session_state.analysis_running:
        try:
            run_real_analysis(
                analysis_params["stock_symbol"],
                analysis_params["analysis_date"],
                analysis_params,
                sidebar_config.get("llm_config", {}),
                sidebar_config.get("selected_analysts", []),
                analysis_params.get("debug_mode", False),
            )
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.session_state.analysis_running = False
            st.session_state.last_error = str(e)
            st.rerun()
    
    # Results section - moved inside main content column
    if st.session_state.analysis_results and not st.session_state.analysis_running:
        # Pre-generate export content
        markdown_content = generate_markdown_report(st.session_state.analysis_results)
        markdown_filename = f"trading_analysis_{st.session_state.analysis_results.get('symbol', 'report')}_{st.session_state.analysis_results.get('date', 'unknown')}.md"

        jsonl_content = generate_jsonl_log(
            st.session_state.analysis_results,
            st.session_state.progress_messages,
            st.session_state.tool_calls,
        )
        jsonl_filename = f"trading_log_{st.session_state.analysis_results.get('symbol', 'log')}_{st.session_state.analysis_results.get('date', 'unknown')}.jsonl"

        decision_summary = get_decision_summary(st.session_state.analysis_results)

        # Header with evenly spaced export buttons
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1], gap="medium")

        with col1:
            st.markdown(
                '<h1 style="font-size: 1.5rem; font-weight: 700; color: #22c55e; margin-top: 0; margin-bottom: 0; white-space: nowrap; line-height: 2.5rem;">📊 Analysis Results</h1>',
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                '<div style="display: flex; align-items: center; height: 2.5rem;">',
                unsafe_allow_html=True,
            )
            st.download_button(
                label="📄 Full Report",
                data=markdown_content,
                file_name=markdown_filename,
                mime="text/markdown",
                use_container_width=True,
                type="secondary",
                help="Download complete analysis in Markdown format",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(
                '<div style="display: flex; align-items: center; height: 2.5rem;">',
                unsafe_allow_html=True,
            )
            st.download_button(
                label="📋 Execution Log",
                data=jsonl_content,
                file_name=jsonl_filename,
                mime="application/jsonl",
                use_container_width=True,
                type="secondary",
                help="Download detailed execution log in JSONL format",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col4:
            st.markdown(
                '<div style="display: flex; align-items: center; height: 2.5rem;">',
                unsafe_allow_html=True,
            )
            if st.button(
                "🎯 Quick Summary",
                use_container_width=True,
                type="secondary",
                help="Toggle quick decision summary display",
                key="quick_summary_toggle"
            ):
                st.session_state.show_quick_summary = not st.session_state.get(
                    "show_quick_summary", False
                )
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # Show summary only when explicitly requested (not by default)
        if st.session_state.get("show_quick_summary", False):
            st.markdown("**Decision Summary:**")
            st.code(decision_summary, language=None)

        if COMPONENTS_AVAILABLE:
            render_analysis_report(
                st.session_state.analysis_results, analysis_params.get("debug_mode", False)
            )
        else:
            # Fallback results display
            results = st.session_state.analysis_results
            st.subheader(f"Results for {results['symbol']} - {results['date']}")

            result_data = results.get("result", {})

            if result_data.get("market_report"):
                st.subheader("📈 Market Analysis")
                st.markdown(result_data["market_report"])

            if result_data.get("news_report"):
                st.subheader("📰 News Analysis")
                st.markdown(result_data["news_report"])

            if result_data.get("fundamentals_report"):
                st.subheader("💰 Fundamentals")
                st.markdown(result_data["fundamentals_report"])

            if result_data.get("trader_investment_plan"):
                st.subheader("🎯 Investment Decision")
                st.markdown(result_data["trader_investment_plan"])

        # JavaScript to directly style export buttons
        st.markdown(
            """
        <script>
        function styleExportButtons() {
            const buttons = document.querySelectorAll('button[kind="secondary"]');
            buttons.forEach(btn => {
                const text = btn.textContent || btn.innerText;
                if (text.includes('📄')) {
                    btn.style.background = 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)';
                    btn.style.color = 'white';
                    btn.style.border = '1px solid #3b82f6';
                } else if (text.includes('📋')) {
                    btn.style.background = 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)';
                    btn.style.color = 'white';
                    btn.style.border = '1px solid #8b5cf6';
                } else if (text.includes('🎯')) {
                    btn.style.background = 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)';
                    btn.style.color = 'white';
                    btn.style.border = '1px solid #06b6d4';
                }
            });
        }

        // Run immediately and on DOM changes
        styleExportButtons();
        setTimeout(styleExportButtons, 100);
        setTimeout(styleExportButtons, 500);

        // Watch for DOM changes
        const observer = new MutationObserver(styleExportButtons);
        observer.observe(document.body, { childList: true, subtree: true });
        </script>
        """,
            unsafe_allow_html=True,
        )

# Agent status panel
with agent_status_col:
    st.markdown("### 🤖 Agent Status")
    
    # Agent status cards
    teams = {
        "📈 Analyst Team": [
            "Market Analyst",
            "Social Analyst",
            "News Analyst",
            "Fundamentals Analyst",
        ],
        "🔍 Research Team": ["Bull Researcher", "Bear Researcher", "Research Manager"],
        "💰 Trading Team": ["Trader"],
        "⚠️ Risk Management": ["Risky Analyst", "Neutral Analyst", "Safe Analyst"],
        "📊 Portfolio Management": ["Portfolio Manager"],
    }

    # Store placeholders for dynamic updates
    if "agent_placeholders" not in st.session_state:
        st.session_state.agent_placeholders = {}

    for team_name, agents in teams.items():
        completed = sum(
            1 for agent in agents if st.session_state.agent_status[agent] == "completed"
        )
        total = len(agents)

        with st.expander(f"{team_name} ({completed}/{total})", expanded=True):
            for agent in agents:
                # Create placeholder for each agent button
                placeholder = st.empty()
                st.session_state.agent_placeholders[agent] = placeholder

                # Initial render
                status = st.session_state.agent_status[agent]
                render_agent_button(placeholder, agent, status)

    # Current Report section (moved to bottom of side pane for better UX)
    st.markdown("### 📊 Current Report")
    report_container = st.empty()
    # Store in session state for access from analysis function
    st.session_state.report_container = report_container

# Error display
if st.session_state.get("last_error") and not st.session_state.analysis_running:
    st.error(f"An error occurred: {st.session_state.last_error}")

st.markdown("</div>", unsafe_allow_html=True)
