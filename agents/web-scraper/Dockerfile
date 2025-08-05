# Web Scraper Agent Dockerfile
# Agentopia-compliant Docker image for Web Scraper Agent
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set an environment variable to indicate running in Docker
ENV RUNNING_IN_DOCKER=true

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash agentopia

# Copy requirements and install Python dependencies (as root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright's system dependencies (as root)
RUN playwright install-deps chromium

# Copy application code and configuration
COPY app/ ./app/
COPY .streamlit/ ./.streamlit/
COPY .env.example .
COPY README.md .

# Change ownership of the entire app directory to the new user
RUN chown -R agentopia:agentopia /app

# Switch to the non-root user
USER agentopia

# Install the Playwright browser itself (as the non-root user)
# This ensures it's stored in the correct user's cache directory
RUN playwright install chromium

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app/web_scraper.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
