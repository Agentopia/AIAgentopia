# {{AGENT_NAME}} - Application Flow

This document describes the high-level execution flow and logic of the {{AGENT_NAME}}.

## Interaction Model

*   **Interaction Type:** `{{INTERACTION_TYPE}}` (e.g., Interactive Streamlit Web App, Command-Line Interface)

## High-Level Execution Flow

The agent follows these primary steps from start to finish:

{{HIGH_LEVEL_FLOW_LIST}}

*Example Flow:*
1.  **Initialization:** The application starts, and session state is initialized. Environment variables (if any) are loaded.
2.  **User Input:** The user provides input via the `{{INPUT_MECHANISM}}` (e.g., file uploader in the web UI, command-line arguments).
3.  **Core Processing:** The main processing logic is triggered. This involves:
    *   [Step A, e.g., Reading and parsing the data]
    *   [Step B, e.g., Executing automated analysis functions]
    *   [Step C, e.g., Generating visualizations]
4.  **(Optional) LLM Interaction:** If configured, the agent sends `{{DATA_SENT_TO_LLM}}` (e.g., aggregated statistics, user queries) to the selected LLM provider.
5.  **Output Generation:** The agent produces its final output, which is `{{OUTPUT_FORMAT}}` (e.g., a downloadable HTML report, files saved to a directory).
6.  **Completion:** The agent completes its run or waits for further user interaction.
