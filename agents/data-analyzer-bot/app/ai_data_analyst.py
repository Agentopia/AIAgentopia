import csv
import os
import tempfile

import pandas as pd
import numpy as np
from dotenv import load_dotenv
import streamlit as st
from phi.assistant import Assistant
from phi.llm.anthropic.claude import Claude
from phi.llm.openai import OpenAIChat
from phi.tools.pandas import PandasTools
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import markdown


# Check if anthropic package is available
def is_anthropic_available():
    try:
        import anthropic

        return True
    except ImportError:
        return False


# Function to preprocess and save the uploaded file
def preprocess_and_save(file):
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
        # Create a custom wrapper for PandasTools to handle DataFrame operations correctly
        class CustomPandasTools(PandasTools):
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
                elif operation == "columns":
                    columns = df.columns.tolist()
                    return f"DataFrame columns: {columns}"

                try:
                    return super().run_dataframe_operation(dataframe_name, operation, operation_parameters)
                except Exception as e:
                    return f"Error running operation '{operation}': {str(e)}"

        st.session_state.pandas_tools_instance = CustomPandasTools()
    if "ai_summary" not in st.session_state:
        st.session_state.ai_summary = None


def main():
    st.set_page_config(page_title="Data Analyzer Bot", page_icon="🤖", layout="wide")

    # --- Sidebar ---
    with st.sidebar:
        st.header("⚙️ Configuration")

        with st.expander("API Keys", expanded=False):
            st.session_state.api_keys["openai"] = st.text_input(
                "OpenAI API Key",
                type="password",
                value=st.session_state.api_keys.get("openai", ""),
                help="Get your key from https://platform.openai.com/api-keys",
            )
            st.session_state.api_keys["anthropic"] = st.text_input(
                "Anthropic API Key",
                type="password",
                value=st.session_state.api_keys.get("anthropic", ""),
                help="Get your key from https://console.anthropic.com/settings/keys",
            )
            st.info("API keys are stored temporarily and will be lost on page refresh.")

        llm_provider_options = ("OpenAI", "Anthropic Claude", "None")
        st.session_state.selected_llm_provider = st.selectbox(
            "Select LLM Provider",
            llm_provider_options,
            index=llm_provider_options.index(st.session_state.selected_llm_provider),
        )

        # Display status based on selection and key presence
        if st.session_state.selected_llm_provider == "None":
            st.info("No LLM provider selected. Querying will be disabled.")
        elif st.session_state.selected_llm_provider == "OpenAI":
            if not st.session_state.api_keys.get("openai"):
                st.warning("OpenAI selected, but API key is missing.")
            else:
                st.success("OpenAI selected and ready.")
        elif st.session_state.selected_llm_provider == "Anthropic Claude":
            if not st.session_state.api_keys.get("anthropic"):
                st.warning("Anthropic Claude selected, but API key is missing.")
            else:
                st.success("Anthropic Claude selected and ready.")

    # --- Main App ---
    st.title("🤖 Data Analyzer Bot")
    st.markdown("**Welcome!** Upload your CSV or Excel file, and I'll help you analyze and explore your data.")

    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        temp_path, columns, df = preprocess_and_save(uploaded_file)
        if temp_path and columns and df is not None:
            st.session_state.df = df

            # --- Tabs for different functionalities ---
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["💬 Interactive Query", "📊 Automated Analysis", "📈 Visualizations", "🤖 AI Summary", "📄 Report"]
            )

            with tab1:
                st.header("Interactive Query with LLM")

                can_proceed_with_llm = False
                active_api_key = None
                if st.session_state.selected_llm_provider == "OpenAI" and st.session_state.api_keys.get("openai"):
                    can_proceed_with_llm = True
                    active_api_key = st.session_state.api_keys["openai"]
                elif st.session_state.selected_llm_provider == "Anthropic Claude" and st.session_state.api_keys.get(
                    "anthropic"
                ):
                    can_proceed_with_llm = True
                    active_api_key = st.session_state.api_keys["anthropic"]

                if can_proceed_with_llm:
                    if st.session_state.selected_llm_provider == "OpenAI":
                        st.session_state.pandas_tools_instance.dataframes = {"df": df}
                        data_analyst_assistant = Assistant(
                            llm=OpenAIChat(model="gpt-4-turbo", api_key=active_api_key),
                            tools=[st.session_state.pandas_tools_instance],
                            show_tool_calls=True,
                            markdown=True,
                            description="You are a world-class data analyst.",
                            instructions=[
                                "The user has provided a pandas DataFrame `df`. Analyze it to answer the user's query."
                            ],
                        )
                    else:  # Anthropic Claude
                        df_columns = df.columns.tolist()
                        df_shape = f"({df.shape[0]} rows, {df.shape[1]} columns)"
                        data_analyst_assistant = Assistant(
                            llm=Claude(model="claude-3-opus-20240229", api_key=active_api_key),
                            tools=[],
                            show_tool_calls=False,
                            markdown=True,
                            description="You are a world-class data analyst.",
                            instructions=[
                                "The user has uploaded a DataFrame with the following properties:",
                                f"Name: 'df', Shape: {df_shape}, Columns: {df_columns}",
                                "Answer the user's questions about this data without using tools.",
                            ],
                        )

                    user_query = st.text_area("Ask a query about the data:")
                    if st.button("Submit Query"):
                        if user_query:
                            with st.spinner("Processing query..."):
                                response = ""
                                for part in data_analyst_assistant.run(user_query):
                                    response += str(part)
                                st.markdown(response)
                        else:
                            st.warning("Please enter a query.")
                else:
                    st.warning(
                        f"Please provide an API key for {st.session_state.selected_llm_provider} to use the interactive query feature."
                    )

            with tab2:
                st.header("Automated Analysis (EDA)")
                st.write("Here is a basic overview of your dataset:")
                st.write("**Data Preview:**")
                st.dataframe(df.head())
                st.write("**Dataset Dimensions:**")
                st.write(f"{df.shape[0]} rows and {df.shape[1]} columns")
                st.write("**Column Data Types:**")
                st.dataframe(df.dtypes.astype(str).rename("Data Type"))

                # --- Missing Value Analysis ---
                st.write("**Missing Value Analysis:**")
                missing_values = df.isnull().sum()
                missing_percentage = (missing_values / len(df)) * 100
                missing_df = pd.DataFrame(
                    {"Missing Count": missing_values, "Missing Percentage": missing_percentage.map("{:.2f}%".format)}
                )
                # Only show columns with missing values to keep it clean
                missing_df_filtered = missing_df[missing_df["Missing Count"] > 0]
                if not missing_df_filtered.empty:
                    st.dataframe(missing_df_filtered.sort_values(by="Missing Count", ascending=False))
                else:
                    st.success("🎉 No missing values found in the dataset.")

                # --- Descriptive Statistics for Numerical Columns ---
                st.write("**Descriptive Statistics for Numerical Columns:**")
                numerical_cols = df.select_dtypes(include=np.number).columns
                if len(numerical_cols) > 0:
                    st.dataframe(df[numerical_cols].describe())
                else:
                    st.info("No numerical columns found to generate statistics.")

                # --- Categorical Column Statistics ---
                st.write("**Categorical Column Statistics:**")
                categorical_cols = df.select_dtypes(include=["object", "category"]).columns
                if len(categorical_cols) > 0:
                    for col in categorical_cols:
                        with st.expander(f"Stats for {col}"):
                            st.write(f"**Unique Values:** {df[col].nunique()}")
                            st.write("**Most Frequent Values:**")
                            st.dataframe(df[col].value_counts().head(10).rename("Frequency"))
                else:
                    st.info("No categorical columns found to generate statistics.")

            with tab3:
                st.header("Automated Visualizations")

                # --- Histograms for Numerical Columns ---
                st.write("**Histograms for Numerical Columns:**")
                numerical_cols = df.select_dtypes(include=np.number).columns
                if len(numerical_cols) > 0:
                    for col in numerical_cols:
                        with st.expander(f"Histogram for {col}"):
                            fig, ax = plt.subplots()
                            sns.histplot(df[col], kde=True, ax=ax)
                            ax.set_title(f"Distribution of {col}")
                            st.pyplot(fig)
                            plt.close(fig)  # Prevent plots from overlapping
                else:
                    st.info("No numerical columns to visualize.")

                # --- Bar Charts for Categorical Columns ---
                st.write("**Bar Charts for Categorical Columns:**")
                categorical_cols = df.select_dtypes(include=["object", "category"]).columns
                if len(categorical_cols) > 0:
                    for col in categorical_cols:
                        # Avoid plotting for high-cardinality columns to prevent clutter
                        if df[col].nunique() > 50:
                            st.info(f"Skipping bar chart for '{col}' due to high cardinality (>50 unique values).")
                            continue

                        with st.expander(f"Bar Chart for {col}"):
                            fig, ax = plt.subplots()
                            sns.countplot(y=col, data=df, order=df[col].value_counts().index[:20], ax=ax)
                            ax.set_title(f"Frequency of Top 20 in {col}")
                            ax.set_xlabel("Count")
                            ax.set_ylabel(col)
                            st.pyplot(fig)
                            plt.close(fig)
                else:
                    st.info("No categorical columns to visualize.")

                # --- Correlation Heatmap ---
                st.write("**Correlation Heatmap for Numerical Columns:**")
                numerical_cols = df.select_dtypes(include=np.number).columns
                if len(numerical_cols) > 1:
                    with st.expander("View Correlation Heatmap"):
                        corr_matrix = df[numerical_cols].corr()
                        fig, ax = plt.subplots(figsize=(10, 8))
                        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
                        ax.set_title("Correlation Heatmap")
                        st.pyplot(fig)
                        plt.close(fig)
                else:
                    st.info("Not enough numerical columns to generate a correlation heatmap.")

            with tab4:
                st.header("🤖 AI-Powered Summary")
                st.info(
                    "Click the button below to generate a natural language summary of the dataset's key characteristics and insights using the selected LLM provider."
                )

                if st.button("Generate AI Summary"):
                    can_proceed_with_llm = False
                    active_api_key = None
                    if st.session_state.selected_llm_provider == "OpenAI" and st.session_state.api_keys.get("openai"):
                        can_proceed_with_llm = True
                        active_api_key = st.session_state.api_keys["openai"]
                    elif st.session_state.selected_llm_provider == "Anthropic Claude" and st.session_state.api_keys.get(
                        "anthropic"
                    ):
                        can_proceed_with_llm = True
                        active_api_key = st.session_state.api_keys["anthropic"]

                    if can_proceed_with_llm:
                        with st.spinner("Generating summary, this may take a moment..."):
                            # 1. Gather all EDA information
                            df_shape = f"{df.shape[0]} rows and {df.shape[1]} columns"
                            df_dtypes = df.dtypes.astype(str).to_dict()
                            missing_values = df.isnull().sum()
                            missing_percentage = (missing_values / len(df)) * 100
                            missing_df = pd.DataFrame(
                                {"Missing Count": missing_values, "Missing Percentage": missing_percentage}
                            )
                            missing_info = missing_df[missing_df["Missing Count"] > 0].to_string()

                            numerical_cols = df.select_dtypes(include=np.number)
                            descriptive_stats = (
                                numerical_cols.describe().to_string()
                                if not numerical_cols.empty
                                else "No numerical columns."
                            )

                            categorical_cols = df.select_dtypes(include=["object", "category"])
                            categorical_info = ""
                            if not categorical_cols.empty:
                                for col in categorical_cols.columns:
                                    categorical_info += f"\n- Column '{col}':\n"
                                    categorical_info += f"  - Unique Values: {df[col].nunique()}\n"
                                    categorical_info += (
                                        f"  - Top 5 Values:\n{df[col].value_counts().head(5).to_string()}\n"
                                    )
                            else:
                                categorical_info = "No categorical columns."

                            # 2. Construct the prompt
                            prompt = f"""
                            You are an expert data analyst. I have a dataset with the following characteristics. Please provide a high-level summary and identify 2-3 key insights, patterns, or anomalies.

                            **1. Dataset Overview:**
                            - Shape: {df_shape}
                            - Column Data Types: {df_dtypes}

                            **2. Missing Values Analysis:**
                            (Only columns with missing data are shown)
                            {missing_info}

                            **3. Descriptive Statistics for Numerical Columns:**
                            {descriptive_stats}

                            **4. Statistics for Categorical Columns:**
                            {categorical_info}

                            Based on this information, please generate a concise summary. Focus on the most important findings that a business user would find valuable. Structure your response in Markdown.
                            """

                            # 3. Initialize and run the LLM
                            if st.session_state.selected_llm_provider == "OpenAI":
                                summary_assistant = Assistant(
                                    llm=OpenAIChat(model="gpt-4o-mini", api_key=active_api_key)
                                )
                            else:  # Anthropic Claude
                                summary_assistant = Assistant(
                                    llm=Claude(model="claude-3-haiku-20240307", api_key=active_api_key)
                                )

                            response = ""
                            for part in summary_assistant.run(prompt):
                                response += str(part)
                            st.session_state.ai_summary = response
                            st.markdown(response)

                    elif st.session_state.selected_llm_provider == "None":
                        st.error("Cannot generate summary. Please select an LLM provider from the sidebar.")
                    else:
                        st.error(
                            f"Cannot generate summary. Please provide an API key for {st.session_state.selected_llm_provider} in the sidebar."
                        )

            with tab5:
                st.header("📄 Generate Report")
                st.info("Select the sections you want to include in the final HTML report.")

                include_analysis = st.checkbox("Automated Analysis", value=True)
                include_visuals = st.checkbox("Visualizations", value=True)

                summary_available = st.session_state.get("ai_summary") is not None
                include_summary = st.checkbox("AI Summary", value=True, disabled=not summary_available)

                if not summary_available and include_summary:
                    st.warning(
                        "Please generate an AI Summary in the 'AI Summary' tab first to include it in the report."
                    )

                st.download_button(
                    label="📥 Generate & Download Report",
                    data=generate_html_report(
                        df, include_analysis, include_visuals, include_summary, st.session_state.get("ai_summary")
                    ),
                    file_name="custom_eda_report.html",
                    mime="text/html",
                )


def generate_html_report(df, include_analysis, include_visuals, include_summary, ai_summary_content):
    """Generates a self-contained HTML report of the EDA."""

    # --- Helper to convert plot to base64 ---
    def plot_to_base64(fig):
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        base64_string = base64.b64encode(buf.getvalue()).decode("utf-8")
        plt.close(fig)
        return base64_string

    # --- Start HTML ---
    html = """<html><head><title>EDA Report</title><style>
        body { font-family: sans-serif; margin: 20px; }
        h1, h2, h3 { color: #333; }
        table { border-collapse: collapse; width: 80%; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .section { margin-bottom: 40px; }
        img { max-width: 100%; height: auto; border: 1px solid #ddd; }
    </style></head><body><h1>Exploratory Data Analysis Report</h1>"""

    # --- Section: Automated Analysis ---
    html += "<div class='section'><h2>Automated Analysis</h2>"
    # Missing Values
    missing_values = df.isnull().sum()
    missing_percentage = (missing_values / len(df)) * 100
    missing_df = pd.DataFrame({"Missing Count": missing_values, "Missing Percentage": missing_percentage})
    html += "<h3>Missing Value Analysis</h3>"
    html += (
        missing_df[missing_df["Missing Count"] > 0].to_html()
        if not missing_df[missing_df["Missing Count"] > 0].empty
        else "<p>No missing values found.</p>"
    )
    # Descriptive Stats
    numerical_cols = df.select_dtypes(include=np.number)
    html += "<h3>Descriptive Statistics (Numerical)</h3>"
    html += numerical_cols.describe().to_html() if not numerical_cols.empty else "<p>No numerical columns.</p>"
    html += "</div>"

    # --- Section: Visualizations ---
    html += "<div class='section'><h2>Visualizations</h2>"
    # Histograms
    html += "<h3>Histograms</h3>"
    if not numerical_cols.empty:
        for col in numerical_cols.columns:
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            ax.set_title(f"Distribution of {col}")
            html += f'<h4>{col}</h4><img src="data:image/png;base64,{plot_to_base64(fig)}">'
    else:
        html += "<p>No numerical columns to visualize.</p>"
    # Bar Charts
    html += "<h3>Bar Charts</h3>"
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    if len(categorical_cols) > 0:
        for col in categorical_cols:
            if df[col].nunique() <= 50:
                fig, ax = plt.subplots()
                sns.countplot(y=col, data=df, order=df[col].value_counts().index[:20], ax=ax)
                ax.set_title(f"Frequency of Top 20 in {col}")
                html += f'<h4>{col}</h4><img src="data:image/png;base64,{plot_to_base64(fig)}">'
    else:
        html += "<p>No categorical columns to visualize.</p>"
    # Heatmap
    html += "<h3>Correlation Heatmap</h3>"
    if len(numerical_cols.columns) > 1:
        corr_matrix = df[numerical_cols.columns].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap")
        html += f'<img src="data:image/png;base64,{plot_to_base64(fig)}">'
    else:
        html += "<p>Not enough numerical columns for a heatmap.</p>"
    html += "</div>"

    # --- End HTML ---
    # --- Section: AI Summary ---
    if include_summary and ai_summary_content:
        html += "<div class='section'><h2>AI Summary</h2>"
        html += markdown.markdown(ai_summary_content)
        html += "</div>"

    # --- End HTML ---
    html += "</body></html>"
    return html


if __name__ == "__main__":
    initialize_session_state()
    main()
