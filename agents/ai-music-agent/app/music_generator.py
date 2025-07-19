# ==========================================
# AI MUSIC AGENT - STREAMLIT APPLICATION
# ==========================================
# This module implements a Streamlit-based AI music generation agent
# that uses OpenAI GPT-4 and ModelsLab API to create custom music tracks
# from natural language prompts.
#
# Key Features:
# - Standardized Agentopia UI/UX with responsive design
# - Environment variable configuration with fallback input
# - Comprehensive error handling and validation
# - Real-time audio playback and local file storage
# ==========================================

# Standard library imports
import os
from typing import Optional, Tuple
from uuid import uuid4

import requests

# Streamlit and configuration imports
import streamlit as st

# AI framework imports
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.tools.models_labs import FileType, ModelsLabTools
from agno.utils.log import logger
from dotenv import load_dotenv

# Import Agentopia UI components for standardized interface
from ui_components import (
    display_agent_title,
    display_sidebar_footer,
    display_sidebar_header,
)

# Load environment variables from .env file if it exists
# This enables automatic API key loading without manual input
load_dotenv()

# ========================================
# STREAMLIT UI CONFIGURATION
# ========================================

# Configure Streamlit page settings for optimal user experience
st.set_page_config(
    page_title="AI Music Agent",
    page_icon="🎵",
    layout="wide",  # Use wide layout for better content organization
    initial_sidebar_state="expanded",  # Show sidebar by default
)

# ========================================
# SIDEBAR PANEL SETUP
# ========================================

# Display standardized Agentopia header with logo and branding
display_sidebar_header()

# Add visual separator and API configuration section
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔑 API Configuration")

# ========================================
# API KEY VALIDATION FUNCTIONS
# ========================================
# These functions validate API key formats and provide user-friendly
# feedback to help users identify and fix configuration issues.
def validate_openai_key(key: Optional[str]) -> Tuple[bool, str]:
    """Validate OpenAI API key format.

    Args:
        key: The OpenAI API key to validate

    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    # Check for empty or None values
    if not key or key.strip() == "":
        return False, "API key is empty"

    # Check for placeholder values from .env.example
    if key == "your_openai_api_key_here":
        return False, "Please replace with your actual OpenAI API key"

    # Validate OpenAI key format (must start with 'sk-')
    if not key.startswith("sk-"):
        return False, "OpenAI API key should start with 'sk-'"

    # Basic length validation (OpenAI keys are typically longer than 20 chars)
    if len(key) < 20:
        return False, "OpenAI API key appears to be too short"

    return True, "Valid"


def validate_modelslab_key(key: Optional[str]) -> Tuple[bool, str]:
    """Validate ModelsLab API key format.

    Args:
        key: The ModelsLab API key to validate

    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    # Check for empty or None values
    if not key or key.strip() == "":
        return False, "API key is empty"

    # Check for placeholder values from .env.example
    if key == "your_modelslab_api_key_here":
        return False, "Please replace with your actual ModelsLab API key"

    # Basic length validation (ModelsLab keys should be at least 10 characters)
    if len(key) < 10:
        return False, "ModelsLab API key appears to be too short"

    return True, "Valid"


# ========================================
# ENVIRONMENT VARIABLE LOADING
# ========================================
# Load API keys from environment variables if available
# This provides a secure way to store credentials without hardcoding

env_openai_key = os.getenv("OPENAI_API_KEY")
env_modelslab_key = os.getenv("MODELSLAB_API_KEY")

# Validate environment variables if they exist and provide status feedback
env_openai_valid, env_openai_msg = (
    validate_openai_key(env_openai_key) if env_openai_key else (False, "Not set")
)
env_modelslab_valid, env_modelslab_msg = (
    validate_modelslab_key(env_modelslab_key)
    if env_modelslab_key
    else (False, "Not set")
)

# ========================================
# API KEY CONFIGURATION UI
# ========================================
# Display environment variable status and provide fallback input fields
# This creates a seamless user experience with automatic loading when possible

# Check if both environment variables are valid
if env_openai_valid and env_modelslab_valid:
    # Both keys are valid from environment - show success status
    st.sidebar.success("✅ API keys loaded from environment variables")
    st.sidebar.markdown("*Keys are securely loaded from your .env file*")
    openai_api_key = env_openai_key
    models_lab_api_key = env_modelslab_key
else:
    # Environment keys missing or invalid - show manual input interface
    st.sidebar.markdown("Configure your API keys to start generating music.")

    # Show specific validation errors for environment variables if they exist but are invalid
    if env_openai_key and not env_openai_valid:
        st.sidebar.error(f"⚠️ OpenAI key in .env file: {env_openai_msg}")
    if env_modelslab_key and not env_modelslab_valid:
        st.sidebar.error(f"⚠️ ModelsLab key in .env file: {env_modelslab_msg}")

    # Provide helpful tip for first-time users
    if not env_openai_key and not env_modelslab_key:
        st.sidebar.info(
            "💡 Tip: Create a .env file with your keys for automatic loading"
        )

    # Manual input fields with pre-populated values from environment (if available)
    # These provide fallback when environment variables are missing or invalid
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        value=env_openai_key or "",  # Pre-fill with env value if available
        type="password",  # Hide the key for security
        help="Required for AI-powered prompt enhancement",
    )
    models_lab_api_key = st.sidebar.text_input(
        "ModelsLab API Key",
        value=env_modelslab_key or "",  # Pre-fill with env value if available
        type="password",  # Hide the key for security
        help="Required for music generation",
    )

    # Real-time validation of manually entered keys with user feedback
    # This provides immediate feedback to help users identify issues
    if openai_api_key:
        openai_valid, openai_msg = validate_openai_key(openai_api_key)
        if not openai_valid:
            st.sidebar.error(f"⚠️ OpenAI API Key: {openai_msg}")

    if models_lab_api_key:
        modelslab_valid, modelslab_msg = validate_modelslab_key(models_lab_api_key)
        if not modelslab_valid:
            st.sidebar.error(f"⚠️ ModelsLab API Key: {modelslab_msg}")

# Display standardized Agentopia footer in sidebar
display_sidebar_footer()

# ========================================
# MAIN CONTENT AREA
# ========================================
# This section contains the primary user interface for music generation
# including the agent title, input form, and generated content display

# Display agent title with music note icon for visual branding
display_agent_title(icon="🎵", agent_name="AI Music Agent")

# ========================================
# RESPONSIVE CSS STYLING
# ========================================
# Add custom CSS for better user experience across different devices
st.markdown(
    """
    <style>
    .stTextArea > div > div > textarea {
        font-size: 14px;
    }
    .stButton > button {
        width: 100%;
        font-size: 16px;
        padding: 0.5rem 1rem;
    }
    @media (max-width: 768px) {
        .stTextArea > div > div > textarea {
            font-size: 16px;
        }
        .stButton > button {
            font-size: 18px;
            padding: 0.75rem 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ========================================
# MUSIC GENERATION INTERFACE
# ========================================
# User input section for music generation prompts and controls

st.markdown("### 🎼 Music Generation")

# Text area for user to describe their desired music
# Pre-filled with example to guide users on effective prompting
prompt = st.text_area(
    "Enter your music generation prompt:",
    "Generate a 30 second classical music piece",  # Example prompt
    height=100,
    help="Describe the style, mood, instruments, and any specific characteristics you want in your music.",
)

# Generate button with smart enabling/disabling based on API key availability
# Always visible for better UX, but disabled when keys are missing
generate_button = st.button(
    "🎵 Generate Music",
    disabled=not (openai_api_key and models_lab_api_key),  # Disable if keys missing
    help="Enter both API keys in the sidebar to enable music generation",
)

# ========================================
# AI AGENT INITIALIZATION
# ========================================
# Initialize the AI agent with proper error handling
# Only proceed if both API keys are available and valid
if openai_api_key and models_lab_api_key:
    try:
        agent = Agent(
            name="ModelsLab Music Agent",
            agent_id="ml_music_agent",
            model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
            show_tool_calls=True,
            tools=[
                ModelsLabTools(
                    api_key=models_lab_api_key,
                    wait_for_completion=True,
                    file_type=FileType.MP3,
                )
            ],
            description="You are an AI agent that can generate music using the ModelsLabs API.",
            instructions=[
                "When generating music, use the `generate_media` tool with detailed prompts that specify:",
                "- The genre and style of music (e.g., classical, jazz, electronic)",
                "- The instruments and sounds to include",
                "- The tempo, mood and emotional qualities",
                "- The structure (intro, verses, chorus, bridge, etc.)",
                "Create rich, descriptive prompts that capture the desired musical elements.",
                "Focus on generating high-quality, complete instrumental pieces.",
            ],
            markdown=True,
            debug_mode=True,
        )
    except Exception as e:
        st.error(
            f"⚠️ Failed to initialize AI agent. Please check your API keys: {str(e)}"
        )
        st.info(
            "💡 Make sure your OpenAI and ModelsLab API keys are valid and have sufficient credits."
        )
        st.stop()

    if generate_button:
        if prompt.strip() == "":
            st.warning("Please enter a prompt first.")
        else:
            with st.spinner("Generating music... 🎵"):
                try:
                    music: RunResponse = agent.run(prompt)

                    if music.audio and len(music.audio) > 0:
                        # Create audio directory with error handling
                        save_dir = "audio_generations"
                        try:
                            os.makedirs(save_dir, exist_ok=True)
                        except PermissionError:
                            st.error(
                                "📁 Permission denied. Cannot create audio directory. Please check folder permissions."
                            )
                            st.stop()
                        except OSError as e:
                            st.error(f"📁 Failed to create audio directory: {str(e)}")
                            st.stop()

                        url = music.audio[0].url
                        st.write(f"🔍 Debug: Attempting to download from URL: {url}")

                        # Download audio file with proper error handling
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        }
                        try:
                            response = requests.get(url, headers=headers, timeout=30)
                        except requests.exceptions.Timeout:
                            st.error("⏱️ Download timed out. Please try again.")
                            st.stop()
                        except requests.exceptions.ConnectionError:
                            st.error(
                                "🌐 Network error. Please check your internet connection."
                            )
                            st.stop()
                        except requests.exceptions.RequestException as e:
                            st.error(f"❌ Download failed: {str(e)}")
                            st.stop()

                        # 🛡️ Validate response
                        if response.status_code != 200:
                            st.error(
                                f"Failed to download audio. Status code: "
                                f"{response.status_code}"
                            )
                            st.stop()
                        # Check if the response content type is audio
                        content_type = response.headers.get("Content-Type", "")
                        if "audio" not in content_type:
                            st.error(
                                f"Invalid file type returned: {content_type}"
                            )
                            st.stop()

                        # Save audio file with error handling
                        filename = f"{save_dir}/music_{uuid4()}.mp3"
                        try:
                            with open(filename, "wb") as f:
                                f.write(response.content)
                        except PermissionError:
                            st.error(
                                "💾 Permission denied. Cannot save audio file. "
                                "Please check folder permissions."
                            )
                            st.stop()
                        except OSError as e:
                            st.error(
                                f"💾 Error saving audio file: {str(e)}"
                            )
                            st.stop()
                        except Exception as e:
                            st.error(f"💾 Unexpected error saving file: {str(e)}")
                            st.stop()

                        # 🎧 Play audio
                        st.success("Music generated successfully! 🎶")
                        audio_bytes = open(filename, "rb").read()
                        st.audio(audio_bytes, format="audio/mp3")

                        st.download_button(
                            label="Download Music",
                            data=audio_bytes,
                            file_name="generated_music.mp3",
                            mime="audio/mp3",
                        )
                    else:
                        st.error("No audio generated. Please try again.")

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    logger.error(f"Streamlit app error: {e}")

else:
    st.sidebar.warning(
        "Please enter both the OpenAI and ModelsLab API keys to use the app."
    )
