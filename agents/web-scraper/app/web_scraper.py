# Import the required libraries
import asyncio
import json
import os
import sys
from typing import Dict, List, Optional

import requests
import streamlit as st
import validators
from playwright.sync_api import sync_playwright
from scrapegraphai.graphs import SmartScraperGraph
from ui_components import (
    display_agent_title_panel,
    display_sidebar_footer,
    display_sidebar_header,
)

# Windows asyncio subprocess transport fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Page configuration
st.set_page_config(
    page_title="AI Agentopia - Web Scraper Agent",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)


class LLMProvider:
    """Base class for LLM providers"""

    def __init__(self, name: str):
        self.name = name

    def is_available(self) -> bool:
        """Check if the provider is available"""
        raise NotImplementedError

    def get_models(self) -> List[str]:
        """Get available models for this provider"""
        raise NotImplementedError

    def get_config(self, model: str, **kwargs) -> Dict:
        """Get configuration for scrapegraphai"""
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI API provider"""

    def __init__(self):
        super().__init__("OpenAI")
        self.models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]

    def is_available(self) -> bool:
        """Check if OpenAI API key is available and valid format"""
        api_key = self._get_api_key()
        if not api_key or len(api_key.strip()) == 0:
            return False
        return self.validate_api_key(api_key)

    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment or session state"""
        # Try environment variable first
        env_key = os.getenv("OPENAI_API_KEY")
        if env_key:
            return env_key

        # Try session state (from UI input)
        return st.session_state.get("openai_api_key", "")

    def get_models(self) -> List[str]:
        """Get available OpenAI models"""
        return self.models

    def validate_api_key(self, api_key: str) -> bool:
        """Validate OpenAI API key format"""
        if not api_key:
            return False

        # Basic format validation (OpenAI keys start with 'sk-')
        if not api_key.startswith("sk-"):
            return False

        # Length validation (OpenAI keys are typically 51 characters)
        if len(api_key) < 40:
            return False

        return True

    def get_config(self, model: str, **kwargs) -> Dict:
        """Get OpenAI configuration for scrapegraphai"""
        api_key = self._get_api_key()
        if not api_key:
            raise ValueError("OpenAI API key is required")

        return {
            "llm": {
                "api_key": api_key,
                "model": model,
                "temperature": kwargs.get("temperature", 0),
            }
        }


class OllamaProvider(LLMProvider):
    """Local Ollama provider"""

    def __init__(self):
        super().__init__("Ollama")
        # Use host.docker.internal if running in Docker, otherwise localhost
        docker_host = "host.docker.internal"
        self.base_url = (
            f"http://{docker_host}:11434"
            if os.getenv("RUNNING_IN_DOCKER")
            else "http://localhost:11434"
        )
        # Include memory-efficient model variants
        self.default_models = ["llama3.2:1b", "llama3.2", "llama3.1:8b", "gemma2:2b"]
        self.embedding_model = "nomic-embed-text"

    def is_available(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_models(self) -> List[str]:
        """Get available Ollama LLM models (excluding embedding models)"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                # Keep full model names including variants (e.g., llama3.2:1b)
                all_models = [model["name"] for model in data.get("models", [])]

                # Filter out embedding models and keep only LLM models
                embedding_models = [
                    "nomic-embed-text",
                    "all-minilm",
                    "sentence-transformers",
                ]
                llm_models = []

                for model in all_models:
                    model_base = model.split(":")[0]
                    if model_base not in embedding_models:
                        llm_models.append(model)

                # Sort to prioritize memory-efficient models
                # Put smaller variants (1b, 2b) first, then larger ones
                def model_priority(model_name):
                    if ":1b" in model_name:
                        return 0  # Highest priority
                    elif ":2b" in model_name:
                        return 1
                    elif ":8b" in model_name:
                        return 2
                    elif "llama3.2:latest" in model_name or model_name == "llama3.2":
                        return 9  # Lower priority due to memory requirements
                    else:
                        return 5  # Medium priority

                llm_models.sort(key=model_priority)

                return llm_models if llm_models else self.default_models
        except requests.RequestException:
            pass

        return self.default_models

    def get_config(self, model: str, **kwargs) -> Dict:
        """Get Ollama configuration for scrapegraphai"""
        return {
            "llm": {
                "model": f"ollama/{model}",
                "temperature": kwargs.get("temperature", 0),
                "format": "json",
                "base_url": self.base_url,
            },
            "embeddings": {
                "model": f"ollama/{self.embedding_model}",
                "base_url": self.base_url,
            },
            "verbose": True,
        }


def initialize_providers() -> Dict[str, LLMProvider]:
    """Initialize all LLM providers"""
    return {"OpenAI": OpenAIProvider(), "Ollama": OllamaProvider()}


def validate_url(url: str) -> bool:
    """Validate URL format"""
    if not url:
        return False

    # Add protocol if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return validators.url(url)


def sanitize_prompt(prompt: str) -> str:
    """Sanitize user input prompt"""
    if not prompt:
        return ""

    # Basic sanitization - remove potentially harmful characters
    sanitized = prompt.strip()

    # Remove excessive whitespace
    sanitized = " ".join(sanitized.split())

    return sanitized


def scrape_with_direct_ollama(url: str, prompt: str, model: str) -> Dict:
    """Direct Ollama integration for web scraping (bypasses scrapegraphai)"""
    # Determine base URL based on environment
    docker_host = "host.docker.internal"
    base_url = (
        f"http://{docker_host}:11434"
        if os.getenv("RUNNING_IN_DOCKER")
        else "http://localhost:11434"
    )
    """Direct Ollama integration for web scraping (bypasses scrapegraphai)"""
    try:
        # Step 1: Scrape the website content using Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to the URL
            page.goto(url, timeout=30000)

            # Wait for content to load
            page.wait_for_timeout(2000)

            # Extract text content
            content = page.evaluate("""
                () => {
                    // Remove script and style elements
                    const scripts = document.querySelectorAll('script, style, nav, footer, header');
                    scripts.forEach(el => el.remove());

                    // Get main content
                    const main = document.querySelector('main') || document.querySelector('article') || document.body;
                    return main ? main.innerText : document.body.innerText;
                }
            """)

            browser.close()

        # Step 2: Limit content size to avoid token limits
        if len(content) > 8000:  # Reasonable limit for context
            content = content[:8000] + "...[content truncated]"

        # Step 3: Create prompt for Ollama
        system_prompt = f"""
You are a web scraping assistant. Analyze the following website content and extract the requested information.

Website URL: {url}
User Request: {prompt}

Website Content:
{content}

Please extract the requested information and return it in a clear, structured JSON format. If the requested information is not found, explain what you found instead.
"""

        # Step 4: Send request to Ollama
        ollama_payload = {
            "model": model,
            "prompt": system_prompt,
            "stream": False,
            "format": "json",
        }

        response = requests.post(
            f"{base_url}/api/generate", json=ollama_payload, timeout=60
        )

        if response.status_code == 200:
            result = response.json()

            # Try to parse the response as JSON
            try:
                extracted_data = json.loads(result.get("response", "{}"))
                return {
                    "success": True,
                    "data": extracted_data,
                    "method": "direct_ollama",
                    "model": model,
                }
            except json.JSONDecodeError:
                # If not valid JSON, return as text
                return {
                    "success": True,
                    "data": {
                        "extracted_content": result.get("response", "No response")
                    },
                    "method": "direct_ollama",
                    "model": model,
                }
        else:
            return {
                "success": False,
                "error": f"Ollama API error: {response.status_code} - {response.text}",
                "method": "direct_ollama",
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Direct Ollama scraping error: {str(e)}",
            "method": "direct_ollama",
        }


def main():
    """Main application function"""

    # Load environment variables
    from dotenv import load_dotenv

    load_dotenv()

    # Initialize providers
    openai_provider = OpenAIProvider()
    ollama_provider = OllamaProvider()

    # Sidebar with Agentopia branding
    display_sidebar_header()
    st.sidebar.markdown("---")

    # Provider selection
    st.sidebar.subheader("🔧 LLM Provider")
    provider_choice = st.sidebar.radio(
        "Select your preferred LLM provider:",
        ["OpenAI", "Ollama"],
        index=0,
        help="Choose between cloud-based OpenAI or local Ollama",
    )

    st.sidebar.markdown("---")

    # Set selected provider based on choice
    selected_provider = (
        openai_provider if provider_choice == "OpenAI" else ollama_provider
    )
    selected_provider_name = provider_choice

    # Provider-specific configuration
    if provider_choice == "OpenAI":
        st.sidebar.subheader("☁️ OpenAI Configuration")

        # Get API key from environment or session state
        env_api_key = os.getenv("OPENAI_API_KEY", "")

        # Initialize session state for API key if not exists
        if "openai_api_key" not in st.session_state:
            st.session_state.openai_api_key = env_api_key

        # API key input with auto-populated value
        api_key_input = st.sidebar.text_input(
            "OpenAI API Key:",
            value=st.session_state.openai_api_key,
            type="password",
            help="Enter your OpenAI API key (auto-loaded from .env if available)",
        )

        # Update session state when user changes the input
        if api_key_input != st.session_state.openai_api_key:
            st.session_state.openai_api_key = api_key_input

        # Check availability and show status (provider gets API key from session state automatically)
        if st.session_state.openai_api_key:
            if openai_provider.validate_api_key(st.session_state.openai_api_key):
                st.sidebar.success("✅ OpenAI: Ready")
                st.sidebar.caption("API key is valid and configured")
            else:
                st.sidebar.warning("⚠️ OpenAI: Invalid API Key")
                st.sidebar.caption("Please check your API key format")
        else:
            st.sidebar.info("ℹ️ OpenAI: Ready to configure")
            st.sidebar.caption("Please enter your API key to get started")

        # Model selection for OpenAI
        st.sidebar.markdown("**Model Selection:**")
        openai_models = openai_provider.get_models()

        # Set gpt-3.5-turbo as default if available
        default_index = 0
        if "gpt-3.5-turbo" in openai_models:
            default_index = openai_models.index("gpt-3.5-turbo")

        selected_model = st.sidebar.selectbox(
            "Choose OpenAI model:",
            openai_models,
            index=default_index,
            help="Select the OpenAI model for scraping",
            disabled=not st.session_state.openai_api_key,
        )

        # Setup instructions if not connected
        if not st.session_state.openai_api_key:
            with st.sidebar.expander("📋 Setup Instructions"):
                st.markdown(
                    "1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)"
                )
                st.markdown("2. Enter it in the field above")
                st.markdown("3. Or set `OPENAI_API_KEY` environment variable")

    else:  # Ollama selected
        # Ollama Configuration Section
        st.sidebar.subheader("🏠 Ollama Configuration")

        # Check Ollama availability
        ollama_available = ollama_provider.is_available()

        # Connection status for Ollama
        if ollama_available:
            st.sidebar.success("✅ Ollama: Connected")
            st.sidebar.caption("🤖 Local Ollama service is running")
        else:
            st.sidebar.warning("⚠️ Ollama: Not Running")
            st.sidebar.caption("💡 Please start Ollama service first")

        # Model selection for Ollama
        st.sidebar.markdown("**Model Selection:**")
        ollama_models = ollama_provider.get_models() if ollama_available else []

        if ollama_models:
            selected_model = st.sidebar.selectbox(
                "Choose Ollama model:",
                ollama_models,
                index=0,
                help="Select the local Ollama model for scraping",
            )
        else:
            st.sidebar.info("ℹ️ No models available")
            st.sidebar.caption("Install models using: `ollama pull llama3.2:1b`")
            selected_model = None

        # Setup instructions if not connected
        if not ollama_available:
            with st.sidebar.expander("📋 Setup Instructions"):
                st.markdown("1. Install [Ollama](https://ollama.ai/)")
                st.markdown("2. Start service: `ollama serve`")
                st.markdown("3. Install models: `ollama pull llama3.2:1b`")
                st.markdown("4. Install embeddings: `ollama pull nomic-embed-text`")

    display_sidebar_footer()

    # Main content with Agentopia styling
    display_agent_title_panel()

    # Input section
    st.markdown("### 🌐 Website & Prompt")

    col1, col2 = st.columns([1, 1])

    with col1:
        url_input = st.text_input(
            "Website URL:",
            placeholder="https://example.com",
            help="Enter the URL of the website you want to scrape",
        )

    with col2:
        prompt_input = st.text_input(
            "What to extract:",
            placeholder="Extract the main article title and summary",
            help="Describe what information you want to extract from the website",
        )

    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        temperature = st.slider(
            "Temperature (creativity):",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Higher values make output more creative but less predictable",
        )

    # Scraping section
    if st.button("🕵️‍♂️ Start Scraping", type="primary"):
        # Validation
        if not url_input:
            st.error("Please enter a website URL")
            return

        if not prompt_input:
            st.error("Please describe what you want to extract")
            return

        # Validate URL
        if not validate_url(url_input):
            st.error("Please enter a valid URL (e.g., https://example.com)")
            return

        # Sanitize inputs
        clean_url = url_input.strip()
        if not clean_url.startswith(("http://", "https://")):
            clean_url = "https://" + clean_url

        clean_prompt = sanitize_prompt(prompt_input)

        # Check provider availability
        if not selected_provider.is_available():
            st.error(
                f"{selected_provider_name} provider is not available. Please check your configuration."
            )
            return

        # Start scraping
        with st.spinner(
            f"🔍 Scraping with {selected_provider_name} ({selected_model})..."
        ):
            try:
                if selected_provider_name == "Ollama":
                    # Use direct Ollama integration to bypass scrapegraphai issues
                    result = scrape_with_direct_ollama(
                        url=clean_url,
                        prompt=clean_prompt,
                        model=selected_model,
                    )

                    if result["success"]:
                        st.success("✅ Scraping completed successfully!")

                        st.markdown("### 📊 Extracted Data")

                        # Display the extracted data
                        extracted_data = result["data"]
                        if isinstance(extracted_data, dict):
                            st.json(extracted_data)
                        else:
                            st.text_area("Result:", str(extracted_data), height=200)

                        # Additional info
                        with st.expander("ℹ️ Scraping Details"):
                            st.write(
                                f"**Provider:** {selected_provider_name} (Direct Integration)"
                            )
                            st.write(f"**Model:** {selected_model}")
                            st.write(f"**URL:** {clean_url}")
                            st.write(f"**Prompt:** {clean_prompt}")
                            st.write(f"**Temperature:** {temperature}")
                            st.write(f"**Method:** {result['method']}")
                    else:
                        st.error(
                            f"❌ Error occurred during scraping: {result['error']}"
                        )

                        with st.expander("🔍 Error Details"):
                            st.code(result["error"])

                            # Check for specific error types and provide targeted help
                            error_msg = result["error"].lower()

                            if "memory" in error_msg or "system memory" in error_msg:
                                st.markdown("**💾 Memory Issue Detected:**")
                                st.markdown(
                                    "- Your system doesn't have enough memory for this model"
                                )
                                st.markdown(
                                    "- Try smaller models: `ollama pull llama3.2:1b` or `ollama pull gemma2:2b`"
                                )
                                st.markdown(
                                    "- Close other applications to free up memory"
                                )
                                st.markdown(
                                    "- Consider using OpenAI instead for memory-intensive tasks"
                                )
                            else:
                                st.markdown("**General Troubleshooting Tips:**")
                                st.markdown(
                                    "- Make sure Ollama service is running: `ollama serve`"
                                )
                                st.markdown(
                                    "- Check if the model is installed: `ollama list`"
                                )
                                st.markdown(
                                    f"- Install missing models: `ollama pull {selected_model}`"
                                )
                                st.markdown(
                                    "- Try a different website or simpler prompt"
                                )
                else:
                    # Use scrapegraphai for OpenAI (works fine)
                    config = selected_provider.get_config(
                        selected_model, temperature=temperature
                    )

                    # Create scraper
                    scraper = SmartScraperGraph(
                        prompt=clean_prompt, source=clean_url, config=config
                    )

                    # Run scraping
                    result = scraper.run()

                    # Display results
                    st.success("✅ Scraping completed successfully!")

                    st.markdown("### 📊 Extracted Data")

                    if isinstance(result, dict):
                        st.json(result)
                    elif isinstance(result, str):
                        st.text_area("Result:", result, height=200)
                    else:
                        st.write(result)

                    # Additional info
                    with st.expander("ℹ️ Scraping Details"):
                        st.write(
                            f"**Provider:** {selected_provider_name} (ScrapegraphAI)"
                        )
                        st.write(f"**Model:** {selected_model}")
                        st.write(f"**URL:** {clean_url}")
                        st.write(f"**Prompt:** {clean_prompt}")
                        st.write(f"**Temperature:** {temperature}")

            except Exception as e:
                st.error(f"❌ Error occurred during scraping: {str(e)}")

                # Detailed error information
                with st.expander("🔍 Error Details"):
                    st.code(str(e))

                    # Provider-specific help
                    if selected_provider_name == "OpenAI":
                        st.markdown("**Troubleshooting Tips:**")
                        st.markdown("- Check your API key is valid and has credits")
                        st.markdown("- Verify the selected model is available")
                        st.markdown("- Try a different website or simpler prompt")
                    else:  # Ollama
                        st.markdown("**Troubleshooting Tips:**")
                        st.markdown(
                            "- Make sure Ollama service is running: `ollama serve`"
                        )
                        st.markdown("- Check if the model is installed: `ollama list`")
                        st.markdown("- Install missing models: `ollama pull llama3.2`")
                        st.markdown("- Try a different website or simpler prompt")


if __name__ == "__main__":
    main()
