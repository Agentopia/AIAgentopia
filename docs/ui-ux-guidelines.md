# Agent UI/UX Guidelines

This document outlines the standard UI/UX patterns for building Streamlit-based agents within the AI Agentopia ecosystem. Following these guidelines ensures a consistent, professional, and user-friendly experience across all agents.

## Core Principles

1.  **Consistency:** All agents should share a common look and feel, reinforcing the AI Agentopia brand.
2.  **Modularity:** Each agent must be self-contained. UI components should be bundled with the agent, not shared from a central library, to simplify dependency management and deployment.
3.  **Clarity:** The user interface should be clean and intuitive, clearly distinguishing between global platform elements and agent-specific controls.

---

## Standard Layout Structure

All Streamlit agents should adopt the following two-panel layout:

### 1. Sidebar: Global Branding & Controls

The sidebar is reserved for global elements and primary agent controls.

-   **AI Agentopia Header:** The top of the sidebar must display the official AI Agentopia logo and title.
-   **Controls:** All primary user controls, such as LLM provider selection, API key inputs, and other configuration settings, should be located here.
-   **Footer:** The copyright footer (`© 2025 Agentopia. All rights reserved.`) must be placed at the bottom of the sidebar.

### 2. Main Panel: Agent-Specific Content

The main panel is dedicated to the agent's unique functionality and user interaction.

-   **Agent Title:** The panel must begin with the agent's specific title and icon. The icon should be the emoji specified in the agent's `agent.json` manifest.
-   **Agent Interface:** The rest of the panel contains the agent's core features, such as file uploaders, chat interfaces, data displays, and results.

---

## Implementation via `ui_components.py` Template

To ensure consistency and simplify development, all new agents must start with a copy of the `ui_components.py` template.

### Getting Started

1.  **Copy the Template:** When creating a new agent, copy the `ui_components.py` file from `AIAgentopia/agents/data-analyzer-bot/app/` into your new agent's `/app` directory.
2.  **Do Not Modify the Core Structure:** This file contains the necessary functions to render the standard layout:
    -   `display_sidebar_header()`: Renders the Agentopia brand in the sidebar.
    -   `display_agent_title(icon, agent_name)`: Renders the agent-specific title in the main panel.
    -   `display_sidebar_footer()`: Renders the copyright notice in the sidebar.
3.  **Integrate into Your App:** Call these functions from your main Streamlit script (`app.py` or similar) to construct the standard UI.

### Example `main.py` Structure:

```python
import streamlit as st
from ui_components import display_sidebar_header, display_agent_title, display_sidebar_footer

def main():
    # --- Sidebar ---
    with st.sidebar:
        display_sidebar_header()
        # ... your agent's controls here ...
        display_sidebar_footer()

    # --- Main Panel ---
    display_agent_title(icon="✨", agent_name="My New Agent")
    # ... your agent's main interface here ...

if __name__ == "__main__":
    main()
```

By adhering to these guidelines, we can build a cohesive and high-quality suite of AI agents.
