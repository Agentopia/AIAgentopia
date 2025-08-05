# Web Scraper Agent - Data Privacy and Security

This document outlines the data handling and privacy policies for the Web Scraper Agent. Our primary design principle is to ensure user data remains secure and private.

## Core Principle: Privacy-First Design

The Web Scraper Agent is designed with user privacy as a priority. It offers two distinct operational modes:

*   **Local-First Processing (Ollama):** When using the Ollama provider, the agent runs entirely on your local machine. No data, prompts, or API keys are ever sent to external servers. All processing happens locally.
*   **Cloud-Based Processing (OpenAI):** When using the OpenAI provider, specific data is sent to the OpenAI API for processing. API key handling is designed to be secure.

## Data Handling Process

1.  A user provides a target website URL and a natural language prompt.
2.  The agent's local Playwright instance navigates to the URL and reads the page content into memory.
3.  The extracted page content and the user's prompt are sent to the selected LLM provider (either local Ollama or remote OpenAI).
4.  The structured data returned by the LLM is displayed in the UI.
5.  **No data is ever stored permanently by the agent.** The process is stateless, and all data is discarded when the application session ends.

## LLM Interaction

When using features that rely on a Large Language Model (LLM):

*   **What is Sent:** The agent sends the following information to the selected LLM provider:
    *   The full HTML content of the target URL.
    *   The user's natural language prompt for extraction.
*   **What is NOT Sent:** The agent does not send any personal data, local file information, or user credentials to the LLM.

## API Key Security

API keys are only required when using the OpenAI provider.

*   Your OpenAI API key is handled securely. You can provide it via a local `.env` file or directly in the UI for the current session.
*   Keys entered in the UI are stored temporarily in the Streamlit session state and are cleared when you close the browser tab. They are never logged or saved permanently by the agent.
*   For maximum security and privacy, we recommend using the Ollama provider, which runs locally and requires no API keys.
