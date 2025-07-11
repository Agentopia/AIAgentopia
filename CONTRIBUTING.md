# Contributing to AIAgentopia

Thank you for your interest in contributing to AIAgentopia! We welcome new agents, improvements, and ideas from the community. Your contributions help us grow and create a vibrant ecosystem of AI agents that run locally, respecting user privacy and control.

This document provides guidelines for contributing to the project. Please read it carefully to ensure a smooth and effective collaboration.

---

## 📜 Code of Conduct

AIAgentopia has adopted the **Contributor Covenant Code of Conduct**. All contributors are expected to adhere to it to foster an open, welcoming, and respectful community.

Please read the full text [here](CODE_OF_CONDUCT.md).

---

## 💖 Community Guidelines

In addition to the formal Code of Conduct, we encourage all community members to:

- Be welcoming and inclusive.
- Respect different perspectives and backgrounds.
- Offer and accept constructive feedback gracefully.
- Help others learn—no question is too basic!
- Celebrate progress and creativity together.

---

## 🌳 Branching Strategy: Feature Branches

To ensure the `main` branch remains stable and production-ready at all times, we follow a simple and effective feature branch workflow.

**Core Principles:**

1.  **`main` is the Source of Truth:** The `main` branch is our definitive, working version of the project. We never commit directly to it.
2.  **Create Branches for Everything:** For any new piece of work—whether it's developing a new agent, fixing a bug, or updating documentation—create a new, descriptively named branch from the latest version of `main`.
3.  **Use Descriptive Prefixes:** Name your branches using prefixes to keep them organized. This helps everyone understand the purpose of the branch at a glance.
    *   **`feature/`**: For new features or agents (e.g., `feature/new-research-agent`).
    *   **`fix/`**: For bug fixes (e.g., `fix/data-analyzer-ui-bug`).
    *   **`docs/`**: For documentation changes (e.g., `docs/update-contributing-guide`).
    *   **`refactor/`**: For code refactoring that doesn't add features or fix bugs.
    *   **`chore/`**: For maintenance tasks (e.g., updating dependencies).
4.  **Merge via Pull Request:** All changes must be merged into `main` through a Pull Request (PR). This allows for code review and discussion before changes are integrated.

This workflow is already reflected in the "General Contribution Workflow" section below.

---

## 🚀 General Contribution Workflow

Contributing to AIAgentopia involves a few key steps, whether you're adding a new agent, fixing a bug, or improving documentation.

### 1. Setting Up Your Environment

1.  **Fork this repository** to your own GitHub account.
2.  **Clone your fork** to your local machine:
    ```bash
    git clone https://github.com/YOUR_USERNAME/AIAgentopia.git
    cd AIAgentopia
    ```
3.  **Set up pre-commit hooks:** We use `ruff` for linting and formatting Python code, managed by `pre-commit`. This helps maintain code consistency.
    ```bash
    # Ensure you have pre-commit installed (e.g., pip install pre-commit)
    pre-commit install
    ```
    This will ensure your Python code is automatically formatted and linted before each commit.

### 2. Planning Your Contribution (Issue Tracking)

1.  **Check for existing issues:** Before starting work, please check the [Issues tab](https://github.com/Agentopia/AIAgentopia/issues) to see if someone else is already working on a similar idea or if a relevant issue already exists. If not, feel free to create one!
2.  **Follow our Issue & Milestone Organization:** For transparency and effective project management, we use a structured approach for tracking work, especially for larger features or new agents. Please refer to the **"Appendix: Issue & Milestone Organization Workflow"** at the end of this document for details on how we use Milestones, Cap/Epic Issues, and Sub-Issues.

### 3. Making Your Changes

1.  **Create a new branch** for your feature, agent, or fix. Choose a descriptive branch name (e.g., `feature/my-new-agent`, `fix/validator-bug`, `docs/update-contributing-guide`):
    ```bash
    git checkout -b feature/your-branch-name
    ```
2.  **Make your code changes,** add new files, or update documentation as planned.
3.  **Commit your changes** with clear and descriptive messages. Pre-commit hooks will run automatically to format and lint your code. If they report errors, please fix them before completing your commit.
    ```bash
    git add .
    git commit -m "feat: Add my new awesome agent framework"
    ```

### 4. Submitting Your Contribution

1.  **Push your branch** to your fork on GitHub:
    ```bash
    git push origin feature/your-branch-name
    ```
2.  **Open a Pull Request (PR)** against the `main` branch of the `Agentopia/AIAgentopia` repository.
3.  **Describe your PR:** Provide a clear title and a detailed description of the changes you've made. Explain the purpose of your contribution and reference any related issues (e.g., "Closes #123"). A good PR description helps reviewers understand your work quickly.
4.  **Engage in the review process:** Project maintainers will review your PR. Be prepared to discuss your changes and make further modifications if requested. We appreciate your patience and collaboration during this stage.

---

## 🤖 Agent Developer Guide

This guide provides a comprehensive, step-by-step walkthrough for developing and contributing a new AI agent to the Agentopia ecosystem. It integrates best practices, links to essential standards, and outlines the validation and review process.

### Phase 1: Conception & Planning

1.  **Define Your Agent's Purpose & Scope:**
    *   **Core Idea:** What problem will your agent solve? Who is the target user? What unique value will it provide?
    *   **Features:** What are the core functionalities for an initial version (Minimum Viable Product - MVP)? What features are explicitly out of scope for now?
    *   **Categorization:** Consider how your agent fits into the [Agent Categories and Types defined in our standards](docs/agent-development-standards.md#agent-categorization).
    *   **Action:** It is highly recommended to create a **Product Requirements Document (`PRD.md`)** for your agent. This document should detail its goals, target audience, features, technical considerations, and success metrics. You can place this PRD inside your agent's specific documentation folder (e.g., `agents/your-agent-name/docs/PRD.md`).

2.  **Review Development Standards & Architecture:**
    *   Thoroughly familiarize yourself with the [**Agent Development Standards**](docs/agent-development-standards.md). This crucial document covers directory structure, manifest requirements, coding practices, documentation standards, testing, configuration, containerization, and more.
    *   If your agent is complex or interacts with multiple components, understand the [**Layered Architecture**](docs/layered-architecture.md) to ensure modularity and maintainability.

### Phase 2: Scaffolding & Initial Setup

1.  **Set Up Your Local Development Environment:**
    *   Ensure you have followed all steps in the "General Contribution Workflow" above (fork, clone, branch, pre-commit hooks).

2.  **Create the Agent Directory Structure:**
    *   Follow the guidelines in the [Agent Development Standards for Directory Structure](docs/agent-development-standards.md#directory-structure).
    *   Typically, you will create a new folder for your agent under the `agents/` directory (e.g., `agents/your-agent-name/`).
    *   Inside your agent's folder, you might have subdirectories like `app/` (for core logic), `data/` (for sample data), `docs/` (for agent-specific documentation like your PRD), etc.
    *   Refer to the established agent onboarding process for guidance on the expected directory structure and initial file setup (e.g., creating necessary subdirectories like `app/`, `docs/`, `tests/`, and essential files like `agent.json`, `README.md`, `requirements.txt`, `Dockerfile`). You'll be creating these manually for a new agent, following the standards.

3.  **Create the Agent Manifest (`agent.json`):**
    *   This JSON file is the heart of your agent's definition and integration with Agentopia. It resides in the root of your agent's directory (e.g., `agents/your-agent-name/agent.json`).
    *   **Refer extensively to the [Agent Manifest Schema Guide](docs/manifest-schema-guide.md)** for detailed explanations of all fields. The raw [Agent Manifest Schema (`agent-manifest.schema.json`)](agent-manifest.schema.json) itself also contains comments and descriptions.
    *   Pay close attention to accurately filling out fields such as: `name`, `icon`, `short_description`, `long_description` (supports Markdown), `category`, `tags`, `features` (list), `setup_instructions` (can be structured for Docker/Python or a Markdown string), `configFields` (for user-configurable parameters), `llm_dependency` (if applicable), `privacy_considerations` (Markdown), and `docker_info`.
    *   Initially, set or ensure the manifest has `"deployment_status": "development"`.

4.  **Create the Agent `README.md`:**
    *   Every agent requires a `README.md` file in its root directory (e.g., `agents/your-agent-name/README.md`). This is the primary user-facing documentation for your agent.
    *   Use the [**Standard Agent README Template**](templates/agent-docs/readme-template.md) as your starting point. This template provides a structured format.
    *   Carefully fill in all sections of the template relevant to your agent, providing clear and comprehensive information for users.

### Phase 3: Development & Implementation

1.  **Develop Your Agent's Core Logic:**
    *   Implement the primary functionality of your agent. This code typically resides in your agent's `app/` subdirectory (e.g., `agents/your-agent-name/app/main.py`).
    *   Adhere to the coding standards outlined in the [Agent Development Standards](docs/agent-development-standards.md#coding-standards) (e.g., Python style, error handling, logging).
    *   Implement robust configuration handling (reading from `configFields` defined in `agent.json`), logging for diagnostics, and graceful error management.

2.  **Implement Setup and Configuration Details:**
    *   Ensure your `setup_instructions` in `agent.json` are extremely clear, accurate, and testable for all specified environments (e.g., Docker, local Python).
    *   If your agent uses `configFields`, ensure your core logic correctly utilizes these parameters.

3.  **Dockerize Your Agent (Recommended for Local-First Agents):**
    *   If your agent is designed to run locally, especially via Docker (which aligns with Agentopia's local-first philosophy), create a `Dockerfile` in your agent's root directory.
    *   Provide clear and tested `docker_info.build_instructions` and `docker_info.run_instructions` in your `agent.json`.
    *   Refer to the [Containerization (Docker) Standards](docs/agent-development-standards.md#containerization-docker).

4.  **Write Unit and Integration Tests:**
    *   Develop tests to verify that your agent functions as expected and that its components integrate correctly.
    *   Refer to the [Testing Standards](docs/agent-development-standards.md#testing) for guidance on types of tests and best practices.

### Phase 4: Validation & Documentation Review

1.  **Local Validation (Crucial Step):**
    *   Before marking your agent for review, **you must** validate its `agent.json` manifest using the provided Node.js script:
        ```bash
        node tools/validate-agents.js agents/your-agent-name/agent.json
        ```
    *   This script checks for schema compliance, required fields, and other critical aspects of the manifest. Address all errors and warnings reported by the script.
    *   For quick, ad-hoc schema checks, you can also use an online tool like [JSON Schema Validator](https://www.jsonschemavalidator.net/) by pasting your `agent.json` content and the content of our [Agent Manifest Schema (`agent-manifest.schema.json`)](agent-manifest.schema.json).

2.  **Self-Review & Thorough Testing:**
    *   Rigorously test all functionalities of your agent in all specified environments.
    *   If Dockerized, build the Docker image and run the container using your `docker_info.run_instructions` to verify they work perfectly.
    *   Critically review all user-facing documentation: your agent's `README.md`, and fields within `agent.json` like `long_description`, `setup_instructions`, `privacy_considerations`. Ensure they are clear, accurate, complete, and easy for users to understand.

### Phase 5: Submission & Review

1.  **Mark for Review:**
    *   Once local validation passes, all tests are successful, and you are confident your agent and its documentation are complete and of high quality, update its `agent.json` to set `"deployment_status": "review"`.

2.  **Submit Pull Request:**
    *   Follow the "Submitting Your Contribution" steps outlined in the "General Contribution Workflow" section above (commit, push, open PR).
    *   In your PR description, clearly state that the agent is ready for review. Highlight key features, any specific areas you'd like reviewers to focus on, and confirm that `tools/validate-agents.js` passes.

3.  **Maintainer Review & Iteration:**
    *   Project maintainers will review your agent's code, manifest, documentation, and overall functionality.
    *   Be responsive to feedback and prepared to make further changes or clarifications based on the review.
    *   (Future Implementation) Automated checks via GitHub Actions may also run `validate-agents.js` and other linters on your PR.

4.  **Approval & Merge:**
    *   Once your agent meets all standards and is approved, maintainers will merge your PR. They may then update the agent's `deployment_status` to `"production"`, making it eligible to be listed on the official Agentopia portal.

Congratulations! You've successfully contributed a new agent to the Agentopia ecosystem!

---

## ⚠️ Common Pitfalls & Troubleshooting

-   **Missing required fields in `agent.json`:** Double-check your manifest against the [Agent Manifest Schema Guide](docs/manifest-schema-guide.md) and ensure all mandatory fields are present and correctly formatted.
-   **Typos in `category`, `type`, or `scale`:** Use only the allowed enum values as defined in the schema to ensure compatibility with portal filters.
-   **Validation errors from `tools/validate-agents.js`:** Carefully read the error messages from the script. They often point directly to the issue in your `agent.json`.
-   **Agent not appearing correctly in the Agentopia portal (during local testing):** Ensure the `sync-agents.js` script (in the `agentopia.github.io` repository) has been run after your changes. Verify your agent's folder name and manifest path are correct.
-   **Docker build or run failures:** Double-check your `Dockerfile` and the `docker_info` instructions in your manifest. Test them meticulously locally.

---

## ❓ FAQ

**Q: Can I use a programming language other than Python for my agent?**
A: Yes! Agentopia is language-agnostic. Ensure your `agent.json` correctly specifies the `entry_point` (if applicable for local non-Docker execution) and that your `setup_instructions` (and `Dockerfile` if used) are comprehensive for your chosen language and environment.

**Q: How do I handle API keys or other sensitive credentials for my agent?**
A: Use the `configFields` in your `agent.json` to define input parameters for such credentials. Instruct users to provide their own keys. **Never hardcode sensitive credentials in your agent's code or manifest.** Refer to the [Agent Development Standards](docs/agent-development-standards.md#security-and-privacy) for more on security.

**Q: What if I’m not sure about a specific field in the `agent.json` or a step in the process?**
A: Don't hesitate to ask! Open an issue in the `AIAgentopia` repository, or ask for clarification in your pull request. We’re here to help you succeed.

**Q: Where can I find examples of existing agents?**
A: Explore the `agents/` directory. The `data-analyzer-bot` is a good reference for a scaffolded agent.

---

## 📚 Resources

-   **Project Documentation:**
    -   [Agent Development Standards](docs/agent-development-standards.md)
    -   [Agent Manifest Schema Guide](docs/manifest-schema-guide.md)
    -   [Agent Manifest Schema File (`agent-manifest.schema.json`)](agent-manifest.schema.json)
    -   [Layered Architecture Guide](docs/layered-architecture.md)
    -   [Standard Agent README Template](templates/agent-docs/readme-template.md)
    -   [Agent Validation Script (`tools/validate-agents.js`)](tools/validate-agents.js)
-   **External Resources:**
    -   [JSON Schema Documentation](https://json-schema.org/)
    -   [GitHub Guides: Forking Projects](https://guides.github.com/activities/forking/)
    -   [GitHub Docs: Creating a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
    -   [Markdown Guide](https://www.markdownguide.org/)
-   **Agentopia Ecosystem:**
    -   [Agentopia Portal Repository (`agentopia.github.io`)](https://github.com/Agentopia/agentopia.github.io)

---

## Appendix: Issue & Milestone Organization Workflow

To keep project management clear, transparent, and scalable, AIAgentopia follows these conventions when creating Issues and Milestones for tracking development work, especially for new features, agents, or significant changes.

### 1. Milestone Usage

-   **Create a Milestone** for each major phase of development (e.g., "Phase 1: Core Infrastructure", "Phase 2: First Agents") or for significant, multi-issue features. This is done via the GitHub UI in the "Issues" tab under "Milestones."
-   Assign all related Issues for that phase or feature to the corresponding Milestone. The Milestone’s progress bar will then update automatically as its associated Issues are closed, providing a clear overview of progress.

### 2. Cap/Epic Issue Convention (Optional but Recommended for Large Efforts)

-   For each major phase or very large feature set (an "Epic"), you may create a special Issue, often prefixed with `[Cap]` or `[Epic]`, to serve as a high-level tracker.
-   In the body of this Cap/Epic Issue, add a Markdown checklist that references all the individual sub-Issues (tasks) by their number (e.g., `- [ ] #12 Sub-task: Implement manifest validation`).
-   Label these Cap/Epic Issues with `cap` or `epic` for easy filtering and identification.
-   Use the Cap/Epic Issue for overall summaries, status updates, high-level discussions, and to provide a single point of reference for the larger effort.

### 3. Sub-Issue Naming & Linking

-   Break down work into manageable, actionable tasks, each represented by its own Issue.
-   Prefix these actionable Issues with a clear indicator like `[Task]`, `[Bug]`, `[Feature]`, or `[Docs]` (e.g., `[Task] Implement Python setup instructions for Data Analyzer Bot`).
-   Assign each sub-Issue to the relevant Milestone.
-   Ensure sub-Issues are referenced in the Cap/Epic Issue’s checklist (if one is being used) for comprehensive tracking.

### 4. Example Workflow

1.  **Create Milestone (via GitHub UI):**
    *   Example Title: `Phase 1: Foundational Agent Framework & Data Analyzer Bot`

2.  **Create Cap/Epic Issue (Optional):**
    *   Title: `[Cap] Phase 1: Foundational Agent Framework & Data Analyzer Bot`
    *   Labels: `cap`, `phase-1`
    *   Body includes a checklist like:
        ```markdown
        ## Phase 1 Task Checklist
        ### Core Framework
        - [ ] #23 Define and document the layered architecture for agents
        - [ ] #24 Establish foundational environment setup guidelines (Docker, venv, dependency management)
        - [ ] #25 Implement core logging and error handling utilities for agents
        - [ ] #26 Implement configuration management utility for agents
        - [ ] #27 Implement LLM interface (supporting API & local/Ollama)
        - [ ] #28 Finalize v1 agent manifest schema and validation tools (`validate-agents.js`)
        ### Data Analyzer Bot
        - [ ] #29 Scaffold Data Analyzer Bot (Manifest, README, PRD)
        - [ ] #30 Implement core Python logic for Data Analyzer Bot
        - [ ] #31 Create Dockerfile for Data Analyzer Bot
        - [ ] #32 Write tests for Data Analyzer Bot
        ```

3.  **Create Sub-Issues:**
    *   Example: `[Task] Scaffold Data Analyzer Bot (Manifest, README, PRD)` (Issue #29)
        *   Assigned to Milestone: `Phase 1: Foundational Agent Framework & Data Analyzer Bot`
        *   Labels: `task`, `data-analyzer-bot`, `scaffolding`
    *   ...and so on for each item in the Cap/Epic checklist.

4.  **Link Sub-Issues in Cap/Epic:**
    *   In the Cap/Epic Issue's body, ensure each checklist item correctly links to its corresponding sub-Issue using the `#issue-number` syntax. GitHub automatically renders these as links and updates the checkboxes as linked issues are closed.

### 5. Tips for Effective Issue Management

-   For most individual contributions or smaller features, a well-described Issue assigned to a Milestone is sufficient. Cap/Epic Issues are more for coordinating larger, multi-faceted efforts.
-   Use descriptive labels (e.g., `bug`, `enhancement`, `documentation`, `agent:data-analyzer`, `priority:high`) to categorize and prioritize Issues.
-   Refer to [GitHub’s documentation on Milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones) and [tracking work with issues](https://docs.github.com/en/issues/tracking-your-work-with-issues) for more details.

By following these conventions, we can maintain a clear, organized, and actionable project backlog, making it easier for everyone to understand priorities and contribute effectively.

---

Thank you for helping make AIAgentopia a truly collaborative and innovative space to build AI agents!
