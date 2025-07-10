"""
Reusable Streamlit UI components for the Data Analyzer Bot.

This module provides standardized functions to display common UI elements like
headers, footers, and titles, ensuring a consistent look and feel across the application.
"""

import streamlit as st
import base64
import os


def display_sidebar_header():
    """Displays a standardized header in the sidebar for Agentopia."""
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
            <div style="display: flex; align-items: center; justify-content: left; margin-bottom: 20px;">
                <img src="data:image/svg+xml;base64,{logo_b64}" width="40">
                <h1 style="margin-left: 10px; color: #FFFFFF; font-size: 22px; font-weight: bold;">AI Agentopia</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.sidebar.error("Agentopia logo not found.")
        st.sidebar.header("AI Agentopia")


def display_agent_title(icon="🤖", agent_name="Data Analyzer Bot"):
    """Displays the specific title for the current agent using an emoji icon."""
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: left; margin-bottom: 20px;">
            <span style="font-size: 40px; margin-right: 15px;">{icon}</span>
            <div style="font-size: 2rem; font-weight: 600; color: #FFFFFF;">{agent_name}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_sidebar_footer():
    """Displays a standardized footer in the sidebar."""
    st.sidebar.markdown("---_---")
    st.sidebar.markdown(
        "<p style='text-align: center; color: #888;'>© 2025 Agentopia. All rights reserved.</p>", unsafe_allow_html=True
    )


def display_welcome_message():
    """Displays a welcome message and instructions on the main page."""
    st.markdown(
        """
        ### Welcome to the Data Analyzer Bot!

        This agent helps you perform Exploratory Data Analysis (EDA) on your datasets.

        **To get started:**

        1.  **Upload your data file** using the file uploader below.
        2.  Once uploaded, use the tabs to interact with your data.

        You can configure your LLM provider and API keys in the sidebar.
        """
    )
