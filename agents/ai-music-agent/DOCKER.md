# AI Music Agent - Docker Setup Guide

This guide provides comprehensive instructions for running the AI Music Agent using Docker, ensuring a consistent and isolated environment across different platforms.

## 🐳 Quick Start

### Prerequisites
- Docker installed on your system
- API keys for OpenAI and ModelsLab

### 1. Clone and Setup
```bash
git clone https://github.com/Agentopia/AIAgentopia.git
cd AIAgentopia/agents/ai-music-agent
```

### 2. Configure Environment
```bash
# Copy the environment template
cp .env.example .env

# Edit .env file with your API keys
# OPENAI_API_KEY=your_openai_api_key_here
# MODELSLAB_API_KEY=your_modelslab_api_key_here
```

### 3. Build and Run
```bash
# Build the Docker image
docker build -t agentopia/ai-music-agent:latest .

# Run the container
docker run -d \
  --name ai-music-agent \
  -p 8501:8501 \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/generated_music:/app/generated_music \
  --restart unless-stopped \
  agentopia/ai-music-agent:latest
```

### 4. Access the Application
Open your browser and navigate to: http://localhost:8501

## 📋 Detailed Instructions

### Building the Image

The Dockerfile is optimized for production use with the following features:
- **Security**: Runs as non-root user `agentopia`
- **Health Checks**: Built-in health monitoring
- **Optimized**: Multi-stage build with minimal dependencies
- **Environment**: Supports `.env` file mounting

```bash
# Build with specific tag
docker build -t agentopia/ai-music-agent:v1.1.0 .

# Build with build arguments (if needed)
docker build --build-arg PYTHON_VERSION=3.11 -t agentopia/ai-music-agent:latest .
```

### Running Options

#### Production Deployment
```bash
docker run -d \
  --name ai-music-agent \
  -p 8501:8501 \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/generated_music:/app/generated_music \
  --restart unless-stopped \
  --memory=1g \
  --cpus=1.0 \
  agentopia/ai-music-agent:latest
```

#### Development Mode
```bash
# Interactive mode with auto-removal
docker run -it --rm \
  -p 8501:8501 \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/generated_music:/app/generated_music \
  -v $(pwd)/app:/app/app \
  agentopia/ai-music-agent:latest
```

#### Debug Mode
```bash
# Run with bash shell for debugging
docker run -it --rm \
  -p 8501:8501 \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/generated_music:/app/generated_music \
  agentopia/ai-music-agent:latest /bin/bash
```

### Volume Mounting

The container uses two important volumes:

1. **Environment File**: `-v $(pwd)/.env:/app/.env`
   - Mounts your local `.env` file with API keys
   - Keeps sensitive data outside the container

2. **Generated Music**: `-v $(pwd)/generated_music:/app/generated_music`
   - Persists generated music files on your host system
   - Allows access to files after container restarts

### Environment Variables

You can also pass environment variables directly:

```bash
docker run -d \
  --name ai-music-agent \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your_key_here \
  -e MODELSLAB_API_KEY=your_key_here \
  -v $(pwd)/generated_music:/app/generated_music \
  agentopia/ai-music-agent:latest
```

## 🔧 Management Commands

### Container Management
```bash
# Check container status
docker ps

# View logs
docker logs ai-music-agent

# Follow logs in real-time
docker logs -f ai-music-agent

# Stop the container
docker stop ai-music-agent

# Start the container
docker start ai-music-agent

# Restart the container
docker restart ai-music-agent

# Remove the container
docker rm ai-music-agent
```

### Health Checks
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' ai-music-agent

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' ai-music-agent
```

### Resource Monitoring
```bash
# Monitor resource usage
docker stats ai-music-agent

# View detailed container information
docker inspect ai-music-agent
```

## 🚀 Docker Compose (Optional)

For easier management, you can use Docker Compose:

```yaml
# docker-compose.yml
version: '3.8'

services:
  ai-music-agent:
    build: .
    container_name: ai-music-agent
    ports:
      - "8501:8501"
    volumes:
      - ./.env:/app/.env
      - ./generated_music:/app/generated_music
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

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## 🔒 Security Considerations

1. **Non-Root User**: Container runs as `agentopia` user
2. **Environment Files**: Keep `.env` files secure and never commit them
3. **Network**: Only expose necessary ports (8501)
4. **Updates**: Regularly update the base image for security patches

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Use a different port
   docker run -p 8502:8501 agentopia/ai-music-agent:latest
   ```

2. **Permission Issues**
   ```bash
   # Ensure proper ownership of mounted directories
   sudo chown -R $USER:$USER generated_music/
   ```

3. **API Key Issues**
   ```bash
   # Verify environment file is properly mounted
   docker exec ai-music-agent cat /app/.env
   ```

4. **Health Check Failures**
   ```bash
   # Check if Streamlit is running
   docker exec ai-music-agent ps aux | grep streamlit
   ```

### Logs and Debugging
```bash
# View application logs
docker logs ai-music-agent

# Access container shell
docker exec -it ai-music-agent /bin/bash

# Check Streamlit process
docker exec ai-music-agent ps aux
```

## 📊 Performance Optimization

### Resource Limits
```bash
# Run with resource constraints
docker run -d \
  --name ai-music-agent \
  -p 8501:8501 \
  --memory=2g \
  --cpus=2.0 \
  --memory-swap=2g \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/generated_music:/app/generated_music \
  agentopia/ai-music-agent:latest
```

### Multi-Stage Builds
The Dockerfile uses optimized practices:
- Minimal base image (python:3.11-slim)
- Efficient layer caching
- Security-focused user management
- Health check integration

## 🔄 Updates and Maintenance

### Updating the Container
```bash
# Pull latest image
docker pull agentopia/ai-music-agent:latest

# Stop current container
docker stop ai-music-agent

# Remove old container
docker rm ai-music-agent

# Run new container
docker run -d \
  --name ai-music-agent \
  -p 8501:8501 \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/generated_music:/app/generated_music \
  --restart unless-stopped \
  agentopia/ai-music-agent:latest
```

### Cleanup
```bash
# Remove unused images
docker image prune

# Remove all stopped containers
docker container prune

# Complete cleanup (use with caution)
docker system prune -a
```

---

For more information, visit the [AI Music Agent documentation](README.md) or the [Agentopia project](https://github.com/Agentopia/AIAgentopia).
