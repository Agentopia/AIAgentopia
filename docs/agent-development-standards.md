# AIAgentopia: Agent Development Standards

**Version:** 1.0.0
**Last Updated:** June 15, 2025

## 1. Introduction

This document outlines the standards, best practices, and mandatory requirements for developing AI agents within the AIAgentopia ecosystem. Adhering to these standards ensures consistency, maintainability, and interoperability of agents.

This guide is intended for all developers contributing agents to the AIAgentopia repository.

## 2. Guiding Principles

*   **Modularity & Isolation:** Agents should be self-contained units, minimizing dependencies on other agents' internal implementations.
*   **Consistency:** Follow established patterns for directory structure, documentation, and manifests to enhance navigability and understanding.
*   **Discoverability:** Agent metadata (via `agent.json`) should be comprehensive and accurate to support the Agentopia portal and other discovery mechanisms.
*   **Quality & Reliability:** Agents should be well-tested and robust.
*   **Security:** Follow security best practices in development and deployment.

## 3. Mandatory Agent Structure

Each agent must reside in its own directory under `AIAgentopia/agents/{agent-name}/` and follow this structure:

```
agents/
└── {agent-name}/
    ├── app/                     # Core source code of the agent
    │   └── main.py              # Primary entry point (or equivalent, e.g., app.py for Streamlit/FastAPI)
    │   └── ...                  # Other modules, packages, and agent logic
    ├── tests/                   # Unit, integration, and other tests for the agent
    ├── docs/                    # Agent-specific detailed documentation
    │   ├── PRD.md               # Product Requirements Document
    │   ├── architecture.md      # Agent's internal architecture
    │   └── ...                  # Other docs like API reference, deployment notes
    ├── .env.example             # Example environment variables file
    ├── agent.json               # **MANDATORY:** Agent manifest file (see Section 4)
    ├── Dockerfile               # **MANDATORY (for deployable agents):** Docker configuration
    ├── requirements.txt         # **MANDATORY:** Python dependencies with pinned versions
    ├── README.md                # **MANDATORY:** Agent overview, setup, usage (see Section 5.1)
    └── ...                      # Other necessary config files, static assets, etc.
```

Refer to [Agent Framework Considerations](./agent-framework-consideration.md) for guidance on integrating different development frameworks.

## 4. Agent Manifest (`agent.json`)

*   Every agent **MUST** have an `agent.json` file in its root directory.
*   This manifest **MUST** validate against the [agent-manifest.schema.json](../../agent-manifest.schema.json).
*   Consult the [Manifest Schema Guide](./manifest-schema-guide.md) for detailed explanations of each field.
*   Keep the manifest accurate and up-to-date as the agent evolves.

## 5. Documentation Standards

### 5.1. Agent `README.md`
*   Each agent **MUST** have a `README.md` in its root directory.
*   This README should follow the structure provided in the [readme-template.md](../../templates/agent-docs/readme-template.md).
*   It serves as the primary entry point for understanding and using the agent.

### 5.2. Agent-Specific `/docs` Directory
*   Each agent **MUST** include a `/docs` directory for more detailed documentation.
*   Standard documents to include (if applicable):
    *   `PRD.md`: Product Requirements Document.
    *   `architecture.md`: Detailed internal architecture, data flows, component interactions.
    *   `api-reference.md`: If the agent exposes an API (e.g., OpenAPI specification).
    *   `deployment-guide.md`: Specific deployment considerations or steps.
    *   `setup-dev-environment.md`: Advanced or specific development setup notes.
*   Templates for these documents may be provided in the top-level `AIAgentopia/templates/agent-docs/` directory.

### 5.3. Code Comments
*   Write clear and concise comments for complex logic, public APIs, and non-obvious code sections.
*   Use docstrings for all public modules, classes, and functions, following PEP 257.

## 6. Dependency Management

*   Each agent **MUST** have a `requirements.txt` file listing all Python dependencies with pinned versions (e.g., `library==1.2.3`).
*   Virtual environments are **MANDATORY** for local development to isolate dependencies.
*   See [Agent Framework Considerations](./agent-framework-consideration.md) for more on managing dependencies with different frameworks.

## 7. Coding Standards & Quality

*   **Linters & Formatters:** Use `ruff` for both linting and formatting Python code. Configurations are provided at the repository root (`pyproject.toml` and `.pre-commit-config.yaml`).
*   **Type Hinting:** Use Python type hints (PEP 484) for all new code.
*   **Error Handling:** Implement robust error handling. Log errors appropriately and provide clear feedback to users or calling systems.
*   **Security:** Follow general security best practices (e.g., input validation, avoid hardcoding secrets, sanitize outputs). Refer to `preferred-tech-stack-guidelines.md` for more.

## 8. Testing

*   Each agent should include tests in its `/tests` directory.
*   Strive for a reasonable level of test coverage, especially for core logic.
*   Include unit tests and, where appropriate, integration tests.
*   Tests should be runnable via a common command (e.g., `pytest` from the agent's root).

## 9. Configuration

*   Use environment variables for configuration that varies between deployments (e.g., API keys, external service URLs).
*   Provide a `.env.example` file in the agent's root directory, listing all required and optional environment variables with explanations.
*   Avoid hardcoding sensitive information.

## 10. Logging

*   Use the standard Python `logging` module.
*   Consider a structured logging format (e.g., JSON) for easier parsing by log management systems, especially for agents intended for production deployment.
*   Log important events, errors, and relevant operational information.
*   Avoid logging sensitive data (PII, API keys).

## 11. Containerization (Docker)

*   Agents intended for deployment as services **MUST** include a `Dockerfile`.
*   Follow Docker best practices: use official base images (e.g., `python:3.10-slim`), minimize layers, run as non-root user, ensure reproducibility.
*   The `Dockerfile` should build a self-contained, runnable image of the agent.
*   See [Agent Framework Considerations](./agent-framework-consideration.md) for Dockerfile examples.

## 12. Frontend / User Experience (UX)

*   For agents that include a user interface or demo:
    *   Strive for a consistent look and feel aligned with the Agentopia platform.
    *   Refer to the [Preferred Tech Stack Guidelines](./preferred-tech-stack-guidelines.md) for recommended frontend technologies (e.g., React + Tailwind CSS for rich UIs, Streamlit/Gradio for simpler demos).
    *   Ensure UIs are user-friendly and accessible.

## 13. Versioning

*   Use semantic versioning (MAJOR.MINOR.PATCH) for your agent, specified in `agent.json` and `README.md`.
*   Update the version appropriately upon new releases or significant changes.

## 14. Contribution Workflow

*   Follow the general [CONTRIBUTING.md](../../CONTRIBUTING.md) guidelines for the repository.
*   Ensure all standards in this document are met before submitting a Pull Request for a new agent or updates to an existing one.

## 15. Document Evolution

This document is a living guide. Suggestions for improvements are welcome via issues or pull requests to this file.

---

*Note on Templates: Standard templates for agent documentation (e.g., `README.md`, `PRD.md`) are located in the top-level `AIAgentopia/templates/agent-docs/` directory to keep all agent-related documentation templates organized.*
