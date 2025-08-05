# Web Scraper Agent - Docker Setup Guide

This guide provides comprehensive instructions for running the Web Scraper Agent using Docker, ensuring a consistent and isolated environment across different platforms.

## 🐳 Quick Start

### Prerequisites
- Docker installed on your system
- An API key for OpenAI (only if you plan to use the OpenAI provider)

### 1. Clone and Setup
```bash
git clone https://github.com/Agentopia/AIAgentopia.git
cd AIAgentopia/agents/web-scraper
```

### 2. Configure Environment
```bash
# Copy the environment template
cp .env.example .env

### Running the Container

#### Simple Command (Recommended for First Use)

This is the simplest way to get the agent running. It starts the container in the background and makes it accessible at `http://localhost:8501`.

```bash
docker run -d --name web-scraper-agent -p 8501:8501 agentopia/web-scraper-agent:latest
```

After running this, you can enter your API key directly in the web interface.

#### Advanced Command (for Persistence)

For regular use, you can mount your local `.env` file to securely provide your API key and set a restart policy. This is more convenient as you won't have to enter your key each time.

1.  **Ensure your `.env` file is in the current directory.**
2.  **Run the command:**

    ```bash
    docker run -d \
      --name web-scraper-agent \
      -p 8501:8501 \
      -v "$(pwd)/.env:/app/.env" \
      --restart unless-stopped \
      agentopia/web-scraper-agent:latest
    ```

### 4. Access the Application
Open your browser and navigate to: http://localhost:8501

## 📋 Detailed Instructions

### Building the Image

The Dockerfile is optimized for production use with the following features:
- **Security**: Runs as a non-root user `agentopia`
- **Health Checks**: Built-in health monitoring
- **Optimized**: Uses a slim base image with minimal dependencies
- **Environment**: Supports `.env` file mounting for API keys

```bash
# Build with a specific tag
docker build -t agentopia/web-scraper-agent:v1.0 .
```

### Running Options

#### Production Deployment
```bash
docker run -d \
  --name web-scraper-agent \
  -p 8501:8501 \
  -v $(pwd)/.env:/app/.env \
  --restart unless-stopped \
  --memory=1g \
  --cpus=1.0 \
  agentopia/web-scraper-agent:latest
```

#### Development Mode
```bash
# Interactive mode with auto-removal and live code reloading
docker run -it --rm \
  -p 8501:8501 \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/app:/app/app \
  agentopia/web-scraper-agent:latest
```

### Volume Mounting

The container uses one important volume:

1.  **Environment File**: `-v $(pwd)/.env:/app/.env`
    -   Mounts your local `.env` file, which can contain your OpenAI API key.
    -   This keeps sensitive data outside the container image.

### Environment Variables

You can also pass environment variables directly without a `.env` file:

```bash
docker run -d \
  --name web-scraper-agent \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your_key_here \
  agentopia/web-scraper-agent:latest
```

## 🔧 Management Commands

### Container Management
```bash
# Check container status
docker ps

# View logs
docker logs web-scraper-agent

# Follow logs in real-time
docker logs -f web-scraper-agent

# Stop the container
docker stop web-scraper-agent

# Start the container
docker start web-scraper-agent

# Remove the container
docker rm web-scraper-agent
```

### Health Checks
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' web-scraper-agent
```

## 🚀 Docker Compose (Optional)

For easier management, you can create a `docker-compose.yml` file:

```yaml
# docker-compose.yml
version: '3.8'

services:
  web-scraper-agent:
    build: .
    container_name: web-scraper-agent
    ports:
      - "8501:8501"
    volumes:
      - ./.env:/app/.env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
```

Run with Docker Compose:
```bash
# Start the service
docker-compose up -d

# Stop the service
docker-compose down
```
