# Data Analyzer Bot - Data Privacy and Security

This document outlines the data handling and privacy policies for the Data Analyzer Bot. Our primary design principle is to ensure user data remains secure and private.

## Core Principle: Local-First Processing

The Data Analyzer Bot is designed to run entirely on your local machine.

*   **Data Storage:** Your data is processed in memory during the application's runtime. It is **never** uploaded to or stored on any external servers.
*   **Local Output:** All outputs, such as reports or generated files, are saved directly to your local filesystem.

## Data Handling Process

1.  A user uploads a file via the web interface.
2.  The application reads the file into an in-memory pandas DataFrame.
3.  All analysis and visualization tasks are performed locally using this in-memory data.
4.  The raw data is discarded when the application session ends or a new file is uploaded.

## LLM Interaction

When using features that rely on a Large Language Model (LLM):

*   **What is Sent:** The agent **does not** send your raw dataset to the LLM. Instead, it only sends necessary, non-sensitive metadata, such as:
    *   Column names and data types
    *   Summary statistics (e.g., mean, median, count)
    *   User-provided natural language queries
*   **What is NOT Sent:** Your raw data rows and values are kept local.

## API Key Security

*   Your API keys are handled securely. You can provide them via a local `.env` file or directly in the UI for the current session.
*   Keys entered in the UI are stored temporarily in the Streamlit session state and are cleared when you close the browser tab. They are never logged or saved permanently by the agent.
