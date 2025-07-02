# Data Analyzer Bot - Deployment Guide

This guide provides detailed instructions for deploying and running the Data Analyzer Bot using Docker, which is the recommended method for a consistent and reliable experience.

## Prerequisites

*   [Docker](https://www.docker.com/get-started) installed and running on your system.

## Running with Docker (Recommended)

### 1. Pull the Docker Image

First, pull the latest official image from the Docker repository:

```bash
docker pull agentopia/data-analyzer-bot:1.0.0
```

### 2. Run the Container

#### Easiest Method

This command starts the agent and makes it accessible on your local machine.

```bash
docker run -it --rm -p 8501:8501 agentopia/data-analyzer-bot:1.0.0
```

*   **Access:** Open your web browser and navigate to `http://localhost:8501`.

#### Advanced Method (Mounting Local Files)

If you want the agent to have access to a local folder on your computer, use the `-v` (volume) flag.

```bash
# Replace /path/to/your/data with the actual path to your folder
docker run -it --rm -p 8501:8501 -v /path/to/your/data:/app/data agentopia/data-analyzer-bot:1.0.0
```

## Local Python Setup (For Development)

Running the agent directly with Python is intended for development purposes.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Agentopia/AIAgentopia.git
    cd AIAgentopia/agents/data-analyzer-bot
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    ```bash
    streamlit run app/ai_data_analyst.py
    ```
