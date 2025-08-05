# Web Scraper Agent

**Version:** `1.1.0`
**Category:** `Data Analysis & Research`
**Maintainer:** `Agentopia Team`

---

## Overview

The Web Scraper Agent is a production-ready, unified application that combines AI language models with advanced web scraping capabilities. It features a clean Streamlit interface with dynamic provider selection between cloud-based OpenAI and privacy-focused local Ollama deployments. The agent uses intelligent error handling, memory-efficient model support, and professional Agentopia branding to deliver enterprise-grade web scraping functionality.

## Features

*   **Unified Application:** Single interface with dynamic LLM provider selection.
*   **Dual LLM Support:** Works with both OpenAI API (cloud) and local Ollama instances.
*   **Professional UI:** Clean, branded Streamlit interface for a great user experience.
*   **Natural Language Prompts:** Use plain English to describe the data you want to extract.
*   **Intelligent Content Extraction:** Leverages LLMs to understand and extract specific data points from complex web pages.
*   **Memory-Efficient:** Supports smaller local models like `llama3.2:1b` for systems with limited resources.
*   **Smart Error Handling:** Provides clear guidance for common issues like missing API keys or unavailable local models.
*   **Privacy-Focused:** Local Ollama support ensures your data and prompts never leave your machine.

## Tech Stack

*   **Core Framework:** Streamlit
*   **Primary Language:** Python
*   **Key Libraries/Dependencies:** Playwright, scrapegraphai, requests, streamlit
*   **LLM(s) Used:** OpenAI (GPT-3.5-Turbo, GPT-4), Ollama (Llama3.2, Gemma2, etc.)

## Directory Structure

```
web-scraper/
├── app/                     # Core source code
│   ├── web_scraper.py       # Main application entry point
│   └── ui_components.py     # Reusable Streamlit UI components
├── docs/                    # Agent-specific detailed documentation
│   └── PRD.md               # Product Requirements Document
├── .env.example             # Example environment variables file
├── agent.json               # Agent manifest file
├── Dockerfile               # Docker configuration for deployment
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Prerequisites

*   Python 3.8+
*   Docker (for containerized deployment)
*   An OpenAI API key (if using the OpenAI provider)
*   A running Ollama instance (if using the Ollama provider). See [ollama.ai](https://ollama.ai/) for setup instructions.

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Agentopia/AIAgentopia.git
cd AIAgentopia/agents/web-scraper
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Configure Environment Variables

Copy the example environment file. This step is only required if you want your OpenAI API key to persist.

```bash
cp .env.example .env
```

Then, edit `.env` with your API key.

**Required Environment Variables:**
*   `OPENAI_API_KEY`: Your secret key for the OpenAI API.

## Usage

Run the Streamlit application:

```bash
streamlit run app/web_scraper.py
```

Then, open your browser to `http://localhost:8501`.

## Docker Deployment

For a consistent and isolated environment, you can run the agent using Docker.

### Simple Command (Recommended)
This is the simplest way to get the agent running. After launching, you can enter your API key in the web interface.
```bash
docker run -d --name web-scraper-agent -p 8501:8501 agentopia/web-scraper-agent:latest
```

### Advanced Command (with Persistent API Key)
For convenience, you can mount your local `.env` file to securely provide your API key.
```bash
docker run -d --name web-scraper-agent -p 8501:8501 -v /path/to/your/.env:/app/.env agentopia/web-scraper-agent:latest
```

## Troubleshooting

*   **Issue:** `Ollama provider is unavailable.`
    *   **Solution:** Ensure your local Ollama application is running. If it is, make sure the model you want to use (e.g., `llama3.2:1b`) has been pulled with `ollama pull <model_name>`.
*   **Issue:** `Playwright browser not found.`
    *   **Solution:** Make sure you have run `playwright install chromium` after installing the Python requirements.

## Roadmap / Future Enhancements

*   Advanced anti-bot and anti-scraping measures
*   A comprehensive automated testing suite
*   Support for more LLM providers

## License

This agent is licensed under the [MIT License](../../../LICENSE).


An intelligent web scraping agent that uses AI to extract specific information from websites. Built with Streamlit and powered by advanced language models.

## 🌟 Features

- **Dual LLM Support**: Choose between OpenAI API (GPT-3.5/GPT-4) or local Ollama (Llama 3.2)
- **Intelligent Scraping**: AI-powered content extraction based on natural language prompts
- **User-Friendly Interface**: Clean Streamlit web interface with Agentopia styling
- **Flexible Configuration**: Environment-based configuration with fallback options
- **Docker Ready**: Containerized deployment for easy setup and scaling

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
# Pull and run the container
docker run -d --name web-scraper-agent -p 8501:8501 agentopia/web-scraper-agent:latest
```

### Option 2: Local Installation
```bash
# Clone the repository
git clone <repository-url>
cd agents/web-scraper

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your API keys and preferences
# Run the application
streamlit run app/ai_scrapper.py
```

## ⚙️ Configuration

Copy `.env.example` to `.env` and configure:

- **OpenAI API Key**: For cloud-based scraping with GPT models
- **Ollama Settings**: For local LLM deployment
- **Model Selection**: Choose your preferred LLM model
- **Scraping Options**: Timeout, retries, and other settings

## 📖 Usage

1. **Launch the application** via Docker or local installation
2. **Configure your LLM**: Choose between OpenAI API or local Ollama
3. **Enter target URL**: Provide the website you want to scrape
4. **Describe what to extract**: Use natural language to specify what information you need
5. **Get results**: The AI agent will intelligently extract and present the requested data

## 🏗️ Architecture

- **Frontend**: Streamlit with Agentopia UI components
- **Backend**: Python with scrapegraphai library
- **LLM Integration**: Configurable OpenAI API or local Ollama
- **Web Engine**: Playwright for robust web scraping

## 📁 Project Structure

```
web-scraper/
├── sample/              # Original reference implementation
├── app/                 # Agentopia-compliant application
│   ├── ai_scrapper.py  # Main application entry point
│   └── ui_components.py # Standardized UI components
├── docs/               # Comprehensive documentation
├── agent.json          # Agent manifest
├── requirements.txt    # Dependencies
├── Dockerfile         # Container configuration
├── .env.example       # Environment template
└── README.md          # This file
```

## 🔒 Privacy & Security

- **Local-First**: Option to run completely locally with Ollama
- **API Key Security**: Secure handling of API credentials
- **No Data Persistence**: Stateless operation for privacy
- **User Control**: You control all data and credentials

## 🤝 Contributing

This agent is part of the Agentopia ecosystem. See the main repository for contribution guidelines.

## 📄 License

[License information to be added]

## 🆘 Support

For issues and support, please refer to the documentation in the `/docs` directory or create an issue in the main Agentopia repository.

---

**Part of the Agentopia AI Agent Ecosystem** 🤖
