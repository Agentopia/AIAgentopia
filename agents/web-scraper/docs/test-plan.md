# Web Scraper Agent - Test Plan

This document outlines the testing strategy and key test cases for the Web Scraper Agent to ensure its functionality, reliability, and quality.

## Testing Objectives

*   Verify that all core features listed in the PRD function as expected.
*   Ensure the agent handles various inputs and edge cases gracefully.
*   Confirm the reliability and correctness of the extracted data.
*   Validate the user interface for both provider selections (OpenAI and Ollama).

## Testing Scope

*   **Integration Testing:** To test the interaction between the Streamlit UI, the scraping backend (Playwright), and both LLM providers.
*   **End-to-End (E2E) Testing:** To test the complete application flow from user input to final JSON output.
*   **UI/UX Testing:** To ensure the user interface is intuitive, responsive, and handles state changes correctly.

## Key Test Cases

The following test cases are derived from the features defined in the `PRD.md`.

| Feature Tested | Test Case Description | Expected Result |
| --- | --- | --- |
| **Provider Selection** | Switch from OpenAI to Ollama provider in the sidebar. | The model dropdown updates to show locally available Ollama models. |
| **Provider Selection** | Switch from Ollama to OpenAI provider in the sidebar. | The model dropdown updates to show available OpenAI models. |
| **OpenAI Integration** | Enter a valid URL and prompt, then scrape with a valid OpenAI API key. | The agent successfully scrapes the site and displays a valid JSON output. |
| **OpenAI Integration** | Attempt to scrape with an invalid OpenAI API key. | A clear error message is displayed, and the application does not crash. |
| **OpenAI Integration** | Attempt to scrape without providing an OpenAI API key. | The "Scrape" button is disabled, and a message prompts the user to enter a key. |
| **Ollama Integration** | Enter a valid URL and prompt, then scrape with a running Ollama instance. | The agent successfully scrapes the site and displays a valid JSON output. |
| **Ollama Integration** | Attempt to scrape when the Ollama application is not running. | A clear error message indicating the provider is unavailable is shown. |
| **Input Validation** | Enter an invalid or non-existent URL (e.g., `htp://invalid-url`). | An error message is displayed, informing the user the URL is invalid. |
| **Input Validation** | Enter a valid URL but leave the prompt empty. | The "Scrape" button is disabled or an error message prompts for a prompt. |
| **Scraping Process** | Scrape a simple, static HTML page. | The content is extracted correctly. |
| **Scraping Process**| Scrape a modern, JavaScript-heavy website. | Playwright correctly renders the page, and the content is extracted. |
| **Output Display** | Successfully complete a scrape. | The output is displayed in a formatted, collapsible JSON viewer. |
| **Output Display** | Click the "Copy" button after a successful scrape. | The JSON output is copied to the clipboard. |
| **Docker Deployment** | Run the agent using the simple `docker run` command. | The container starts, and the app is accessible at `http://localhost:8501`. |
| **Docker Deployment** | Run the agent using the advanced command with a mounted `.env` file. | The container starts, and the OpenAI API key is automatically loaded from the file. |
