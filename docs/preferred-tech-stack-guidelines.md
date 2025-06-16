# Preferred Tech Stack & Guidelines for Agentopia AI Agents

This document outlines the recommended technology stack, UI/UX standards, and repo-wide conventions for building and integrating AI agents in the AIAgentopia ecosystem. The goal is to ensure a consistent, high-quality, and maintainable experience for both developers and users, while still allowing flexibility for innovation.

---

## 1. Frontend/UI/UX

### Preferred Technologies
- **Web UI:** React + Tailwind CSS (recommended)
- **Rapid Prototyping/Demos:**
  - **Streamlit** (for Python-based agents, flexible dashboards)
  - **Gradio** (for simple, quick model demos; especially suited for Hugging Face Spaces)
- **Reusable Theme:** Use the Agentopia theme (color palette, logo, and shared components)

> **Note:** You may choose Streamlit or Gradio for demos based on the agent’s needs. Gradio is ideal for quick, minimal UIs; Streamlit is better for more custom or data-rich dashboards. The choice is left to the developer’s discretion for each agent.

#### Example: Streamlit Demo
```python
# streamlit_app.py
import streamlit as st

st.title("My AI Agent Demo")
user_input = st.text_input("Enter some text:")
if user_input:
    st.write(f"Echo: {user_input}")
```
_Run with: `streamlit run streamlit_app.py`_

#### Example: Gradio Demo
```python
# gradio_app.py
import gradio as gr

def echo(text):
    return f"Echo: {text}"

demo = gr.Interface(fn=echo, inputs="text", outputs="text", title="My AI Agent Demo")
demo.launch()
```
_Run with: `python gradio_app.py`_

---

### Best Practices for Demo UI/UX

- **Clarity & Simplicity:**
  - Keep the interface clean and focused on the main demo task.
  - Avoid unnecessary controls or clutter.
- **Consistent Branding:**
  - Use Agentopia colors, logo, and style guide where possible.
  - Add a title and brief description at the top.
- **Instructions & Hints:**
  - Provide clear instructions for what the user should do.
  - Use placeholder text or tooltips for input fields.
- **Input Validation & Error Handling:**
  - Validate user input and provide helpful error messages.
  - Prevent crashes or confusing states.
- **Responsive Design:**
  - Ensure the demo works well on desktops, tablets, and phones.
- **Accessibility:**
  - Use readable fonts, good color contrast, and accessible labels.
  - Support keyboard navigation where possible.
- **Feedback & Loading Indicators:**
  - Show progress or loading spinners for long operations.
  - Give immediate feedback after user actions.
- **Minimal Distractions:**
  - Avoid pop-ups, auto-playing sounds, or unnecessary animations.
- **Demo Data:**
  - Provide example input or sample data for users to try.

> **Tip:** Test your demo with someone unfamiliar with your agent. If they can use it easily without help, your UI/UX is on the right track!

### Guidelines
- Maintain a clean, modern, and accessible layout
- Use the shared component library and follow the Agentopia style guide
- For demos, aim for consistent navigation and branding
- Allow exceptions for imported agents, but encourage adaptation over time

## 2. Backend & APIs

### Preferred Technologies
- **Python** (main agent logic)
- **FastAPI** (for REST APIs)
- **Node.js** (if agent logic is JavaScript-based)

### Guidelines
- Expose APIs using standard REST (OpenAPI/Swagger if possible)
- Document all endpoints
- Use environment variables for secrets/configuration

## 3. Database & Storage

### Preferred Choices
- **Local:** SQLite
- **Cloud/Remote:** PostgreSQL
- **Vector DBs:** ChromaDB, FAISS (for embeddings)

### Guidelines
- Default to SQLite for local development
- Use PostgreSQL for production/cloud deployments
- If a different DB is required (by imported agent), document and justify the choice
- Provide adapters where possible

## 4. Directory Structure & Organization

```
agent-name/
  /sample           # Original open-source codebase
  /app              # Adapted/new source code
  /tests            # Tests
  /docs             # Documentation (PRD.md, ARCHITECTURE.md, etc.)
  agent.json        # Agent manifest
  README.md         # User guide
  requirements.txt  # Python dependencies
  app/main.py       # Entry point
  Dockerfile        # Containerization
```

## 5. Manifest & Metadata
- Every agent must include a valid `agent.json` manifest
- Follow the Agentopia manifest schema for metadata, config, and dependencies

## 6. Documentation
- Each agent must provide:
  - `README.md` (overview, setup, usage)
  - `PRD.md` (product requirements)
  - Setup instructions for both local and Docker
  - API documentation if applicable

## 7. Linting, Formatting & Testing
- Use **Ruff** for Python linting/formatting
- Use **Prettier** and **ESLint** for JS/React
- Provide at least basic tests (unit or smoke tests)

## 8. Dockerization
- Provide a `Dockerfile` for each agent
- Follow best practices for small, secure, and reproducible images

## 9. Exceptions & Flexibility
- Imported agents may initially use their own stack
- Over time, aim to migrate to preferred standards where feasible
- All deviations must be documented in the agent's `README.md`

---

## Summary Table
| Area      | Preferred Tech         | Alternatives/Notes           |
|-----------|-----------------------|------------------------------|
| Frontend  | React + Tailwind CSS  | Streamlit, custom UI allowed |
| Backend   | Python, FastAPI       | Node.js, others w/ docs      |
| Database  | SQLite, PostgreSQL    | Other DBs if justified       |
| Lint/Test | Ruff, Prettier, ESLint| Pytest, Jest, etc.           |
| Container | Docker                |                             |

---

## Further Reading
- [Agentopia Manifest Schema Guide](./manifest-schema-guide.md)
- [12 Factor App Methodology](https://12factor.net/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [OpenAPI Specification](https://swagger.io/specification/)

---

*This guideline will be updated as the project evolves. Suggestions and improvements are welcome!*
