"""
Agentopia UI Components for Web Scraper Agent
Standardized UI components following Agentopia design patterns
"""

import streamlit as st


def display_sidebar_header():
    """Display the standardized Agentopia sidebar header with logo"""
    import base64
    import os

    # The logo path is relative to this script's location
    logo_path = "images/logo.svg"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abs_logo_path = os.path.join(script_dir, logo_path)

    try:
        with open(abs_logo_path, "rb") as f:
            logo_bytes = f.read()
        logo_b64 = base64.b64encode(logo_bytes).decode("utf-8")

        st.sidebar.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: center;
                        flex-direction: column; padding: 1rem 0;">
                <div style="margin-bottom: 10px;">
                    <img src="data:image/svg+xml;base64,{logo_b64}" width="60">
                </div>
                <h2 style="color: #2E86AB; margin: 0;">AI Agentopia</h2>
                <p style="color: #666; margin: 0; font-size: 0.9rem;">AI Agent Ecosystem</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        # Fallback to emoji if logo file is not found
        st.sidebar.markdown(
            """
            <div style="text-align: center; padding: 1rem 0;">
                <div style="margin-bottom: 0.5rem; font-size: 2.5rem;">
                    🤖
                </div>
                <h2 style="color: #2E86AB; margin: 0;">AI Agentopia</h2>
                <p style="color: #666; margin: 0; font-size: 0.9rem;">AI Agent Ecosystem</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def display_agent_title_panel():
    """Display the agent-specific title panel with emoji and description"""
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0 1rem 0;">
            <h1 style="color: #2E86AB; margin-bottom: 0.5rem;">
                🕵️‍♂️ Web Scraper Agent
            </h1>
            <p style="color: #666; font-size: 1.1rem; margin: 0;">
                Intelligent AI-powered web scraping with natural language prompts
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_sidebar_footer():
    """Display the standardized Agentopia sidebar footer"""
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="text-align: center; padding: 1rem 0; color: #666; font-size: 0.8rem;">
            <p>🔒 Privacy-First AI Agents</p>
            <p>Built with ❤️ by Agentopia</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_info_box(title: str, content: str, box_type: str = "info"):
    """
    Display an information box with consistent styling

    Args:
        title: Box title
        content: Box content
        box_type: Type of box (info, success, warning, error)
    """
    colors = {
        "info": {"bg": "#E3F2FD", "border": "#2196F3", "text": "#1565C0"},
        "success": {"bg": "#E8F5E8", "border": "#4CAF50", "text": "#2E7D32"},
        "warning": {"bg": "#FFF3E0", "border": "#FF9800", "text": "#F57C00"},
        "error": {"bg": "#FFEBEE", "border": "#F44336", "text": "#C62828"},
    }

    color = colors.get(box_type, colors["info"])

    st.markdown(
        f"""
        <div style="
            background-color: {color['bg']};
            border-left: 4px solid {color['border']};
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 4px 4px 0;
        ">
            <h4 style="color: {color['text']}; margin: 0 0 0.5rem 0;">{title}</h4>
            <p style="color: {color['text']}; margin: 0;">{content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_feature_card(icon: str, title: str, description: str):
    """Display a feature card with icon, title, and description"""
    st.markdown(
        f"""
        <div style="
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <h3 style="color: #2E86AB; margin: 0.5rem 0;">{title}</h3>
                <p style="color: #666; margin: 0;">{description}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_status_indicator(status: str, message: str):
    """Display a status indicator with appropriate styling"""
    status_config = {
        "success": {"color": "#4CAF50", "icon": "✅"},
        "error": {"color": "#F44336", "icon": "❌"},
        "warning": {"color": "#FF9800", "icon": "⚠️"},
        "info": {"color": "#2196F3", "icon": "ℹ️"},
        "loading": {"color": "#9C27B0", "icon": "⏳"},
    }

    config = status_config.get(status, status_config["info"])

    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: center;
            padding: 0.5rem;
            margin: 0.5rem 0;
            color: {config['color']};
            font-weight: 500;
        ">
            <span style="margin-right: 0.5rem; font-size: 1.2rem;">{config['icon']}</span>
            <span>{message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
