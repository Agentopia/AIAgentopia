# AI Music Agent

An AI-powered music generation agent that creates custom music tracks based on user prompts using ModelsLab API and OpenAI GPT-4.

## Overview

The AI Music Agent is a Streamlit-based web application that enables users to generate high-quality music tracks through natural language prompts. By combining the power of OpenAI's GPT-4 for prompt enhancement and ModelsLab's music generation API, users can create diverse musical compositions ranging from classical pieces to modern electronic tracks.

## Features

- **🎵 Text-to-Music Generation**: Convert detailed text prompts into high-quality music tracks
- **🎧 Real-time Playback**: Listen to generated music directly in the browser
- **📥 Download Support**: Save generated music as MP3 files
- **🎨 Custom Prompt Engineering**: Detailed instructions for genre, instruments, mood, and structure
- **🔒 Secure API Integration**: User-provided API keys with password-masked input
- **⚡ Real-time Feedback**: Loading indicators and comprehensive error handling

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ModelsLab API key ([Get one here](https://modelslab.com/dashboard/api-keys))

### Installation

#### Option 1: Docker Deployment (Recommended)

1. **Pull and run the Docker image**:
   ```bash
   docker run -d --name ai-music-agent -p 8501:8501 agentopia/ai-music-agent:latest
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Enter your API keys** in the sidebar and start generating music!

For advanced Docker usage, environment variables, and volume mounting, see [DOCKER.md](DOCKER.md).

#### Option 2: Local Python Installation

1. **Navigate to the agent directory**:
   ```bash
   cd agents/ai-music-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app/music_generator.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

### Usage

1. **Enter API Keys**: In the sidebar, provide your OpenAI and ModelsLab API keys
2. **Create a Prompt**: Describe the music you want to generate (genre, instruments, mood, etc.)
3. **Generate Music**: Click "Generate Music" and wait for the AI to create your track
4. **Listen & Download**: Play the generated music and download it as an MP3 file

## Example Prompts

- "Generate a 30 second classical music piece with piano and strings, peaceful and contemplative"
- "Create an upbeat electronic dance track with synthesizers and a driving beat"
- "Compose a jazz ballad with saxophone, piano, and soft drums in a minor key"
- "Generate ambient background music with nature sounds and soft melodies"

## Technical Details

- **Framework**: Streamlit for web interface
- **AI Framework**: Agno for agent orchestration
- **LLM**: OpenAI GPT-4o for prompt enhancement
- **Music Generation**: ModelsLab API for audio synthesis
- **Output Format**: MP3 audio files
- **Storage**: Local filesystem with UUID-based naming
- **Deployment**: Docker containerization with security best practices
- **Container**: Non-root user, health checks, optimized build context

## Configuration

The agent uses the following key configurations:
- **Model**: GPT-4o for language processing
- **Output Format**: MP3 audio files
- **File Storage**: `audio_generations/` directory
- **Debug Mode**: Enabled for development

## API Requirements & Setup

This agent requires two API keys. You can configure them using environment variables (recommended) or enter them manually in the sidebar.

### Method 1: Environment Variables (Recommended)

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your actual API keys:
   ```bash
   # Required API Keys
   OPENAI_API_KEY=sk-your-actual-openai-key-here
   MODELSLAB_API_KEY=your-actual-modelslab-key-here

   # Optional Configuration
   DEBUG_MODE=false
   AUDIO_OUTPUT_DIR=audio_generations
   ```

3. **Restart the application** - your keys will be loaded automatically!

### Method 2: Manual Entry

If you prefer not to use environment variables, you can enter your API keys directly in the sidebar when the app is running.

### Getting Your API Keys

1. **OpenAI API Key**
   - Used for GPT-4 model access and prompt enhancement
   - Sign up at [OpenAI Platform](https://platform.openai.com/api-keys)
   - Keys start with `sk-` and are required for AI-powered features

2. **ModelsLab API Key**
   - Used for music generation API access
   - Sign up at [ModelsLab Dashboard](https://modelslab.com/dashboard/api-keys)
   - Required for converting prompts to audio files

### Security Notes

- ✅ The `.env` file is automatically excluded from version control
- ✅ API keys are validated for proper format before use
- ✅ Keys loaded from `.env` are never displayed in the UI
- ⚠️ Never commit your `.env` file or share your API keys publicly

## Privacy & Security

- **User-Controlled**: All API keys are provided by the user
- **No Data Storage**: API keys are not stored permanently
- **Local Files**: Generated music is saved locally on your machine
- **Secure Input**: API keys are masked in the interface

## Limitations

- Requires internet connection for API access
- Depends on external service availability
- API rate limits may apply based on your subscription
- Music quality depends on prompt specificity and detail

## Development Roadmap

The AI Music Agent follows a phased development approach with clear milestones and priorities. See the complete [PRD](docs/PRD.md) for detailed action checklists.

### Phase 1: Agentopia Integration & Standardization ✅ *Complete*
- [x] UI/UX standardization with Agentopia components
- [x] Environment variable configuration management
- [x] Code quality improvements and comprehensive error handling
- [x] Comprehensive inline code documentation
- [x] Agentopia schema validation compliance
- [x] Docker containerization with security best practices
- [x] Production code cleanup and debug message removal
- [x] Portal integration with proper Docker run commands
- [ ] Testing framework implementation *(intentionally skipped for simplicity)*

### Phase 2: Enhanced Privacy & Local-First Features
- [ ] Local LLM integration (Ollama support)
- [ ] Advanced configuration options and quality settings
- [ ] Offline capabilities and local caching
- [ ] Batch generation and automation features

### Phase 3: Advanced Features & User Experience
- [ ] Music management and basic editing tools
- [ ] Style transfer and variation generation
- [ ] Community features and template sharing
- [ ] RESTful API and CLI interface

### Phase 4: Professional & Commercial Features
- [ ] High-quality audio formats and professional metadata
- [ ] Commercial licensing integration and compliance
- [ ] Enterprise features and multi-user support
- [ ] Custom branding and white-label options

**Current Status:** Phase 1 is complete with full Agentopia compliance achieved. The agent now passes schema validation, features comprehensive documentation, and is production-ready. Ready to begin Phase 2 development or community deployment.

**Development Principles:** Incremental development, user feedback integration, backward compatibility, documentation-first approach, and privacy-first enhancements.

## Contributing

This agent is part of the Agentopia ecosystem. For contribution guidelines, please refer to the main [CONTRIBUTING.md](../../CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE.md](../../LICENSE.md) file for details.

## Support

For issues, questions, or contributions, please refer to the main Agentopia repository or create an issue in the project's GitHub repository.
