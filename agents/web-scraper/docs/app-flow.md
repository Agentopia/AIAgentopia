# Web Scraper Agent - Application Flow

This document describes the high-level execution flow and logic of the Web Scraper Agent.

## Interaction Model

*   **Interaction Type:** Interactive Streamlit Web App

## High-Level Execution Flow

The agent follows these primary steps from start to finish:

1.  **Initialization:** The Streamlit application starts, and the session state is initialized. Environment variables (e.g., `OPENAI_API_KEY`) are loaded if present.
2.  **Provider & Model Selection:** The user selects an LLM provider (OpenAI or Ollama) and a specific model from a dynamically populated list in the sidebar.
3.  **Authentication (If Needed):** If using OpenAI and no API key is found in the environment, the user enters their key into a secure input field.
4.  **User Input:** The user provides the target website URL and a natural language prompt describing the information to be extracted in the main panel.
5.  **Core Processing:** The user clicks the "Scrape" button, which triggers the main processing logic. This involves:
    *   Launching a headless Playwright browser instance.
    *   Navigating to the specified URL and extracting the raw page content.
    *   Passing the extracted content and the user's prompt to the selected LLM.
6.  **LLM Interaction:** The selected LLM provider receives the page content and the user's prompt. It analyzes the content to find and structure the requested information.
7.  **Output Generation:** The agent receives the structured data from the LLM and displays it as a formatted, collapsible JSON object in the web interface.
8.  **Completion:** The agent's run is complete, and it waits for the user to start a new scraping task or copy the results.
