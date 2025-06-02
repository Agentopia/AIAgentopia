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
   - Use [jsonschemavalidator.net](https://www.jsonschemavalidator.net/) or a similar tool.
   - Paste your `agent.json` and the [schema file](./agent-manifest.schema.json) to check for errors.

4. **Add Your Agent Code**
   - Include the main entry point file (e.g., `main.py`) and any supporting files in your agent’s folder.

5. **Test Your Agent**
   - Run the sync script in the portal repo to ensure your agent appears in the Agentopia portal.
   - Check that all required fields display correctly and setup instructions are clear.

6. **Submit a Pull Request**
   - Push your branch to your fork and open a pull request with a clear description of your changes.

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

Thank you for helping make AIAgentopia a truly ONE happy place to build AI agents!
