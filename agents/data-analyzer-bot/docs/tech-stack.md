# Data Analyzer Bot - Tech Stack

This document outlines the core technologies, libraries, and frameworks used to build and run the Data Analyzer Bot.

## Core Technologies

*   **Programming Language:** Python 3.11
*   **Primary Framework:** Streamlit

## Key Dependencies

This agent relies on the following key Python libraries:

*   **Data Handling:** `pandas`, `numpy`, `openpyxl`
*   **Web Interface:** `streamlit`
*   **LLM Interaction:** `phi-llm`, `openai`, `anthropic`
*   **Visualization:** `matplotlib`, `seaborn`
*   **Configuration:** `python-dotenv`
*   **Report Generation:** `markdown`

*A full list of dependencies can be found in the `requirements.txt` file.*

## External Services

*   **LLM Providers:** This agent can connect to the following Large Language Model providers:
    *   OpenAI (gpt-4o-mini)
    *   Anthropic (claude-3-opus-20240229)
*   **Other Services:** None

## Development & Deployment

*   **Containerization:** Docker
*   **Environment Management:** `venv` (standard Python)
