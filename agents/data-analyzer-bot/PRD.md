# Product Requirements Document: Data Analyzer Bot

**Version:** 0.1
**Date:** 2025-06-04
**Status:** Draft
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
