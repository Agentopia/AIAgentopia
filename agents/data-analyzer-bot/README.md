# Data Analyzer Bot 📊

**Version:** 0.1.0
**Author:** Agentopia Core Team
**Category:** Data Analysis & Research
**Type:** Regular Agent

## Overview

The Data Analyzer Bot empowers you to quickly understand your tabular datasets (CSV or Excel files) without writing any code. Upload your data, and the bot performs an automated Exploratory Data Analysis (EDA), saving a comprehensive report and individual analysis files directly to your local machine.

The generated output includes:

*   **Data Profile:** Key statistics such as row and column counts, data type identification for each column, analysis of missing values, descriptive statistics for numerical columns (mean, median, standard deviation, min/max), and frequency counts for categorical columns.
*   **Automated Visualizations:** A suite of common charts to help you visualize your data, including histograms for numerical distributions, bar charts for categorical frequencies, and a correlation heatmap for numerical features. These are saved as individual image files.
*   **LLM-Powered Summary (Optional):** If configured with an API key (e.g., OpenAI), the bot can generate a natural language summary of the dataset's main characteristics, highlighting 2-3 potentially interesting observations or anomalies.
*   **Consolidated HTML Report:** A user-friendly HTML file (`report.html`) is generated in your specified output directory. You can open this file in any web browser to view all analyses, statistics, and visualizations in one convenient place.

This bot is designed with a **local-first** approach, ensuring your data remains private and is processed on your own machine. It's an ideal tool for data analysts needing a rapid first look at new data, business users aiming to understand data without delving into code, or anyone requiring a quick, standardized report on a dataset.

## Key Features

*   Supports CSV and Excel file inputs.
*   Performs automated data profiling (dimensions, data types, missing values).
*   Calculates descriptive statistics for both numerical and categorical columns.
*   Generates key visualizations (histograms, bar charts, correlation heatmap) and saves them as image files.
*   Optionally provides an LLM-generated natural language summary of data characteristics and insights.
*   Outputs a consolidated HTML report for easy viewing and sharing.
*   All data processing and report generation occurs locally, respecting your data privacy.

## Use Cases

*   Get a quick overview and initial understanding of a new dataset.
*   Automate the initial, often time-consuming, steps of Exploratory Data Analysis (EDA).
*   Identify potential data quality issues (e.g., missing values, outliers) early in your workflow.
*   Generate a basic, shareable HTML report with key statistics and visualizations for a dataset.
*   Prepare for more in-depth analysis or machine learning model training by understanding fundamental data characteristics.

## Prerequisites

*   Python 3.8 or higher installed on your system.
*   Docker installed and running (if you choose the Docker-based execution).
*   An OpenAI API key (or other supported LLM provider key) if you wish to use the LLM-powered summary feature. This should be set as an environment variable (`OPENAI_API_KEY`).

## Setup and Execution

You can run the Data Analyzer Bot using Docker (recommended for ease of use and dependency management) or directly with Python.

### Option 1: Running with Docker (Recommended)

1.  **Pull the Docker Image:**
    ```bash
    docker pull agentopia/data-analyzer-bot:0.1.0
    ```

2.  **Prepare Your Data and Output Directory:**
    *   Create a working directory on your host machine (e.g., `C:\my_data_analysis` or `/home/user/my_data_analysis`).
    *   Place the CSV or Excel file you want to analyze into this directory (e.g., `C:\my_data_analysis\my_dataset.csv`).
    *   The bot will save its output (including `report.html` and chart images) into a subdirectory (e.g., `output`) within this working directory.

3.  **Set Environment Variables (If using LLM for summaries):**
    *   `OPENAI_API_KEY`: Your OpenAI API key.

4.  **Run the Docker Container:**
    Open your terminal or command prompt and execute the following command, replacing placeholders with your actual paths and API key:

    ```bash
    docker run -it --rm \
      -v /path/to/your/work_dir:/app/data \
      -e OPENAI_API_KEY="your_openai_api_key_here" \
      agentopia/data-analyzer-bot:0.1.0 \
      --data_file /app/data/your_file_name.csv \
      --output_dir /app/data/output
    ```

    **Command Explanation:**
    *   `docker run -it --rm`: Runs the container in interactive mode (`-it`) and automatically removes it when it exits (`--rm`).
    *   `-v /path/to/your/work_dir:/app/data`: This is crucial. It mounts your local working directory (e.g., `C:\my_data_analysis`) into the container at the `/app/data` path.
        *   **Replace `/path/to/your/work_dir` with the absolute path to your actual working directory.**
    *   `-e OPENAI_API_KEY="your_openai_api_key_here"`: Sets the OpenAI API key as an environment variable inside the container.
        *   **Replace `your_openai_api_key_here` with your actual key.** Omit this line if you don't want to use LLM-powered summaries.
    *   `agentopia/data-analyzer-bot:0.1.0`: Specifies the Docker image to use.
    *   `--data_file /app/data/your_file_name.csv`: This argument is passed to the agent's script. It tells the bot where to find the data file *inside the container's file system*.
        *   **Replace `your_file_name.csv` with the actual name of your data file.**
    *   `--output_dir /app/data/output`: This argument tells the bot where to save the generated report and files *inside the container*. These will appear in `/path/to/your/work_dir/output` on your local machine.

5.  **Accessing Results:**
    After the bot finishes processing, navigate to the output directory you specified (e.g., `/path/to/your/work_dir/output`) on your local machine. Open the `report.html` file in your web browser to view the full analysis.

### Option 2: Running Locally with Python

1.  **Clone/Download Agent Files:**
    Obtain the agent's source code. If it's part of a larger repository, navigate to the `agents/data-analyzer-bot` directory.

2.  **Create and Activate Virtual Environment:**
    It's highly recommended to use a Python virtual environment.
    ```bash
    python -m venv .venv
    ```
    Activate it:
    *   Windows: `.venv\Scripts\activate`
    *   macOS/Linux: `source .venv/bin/activate`

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Note: A `requirements.txt` file would need to be created for the bot, listing pandas, numpy, matplotlib, seaborn, openpyxl, python-dotenv, openai, jinja2).

4.  **Set Environment Variables (If using LLM):**
    Set the `OPENAI_API_KEY` environment variable in your terminal session or using a `.env` file (if the script supports `python-dotenv`).
    *   Example (bash/zsh): `export OPENAI_API_KEY="your_openai_api_key_here"`
    *   Example (PowerShell): `$env:OPENAI_API_KEY="your_openai_api_key_here"`

5.  **Run the Streamlit App:**
    Execute the Streamlit application directly using the virtual environment's Streamlit executable:
    ```bash
    # On Windows:
    .venv\Scripts\streamlit.exe run app\ai_data_analyst.py

    # On macOS/Linux:
    .venv/bin/streamlit run app/ai_data_analyst.py
    ```

    This will start the Streamlit web interface. Open your browser to the URL shown in the terminal (typically http://localhost:8501) to access the Data Analyzer Bot's interface.

6.  **Accessing Results:**
    After the script finishes, navigate to the output directory you specified (e.g., `./my_eda_results`). Open `report.html` in your web browser.

## Configuration

The Data Analyzer Bot is configured through its web-based user interface:

1. **Data Upload**: The Streamlit interface allows you to upload CSV or Excel files directly through the browser.

2. **Output Directory**: You can specify the output directory for reports and visualizations within the web interface.

3. **LLM Provider Selection**: Choose between OpenAI or Anthropic Claude for generating insights (if API keys are provided).

Environment Variables:
*   `OPENAI_API_KEY`: (Optional) Your API key for OpenAI if you want to enable OpenAI-based summaries.
*   `ANTHROPIC_API_KEY`: (Optional) Your API key for Anthropic if you want to use Claude for generating insights.

## LLM Dependency and Privacy

*   **LLM Usage:** This agent can optionally use an LLM (e.g., OpenAI's GPT models) to generate natural language summaries and insights based on the structured data profile and visualizations it creates.
*   **API Key:** To use LLM features, you must provide your own API key (e.g., `OPENAI_API_KEY` as an environment variable). You are responsible for any costs associated with the LLM API usage.
*   **Data Sent to LLM:** The bot is designed to send only aggregated statistics, column names, and contextual information about the data (not the raw data itself in bulk) to the LLM for generating summaries. However, always be mindful of the data being processed and the LLM provider's policies.
*   **Local Processing:** All core data loading, profiling, and visualization generation happen locally on your machine. The generated HTML report and image files are also saved locally.

## Roadmap Features

We plan to enhance the Data Analyzer Bot with features like:

*   Interactive chart customization within the HTML report.
*   Natural language querying of the dataset.
*   Advanced statistical tests (e.g., t-tests, ANOVA).
*   Data cleaning suggestions.
*   Support for more data formats.

## Contributing

(Details to be added later - e.g., link to `CONTRIBUTING.md` in the main project)

## Issues

(Details to be added later - e.g., link to GitHub issues for the project)
