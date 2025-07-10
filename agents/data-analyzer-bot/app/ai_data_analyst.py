"""
Main Streamlit application for the Data Analyzer Bot.

This script launches a web-based interface that allows users to upload a dataset
(CSV or Excel) and perform various data analysis tasks, including interactive
queries, automated analysis, visualization generation, and AI-powered summaries.
It integrates with multiple LLM providers to power its analytical capabilities.
"""

import csv
import os
import tempfile

import pandas as pd
import numpy as np
from dotenv import load_dotenv
import streamlit as st
import markdown
from phi.assistant import Assistant
from phi.llm.anthropic.claude import Claude
from phi.llm.openai import OpenAIChat
from phi.tools.pandas import PandasTools
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import logging

# Import custom UI components
from ui_components import display_sidebar_header, display_agent_title, display_sidebar_footer, display_welcome_message


# Create a custom wrapper for PandasTools to handle DataFrame operations correctly
class CustomPandasTools(PandasTools):
    """
    A custom toolkit for pandas DataFrame operations, extending the base PandasTools.

    This class is initialized with a pandas DataFrame and provides various methods
    to analyze and manipulate the data, which can be exposed as tools to an AI assistant.
    """

    def run_dataframe_operation(self, dataframe_name, operation, operation_parameters=None):
        if operation_parameters is None:
            operation_parameters = {}

        df = self.dataframes.get(dataframe_name)
        if df is None:
            return f"DataFrame '{dataframe_name}' not found."

        if operation == "shape":
            shape = df.shape
            return f"DataFrame shape: {shape[0]} rows × {shape[1]} columns"
        elif operation == "info":
            import io

            buffer = io.StringIO()
            df.info(buf=buffer)
            return buffer.getvalue()

        try:
            # Get the attribute or method from the DataFrame
            attr = getattr(df, operation)
            if callable(attr):
                # If it's a method, call it with parameters
                result = attr(**operation_parameters)
            else:
                # If it's an attribute, just return it
                result = attr
            return result
        except Exception as e:
            return f"Error running operation '{operation}': {e}"


# --- Page Configuration ---
st.set_page_config(page_title="Data Analyzer Bot", page_icon="🤖", layout="wide")

# --- Logger Configuration ---
logger = logging.getLogger(__name__)


# Check if anthropic package is available
def is_anthropic_available():
    try:
        import anthropic

        return True
    except ImportError:
        return False


# Function to preprocess and save the uploaded file
def preprocess_and_save(file):
    """
    Preprocesses an uploaded data file and saves it to a temporary CSV.

    Handles CSV and Excel files, attempts to parse dates and numeric types,
    and ensures string columns are properly quoted for reliable processing.

    Args:
        file: An uploaded file object from Streamlit's file_uploader.

    Returns:
        A tuple containing the path to the temporary file, a list of column names,
        and the processed pandas DataFrame. Returns (None, None, None) on error.
    """
    try:
        # Read the uploaded file into a DataFrame
        if file.name.endswith(".csv"):
            df = pd.read_csv(file, encoding="utf-8", na_values=["NA", "N/A", "missing"])
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file, na_values=["NA", "N/A", "missing"])
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None, None, None

        # Ensure string columns are properly quoted
        for col in df.select_dtypes(include=["object"]):
            df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)

        # Parse dates and numeric columns
        for col in df.columns:
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col], errors="coerce")
            elif df[col].dtype == "object":
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    # Keep as is if conversion fails
                    pass

        # Create a temporary file to save the preprocessed data
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_path = temp_file.name
            # Save the DataFrame to the temporary CSV file with quotes around string fields
            df.to_csv(temp_path, index=False, quoting=csv.QUOTE_ALL)

        return temp_path, df.columns.tolist(), df  # Return the DataFrame as well
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None, None, None


# Load environment variables from .env file
load_dotenv()


# Function to initialize session state variables
def initialize_session_state():
    """Initializes all required keys in Streamlit's session state.

    This function ensures that all necessary variables for tracking API keys,
    LLM providers, dataframes, chat history, and analysis results are available
    from the start of the user session, preventing KeyErrors.
    """
    # Initialize dictionary to hold API keys, loading from environment variables if available
    if "api_keys" not in st.session_state:
        st.session_state.api_keys = {
            "openai": os.getenv("OPENAI_API_KEY", ""),
            "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
        }

    # Initialize selected LLM provider
    if "selected_llm_provider" not in st.session_state:
        st.session_state.selected_llm_provider = "OpenAI"

    # Initialize PandasTools instance
    if "pandas_tools_instance" not in st.session_state:
        st.session_state.pandas_tools_instance = CustomPandasTools()
    if "ai_summary" not in st.session_state:
        st.session_state.ai_summary = None
    if "df" not in st.session_state:
        st.session_state.df = None
    if "automated_analysis" not in st.session_state:
        st.session_state.automated_analysis = ""
    if "query_responses" not in st.session_state:
        st.session_state.query_responses = []
    if "plots" not in st.session_state:
        st.session_state.plots = []
    if "html_report" not in st.session_state:
        st.session_state.html_report = None


# Helper function to convert matplotlib figures to base64
def fig_to_base64(fig):
    img = BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()


def get_llm_instance(provider, api_key):
    """Initializes and returns an LLM instance based on the selected provider.

    Args:
        provider (str): The name of the LLM provider (e.g., 'OpenAI', 'Ollama').
        api_key (str): The API key for the selected provider.

    Returns:
        An instance of the phi-llm class corresponding to the provider, or None if
        the provider is unsupported or unavailable.
    """
    if provider == "OpenAI":
        return OpenAIChat(model="gpt-4-turbo", api_key=api_key)
    elif provider == "Anthropic":
        if is_anthropic_available():
            return Claude(model="claude-3-opus-20240229", api_key=api_key)
        else:
            st.warning("Anthropic package not found. Please install it to use Claude models.")
            return None
    elif provider == "Ollama":
        from phi.llm.ollama import Ollama

        return Ollama(model="llama3")  # Assumes llama3 is the model to use
    else:
        st.error(f"Provider {provider} not currently supported.")
        return None


def generate_visualizations(df):
    """Generates a variety of plots for a given DataFrame.

    Creates histograms for numerical columns, bar charts for categorical columns,
    a correlation heatmap, and a pair plot if applicable.

    Args:
        df (pd.DataFrame): The DataFrame to visualize.

    Returns:
        A list of tuples, where each tuple contains a plot title and a
        matplotlib figure object.
    """
    plots_list = []
    numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if numerical_cols:
        for col in numerical_cols:
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            ax.set_title(f"Histogram of {col}")
            plots_list.append((f"Histogram of {col}", fig))

    if categorical_cols:
        for col in categorical_cols:
            if 1 < df[col].nunique() < 50:
                fig, ax = plt.subplots()
                sns.countplot(y=col, data=df, order=df[col].value_counts().index[:20])
                ax.set_title(f"Bar Chart of {col}")
                plots_list.append((f"Bar Chart of {col}", fig))

    if len(numerical_cols) > 1:
        fig, ax = plt.subplots(figsize=(10, 8))
        corr = df[numerical_cols].corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Matrix")
        plots_list.append(("Correlation Heatmap", fig))

    if 1 < len(numerical_cols) <= 5:
        pair_plot_fig = sns.pairplot(df[numerical_cols])
        plots_list.append(("Pair Plot", pair_plot_fig.fig))

    return plots_list


def main():
    """
    Main function to run the Streamlit application.
    It handles the UI layout, user inputs, and orchestrates the data analysis process.
    """
    # --- Sidebar Controls ---
    with st.sidebar:
        display_sidebar_header()
        st.header("⚙️ Controls")
        st.info("Manage your analysis settings here. Upload your data in the main panel to get started.")

        # LLM Provider Selection
        llm_provider_options = ["OpenAI", "Groq", "Ollama"]
        if is_anthropic_available():
            llm_provider_options.insert(1, "Anthropic")

        llm_provider = st.selectbox(
            "Choose LLM Provider",
            options=llm_provider_options,
            index=0,
            help="Select the Large Language Model provider you want to use.",
        )
        st.session_state.selected_llm_provider = llm_provider

        # API Key Input
        api_key = ""
        if llm_provider in ["OpenAI", "Anthropic", "Groq"]:
            key_name = llm_provider.lower()
            api_key_label = f"{llm_provider} API Key"
            api_key = st.text_input(
                api_key_label,
                type="password",
                value=st.session_state.api_keys.get(key_name, ""),
                help=f"Enter your {api_key_label} to enable AI features.",
            )
            st.session_state.api_keys[key_name] = api_key
        elif llm_provider == "Ollama":
            st.info("Ollama is running locally. No API key needed.")
            api_key = "ollama"  # A non-empty string to pass checks

        # Advanced Settings
        with st.expander("Advanced Settings"):
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.2,
                step=0.1,
                help="Controls the randomness of the AI's responses. Lower is more deterministic.",
            )
            st.session_state.temperature = temperature

        display_sidebar_footer()

    # --- Main Application Panel ---
    display_agent_title(icon="📊", agent_name="Data Analyzer Bot")

    # Check if data is loaded
    if "df" not in st.session_state or st.session_state.df is None:
        # Show welcome message and file uploader if no data is loaded
        display_welcome_message()
        uploaded_file = st.file_uploader(
            "Upload a CSV or Excel file to start analyzing.",
            type=["csv", "xlsx"],
            label_visibility="collapsed",
        )
        if uploaded_file:
            with st.spinner("⏳ Processing your data... This may take a moment."):
                file_path, _, df = preprocess_and_save(uploaded_file)
                if file_path and df is not None:
                    st.session_state.file_path = file_path
                    st.session_state.df = df
                    st.session_state.file_name = uploaded_file.name
                    st.rerun()
    else:
        # Data is loaded, show the main analysis interface
        df = st.session_state.df
        # Ensure the dataframe is always available in the tools instance
        st.session_state.pandas_tools_instance.dataframes = {"df": df}
        st.success(f"Successfully loaded and processed `{st.session_state.file_name}`.")

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "❓ Interactive Query",
                "📊 Automated Analysis",
                "📈 Visualizations",
                "🤖 AI Summary",
                "📄 HTML Report",
            ]
        )

        with tab1:
            st.header("❓ Ask Questions About Your Data")
            st.info(
                "Use the chat interface below to ask questions about your dataset. "
                "The AI will generate Python code to answer your question and display the result."
            )

            query_input = st.text_input(
                "Enter your question:",
                placeholder="e.g., 'What is the average value of column X?' or 'Plot a histogram of the age column'",
            )

            if st.button("Get Answer"):
                if not query_input:
                    st.warning("Please enter a question.")
                else:
                    can_proceed_with_llm = False
                    active_api_key = None
                    provider = st.session_state.selected_llm_provider

                    if provider in ["OpenAI", "Anthropic", "Groq"] and st.session_state.api_keys.get(provider.lower()):
                        can_proceed_with_llm = True
                        active_api_key = st.session_state.api_keys[provider.lower()]
                    elif provider == "Ollama":
                        can_proceed_with_llm = True

                    if not can_proceed_with_llm:
                        st.error(f"Please provide an API key for {provider} in the sidebar.")
                    else:
                        with st.spinner("🤔 Thinking..."):
                            try:
                                df_head = df.head().to_string()
                                df_shape = f"{df.shape[0]} rows, {df.shape[1]} columns"
                                df_columns = ", ".join(df.columns)
                                final_query = f"""I have a pandas DataFrame named 'df'. Here are its properties:
- Shape: {df_shape}
- Columns: {df_columns}
- Head:\n{df_head}\n\nBased on this dataframe, please answer the following question: {query_input}"""

                                data_analyst_assistant = Assistant(
                                    llm=get_llm_instance(provider, active_api_key),
                                    tools=[st.session_state.pandas_tools_instance],
                                    show_tool_calls=True,
                                    markdown=True,
                                )

                                response = ""
                                for part in data_analyst_assistant.run(final_query):
                                    response += str(part)

                                st.session_state.query_responses.append({"query": query_input, "response": response})

                            except Exception as e:
                                st.error(f"An error occurred: {e}")

            st.markdown("---")
            st.markdown("### Conversation History")
            if not st.session_state.query_responses:
                st.info("Your conversation history will appear here.")
            else:
                for item in reversed(st.session_state.query_responses):
                    with st.expander(f"**You:** {item['query']}"):
                        st.markdown(item["response"])

        with tab2:
            st.header("📊 Automated Analysis")
            st.info("Click the button to generate a comprehensive automated analysis of your dataset.")

            if "automated_analysis" not in st.session_state:
                st.session_state.automated_analysis = ""

            if not st.session_state.automated_analysis:
                if st.button("Generate Automated Analysis"):
                    provider = st.session_state.get("selected_llm_provider")
                    api_key = st.session_state.api_keys.get(provider.lower()) if provider else None

                    if provider and (api_key or provider == "Ollama"):
                        with st.spinner("🤖 Performing automated analysis..."):
                            try:
                                analysis_prompt = (
                                    "Please perform a comprehensive automated exploratory data analysis (EDA) on the dataframe `df`. "
                                    "Your analysis should be well-structured and include the following sections:\n"
                                    "1. **Data Overview:** Provide the shape (rows, columns), data types of each column, and check for missing values.\n"
                                    "2. **Descriptive Statistics:** Summarize the main statistical metrics for all numerical columns (mean, median, std, min, max, etc.).\n"
                                    "3. **Key Insights & Observations:** Based on the analysis, identify at least 3-5 key insights, patterns, or anomalies in the data. What are the most important takeaways?"
                                )
                                df_head = df.head().to_string()
                                df_shape = f"{df.shape[0]} rows, {df.shape[1]} columns"
                                df_columns = ", ".join(df.columns)
                                final_prompt = f"""I have a pandas DataFrame named 'df'.\nHere are its properties:\n- Shape: {df_shape}\n- Columns: {df_columns}\n- Head:\n{df_head}\n\nBased on this dataframe, please perform the following task: {analysis_prompt}"""

                                llm_instance = get_llm_instance(provider, api_key)
                                auto_analyst_assistant = Assistant(
                                    llm=llm_instance,
                                    description="You are a world-class data analyst.",
                                    show_tool_calls=False,
                                )

                                response_generator = auto_analyst_assistant.run(final_prompt)
                                st.session_state.automated_analysis = "".join(str(part) for part in response_generator)
                                st.rerun()

                            except Exception as e:
                                st.error(f"An error occurred during automated analysis: {e}")
                    else:
                        st.warning(
                            "Please select a provider and enter an API key in the sidebar to generate the analysis."
                        )

            if st.session_state.automated_analysis:
                st.markdown(st.session_state.automated_analysis)

        with tab3:
            st.header("📈 Visualizations")
            st.info("This tab automatically generates visualizations based on your data's column types.")

            if "plots" not in st.session_state or not st.session_state.plots:
                with st.spinner("📊 Generating visualizations..."):
                    st.session_state.plots = generate_visualizations(df)

            for title, fig in st.session_state.plots:
                st.write(f"### {title}")
                st.pyplot(fig)
                plt.close(fig)

        with tab4:
            st.header("🤖 AI Summary")
            st.info("Click the button to generate a high-level, executive summary of the data analysis.")

            if "ai_summary" not in st.session_state:
                st.session_state.ai_summary = ""

            if not st.session_state.ai_summary:
                if st.button("Generate AI Summary"):
                    provider = st.session_state.get("selected_llm_provider")
                    api_key = st.session_state.api_keys.get(provider.lower()) if provider else None

                    if provider and (api_key or provider == "Ollama"):
                        with st.spinner("✍️ Generating AI summary..."):
                            try:
                                summary_prompt = (
                                    "Please provide a high-level executive summary based on the provided data overview, analysis, and key insights. "
                                    "Focus on the most critical findings and their potential business implications. The summary should be concise and easy for a non-technical audience to understand."
                                )
                                df_head = df.head().to_string()
                                df_shape = f"{df.shape[0]} rows, {df.shape[1]} columns"
                                automated_analysis_context = st.session_state.get(
                                    "automated_analysis", "No analysis available."
                                )
                                final_prompt = f"""I have a pandas DataFrame with these properties:\n- Shape: {df_shape}\n- Head:\n{df_head}\n\nAn automated analysis was performed, yielding these results:\n{automated_analysis_context}\n\nBased on all this information, please perform the following task: {summary_prompt}"""

                                llm_instance = get_llm_instance(provider, api_key)
                                summary_assistant = Assistant(
                                    llm=llm_instance,
                                    description="You are an expert data analyst providing an executive summary.",
                                    show_tool_calls=False,
                                )

                                response_generator = summary_assistant.run(final_prompt)
                                st.session_state.ai_summary = "".join(str(part) for part in response_generator)
                                st.rerun()

                            except Exception as e:
                                st.error(f"An error occurred during AI summary generation: {e}")
                    else:
                        st.warning(
                            "Please select a provider and enter an API key in the sidebar to generate the summary."
                        )

            if st.session_state.ai_summary:
                st.markdown(st.session_state.ai_summary)

        with tab5:
            st.header("📄 HTML Report")
            st.info("Generate and download a complete HTML report of the analysis.")

            # Use checkboxes to select which sections to include
            include_summary = st.checkbox("Include AI Summary", value=True, key="include_summary_html")
            include_analysis = st.checkbox("Include Automated Analysis", value=True, key="include_analysis_html")
            include_visuals = st.checkbox("Include Visualizations", value=True, key="include_visuals_html")

            if st.button("Generate Report"):
                with st.spinner("Building your report..."):
                    # Fetch content from session state based on checkbox selection
                    summary_content = st.session_state.get("ai_summary", "") if include_summary else ""
                    analysis_content = st.session_state.get("automated_analysis", "") if include_analysis else ""
                    plots_content = st.session_state.get("plots", []) if include_visuals else []

                    # Generate the HTML
                    html_report = generate_html_report(df, summary_content, analysis_content, plots_content)
                    st.session_state.html_report = html_report
                    st.success("Report generated successfully!")

            # Display download button and preview if the report exists
            if st.session_state.get("html_report"):
                st.download_button(
                    label="📥 Download Report",
                    data=st.session_state.html_report,
                    file_name="data_analysis_report.html",
                    mime="text/html",
                )
                st.write("### Report Preview")
                st.components.v1.html(st.session_state.html_report, height=600, scrolling=True)


def generate_html_report(df, summary_content, analysis_content, plots):
    """Generates a self-contained HTML report of the EDA.

    Args:
        df (pd.DataFrame): The dataframe containing the data.
        summary_content (str): The AI-generated summary.
        analysis_content (str): The automated analysis markdown.
        plots (dict): A dictionary of plot titles and matplotlib figures.

    Returns:
        str: The complete HTML for the report.
    """
    # Convert plots to base64
    plots_html = ""
    if plots:
        for title, fig in plots.items():
            fig_b64 = fig_to_base64(fig)
            plots_html += f'<h2>{title}</h2>\n<img src="data:image/png;base64,{fig_b64}" alt="{title}">\n'

    # Convert markdown to HTML
    summary_html = markdown.markdown(summary_content) if summary_content else "<p>No summary generated.</p>"
    analysis_html = markdown.markdown(analysis_content) if analysis_content else "<p>No analysis generated.</p>"
    df_html = df.head().to_html(classes="table table-striped", justify="left")

    html_content = f"""
    <html>
    <head>
        <title>Data Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f9f9f9; }}
            h1, h2 {{ color: #333; border-bottom: 2px solid #ddd; padding-bottom: 10px;}}
            .section {{ background-color: #fff; border: 1px solid #ddd; padding: 20px; margin-bottom: 30px; border-radius: 5px; }}
            img {{ max-width: 100%; height: auto; border: 1px solid #ddd; padding: 5px; border-radius: 5px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Data Analysis Report</h1>
        
        <div class="section">
            <h2>AI Summary</h2>
            {summary_html}
        </div>
        
        <div class="section">
            <h2>Automated Analysis</h2>
            {analysis_html}
        </div>

        <div class="section">
            <h2>Data Preview (First 5 Rows)</h2>
            {df_html}
        </div>
        
        <div class="section">
            <h2>Visualizations</h2>
            {plots_html}
        </div>
    </body>
    </html>
    """
    return html_content


if __name__ == "__main__":
    initialize_session_state()
    main()
