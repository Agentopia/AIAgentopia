# Agent Manifest Schema Guide (`agent-manifest.schema.json`)

## 1. Introduction
*   Purpose of the agent manifest (`agent.json`).
*   Its role as the source of truth for agent metadata and configuration for the Agentopia platform.
*   The schema is designed to support Agentopia's core vision of privacy-first, locally-run agents. For more details, please see the [Agentopia Vision & Plan](./agentopia-vision-plan.md).
*   Manifest files are in JSON format. The formal schema definition can be found in the root of the `AIAgentopia` repository: [`agent-manifest.schema.json`](../agent-manifest.schema.json).

## 2. General Information & Identification

*   **`name`**: (string, required)
    *   Description: Unique, human-readable name for the agent. This name is used for display in the portal and for identification.
    *   Example: `"Data Analyzer Bot"`
*   **`description`**: (string, required)
    *   Description: A brief, one-sentence summary of the agent's primary function. This is often shown in list views or cards.
    *   Example: `"Analyzes CSV data to provide statistical insights and visualizations."`
*   **`long_description`**: (string, required)
    *   Description: A detailed explanation of the agent, its purpose, capabilities, and primary use cases. This field supports Markdown for rich formatting and will be the main content for the agent's overview section on its detail page.
    *   Example: `"This agent provides a comprehensive suite of tools for CSV data analysis. Users can upload their CSV files, and the agent will automatically perform data validation, generate descriptive statistics (mean, median, mode, standard deviation), identify outliers, and create interactive charts like histograms, scatter plots, and box plots to help visualize data distributions and relationships. It's designed for anyone needing to quickly understand datasets without writing complex code."`
*   **`version`**: (string, required)
    *   Description: Semantic version number for the agent (e.g., "1.0.0", "0.2.1-alpha"). Adhering to [SemVer](https://semver.org/) is recommended.
    *   Example: `"1.0.2"`
*   **`author`**: (string, required)
    *   Description: Name of the individual, team, or organization that created and/or maintains the agent.
    *   Example: `"Agentopia Core Team"`
*   **`deployment_status`**: (string, optional, default: `"development"`)
    *   Description: Indicates the current readiness state of the agent for deployment and visibility on the Agentopia portal. This helps manage the agent lifecycle from initial development to production release.
    *   Enum Values:
        *   `"development"`: The agent is currently under active development. It may be incomplete, unstable, or not yet fully documented. Agents in this state are typically not considered for public listing.
        *   `"review"`: The agent developer considers the agent feature-complete, well-documented, and has passed local validation (e.g., using `validate-agents.js`). It is ready for review by project maintainers or for staging/testing before production.
        *   `"production"`: The agent has been reviewed, validated, and approved for public listing on the Agentopia portal. It is considered stable and ready for general use.
    *   Example: `"development"`
*   **`icon`**: (string, optional, default: `""`)
    *   Description: An emoji character or a relative path to an icon image file (e.g., within the agent's own directory in the `AIAgentopia` repo) representing the agent. If using a path, ensure the portal can resolve it. Emojis are generally recommended for simplicity.
    *   Example: `"🤖"` or `"img/data-analyzer-icon.png"`

## 3. Categorization & Discovery

*   **`category`**: (string, required)
    *   Description: Primary functional or domain-oriented category for the agent.
    *   Enum Values:
        *   `"Productivity & Organization"`
        *   `"Content Creation & Design"`
        *   `"Data Analysis & Research"`
        *   `"Automation & Utilities"`
        *   `"Education & Learning"`
        *   `"Business & Finance"`
    *   Example: `"Data Analysis & Research"`
*   **`subcategory`**: (string, optional)
    *   Description: Optional sub-category for more granular functional classification.
    *   Example: `"Task Management"` (under `"Productivity & Organization"`)
*   **`agentType`**: (string, required)
    *   Description: Describes the agent's primary operational mode: Assistant (user-directed), Autonomous (self-directed), or Hybrid (mixed-initiative).
    *   Enum Values:
        *   `"Assistant"`
        *   `"Autonomous"`
        *   `"Hybrid"`
    *   Example: `"Autonomous"`
*   **`agentScale`**: (string, required)
    *   Description: Describes the structural complexity: Single-Agent (operates individually) or Multi-Agent (part of a coordinated team or system).
    *   Enum Values:
        *   `"Single-Agent"`
        *   `"Multi-Agent"`
    *   Example: `"Single-Agent"`
*   **`tags`**: (array of strings, required, minItems: 1)
    *   Description: A list of relevant keywords or phrases that help users discover the agent through search or tag-based filtering.
    *   Example: `["csv", "data analysis", "statistics", "visualization", "python"]`
*   **`use_cases`**: (array of strings, required, default: `[]`)
    *   Description: Specific, practical tasks or problems the agent is designed to solve. These provide concrete examples of the agent's utility.
    *   Example: `["Identifying sales trends from quarterly reports", "Automated data cleaning for machine learning datasets", "Generating quick summaries of long text documents"]`

## 4. Features & Development

*   **`features`**: (array of strings, required, minItems: 1)
    *   Description: A list of key capabilities or functionalities the agent currently offers.
    *   Example: `["CSV parsing and validation", "Descriptive statistics generation (mean, median, mode)", "Interactive chart plotting (histograms, scatter plots)", "Data export to JSON or Markdown"]`
*   **`roadmap_features`**: (array of strings, optional, default: `[]`)
    *   Description: A list of features or enhancements planned for future versions of this agent. This helps users understand the agent's development trajectory and potential.
    *   Example: `["Support for Excel (.xlsx) files", "Advanced time-series forecasting models", "Integration with SQL databases"]`

## 5. Setup, Execution & Configuration (Local First)

This section details how users will set up and run the agent, with a strong emphasis on local execution via Docker for privacy and control.

*   **`entry_point`**: (string, required)
    *   Description: Historically, the main script or command to start the agent. For Dockerized agents, this might be the `CMD` or `ENTRYPOINT` in the Dockerfile. While less directly invoked by users if `docker_run_instructions` are comprehensive, it's good for developers to specify the core executable or script.
    *   Example: `"app/main.py"` or `"run.sh"`
*   **`setup_instructions`**: (string, optional, default: `""`)
    *   Description: General introductory setup notes or prerequisites that users should be aware of before attempting to run the agent (e.g., "Requires Docker Desktop version X.Y or higher installed and running."). Detailed Docker execution steps belong in `docker_run_instructions`. Supports Markdown.
*   **`requirements`**: (array of strings, optional, default: `[]`)
    *   Description: A list of primary software dependencies or system requirements if they are not fully encapsulated by the Docker container (e.g., specific versions of Python or Node.js if the user were to build the Docker image themselves, or if there are client-side tools needed to interact with the agent). For end-users running a pre-built Docker image, this might be less critical but is useful for developers.
    *   Example: `["Python 3.9+", "Pandas >= 1.3", "A modern web browser for UI interaction (if applicable)"]`
*   **`docker_image_name`**: (string, required)
    *   Description: The full name of the Docker image for this agent, including any namespace and tag. This is used in `docker pull` and `docker run` commands.
    *   Example: `"agentopia/data-analyzer-bot:1.0.2"` or `"yourusername/youragent:latest"`
*   **`docker_pull_instructions`**: (string, optional, default: `""`)
    *   Description: Specific command or brief instructions for pulling the Docker image. If left empty, the Agentopia portal might default to displaying `docker pull [docker_image_name]`. Can be overridden for special cases (e.g., private registries requiring login). Supports Markdown.
    *   Example: `"docker pull agentopia/data-analyzer-bot:1.0.2"`
*   **`docker_run_instructions`**: (string, required)
    *   Description: Detailed instructions and example commands for running the agent via Docker. This is a critical field for user success and should cover essential aspects like:
        *   Volume mounting for input data and output results (e.g., `-v /path/to/your/data:/data`).
        *   Port mapping if the agent exposes a web UI or API (e.g., `-p 8080:5000`).
        *   Passing necessary environment variables for configuration (e.g., `-e API_KEY=your_value -e OUTPUT_FORMAT=json`).
        *   Any other required Docker flags or considerations.
        Supports Markdown for clarity and code blocks.
    *   Example (Markdown):
        ```markdown
        To run the Data Analyzer Bot, use the following command:

        ```
        docker run -it --rm \
          -v /local/path/to/input_csv_files:/app/input \
          -v /local/path/to/output_reports:/app/output \
          -e REPORT_TITLE="My Sales Analysis" \
          agentopia/data-analyzer-bot:1.0.2
        ```

        *   Mount your input CSV files to `/app/input`.
        *   Analysis reports will be saved in the directory mounted to `/app/output`.
        *   Set `REPORT_TITLE` for your generated reports.
        ```
*   **`config_fields`**: (array of objects, optional, default: `[]`)
    *   Description: Defines configuration options for the agent. These often translate to environment variables that need to be passed to the Docker container during `docker run` (e.g., using the `-e VAR=value` flag), or they might describe settings for a configuration file that can be volume-mounted. This section helps users understand how to customize the agent's behavior.
    *   Each object in the array has the following properties:
        *   `name`: (string, required) - The actual name of the configuration parameter or environment variable (e.g., `"API_KEY"`, `"OUTPUT_PATH"`).
        *   `label`: (string, required) - A human-readable label for the configuration field (e.g., `"Your OpenAI API Key"`, `"Default Output Directory"`).
        *   `type`: (string, required, enum: `["text", "password", "number", "select", "boolean"]`) - The data type of the field. `password` suggests the input might be sensitive.
        *   `required`: (boolean, optional, default: `false`) - Whether this configuration is mandatory for the agent to run.
        *   `default_value`: (string | number | boolean, optional) - A default value for the configuration if not provided by the user.
        *   `description`: (string, optional) - A brief explanation of what this configuration option does.
    *   Example:
        ```json
        [
          {
            "name": "OPENAI_API_KEY",
            "label": "OpenAI API Key",
            "type": "password",
            "required": true,
            "description": "Your OpenAI API key, required for accessing GPT models."
          },
          {
            "name": "DEFAULT_MODEL",
            "label": "Default LLM Model",
            "type": "text",
            "required": false,
            "default_value": "gpt-4o-mini",
            "description": "The default OpenAI model to use for analysis."
          }
        ]
        ```
*   **`llm_dependency`**: (object, required)
    *   Description: Describes if and how the agent utilizes Large Language Models (LLMs). This is essential for transparency regarding external service use and informs the user about necessary configurations (like API keys).
    *   Properties:
        *   `type`: (string, required, enum: `["openai", "anthropic", "google", "cohere", "local_api", "huggingface_api", "none"]`) - Specifies the type of LLM or LLM provider the agent is designed to work with. `"none"` indicates the agent does not use any LLM.
        *   `apiKeyEnvVar`: (string, optional) - The name of the environment variable the agent expects for the LLM API key (e.g., `"OPENAI_API_KEY"`). This is typically required if `type` refers to a cloud-based LLM provider.
        *   `apiEndpointEnvVar`: (string, optional) - The name of the environment variable the agent expects for the LLM API endpoint URL. Useful for `"local_api"` (e.g., Ollama, LM Studio) or self-hosted models.
        *   `modelRecommendation`: (string, optional) - A recommended model or family of models that work well with this agent (e.g., `"gpt-4o-mini"`, `"claude-3-opus"`, `"ollama/llama3"`).
        *   `notes`: (string, optional, default: `""`) - Additional important notes regarding LLM setup, such as specific API requirements, version compatibility, or guidance on choosing models. Supports Markdown.
    *   Example:
        ```json
        {
          "type": "openai",
          "apiKeyEnvVar": "OPENAI_API_KEY",
          "modelRecommendation": "gpt-4o-mini",
          "notes": "Ensure your OpenAI account has sufficient credits. This agent works best with models from the GPT-3.5 series or newer."
        }
        ```
        Or for no LLM:
        ```json
        {
          "type": "none"
        }
        ```

## 6. Access & Privacy

*   **`demo_url`**: (string, optional, format: `uri`, default: `""`)
    *   Description: A URL to an interactive online demo of the agent, if available (e.g., a Hugging Face Space, a Gradio app). It should be clearly communicated on the portal that online demos are for illustrative purposes with non-sensitive data; for use with private or sensitive data, the local Docker version of the agent must be used.
*   **`source_url`**: (string, optional, format: `uri`, default: `""`)
    *   Description: A URL to the agent's primary source code repository or a key resource for exploring its code (e.g., a GitHub repository, a Google Colab notebook).
*   **`privacy_considerations`**: (string, optional, default: `""`)
    *   Description: A dedicated section for the agent developer to explicitly state how the agent handles data, its privacy implications (especially if it interacts with any external services beyond user-configured LLMs), and any security notes. This reinforces Agentopia's commitment to user privacy. Supports Markdown.
    *   Example: `"This agent processes all data locally within its Docker container. No data is transmitted to external servers unless you configure it to use an external LLM, in which case data will be sent to your chosen LLM provider according to their terms. Output files are saved only to the local directory you specify."`

## 7. Example `agent.json`

```json
{
  "name": "Example Data Analyzer Bot",
  "description": "Analyzes CSV data for insights.",
  "long_description": "A more detailed description using **Markdown** for formatting. Explains what the bot does, its key benefits, and typical use cases. Designed for local execution to ensure data privacy.",
  "version": "1.0.0",
  "author": "Agentopia Team",
  "deployment_status": "development",
  "icon": "📊",
  "category": "Analytics",
  "type": "tool",
  "scale": "intermediate",
  "tags": ["data analysis", "csv", "python", "docker"],
  "use_cases": [
    "Quickly generate statistical summaries from CSV files.",
    "Visualize data distributions without coding."
  ],
  "features": [
    "Supports CSV and TSV file inputs.",
    "Generates mean, median, mode, and standard deviation.",
    "Outputs results as a Markdown report."
  ],
  "roadmap_features": [
    "Support for Parquet files.",
    "Correlation matrix generation."
  ],
  "entry_point": "analyzer/main.py",
  "setup_instructions": "Requires Docker Desktop. Ensure Docker is running before proceeding.",
  "requirements": ["Python 3.9+"],
  "docker_image_name": "agentopia/example-data-analyzer:1.0.0",
  "docker_pull_instructions": "docker pull agentopia/example-data-analyzer:1.0.0",
  "docker_run_instructions": "```bash\ndocker run --rm -it -v /path/to/your/data:/data -e OUTPUT_FILENAME=report.md agentopia/example-data-analyzer:1.0.0 your_input_file.csv\n```\nReplace `/path/to/your/data` with the actual path to your data directory on your host machine. The input CSV file should be inside this directory. The output report will be named `report.md` (or as specified by `OUTPUT_FILENAME`) and saved in the same mounted directory.",
  "config_fields": [
    {
      "name": "OUTPUT_FILENAME",
      "label": "Output Report Filename",
      "type": "text",
      "required": false,
      "default_value": "analysis_report.md",
      "description": "The desired filename for the output analysis report."
    }
  ],
  "llm_dependency": {
    "type": "none"
  },
  "demo_url": "https://huggingface.co/spaces/agentopia/example-data-analyzer-demo",
  "source_url": "https://github.com/Agentopia/AIAgentopia/tree/main/agents/example-data-analyzer",
  "privacy_considerations": "This agent runs entirely locally. All data processing occurs on your machine within the Docker container. No data is sent to Agentopia or any third parties."
}
```

This guide should help developers create comprehensive and consistent `agent.json` manifest files that align with Agentopia's vision and provide users with all necessary information.
