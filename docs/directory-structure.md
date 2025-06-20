# Directory Structure Reference

**Version:** v1.0
**Date:** 2025-06-06

---

## Overview

This document describes the recommended directory structure for the AIAgentopia repository. The structure is designed to:
- Keep each agent isolated
- Promote code reuse via shared tools and frameworks
- Make documentation and scripts easy to find
- Support future growth and new agent types

---

## Sample Directory Structure

```plaintext
AIAgentopia/
├── agents/
│   ├── data-analyzer-bot/
│   │   ├── app/
│   │   │   └── main.py
│   │   ├── docs/
│   │   │   └── PRD.md
│   │   ├── requirements.txt
│   │   ├── agent.json
│   │   ├── README.md
│   │   ├── Dockerfile
│   │   └── tests/
│   ├── agent-2/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── agent.json
│   │   └── ...
│   └── ...
├── tools/
│   ├── llm_interface.py
│   ├── manifest_validator.py
│   ├── config_utils.py
│   ├── logging_utils.py
│   ├── sync_agents.py
│   └── ...
├── frameworks/
│   ├── langchain_helpers.py
│   ├── crewai_helpers.py
│   └── ...
├── docs/
│   ├── agent-development-guide.md
│   ├── architecture.md
│   ├── integration-workflow.md
│   └── ...
├── scripts/
│   ├── setup_env.sh
│   ├── deploy_agent.py
│   └── ...
├── .env.example
├── agent-manifest.schema.json
├── requirements.txt
├── Dockerfile
├── README.md
└── CONTRIBUTING.md
```

---

## Notes
- Each agent lives in its own subdirectory under `/agents/`.
    - **New agents should place their core source code within an `app/` subdirectory** (e.g., `agents/{agent-name}/app/main.py`) as per the [Agent Development Standards](./agent-development-standards.md#directory-structure).
    - Some existing agents may have their main script directly in their root folder (e.g., `agents/{agent-name}/main.py`).
- Shared utilities and tools go in `/tools/`.
- Framework-specific helpers are in `/frameworks/`.
- All project-level documentation is kept in `/docs/`. Agent-specific documentation resides within each agent's own `/docs` subfolder.
- Scripts for setup, deployment, or automation are in `/scripts/`.
- The root contains project-wide configs and top-level documentation (`README.md`, `CONTRIBUTING.md`).

---

## Revision History
- **v1.0 (2025-06-06):** Initial version with sample directory structure and notes.

---

*Update this document as the project grows or the structure changes.*
