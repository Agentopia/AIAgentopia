# Contributing to AIAgentopia

Thank you for your interest in contributing to AIAgentopia!
We welcome new agents, improvements, and ideas from the community.

---

## 🚀 Getting Started

1. **Fork this repository** to your own GitHub account.
2. **Clone your fork** to your local machine.
3. **Create a new branch** for your feature or agent.
4. Follow the steps below to add your agent or make improvements.

---

## 🧩 How to Add a New Agent

1. **Create a New Agent Folder**
   - In the `agents/` directory, create a folder for your agent (e.g., `agents/my-awesome-agent`).

2. **Add an `agent.json` Manifest**
   - Every agent must include an `agent.json` file that follows our [Agent Manifest Schema](./agent-manifest.schema.json).
   - See the schema file for required and optional fields.
   - Example manifest is provided in the schema and below.

3. **Validate Your Manifest**
   - **Primary Method (Recommended):** Use the local validation script: `node tools/validate-agents.js path/to/your/agent/agent.json`. (Note: This script is under development and will be enhanced to perform comprehensive checks beyond basic schema validation.)
   - **Alternative:** You can also use an online tool like [jsonschemavalidator.net](https://www.jsonschemavalidator.net/) for quick schema checks. Paste your `agent.json` and the [schema file](./agent-manifest.schema.json) to check for basic errors.

4. **Add Your Agent Code**
   - Include the main entry point file (e.g., `main.py`) and any supporting files in your agent’s folder.

5. **Test Your Agent**
   - Run the sync script in the portal repo to ensure your agent appears in the Agentopia portal.
   - Check that all required fields display correctly and setup instructions are clear.

6. **Submit a Pull Request**
   - Push your branch to your fork and open a pull request with a clear description of your changes.

---

## 🌊 Agent Lifecycle & Validation Process

To ensure quality and a smooth integration into Agentopia, agents go through a defined lifecycle managed by the `deployment_status` field in their `agent.json` manifest and a validation process.

### Agent `deployment_status`

This field indicates the current readiness of your agent:

*   `"development"` (Default): Your agent is under active development. It might be incomplete, not fully tested, or documentation might be pending. Use this status while you are actively working on the agent.
*   `"review"`: You've completed development, thoroughly tested your agent locally, ensured all documentation (especially `long_description`, `docker_run_instructions`, and `privacy_considerations`) is comprehensive, and successfully run the local validation script (`tools/validate-agents.js`). Your agent is now ready for review by project maintainers.
*   `"production"`: Your agent has been reviewed, approved, and is ready to be listed on the official Agentopia portal. This status is typically set by project maintainers after a successful review.

### Contribution Workflow & Validation

1.  **Develop Your Agent:**
    *   Create your agent files and `agent.json` manifest as described in "How to Add a New Agent."
    *   Initially, your `agent.json` should have `"deployment_status": "development"` (or omit it to use the default).

2.  **Local Validation (Crucial Step):**
    *   Before marking your agent for review, **you must** run the local validation script against your agent's manifest:
      ```bash
      node tools/validate-agents.js path/to/your/agent/agent.json
      ```
    *   This script will check for schema compliance and perform other sanity checks on critical fields (e.g., ensuring descriptions are not empty, Docker instructions are present, etc.).
    *   Address all errors and warnings reported by the script.

3.  **Self-Review & Testing:**
    *   Thoroughly test your agent's functionality, especially the Docker setup as described in `docker_run_instructions`.
    *   Ensure all user-facing documentation in the manifest (like `long_description`, `setup_instructions`, `docker_run_instructions`, `privacy_considerations`) is clear, accurate, and complete.

4.  **Mark for Review:**
    *   Once local validation passes and you are confident your agent is ready, update its `agent.json` to `"deployment_status": "review"`.

5.  **Submit Pull Request:**
    *   Commit your changes, including the updated `agent.json`.
    *   Push your branch to your fork and open a Pull Request to the `AIAgentopia` repository.
    *   In your PR description, mention that the agent is ready for review.

6.  **Automated Checks & Maintainer Review:**
    *   (Future Implementation) Automated checks (e.g., via GitHub Actions) will run `validate-agents.js` on your PR to ensure compliance.
    *   Project maintainers will review your agent's code, documentation, and functionality.
    *   If approved, maintainers will merge your PR and may update the status to `"production"`.

By following this process, you help maintain the quality and reliability of agents in Agentopia.

---

## 📝 Guidelines

- **Follow the [Agent Manifest Schema](./agent-manifest.schema.json)** for all agents.
- Write clear, concise descriptions and setup instructions.
- Use consistent naming for features, tags, and categories.
- Keep your code organized and well-documented.
- Be respectful and constructive in all communications.

---

## ⚠️ Common Pitfalls & Troubleshooting

- **Missing required fields:** Double-check your `agent.json` against the schema.
- **Typos in category/type/scale:** Use values that match the schema and portal filters.
- **Validation errors:** Use the online JSON schema validator to catch mistakes.
- **Agent not appearing in portal:** Make sure you ran the sync script and your agent folder/manifest is correctly structured.

---

## ❓ FAQ

**Q: Can I use a different programming language for my agent?**
A: Yes! Just make sure your `entry_point` field is accurate and your setup instructions are clear.

**Q: How do I add setup instructions for API keys or credentials?**
A: Use the `setup_instructions` and `config_fields` fields in your manifest. See the schema for examples.

**Q: What if I’m not sure about a field?**
A: Open an issue or ask for help in your pull request—we’re here to help!

---

## 📚 Resources

- [JSON Schema Documentation](https://json-schema.org/)
- [GitHub Guides: Forking Projects](https://guides.github.com/activities/forking/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Agentopia Portal Repo](https://github.com/Agentopia/agentopia.github.io)

---

## 🤝 Community Guidelines

- Be welcoming and inclusive.
- Respect different perspectives and backgrounds.
- Help others learn—no question is too basic!
- Celebrate progress and creativity.

---

## 🗂️ Issue & Milestone Organization Workflow

To keep project management clear and scalable, follow these conventions when creating Issues and Milestones for each development phase:

### 1. Milestone Usage
- **Create a Milestone** for each major phase (e.g., Phase 1, Phase 2) via the GitHub UI.
- Assign all related Issues for that phase to the Milestone. The Milestone’s progress bar will update automatically as Issues are closed.

### 2. Cap/Epic Issue Convention (Optional but Recommended)
- For each phase, you may create a `[Cap]` or `[Epic]` Issue as a high-level tracker.
- Add a Markdown checklist in the Cap/Epic Issue referencing all sub-Issues by number (e.g., `- [ ] #12 Sub-task`).
- Label Cap/Epic Issues with `cap` or `epic` for clarity.
- Use the Cap/Epic Issue for summaries, status updates, and discussion.

### 3. Sub-Issue Naming & Linking
- Prefix actionable Issues with `[Task]` or another clear label.
- Assign each sub-Issue to the relevant Milestone.
- Reference sub-Issues in the Cap/Epic Issue’s checklist for easy tracking.

### 4. Example Workflow
1. **Create Milestone:**
   - `[Milestone] Phase 1: Foundational & Core Infrastructure`
2. **Create Cap/Epic Issue:**
   - Title: `[Cap] Phase 1: Foundational & Core Infrastructure`
   - Body includes:
     ```markdown
     ## Phase 1 Task Checklist
     - [ ] #2 Create and document the layered architecture
     - [ ] #3 Establish foundational environment setup (Docker, venv, dependency management)
     - [ ] #4 Implement logging and error handling utilities
     - [ ] #5 Implement config management utility
     - [ ] #6 Implement LLM interface (API & local/Ollama)
     - [ ] #7 Implement manifest schema and validation tools
     ```
3. **Create Sub-Issues:**
   - `[Task] Create and document the layered architecture` (assigned to Milestone)
   - `[Task] Establish foundational environment setup (Docker, venv, dependency management)` (assigned to Milestone)
   - ...and so on for each task.
4. **Link Sub-Issues:**
   - In the Cap/Epic Issue, reference each sub-Issue by number using `#issue-number`.
   - Checkboxes will auto-update as Issues are closed.

### 5. Tips
- For most tracking, the Milestone alone is sufficient. Use Cap/Epic Issues for extra clarity or discussion.
- Use labels like `task`, `cap`, `epic`, and `phase-1` to organize Issues.
- See [GitHub’s Milestone documentation](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones) for more details.

---

Thank you for helping make AIAgentopia a truly ONE happy place to build AI agents!
