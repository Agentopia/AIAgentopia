"""
Report Components
Modular components for rendering the final analysis report.
"""

import streamlit as st


def _first_non_empty(*values):
    """Return the first value that is not falsy (None/""/{}), else None."""
    for v in values:
        if v:
            return v
    return None


def normalize_final_state_keys(final_state: dict) -> dict:
    """Normalize backend result keys to the canonical schema expected by the UI.

    This function is non-destructive: it only fills canonical fields when missing,
    using values from known alias keys. It returns the same dict instance for
    convenience.

    Canonical keys expected by the UI tabs:
      - investment_debate_state: {bull_history, bear_history, judge_decision}
      - risk_debate_state: {risky_history, neutral_history, safe_history, judge_decision}
      - trader_investment_plan (str)
      - final_trade_decision (str)
    """
    if not isinstance(final_state, dict):
        return final_state

    # --- Research/Investment debate normalization ---
    inv_state = final_state.get("investment_debate_state")
    research_alias = _first_non_empty(
        inv_state,
        final_state.get("research_debate_state"),
        final_state.get("investment_debate"),
        final_state.get("debate_state"),
    )
    if isinstance(research_alias, dict):
        canonical = dict(inv_state) if isinstance(inv_state, dict) else {}
        canonical.setdefault(
            "bull_history",
            _first_non_empty(research_alias.get("bull_history"), research_alias.get("bull")),
        )
        canonical.setdefault(
            "bear_history",
            _first_non_empty(research_alias.get("bear_history"), research_alias.get("bear")),
        )
        canonical.setdefault(
            "judge_decision",
            _first_non_empty(
                research_alias.get("judge_decision"),
                research_alias.get("decision"),
            ),
        )
        final_state["investment_debate_state"] = canonical

    # --- Risk debate normalization ---
    risk_state = final_state.get("risk_debate_state")
    risk_alias = _first_non_empty(
        risk_state,
        final_state.get("risk_debate"),
        final_state.get("risk_assessment_state"),
    )
    if isinstance(risk_alias, dict):
        canonical_risk = dict(risk_state) if isinstance(risk_state, dict) else {}
        canonical_risk.setdefault(
            "risky_history",
            _first_non_empty(risk_alias.get("risky_history"), risk_alias.get("aggressive")),
        )
        canonical_risk.setdefault("neutral_history", risk_alias.get("neutral_history"))
        canonical_risk.setdefault(
            "safe_history",
            _first_non_empty(risk_alias.get("safe_history"), risk_alias.get("conservative")),
        )
        canonical_risk.setdefault(
            "judge_decision",
            _first_non_empty(risk_alias.get("judge_decision"), risk_alias.get("decision")),
        )
        final_state["risk_debate_state"] = canonical_risk

    # --- Trader plan normalization ---
    if not final_state.get("trader_investment_plan"):
        final_state["trader_investment_plan"] = _first_non_empty(
            final_state.get("trader_investment_plan"),
            final_state.get("investment_plan"),
            final_state.get("trader_plan"),
        )

    # --- Final decision normalization ---
    if not final_state.get("final_trade_decision"):
        final_state["final_trade_decision"] = _first_non_empty(
            final_state.get("final_trade_decision"),
            final_state.get("final_decision"),
            final_state.get("portfolio_decision"),
        )

    return final_state


def render_analysis_report(results, debug_mode):
    """Render the full analysis report with tabs for each section."""

    # Results Header with Metrics

    # Force CSS styles with JavaScript fallback
    st.markdown("""
    <style>
    /* === ANALYSIS RESULTS VISUAL HIERARCHY === */
    
    /* Tab Navigation - 1.0rem, semi-bold with higher specificity */
    div[data-testid="stTabs"] div[data-baseweb="tab-list"] button,
    .stTabs [data-baseweb="tab-list"] button,
    [data-baseweb="tab-list"] button {
        font-size: 1.0rem !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Metric containers - bright yellow values, white labels with higher specificity */
    div[data-testid="metric-container"] div[data-testid="metric-value"],
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #fbbf24 !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="metric-label"],
    [data-testid="metric-container"] [data-testid="metric-label"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }
    </style>
    
    <script>
    // JavaScript to force styles when CSS fails
    function forceAnalysisResultsStyles() {
        // Force tab button styles - bold text, red when selected, white when not
        const tabButtons = document.querySelectorAll('[data-baseweb="tab-list"] button');
        tabButtons.forEach(btn => {
            btn.style.setProperty('font-size', '1.0rem', 'important');
            btn.style.setProperty('font-weight', '700', 'important'); // Bold
            
            // Check if tab is selected (has aria-selected="true" or active class)
            const isSelected = btn.getAttribute('aria-selected') === 'true' || 
                             btn.classList.contains('active') ||
                             btn.hasAttribute('data-selected');
            
            if (isSelected) {
                btn.style.setProperty('color', '#ef4444', 'important'); // Red when selected
            } else {
                btn.style.setProperty('color', '#ffffff', 'important'); // White when not selected
            }
        });
        
        // Force metric value styles - target all possible selectors
        const metricValues = document.querySelectorAll('[data-testid="metric-value"], .metric-value, [class*="metric"] [class*="value"]');
        metricValues.forEach(val => {
            val.style.setProperty('font-size', '0.875rem', 'important');
            val.style.setProperty('font-weight', '600', 'important');
            val.style.setProperty('color', '#fbbf24', 'important');
        });
        
        // Also target any large text in metric containers
        const metricContainers = document.querySelectorAll('[data-testid="metric-container"]');
        metricContainers.forEach(container => {
            const allElements = container.querySelectorAll('*');
            allElements.forEach(el => {
                if (el.textContent && (el.textContent.includes('CRCL') || el.textContent.includes('2025-') || el.textContent.includes('BUY') || el.textContent.includes('SELL') || el.textContent.includes(':'))) {
                    el.style.setProperty('font-size', '0.875rem', 'important');
                    el.style.setProperty('font-weight', '600', 'important');
                    el.style.setProperty('color', '#fbbf24', 'important');
                }
            });
        });
        
        // Force metric label styles
        const metricLabels = document.querySelectorAll('[data-testid="metric-label"]');
        metricLabels.forEach(label => {
            label.style.setProperty('font-size', '1.1rem', 'important');
            label.style.setProperty('font-weight', '600', 'important');
            label.style.setProperty('color', '#ffffff', 'important');
        });
        
        // Force all report body text to be white
        const reportContainer = document.querySelector('[data-testid="stTabs"]');
        if (reportContainer) {
            const allTextElements = reportContainer.querySelectorAll('*');
            allTextElements.forEach(el => {
                // Skip elements that should keep their specific colors (like success/info boxes)
                if (!el.closest('[data-testid="stAlert"]') && 
                    !el.closest('[data-testid="stSuccess"]') && 
                    !el.closest('[data-testid="stInfo"]') &&
                    !el.closest('[data-testid="metric-value"]')) {
                    
                    // Force white color for text content
                    if (el.textContent && el.textContent.trim()) {
                        el.style.setProperty('color', '#ffffff', 'important');
                    }
                }
            });
        }
    }
    
    // Run immediately and repeatedly
    setTimeout(forceAnalysisResultsStyles, 100);
    setTimeout(forceAnalysisResultsStyles, 500);
    setTimeout(forceAnalysisResultsStyles, 1000);
    setInterval(forceAnalysisResultsStyles, 2000);
    </script>
    """, unsafe_allow_html=True)
    
    # Additional CSS for tab content styling
    st.markdown("""
    <style>
    /* Tab styling */
    [data-baseweb="tab-list"] button {
        font-size: 1.0rem !important;
        font-weight: 700 !important; /* Bold */
        background-color: transparent !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        margin: 0 0.25rem !important;
        border-radius: 0.5rem !important;
        transition: all 0.2s ease !important;
        color: #ffffff !important; /* White by default */
    }
    
    [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: rgba(239, 68, 68, 0.1) !important;
        border-bottom: 2px solid #ef4444 !important;
        color: #ef4444 !important; /* Red when selected */
    }
    
    /* Force all text in report tabs to be white */
    [data-testid="stTabs"] * {
        color: #ffffff !important;
    }
    
    /* Preserve specific component colors */
    [data-testid="stAlert"] *, 
    [data-testid="stSuccess"] *, 
    [data-testid="stInfo"] *,
    [data-testid="stWarning"] *,
    [data-testid="stError"] * {
        color: inherit !important;
    }
    
    /* Section headers within tabs - moderate size */
    .stTabs h2 {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.75rem !important;
        color: #ffffff !important;
    }
    
    .stTabs h4 {
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
        color: #ffffff !important;
    }
    
    /* Body text in tabs */
    .stTabs p {
        font-size: 0.875rem !important;
        line-height: 1.5 !important;
        color: #ffffff !important;
    }
    
    /* Alert boxes */
    .stAlert {
        font-size: 0.875rem !important;
    }
    
    /* Lists */
    .stTabs li {
        font-size: 0.875rem !important;
        line-height: 1.4 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Symbol", results["symbol"])
    with col_m2:
        st.metric("Date", results["date"])
    with col_m3:
        st.metric(
            "Completed",
            results["timestamp"].split()[1]
            if " " in results["timestamp"]
            else results["timestamp"],
        )
    with col_m4:
        # Extract decision from results for metric - handle missing decision key
        decision = results.get(
            "decision", results.get("final_trade_decision", "Analysis Complete")
        )
        if decision and isinstance(decision, str):
            decision_summary = (
                "BUY"
                if "BUY" in decision.upper()
                else "HOLD"
                if "HOLD" in decision.upper()
                else "SELL"
                if "SELL" in decision.upper()
                else "ANALYZE"
            )
        else:
            decision_summary = "ANALYZE"
        st.metric("Decision", decision_summary)

    # Add comprehensive CSS for consistent Analysis Results font sizing
    st.markdown("""
    <style>
    /* Consistent font sizing for Analysis Results section */
    .stTabs [data-baseweb="tab-list"] {
        font-size: 0.875rem !important;
    }
    
    /* Reduce subheader sizes */
    .stMarkdown h2 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Reduce h4 header sizes */
    .stMarkdown h4 {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
        margin-top: 1rem !important;
    }
    
    /* Consistent body text in report content */
    .stMarkdown p {
        font-size: 0.875rem !important;
        line-height: 1.5 !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* Reduce italic text size */
    .stMarkdown em {
        font-size: 0.8rem !important;
    }
    
    /* Success/info/warning boxes */
    .stAlert {
        font-size: 0.875rem !important;
    }
    
    /* Tab content */
    .stTabs [data-baseweb="tab-panel"] {
        font-size: 0.875rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Complete Team-Based Report Sections (100% CLI feature parity)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "🎯 Final Decision",
            "📊 I. Analyst Team", 
            "🔍 II. Research Team",
            "💰 III. Trading Team",
            "⚖️ IV. Risk Management",
            "📈 V. Portfolio Manager",
        ]
    )

    final_state = results.get("result", {})
    # Normalize keys to ensure tabs populate even if backend uses aliases
    final_state = normalize_final_state_keys(final_state)

    with tab1:
        st.subheader("🎯 Final Trading Decision & Summary")

        # Display final decision prominently
        if results["decision"]:
            st.success(f"**Final Recommendation:** {results['decision']}")

            # Show decision breakdown if available
            if isinstance(results["decision"], dict):
                with st.expander("📋 Decision Details"):
                    st.json(results["decision"])

        # Executive Summary
        st.markdown("### 📋 Executive Summary")

        # Quick overview of all team decisions
        summary_cols = st.columns(2)

        with summary_cols[0]:
            st.markdown("**🔍 Research Team Conclusion:**")
            if final_state.get("investment_debate_state", {}).get("judge_decision"):
                research_decision = (
                    final_state["investment_debate_state"]["judge_decision"][:200]
                    + "..."
                )
                st.info(research_decision)
            else:
                st.warning("Research decision pending")

        with summary_cols[1]:
            st.markdown("**📈 Portfolio Manager Decision:**")
            if final_state.get("risk_debate_state", {}).get("judge_decision"):
                portfolio_decision = (
                    final_state["risk_debate_state"]["judge_decision"][:200] + "..."
                )
                st.success(portfolio_decision)
            else:
                st.warning("Portfolio decision pending")

    with tab2:
        st.subheader("📊 I. Analyst Team Reports")
        st.markdown("*Detailed analysis from our core analyst team*")

        # Market Analyst Report
        if final_state.get("market_report"):
            with st.container():
                st.markdown("#### 📈 Market Analyst Report")
                st.markdown(final_state["market_report"])
                st.divider()

        # Social Analyst Report
        if final_state.get("sentiment_report"):
            with st.container():
                st.markdown("#### 👥 Social Analyst Report")
                st.markdown(final_state["sentiment_report"])
                st.divider()

        # News Analyst Report
        if final_state.get("news_report"):
            with st.container():
                st.markdown("#### 📰 News Analyst Report")
                st.markdown(final_state["news_report"])
                st.divider()

        # Fundamentals Analyst Report
        if final_state.get("fundamentals_report"):
            with st.container():
                st.markdown("#### 💼 Fundamentals Analyst Report")
                st.markdown(final_state["fundamentals_report"])

        # Show message if no reports available
        if not any(
            [
                final_state.get("market_report"),
                final_state.get("sentiment_report"),
                final_state.get("news_report"),
                final_state.get("fundamentals_report"),
            ]
        ):
            st.info("📊 Analyst team reports are still being generated...")

    with tab3:
        st.subheader("🔍 II. Research Team Decision")
        st.markdown("*Investment research debate and conclusions*")

    if final_state.get("investment_debate_state"):
        debate_state = final_state["investment_debate_state"]

        # Bull Researcher Analysis
        if debate_state.get("bull_history"):
            with st.container():
                st.markdown("#### 🐂 Bull Researcher Analysis")
                st.markdown(debate_state["bull_history"])
                st.divider()

        # Bear Researcher Analysis
        if debate_state.get("bear_history"):
            with st.container():
                st.markdown("#### 🐻 Bear Researcher Analysis")
                st.markdown(debate_state["bear_history"])
                st.divider()

        # Research Manager Decision
        if debate_state.get("judge_decision"):
            with st.container():
                st.markdown("#### 🎯 Research Manager Decision")
                st.success(debate_state["judge_decision"])
    else:
        st.info("🔍 Research team debate is still in progress...")

    with tab4:
        st.subheader("💰 III. Trading Team Plan")
        st.markdown("*Strategic trading recommendations and execution plan*")

    if final_state.get("trader_investment_plan"):
        with st.container():
            st.markdown("#### 💰 Trader Investment Plan")
            st.markdown(final_state["trader_investment_plan"])
    else:
        st.info("💰 Trading team plan is still being developed...")

    with tab5:
        st.subheader("⚖️ IV. Risk Management Team Decision")
        st.markdown("*Comprehensive risk assessment from multiple perspectives*")

    if final_state.get("risk_debate_state"):
        risk_state = final_state["risk_debate_state"]

        # Aggressive (Risky) Analyst Analysis
        if risk_state.get("risky_history"):
            with st.container():
                st.markdown("#### ⚡ Aggressive Analyst Analysis")
                st.markdown(risk_state["risky_history"])
                st.divider()

        # Conservative (Safe) Analyst Analysis
        if risk_state.get("safe_history"):
            with st.container():
                st.markdown("#### 🛡️ Conservative Analyst Analysis")
                st.markdown(risk_state["safe_history"])
                st.divider()

        # Neutral Analyst Analysis
        if risk_state.get("neutral_history"):
            with st.container():
                st.markdown("#### ⚖️ Neutral Analyst Analysis")
                st.markdown(risk_state["neutral_history"])
    else:
        st.info("⚖️ Risk management team assessment is still in progress...")

    with tab6:
        st.subheader("📈 V. Portfolio Manager Final Decision")
        st.markdown(
            "*Executive summary and final trading recommendation and investment decision*"
        )

        if final_state.get("risk_debate_state", {}).get("judge_decision"):
            with st.container():
                st.success(final_state["risk_debate_state"]["judge_decision"])

                # Show final trade decision if available
                if final_state.get("final_trade_decision"):
                    st.markdown("#### 🎯 Final Trade Decision")
                    st.info(final_state["final_trade_decision"])
        else:
            st.info("📈 Portfolio manager decision is still being finalized...")

    # Detailed Analysis (if debug mode)
    if debug_mode and results["result"]:
        st.divider()
        st.subheader("🔍 Complete Technical Analysis (Debug Mode)")
        with st.expander("View Full Raw Analysis Results"):
            if isinstance(results["result"], dict):
                st.json(results["result"])
            else:
                st.text(str(results["result"]))

    st.markdown("</div>", unsafe_allow_html=True)


def build_partial_report_md(sections: dict) -> str:
    """Build a concise markdown summary of currently available report sections.

    This is designed for incremental updates during streaming to show a
    "report-so-far" in the main UI. It lists available sections and includes
    short previews where useful.
    """

    if not isinstance(sections, dict):
        return "_No report sections available yet._"

    lines = ["#### 📊 Report So Far", ""]

    def short(text: str, n: int = 200) -> str:
        if not text:
            return ""
        text = str(text).strip()
        return text if len(text) <= n else text[: n - 3] + "..."

    # Define section order, titles and icons
    ordered = [
        ("market_report", "📈 Market Analyst"),
        ("sentiment_report", "👥 Social Analyst"),
        ("news_report", "📰 News Analyst"),
        ("fundamentals_report", "💼 Fundamentals Analyst"),
        ("investment_plan", "🔍 Research Team"),
        ("trader_investment_plan", "💰 Trading Team Plan"),
        ("final_trade_decision", "📈 Portfolio Decision"),
    ]

    ready = 0
    total = len(ordered)
    for key, title in ordered:
        if sections.get(key):
            lines.append(f"- ✅ {title}: available")
            ready += 1
        else:
            lines.append(f"- ◻️ {title}: pending")

    lines.insert(1, f"_Sections ready: **{ready}/{total}**_")

    # Provide a small preview of the latest available section for context
    preview = None
    for key in [
        "final_trade_decision",
        "trader_investment_plan",
        "investment_plan",
        "fundamentals_report",
        "news_report",
        "sentiment_report",
        "market_report",
    ]:
        if sections.get(key):
            preview = sections.get(key)
            break

    lines.append("")
    if preview:
        lines.append("**Latest update:**")
        lines.append("")
        lines.append(short(preview, 280))
    else:
        lines.append("_Waiting for first results..._")

    return "\n".join(lines)
