# Data Analyzer Bot - Product Requirements Document (PRD)

**Version:** 1.0
**Status:** Active
**Last Updated:** 2025-06-17

---

## 1. Overview & Introduction

*   **Product Name:** Data Analyzer Bot
*   **One-Liner:** An AI-powered agent that automates Exploratory Data Analysis (EDA) on local tabular data, generating a comprehensive HTML report.
*   **Problem Statement:** Users with tabular data often spend significant time on repetitive initial analysis tasks (profiling, visualizing, checking quality). This agent automates this process, enabling users of all skill levels to quickly gain foundational insights from their data without writing code, while ensuring complete data privacy.
*   **Target Audience:**
    *   Data Analysts / Scientists
    *   Business Users / Citizen Data Scientists
    *   Students / Researchers
    *   Anyone working with tabular data who needs a quick profiling tool.

## 2. Goals & Success Metrics

*   **Primary Goal:** To accelerate the initial phase of data analysis by automatically generating a comprehensive profile, visualizations, and summary for a given tabular dataset.
*   **Key Success Metrics:**
    *   **Adoption Rate:** Number of downloads/pulls of the Docker image or clones of the agent code.
    *   **Completion Rate:** Percentage of analyses run successfully without critical errors.
    *   **User Feedback:** Qualitative feedback gathered through GitHub issues or community channels.
    *   **Contribution:** Number of community contributions (e.g., bug fixes, feature suggestions).

## 3. Features & Scope

### 3.1. Core Features (MVP)

*   **Feature 1: Automated Data Profiling**
    *   **Description:** The agent will automatically calculate and report on dataset dimensions, column types, missing values, descriptive statistics for numerical columns, and frequency counts for categorical columns.
    *   **User Story:** As a Data Analyst, I want the agent to automatically profile my dataset so that I can quickly understand its structure and statistical properties.
*   **Feature 2: Automated Visualization**
    *   **Description:** The agent will generate and save standard visualizations as image files, including histograms for numerical columns, bar charts for categorical columns, and a correlation heatmap.
    *   **User Story:** As a Business User, I want to see visual charts of my data so that I can easily identify patterns and distributions without interpreting raw numbers.
*   **Feature 3: Optional LLM-Powered Summary**
    *   **Description:** If the user provides an API key, the agent will send aggregated statistics (not raw data) to an LLM to generate a natural language summary of the dataset's characteristics and potential insights.
    *   **User Story:** As a Researcher, I want an AI-generated summary of the key findings so that I can quickly grasp the main takeaways from the analysis.
*   **Feature 4: Consolidated HTML Report**
    *   **Description:** All generated profiles, statistics, and visualizations will be compiled into a single, self-contained HTML file that can be easily viewed in a browser and shared.
    *   **User Story:** As a Data Analyst, I want a single, shareable HTML report so that I can easily present my initial findings to stakeholders.
*   **Feature 5: API Key Management (Web UI)**
    *   **Description:** User-provided API keys for LLMs (e.g., OpenAI, Anthropic Claude) are input via secure fields in the Streamlit sidebar. These keys are stored in `st.session_state` for the duration of the user's session and are not persisted beyond that, ensuring data privacy.
    *   **User Story:** As a user, I want to securely provide my API keys for different LLM providers within the agent's interface for the current session, so the agent can access the chosen LLM.
*   **Feature 6: Multiple LLM Provider Support (Web UI)**
    *   **Description:** The agent supports both OpenAI (via `OpenAIChat`) and Anthropic Claude (via the native `Claude` class from `phi-llm`) as LLM providers. Users can select their preferred provider from a dropdown in the sidebar.
    *   **User Story:** As a user, I want to be able to choose between OpenAI and Anthropic Claude for data analysis, depending on my preference or task requirements.
*   **Feature 7: LLM Selection (Web UI)**
    *   **Description:** A dropdown menu in the Streamlit sidebar allows users to select their desired LLM provider ("OpenAI", "Anthropic Claude", or "None"). This selection is stored in `st.session_state` for the current session.
    *   **User Story:** As a user, I want to easily switch between LLM providers or opt-out of LLM use for a given session via the agent's interface.

### 3.2. Out of Scope (for this version)

*   Advanced statistical modeling or predictive analytics.
*   Direct data cleaning or transformation capabilities.
*   Real-time data streaming or analysis of data in databases.
*   Interactive dashboards or UIs (report is static HTML).
*   Support for data formats other than CSV and Excel.

## 4. User Flow & Interaction Model

*   **Interaction Type:** CLI Tool, run locally or via a Docker container.
*   **High-Level User Flow:**
    1.  User prepares a data file (CSV/Excel) on their local machine.
    2.  User runs the agent from the command line, providing the path to the input file and a desired output directory.
    3.  (Optional) User sets an environment variable for their LLM API key.
    4.  The agent performs the analysis, saving charts to the output directory.
    5.  The agent generates a final `report.html` file in the output directory.
    6.  User opens `report.html` in their web browser to view the results.

## 5. Technical Considerations

*   **Key Dependencies:** Python, Pandas, NumPy, Matplotlib/Seaborn, Jinja2, Openpyxl. (For the backend/core logic. Frontend might use HTML/CSS/JS, potentially with a framework like Streamlit, Flask+Templates, or FastAPI+Templates).
*   **Configuration Management (Web UI):** API keys for OpenAI and Anthropic Claude, along with the selected LLM provider, are managed via input fields and dropdowns in the Streamlit sidebar. This information is stored in `st.session_state` for the current session only and is not persisted across sessions or in `localStorage` to enhance security and privacy.
*   **Data Handling:** Data is uploaded via the web UI, read into a pandas DataFrame in memory by the backend. All processing occurs locally on the server running the agent (which could be the user's machine if running locally). The agent generates an HTML report viewable in the UI or as a downloadable file, and image files that can be embedded or downloaded.
*   **LLM Interaction (if applicable):**
    *   When an API key is provided and an LLM is selected, the `phi-llm` library's `Assistant` is initialized.
    *   For **OpenAI**, `PandasTools` is used, allowing the LLM to interact with the DataFrame through predefined tool calls.
    *   For **Anthropic Claude**, direct tool usage with `PandasTools` is currently bypassed (by setting `tools=[]` during `Assistant` initialization) due to JSON schema compatibility issues (Claude requires JSON Schema draft 2020-12). Instead, a comprehensive description of the DataFrame (including shape, column names, data types, and summary statistics) is provided directly in the `Assistant`'s instructions. This allows Claude to perform analysis based on this metadata without direct tool execution.
    *   The raw dataset itself is not transmitted externally.

## 6. Future Enhancements (Roadmap)

*   Interactive HTML reports (e.g., using Plotly).
*   Data cleaning suggestions.
*   Support for more data formats (e.g., Parquet).
*   Direct database connections.
*   Customizable analysis options within the web UI (e.g., checkboxes to select specific charts or analyses).
*   Enhanced error handling and user feedback for API key issues or LLM communication problems.
