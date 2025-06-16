# Agentopia: Vision & Plan

## 1. Introduction: Agentopia - A Happy Place for AI Agents
*   **Our Mission:** To empower users with powerful and accessible AI agents.
*   **Core Value Proposition:** Delivering innovative AI tools while championing user data privacy, control, and transparency. Agentopia aims to be a trusted resource where users can confidently discover, understand, and utilize AI agents.

## 2. Guiding Principles
*   **Principle 1: Absolute User Data Privacy.**
    *   Commitment: User data stays with the user. Agents are designed to operate without requiring users to upload private data to Agentopia's or third-party servers (excluding user-chosen LLM providers).
    *   Mechanism: Primarily through local execution of agents.
*   **Principle 2: User Control & Empowerment.**
    *   Execution: Users run agents in their own local environments.
    *   Credentials: Users manage their own API keys for any external services (like LLMs) that agents might use.
    *   Data Flow: Users control the data inputs and outputs.
*   **Principle 3: Transparency & Openness.**
    *   Clarity: Clear documentation on how each agent works, its data requirements, and configuration.
    *   Access: Wherever feasible, provide access to understand the agent's source code or core logic.
*   **Principle 4: Simplicity & Ease of Use.**
    *   Accessibility: Strive to make agent setup and operation straightforward, primarily through containerization (Docker).
    *   Guidance: Provide clear, comprehensive instructions.
*   **Principle 5: No Hidden Costs or "Gotchas".**
    *   Honesty: Agent capabilities, requirements (e.g., needing an LLM API key), and operational model will be stated upfront.

## 3. The Agentopia Operational Model
*   **Agent Discovery & Information:**
    *   `agentopia.github.io`: The public portal for showcasing agents, providing detailed information, and linking to resources.
    *   `AIAgentopia` (GitHub Repository): The development hub, containing agent manifests, source code (or links), and development guidelines.
*   **Primary Agent Delivery: Local, Containerized Execution.**
    *   **Technology:** Docker will be the primary method for packaging and distributing agents.
    *   **Benefits:** Ensures portability, manages dependencies, and provides a consistent execution environment on the user's machine.
    *   **User Workflow:**
        1.  Discover agent on the Agentopia portal.
        2.  Follow instructions to pull the agent's Docker image.
        3.  Configure and run the agent locally using Docker commands.
*   **Data Management:**
    *   Agents are designed to process data residing on the user's local system.
    *   Input/output is typically handled via Docker volume mounts or by agents interacting with the user's local filesystem as permitted by the container setup.
*   **LLM Integration (If an agent uses Large Language Models):**
    *   Agents will **not** use centrally managed or Agentopia-provided LLM instances for user tasks.
    *   Users will configure agents with their **own LLM API keys** (e.g., OpenAI, Anthropic) or point them to their **own local LLM instances** (e.g., Ollama, LM Studio).
    *   This ensures users control LLM usage, costs, and choice of models (where supported by the agent).
*   **Local Persistence (Databases/Storage):**
    *   If an agent requires persistent storage (e.g., for its own operational database or user-generated content), it should be designed to use local solutions (e.g., SQLite within the container, or data stored in mounted volumes).

## 4. Agent Demonstrations & Source Code Access
*   **Interactive Demos (e.g., via Hugging Face Spaces with Gradio):**
    *   **Purpose:** To offer a quick, web-based way for users to experience an agent's functionality with sample or non-sensitive data.
    *   **Important Clarification:** These online demos are for illustrative purposes. For use with private or sensitive data, users **must** use the locally runnable Docker version of the agent. This will be clearly communicated.
*   **Source Code Exploration (e.g., via Google Colab, GitHub links):**
    *   **Purpose:** To promote transparency and allow users to understand the agent's inner workings.
    *   This aligns with the principle of openness and allows for community learning and potential contributions.

## 5. Agent Development on Agentopia
*   Agent developers contributing to Agentopia are expected to align with these principles.
*   Manifests (`agent.json`) must be detailed and accurately reflect the agent's architecture, data handling, configuration, and LLM usage model.
*   Comprehensive setup instructions, especially for Docker-based execution, are paramount.
*   Refer to the [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed development guidelines.

## 6. Our Commitment to the Future
*   Agentopia will continue to evolve, always prioritizing these core principles of user privacy, control, and transparency.
*   We aim to foster a vibrant ecosystem of useful, safe, and respectful AI agents.
