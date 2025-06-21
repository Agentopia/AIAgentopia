# Product Requirements Document: AI Data Analyst (Sample Agent - As-Is)

**Version:** 0.1.0 (As-Is Snapshot)
**Status:** Baseline for Migration
**Date:** 2025-06-16

## 1. Version History

| Version | Date       | Author        | Summary of Changes                                       |
|---------|------------|---------------|----------------------------------------------------------|
| 0.1.0   | 2025-06-16 | Cascade (AI)  | Initial "as-is" PRD based on sample `ai_data_analyst.py` |

## 2. Overview

### 2.1. Agent Purpose and Goals
The AI Data Analyst sample agent is a Streamlit web application designed to allow users to upload tabular data (CSV or Excel files) and perform data analysis by asking natural language questions. The primary goal is to translate these questions into SQL queries, execute them on the uploaded data using DuckDB, and display the results, leveraging an LLM (OpenAI GPT-4) for the natural language to SQL conversion.

### 2.2. Target Audience
Users who:
- Have tabular data in CSV or Excel format.
- Want to query and get insights from their data without writing SQL.
- Have access to an OpenAI API key.
- Are comfortable running a local Python Streamlit application.

### 2.3. Key Features (As observed in `ai_data_analyst.py`)
-   **File Upload:** Supports CSV and Excel (`.xlsx`) file uploads.
-   **Data Preview:** Displays a preview of the uploaded dataset.
-   **Natural Language Querying:** Allows users to input questions in plain text.
-   **NL-to-SQL Conversion:** Uses OpenAI GPT-4 to convert natural language queries into SQL.
-   **SQL Execution:** Executes the generated SQL on the uploaded data using DuckDB.
-   **Results Display:** Shows the query results (textual answers and/or SQL queries) in the Streamlit UI.
-   **OpenAI API Key Input:** Secure input field for the user's OpenAI API key.
-   **Basic Error Handling:** Manages unsupported file formats, empty queries, and API errors.

## 3. Technical Specifications

### 3.1. System Architecture
-   **Application Type:** Local Streamlit web application.
-   **Core Logic:** Contained within a single Python script (`ai_data_analyst.py`).
-   **UI:** Generated and managed by Streamlit.
-   **Data Processing:**
    -   Pandas for reading and initial manipulation of uploaded data.
    -   Data is temporarily stored as a local CSV file.
    -   DuckDB for in-memory SQL database and query execution.
-   **LLM Integration:**
    -   Uses `phidata` library, specifically `phi.agent.duckdb.DuckDbAgent`.
    -   Uses `agno` library for `agno.models.openai.OpenAIChat` (configured for GPT-4) and `agno.tools.pandas.PandasTools`.
    -   Requires user-provided OpenAI API key.

### 3.2. Dependencies
-   Python 3.x
-   `streamlit==1.41.1`
-   `openai==1.58.1`
-   `duckdb==1.1.3`
-   `pandas` (version not pinned in sample's `requirements.txt`)
-   `numpy==1.26.4`
-   `phidata` (version not pinned)
-   `agno` (version not pinned)

### 3.3. Integration Points
-   **User:** Interacts via the Streamlit web interface.
-   **OpenAI API:** External API call for LLM services.
-   **Local File System:** For temporary storage of uploaded data.

## 4. User Flows

### 4.1. Main Workflows
1.  **Initialization & API Key Entry:**
    *   User launches the Streamlit app.
    *   User enters their OpenAI API key in the sidebar.
2.  **Data Upload & Preview:**
    *   User uploads a CSV or Excel file.
    *   Application validates file type.
    *   Application saves data to a temporary local CSV.
    *   Application displays a preview of the data.
3.  **Querying Data:**
    *   User types a natural language query into the text input area.
    *   User submits the query.
4.  **Processing & Results:**
    *   Agent (DuckDbAgent with GPT-4) converts NL query to SQL.
    *   SQL query is executed on the data in DuckDB.
    *   Results (text, SQL) are displayed in the UI.

### 4.2. Input/Output Specifications
-   **Input:**
    -   OpenAI API Key: String.
    -   Data File: `.csv`, `.xlsx`.
    -   User Query: Plain text.
-   **Output:**
    -   Data Preview: Streamlit DataFrame.
    -   Query Response: Markdown formatted text (answer, SQL query).
    -   Error/Warning Messages: Text in UI.

### 4.3. Error Handling (Observed)
-   Unsupported file format upload: Error message displayed.
-   Errors during file reading/preprocessing: Error message displayed.
-   Empty query submission: Warning message displayed.
-   Errors during agent's query processing or LLM interaction: Error message displayed.
-   Missing OpenAI API key: Warning message displayed, query submission prevented.

## 5. Configuration

### 5.1. Environment Variables
-   No explicit use of environment variables for configuration is observed in the sample script itself, other than the OpenAI API key which is input via the UI.

### 5.2. Required Services
-   Internet access (for OpenAI API).
-   Locally running Python environment with all dependencies.

### 5.3. Security Considerations (As-Is)
-   **OpenAI API Key:** Handled via Streamlit session state. The security relies on Streamlit's session management and the local environment's security. The key is not persistently stored by the application beyond the session.
-   **Data Privacy:** Uploaded data is processed locally and stored in a temporary file on the user's machine. It is sent to the OpenAI API only as part of the context for query generation if the `DuckDbAgent` includes data snippets in its prompts (behavior of `DuckDbAgent` schema/prompting needs deeper inspection if data privacy is paramount for the actual data content). The sample README mentions, "Your data is processed locally."

## 6. Deployment (As-Is for the Sample)

### 6.1. System Requirements
-   Python 3.x installed.
-   Ability to install Python packages via pip.
-   Web browser to access the Streamlit application.
-   Internet connection.

### 6.2. Installation Steps (for the sample)
1.  Clone the repository (or obtain the `ai_data_analyst.py` and `requirements.txt` files).
2.  Create a Python virtual environment (recommended).
3.  Install dependencies: `pip install -r requirements.txt`.
4.  Run the application: `streamlit run ai_data_analyst.py`.

### 6.3. Configuration Management
-   OpenAI API key is configured at runtime via the UI.
-   No other external configuration files are used by the sample.

---

This "as-is" PRD aims to capture the current state of the sample `ai_data_analyst.py` script. It will serve as the baseline for the `/agent-boarding-transfer` workflow, where it will be compared against the target `agent.json` for the `data-analyzer-bot` to identify gaps and plan refactoring.
**Author:** Agentopia Core Team

## 1. Introduction

The Data Analyzer Bot is an AI-powered agent designed to automate the initial stages of Exploratory Data Analysis (EDA) for tabular datasets (CSV and Excel files). It aims to provide users with a quick, comprehensive, and easy-to-understand overview of their data, including statistical profiles, visualizations, and (optionally) LLM-generated insights, all while ensuring data privacy through local execution.

## 2. Goals and Objectives

*   **Democratize Data Understanding:** Enable users with varying technical skills (from data analysts to business users) to quickly gain insights from their data without needing to write code.
*   **Accelerate EDA:** Significantly reduce the time and effort required for initial data exploration and reporting.
*   **Promote Data Quality Awareness:** Help users identify potential data quality issues (e.g., missing values, outliers, inconsistent types) early in their workflow.
*   **Facilitate Data-Driven Decisions:** Provide a foundational understanding of datasets to support better decision-making and further analysis.
*   **Uphold Privacy:** Ensure user data remains on their local machine throughout the analysis process.

## 3. Target Audience

*   **Data Analysts / Scientists:** As a tool for rapid initial assessment of new datasets, freeing up time for more complex analysis.
*   **Business Users / Citizen Data Scientists:** To explore and understand data relevant to their domain without requiring deep programming or statistical knowledge.
*   **Students / Researchers:** As an educational tool to learn about datasets and EDA principles.
*   **Anyone working with tabular data:** Who needs a quick and standardized way to profile and visualize datasets.

## 4. Scope

### 4.1. In Scope (Minimum Viable Product - MVP)

*   **Data Input:**
    *   Support for local CSV files.
    *   Support for local Excel files (`.xlsx`, `.xls`), reading the first sheet by default.
*   **Core EDA Operations (Automated):**
    *   **Data Profiling:**
        *   Dataset dimensions (number of rows, columns).
        *   Column names and inferred data types (numerical, categorical, datetime, boolean).
        *   Count and percentage of missing values per column.
        *   Basic descriptive statistics for numerical columns (mean, median, mode, std dev, min, 25th/50th/75th percentiles, max).
        *   Frequency counts and unique value counts for categorical columns.
    *   **Automated Visualizations (Saved as image files):**
        *   Histograms for numerical columns.
        *   Bar charts for high-cardinality categorical columns (e.g., top N categories).
        *   Correlation heatmap for numerical columns (Pearson correlation).
*   **LLM-Powered Insights (Optional, via user-provided API key):**
    *   Generation of a natural language summary of the dataset's key characteristics.
    *   Identification of 2-3 potentially interesting patterns, anomalies, or insights based on the programmatic EDA results.
*   **Output:**
    *   All generated files (charts, text summaries) saved to a user-specified local directory.
    *   A consolidated HTML report (`report.html`) summarizing all findings, viewable in a local web browser.
*   **Execution Environment:**
    *   Runnable via Docker container.
    *   Runnable as a local Python script.
*   **Configuration:**
    *   Command-line arguments for input file path and output directory path.
    *   Environment variable for LLM API key (e.g., `OPENAI_API_KEY`).

### 4.2. Out of Scope (for MVP)

*   Advanced statistical modeling or predictive analytics.
*   Direct data cleaning or transformation capabilities (beyond basic type inference).
*   Real-time data streaming or analysis of data in databases (MVP focuses on local files).
*   Interactive dashboards or UIs beyond the static HTML report.
*   User authentication or multi-user collaboration features.
*   Support for data formats other than CSV/Excel.
*   Complex time-series specific analysis.
*   Generation of code (e.g., Python scripts for further analysis).

## 5. Features (MVP)

| Feature ID | Feature Name                      | Description                                                                                                                                                              | User Benefit                                                                                                |
| :--------- | :-------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------- |
| F01        | CSV File Input                    | User can provide a path to a local CSV file for analysis.                                                                                                                | Supports a common data format.                                                                              |
| F02        | Excel File Input                  | User can provide a path to a local Excel file (`.xlsx`, `.xls`) for analysis.                                                                                            | Supports another widely used business data format.                                                          |
| F03        | Data Dimensions                   | Report the number of rows and columns in the dataset.                                                                                                                    | Provides a basic understanding of dataset size.                                                             |
| F04        | Column Profiling                  | List all column names and their inferred data types (e.g., integer, float, string, boolean, date).                                                                       | Helps understand data structure and identify potential type issues.                                         |
| F05        | Missing Value Analysis            | For each column, report the count and percentage of missing values.                                                                                                      | Highlights data completeness issues critical for further analysis.                                          |
| F06        | Numerical Column Statistics       | For numerical columns, calculate and display mean, median, mode, std dev, min, 25th/50th/75th percentiles, max.                                                            | Offers a statistical summary of numerical data distributions.                                               |
| F07        | Categorical Column Statistics     | For categorical columns, display unique value counts and frequency of top N categories.                                                                                    | Summarizes categorical data distributions and identifies common values.                                     |
| F08        | Numerical Distribution (Histogram) | Generate and save histograms for each numerical column.                                                                                                                  | Visualizes the distribution of numerical features.                                                          |
| F09        | Categorical Distribution (Bar Chart) | Generate and save bar charts for high-cardinality categorical columns (displaying top N categories and their frequencies).                                               | Visualizes the frequency of categorical features.                                                           |
| F10        | Correlation Heatmap               | Generate and save a heatmap showing Pearson correlation coefficients between numerical columns.                                                                            | Helps identify linear relationships between numerical variables.                                            |
| F11        | LLM Summary (Optional)            | If an API key is provided, use an LLM to generate a natural language summary of the dataset's characteristics and 2-3 notable observations from the EDA.                  | Provides an easy-to-digest narrative of the data, making insights more accessible.                          |
| F12        | Local HTML Report                 | Consolidate all analyses, statistics, and visualizations into a single HTML file saved locally, viewable in a browser.                                                   | Offers a comprehensive, shareable, and easily accessible output of the EDA.                                 |
| F13        | Docker Execution                  | Provide a Dockerfile and instructions to run the agent in a containerized environment.                                                                                   | Simplifies setup and ensures consistent execution across different systems.                                 |
| F14        | Local Python Execution            | Allow users to run the agent as a Python script directly in their local environment (with dependencies managed via `requirements.txt`).                                    | Offers flexibility for users who prefer not to use Docker or want to integrate with other Python workflows. |
| F15        | Configurable Input/Output Paths   | Allow users to specify input data file path and output directory path via command-line arguments.                                                                        | Gives users control over where their data is read from and where results are saved.                         |

## 6. Success Metrics

*   **Adoption Rate:** Number of downloads/pulls of the Docker image or clones of the agent code.
*   **User Feedback:** Qualitative feedback gathered through surveys, GitHub issues, or community channels.
*   **Completion Rate:** Percentage of analyses run successfully without critical errors.
*   **Time Saved:** Estimated time saved by users compared to manual EDA (can be gauged via user feedback).
*   **Contribution:** Number of community contributions (e.g., bug fixes, feature suggestions, documentation improvements).

## 7. Future Enhancements / Roadmap

*   **Interactive HTML Report:** Incorporate JavaScript libraries (e.g., Plotly, D3.js) for interactive charts within the HTML report (zooming, panning, tooltips).
*   **Data Cleaning Suggestions:** Identify common data issues (e.g., outliers, mixed data types in a column) and suggest potential cleaning steps.
*   **Advanced Statistical Tests:** Option to perform basic statistical tests (e.g., t-tests, chi-squared tests) based on data characteristics.
*   **Natural Language Querying:** Allow users to ask simple questions about their data (e.g., "What's the average of column X?").
*   **Support for More Data Formats:** Add support for Parquet, JSON lines, etc.
*   **Direct Database Connection:** Allow analysis of data directly from SQL databases.
*   **Customizable Analysis:** Allow users to select which analyses or visualizations to run via a configuration file or CLI flags.
*   **Trend and Anomaly Detection:** Basic time-series decomposition and anomaly highlighting if date/time columns are present.
*   **Export Options:** Allow exporting the report to PDF or other formats.

## 8. Technical Considerations

*   **Primary Language:** Python.
*   **Core Libraries:** Pandas (data manipulation), NumPy (numerical operations), Matplotlib/Seaborn (static visualizations), Jinja2 (HTML templating), Openpyxl (Excel reading).
*   **LLM Integration:** OpenAI API (initially), with potential to support other local or cloud-based LLMs.
*   **Execution:** Local execution via Docker or Python script. No external server dependencies for core functionality.
*   **Output:** HTML, PNG/JPG for charts, TXT/Markdown for summaries.

## 9. Privacy and Security

*   **Local First:** All user data (input files) and generated reports remain on the user's local machine. Data is not uploaded to any central server by the agent.
*   **LLM Data Transmission:** If LLM features are used, only aggregated statistics, column metadata, and contextual information (not the raw dataset itself in bulk) will be sent to the LLM provider. Users will be informed of this and will use their own API keys.
*   **API Key Management:** LLM API keys are to be managed by the user as environment variables and are not stored by the agent.
