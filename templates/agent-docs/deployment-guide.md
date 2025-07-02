# {{AGENT_NAME}} - Deployment Guide

This guide provides detailed instructions for deploying and running the {{AGENT_NAME}} using Docker, which is the recommended method for a consistent and reliable experience.

## Prerequisites

*   [Docker](https://www.docker.com/get-started) installed and running on your system.

## Running with Docker (Recommended)

### 1. Pull the Docker Image

First, pull the latest official image from the Docker repository:

```bash
docker pull {{DOCKER_IMAGE_NAME}}
```

### 2. Run the Container

#### Easiest Method

This command starts the agent and makes it accessible on your local machine.

```bash
{{EASY_RUN_COMMAND}}
```

*   **Access:** Open your web browser and navigate to `http://localhost:8501`.

#### Advanced Method (Mounting Local Files)

If you want the agent to have access to a local folder on your computer, use the `-v` (volume) flag.

```bash
# Replace /path/to/your/data with the actual path to your folder
{{ADVANCED_RUN_COMMAND}}
```

## Local Python Setup (For Development)

Running the agent directly with Python is intended for development purposes.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Agentopia/AIAgentopia.git
    cd AIAgentopia/agents/{{AGENT_FOLDER_NAME}}
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
    streamlit run app/{{ENTRY_POINT_SCRIPT}}
    ```
