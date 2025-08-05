# Web Scraper Agent - Deployment Guide

This guide provides detailed instructions for deploying and running the Web Scraper Agent using Docker, which is the recommended method for a consistent and reliable experience.

## Prerequisites

*   [Docker](https://www.docker.com/get-started) installed and running on your system.
*   An active internet connection.

## Running with Docker (Recommended)

### 1. Pull the Docker Image

First, pull the latest official image from the Docker repository:

```bash
docker pull agentopia/web-scraper-agent:latest
```

### 2. Run the Container

#### Simple Command (Recommended)

This command starts the agent and makes it accessible on your local machine. After launching, you can enter your API key in the web interface.

```bash
docker run -d --name web-scraper-agent -p 8501:8501 agentopia/web-scraper-agent:latest
```

*   **Access:** Open your web browser and navigate to `http://localhost:8501`.

#### Advanced Command (with Persistent API Key)

If you want the agent to automatically use your OpenAI API key, you can securely mount your local `.env` file containing the key.

```bash
# Replace /path/to/your/.env with the actual path to your file
docker run -d --name web-scraper-agent -p 8501:8501 -v /path/to/your/.env:/app/.env agentopia/web-scraper-agent:latest
```

## Local Python Setup (For Development)

Running the agent directly with Python is intended for development purposes.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Agentopia/AIAgentopia.git
    cd AIAgentopia/agents/web-scraper
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```

4.  **Run the Application:**
    ```bash
    streamlit run app/web_scraper.py
    ```
