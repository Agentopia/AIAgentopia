# Data Analyzer Bot - Application Flow

This document describes the high-level execution flow and logic of the Data Analyzer Bot.

## Interaction Model

*   **Interaction Type:** Interactive Streamlit Web App

## High-Level Execution Flow

The agent follows these primary steps from start to finish:

1.  **Initialization:** The Streamlit application starts, and the session state is initialized. API keys from the `.env` file (if present) are loaded.
2.  **User Input:** The user uploads a CSV or Excel file via the file uploader in the web UI's sidebar.
3.  **Core Processing:** The main processing logic is triggered once a file is uploaded. This involves:
    *   Reading and parsing the data into a pandas DataFrame.
    *   Displaying tabs for different analysis types (Automated Analysis, Visualizations, AI Summary, etc.).
    *   Calculating and displaying statistical analyses within the 'Automated Analysis' tab.
    *   Generating and displaying plots within the 'Visualizations' tab.
4.  **(Optional) LLM Interaction:** If the user provides an API key and uses the 'AI Summary' or 'Interactive Query' tab, the agent sends aggregated statistics and user queries to the selected LLM provider (OpenAI or Anthropic).
5.  **Output Generation:** The agent produces its final output when the user clicks the 'Generate Report' button. This creates a downloadable, self-contained HTML report.
6.  **Completion:** The agent remains active, waiting for further user interaction (e.g., uploading a new file, asking more questions).
