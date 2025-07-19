"""
Reusable Streamlit UI components for the AI Music Agent.

This module provides standardized functions to display common UI elements like
headers, footers, and titles, ensuring a consistent look and feel across the
application.
"""

import base64
import os

import streamlit as st


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
            <div style="display: flex; align-items: center; justify-content: left;
                        margin-bottom: 20px;">
                <img src="data:image/svg+xml;base64,{logo_b64}" width="40">
                <h1 style="margin-left: 10px; color: #FFFFFF; font-size: 22px;
                           font-weight: bold;">AI Agentopia</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.sidebar.error("Agentopia logo not found.")
        st.sidebar.header("AI Agentopia")


def display_agent_title(icon="🎵", agent_name="AI Music Agent"):
    """Displays the specific title for the current agent using an emoji icon."""
    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: center;
            justify-content: left;
            margin-bottom: 20px;
            flex-wrap: wrap;
        ">
            <span style="
                font-size: clamp(30px, 8vw, 40px);
                margin-right: 15px;
                margin-bottom: 5px;
            ">{icon}</span>
            <div style="
                font-size: clamp(1.5rem, 5vw, 2rem);
                font-weight: 600;
                color: #FFFFFF;
                line-height: 1.2;
            ">{agent_name}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_sidebar_footer():
    """Displays a standardized footer in the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<p style='text-align: center; color: #888;'>© 2025 Agentopia. "
        "All rights reserved.</p>",
        unsafe_allow_html=True,
    )


def display_welcome_message():
    """Displays a welcome message and instructions on the main page."""
    st.markdown(
        """
        ### Welcome to the AI Music Agent! 🎵

        This agent helps you generate custom music tracks from natural language
        prompts using AI.

        **To get started:**

        1.  **Configure your API keys** in the sidebar (OpenAI and ModelsLab).
        2.  **Enter your music prompt** describing the style, mood, or genre you
            want.
        3.  **Click "Generate Music"** and wait for your custom track to be created.
        4.  **Play and download** your generated music.

        You can configure your API keys in the sidebar or use environment variables for
        convenience.
        """
    )
