# AI Music Agent Dockerfile
# Agentopia-compliant Docker image for AI Music Agent
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including curl for health checks
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and configuration
COPY app/ ./app/
COPY .env.example .
COPY README.md .

# Create directory for generated music files
RUN mkdir -p generated_music

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash agentopia
RUN chown -R agentopia:agentopia /app
USER agentopia

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app/music_generator.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
