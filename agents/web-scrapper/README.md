# Web Scraper Agent 🕵️‍♂️

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
