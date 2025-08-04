# Web Scraper Agent - Product Requirements Document (PRD)

**Version:** 1.0
**Date:** August 4, 2025
**Status:** Draft

---

## 1. Overview

### 1.1 Agent Purpose and Goals
The Web Scraper Agent is an AI-powered web scraping tool that enables users to extract and analyze content from websites using natural language prompts. The agent combines modern web scraping technology (Playwright) with Large Language Models (LLMs) to provide intelligent, context-aware content extraction.

### 1.2 Target Audience
- **Data Analysts** seeking to extract structured information from websites
- **Researchers** needing to gather content from multiple web sources
- **Content Creators** looking to analyze competitor websites
- **Developers** requiring automated web content extraction
- **Business Intelligence Teams** monitoring web-based data sources

### 1.3 Key Features
- **Unified LLM Support**: Seamless integration of both OpenAI API and local Ollama models
- **Intelligent Content Extraction**: AI-powered analysis and summarization of web content
- **Dynamic Model Selection**: Real-time listing and selection of available models
- **Flexible Authentication**: Support for environment variables and UI-based API key management
- **Anti-Bot Protection Handling**: Built-in strategies for common web scraping challenges
- **Agentopia UI Integration**: Consistent branding and user experience

---

## 2. Technical Specifications

### 2.1 System Architecture

#### Core Components
- **Frontend**: Streamlit-based web interface with Agentopia UI components
- **Backend**: Python application using scrapegraphai library
- **Browser Engine**: Playwright for web automation and content extraction
- **LLM Integration**: Dual support for OpenAI API and local Ollama models
- **Configuration Management**: Environment-based and UI-based settings

#### Technology Stack
- **Framework**: Streamlit 1.47+
- **Web Scraping**: scrapegraphai 1.61+, Playwright 1.53+
- **LLM Integration**: OpenAI API, Ollama local models
- **UI Components**: Custom Agentopia design system
- **Environment Management**: python-dotenv for configuration

### 2.2 Dependencies
```
streamlit>=1.28.0
scrapegraphai>=1.0.0
playwright>=1.40.0
python-dotenv>=1.0.0
requests>=2.31.0
validators>=0.22.0
loguru>=0.7.0
```

### 2.3 Integration Points
- **OpenAI API**: Direct integration for cloud-based LLM processing
- **Ollama**: Local model integration via REST API (localhost:11434)
- **Playwright**: Browser automation for content extraction
- **Agentopia Portal**: Standardized agent manifest and deployment

---

## 3. User Flows

### 3.1 Main Workflow
1. **Model Selection**: User selects between OpenAI or Ollama models
2. **Authentication**: API key provided via environment or UI input
3. **Target Configuration**: User enters website URL to scrape
4. **Prompt Definition**: Natural language description of desired extraction
5. **Execution**: Agent launches browser, extracts content, and processes with LLM
6. **Results Display**: Structured output presented in JSON format

### 3.2 Input Specifications
- **URL**: Valid HTTP/HTTPS website URL
- **Prompt**: Natural language description (e.g., "Extract product features and pricing")
- **Model Selection**: Dropdown with available OpenAI and Ollama models
- **API Key**: Optional if provided via environment variables

### 3.3 Output Specifications
- **Format**: JSON structure with extracted content
- **Content**: AI-analyzed and summarized information based on user prompt
- **Metadata**: Processing time, model used, success/error status
- **Error Handling**: Detailed error messages with troubleshooting guidance

### 3.4 Error Handling
- **Network Issues**: Retry mechanisms and timeout handling
- **Anti-Bot Protection**: Detection and user notification with workaround suggestions
- **LLM Failures**: Fallback strategies and clear error reporting
- **Invalid URLs**: Input validation and user feedback
- **Model Unavailability**: Dynamic model checking and user notification

---

## 4. Configuration

### 4.1 Environment Variables
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_LLM_MODEL=gpt-3.5-turbo

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Scraping Configuration
SCRAPING_TIMEOUT=30
MAX_RETRY_ATTEMPTS=3
USER_AGENT=Mozilla/5.0 (compatible; AgentopiaBot/1.0)

# Security Configuration
ENABLE_STEALTH_MODE=true
RESPECT_ROBOTS_TXT=true
```

### 4.2 Required Services
- **Ollama** (for local model support): Must be running on localhost:11434
- **Internet Connection**: Required for OpenAI API and web scraping
- **Playwright Browsers**: Chromium, Firefox, and WebKit binaries

### 4.3 Security Considerations
- **API Key Protection**: Environment variables preferred over UI input
- **Rate Limiting**: Built-in delays to respect website resources
- **User-Agent Management**: Configurable browser identification
- **Robots.txt Compliance**: Optional respect for website scraping policies

---

## 5. User Interface Design

### 5.1 Layout Structure
- **Sidebar**: Model selection, API key management, configuration options
- **Main Panel**: URL input, prompt input, results display
- **Header**: Agentopia branding and agent identification
- **Footer**: Privacy notice and support links

### 5.2 Model Selection Interface
- **Provider Toggle**: Radio buttons for OpenAI vs. Ollama
- **Model Dropdown**: Dynamic list of available models
  - OpenAI: gpt-3.5-turbo, gpt-4, gpt-4-turbo, etc.
  - Ollama: Real-time query of locally available models
- **Model Status**: Indicators for model availability and health

### 5.3 API Key Management
- **Environment Detection**: Automatic loading from .env file
- **UI Input**: Secure password field for manual entry
- **Status Indicator**: Visual confirmation of valid API key
- **Priority**: Environment variables take precedence over UI input

### 5.4 Results Display
- **JSON Viewer**: Formatted, collapsible JSON output
- **Copy Functionality**: One-click copying of results
- **Export Options**: Save results to file
- **Processing Indicators**: Loading spinners and progress feedback

---

## 6. Deployment

### 6.1 System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **Memory**: Minimum 4GB RAM, 8GB recommended
- **Storage**: 2GB free space for dependencies and browser binaries
- **Network**: Internet connection for API access and web scraping

### 6.2 Installation Steps
1. **Environment Setup**: Create and activate Python virtual environment
2. **Dependencies**: Install requirements via `pip install -r requirements.txt`
3. **Browser Setup**: Run `playwright install` for browser binaries
4. **Configuration**: Set up `.env` file with API keys and preferences
5. **Ollama Setup** (optional): Install and configure local models
6. **Launch**: Start application with `streamlit run app/web_scraper.py`

### 6.3 Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt && playwright install
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app/web_scraper.py", "--server.port=8501"]
```

### 6.4 Configuration Management
- **Environment Files**: `.env` for local development
- **Docker Secrets**: Secure API key management in containers
- **Health Checks**: Endpoint monitoring for deployment validation
- **Logging**: Structured logging for debugging and monitoring

---

## 7. Integration Roadmap

### 7.1 Current State (Phase 1)
- ✅ Separate OpenAI and Ollama implementations validated
- ✅ Core scraping functionality working
- ✅ Windows compatibility issues resolved
- ✅ Agentopia UI components integrated

### 7.2 Phase 2: Unification (Next Sprint)
- [ ] **Unified Application**: Merge separate implementations into single app
- [ ] **Dynamic Model Discovery**: Real-time querying of available models
- [ ] **Enhanced Configuration**: Comprehensive settings management
- [ ] **Improved Error Handling**: Better user feedback and recovery
- [ ] **JSON Output Parsing**: Fix malformed JSON response handling

### 7.3 Phase 3: Enhancement (Future)
- [ ] **Batch Processing**: Multiple URL scraping in single session
- [ ] **Result Export**: CSV, Excel, and other format support
- [ ] **Scheduling**: Automated periodic scraping
- [ ] **Advanced Anti-Bot**: Stealth mode and proxy support
- [ ] **Custom Prompts**: Template library for common use cases

### 7.4 Phase 4: Enterprise Features
- [ ] **Team Collaboration**: Shared configurations and results
- [ ] **API Access**: RESTful API for programmatic access
- [ ] **Audit Logging**: Comprehensive usage tracking
- [ ] **Enterprise SSO**: Integration with corporate authentication
- [ ] **Compliance Tools**: GDPR and data protection features

---

## 8. Success Criteria

### 8.1 Functional Requirements
- [ ] Successfully scrape content from 95% of tested websites
- [ ] Support both OpenAI and Ollama models seamlessly
- [ ] Process user prompts and return structured results
- [ ] Handle common anti-bot protections gracefully
- [ ] Maintain consistent Agentopia UI/UX standards

### 8.2 Performance Requirements
- [ ] Average scraping time under 30 seconds per URL
- [ ] Support concurrent users (minimum 10 simultaneous sessions)
- [ ] Memory usage under 1GB during normal operation
- [ ] 99% uptime for deployed instances

### 8.3 User Experience Requirements
- [ ] Intuitive model selection and configuration
- [ ] Clear error messages with actionable guidance
- [ ] Responsive UI with loading indicators
- [ ] One-click result copying and export
- [ ] Consistent branding with Agentopia ecosystem

### 8.4 Technical Requirements
- [ ] Cross-platform compatibility (Windows, macOS, Linux)
- [ ] Docker containerization support
- [ ] Comprehensive error logging and monitoring
- [ ] Secure API key management
- [ ] Automated testing coverage >80%

---

## 9. Risk Assessment

### 9.1 Technical Risks
- **Anti-Bot Evolution**: Websites may implement stronger protections
- **Model Compatibility**: Changes in OpenAI API or Ollama interfaces
- **Browser Dependencies**: Playwright updates may require adjustments
- **Performance Scaling**: Memory usage with large-scale scraping

### 9.2 Mitigation Strategies
- **Adaptive Scraping**: Multiple strategies for different protection types
- **Version Pinning**: Controlled dependency updates with testing
- **Graceful Degradation**: Fallback options for failed components
- **Resource Monitoring**: Proactive memory and performance tracking

---

## 10. Appendices

### 10.1 Code Review Findings
Based on the comprehensive code review conducted during the transfer phase:
- Core functionality successfully validated with both model types
- Windows-specific asyncio issues identified and resolved
- Playwright browser binary requirements documented
- JSON parsing improvements identified for future enhancement

### 10.2 Reference Architecture
The unified Web Scraper Agent will consolidate the proven architectures of both existing variants while adding dynamic model selection and enhanced configuration management.

### 10.3 Change Log
- **v1.0** (August 4, 2025): Initial PRD creation based on transfer phase validation

---

**Document Prepared By:** Cascade AI Assistant
**Review Status:** Pending stakeholder review
**Next Review Date:** TBD
