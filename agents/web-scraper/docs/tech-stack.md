# Web Scraper Agent - Tech Stack

This document outlines the core technologies, libraries, and frameworks used to build and run the Web Scraper Agent.

## Core Technologies

*   **Programming Language:** Python 3.8+
*   **Primary Framework:** Streamlit

## Key Dependencies

This agent relies on the following key Python libraries:

*   **Web Scraping & Automation:** `scrapegraphai`, `playwright`
*   **Web Interface:** `streamlit`
*   **LLM Interaction:** `requests` (for direct Ollama API calls)
*   **Configuration:** `python-dotenv`

*A full list of dependencies can be found in the `requirements.txt` file.*

## External Services

*   **LLM Providers:** This agent can connect to the following Large Language Model providers:
    *   OpenAI API (Cloud)
    *   Ollama (Local)
*   **Other Services:** None

## Development & Deployment

*   **Containerization:** Docker
*   **Environment Management:** `venv` (standard Python)
