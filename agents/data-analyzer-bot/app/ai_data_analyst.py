import csv
import tempfile

import pandas as pd
import streamlit as st
from phi.assistant import Assistant
from phi.llm.anthropic.claude import Claude
from phi.llm.openai import OpenAIChat
from phi.tools.pandas import PandasTools


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


# Streamlit app
st.title("🤖 Data Analyzer Bot")

# Initialize PandasTools in session state if it doesn't exist
if "pandas_tools_instance" not in st.session_state:
    # Create a custom wrapper for PandasTools to handle DataFrame operations correctly
    class CustomPandasTools(PandasTools):
        def run_dataframe_operation(
            self, dataframe_name, operation, operation_parameters=None
        ):
            # If operation_parameters is None, initialize it as an empty dict
            if operation_parameters is None:
                operation_parameters = {}

            # Get the DataFrame from the dataframes dictionary
            df = self.dataframes.get(dataframe_name)
            if df is None:
                return f"DataFrame '{dataframe_name}' not found."

            # Handle specific operations directly
            if operation == "shape":
                shape = df.shape
                return f"DataFrame shape: {shape[0]} rows × {shape[1]} columns"

            elif operation == "info":
                # Capture the output of df.info() using a string buffer
                import io

                buffer = io.StringIO()
                df.info(buf=buffer)
                return buffer.getvalue()

            elif operation == "columns":
                columns = df.columns.tolist()
                return f"DataFrame columns: {columns}"

            # For other operations, use the parent method
            try:
                return super().run_dataframe_operation(
                    dataframe_name, operation, operation_parameters
                )
            except Exception as e:
                return f"Error running operation '{operation}': {str(e)}"

    st.session_state.pandas_tools_instance = CustomPandasTools()

# Sidebar for User Configuration
with st.sidebar:
    st.header("⚙️ User Configuration")

    st.subheader("API Keys")
    # Initialize session state for API keys if not already present
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = ""
    if "anthropic_api_key" not in st.session_state:
        st.session_state.anthropic_api_key = ""

    openai_key_input = st.text_input(
        "OpenAI API Key:",
        type="password",
        value=st.session_state.openai_api_key,
        key="openai_key_input_widget",
    )
    if openai_key_input != st.session_state.openai_api_key:
        st.session_state.openai_api_key = openai_key_input
        # st.experimental_rerun() # Optional: rerun if immediate feedback on key change is needed

    anthropic_key_input = st.text_input(
        "Anthropic Claude API Key:",
        type="password",
        value=st.session_state.anthropic_api_key,
        key="anthropic_key_input_widget",
    )
    if anthropic_key_input != st.session_state.anthropic_api_key:
        st.session_state.anthropic_api_key = anthropic_key_input
        # st.experimental_rerun()

    st.info(
        "API keys are stored in session state and will be lost on page refresh/tab close."
    )

    st.subheader("LLM Selection")
    # Initialize session state for LLM provider if not already present
    if "selected_llm_provider" not in st.session_state:
        st.session_state.selected_llm_provider = "OpenAI"

    llm_provider_options = ("OpenAI", "Anthropic Claude", "None")
    current_provider_index = (
        llm_provider_options.index(st.session_state.selected_llm_provider)
        if st.session_state.selected_llm_provider in llm_provider_options
        else 0
    )

    llm_provider = st.selectbox(
        "Choose LLM Provider:",
        llm_provider_options,
        index=current_provider_index,
        key="llm_provider_selectbox_widget",
    )
    if llm_provider != st.session_state.selected_llm_provider:
        st.session_state.selected_llm_provider = llm_provider
        # st.experimental_rerun()

    # Feedback messages based on selection
    if st.session_state.selected_llm_provider == "None":
        st.warning("No LLM provider selected. LLM-based features will be disabled.")
    elif st.session_state.selected_llm_provider == "OpenAI":
        if not st.session_state.openai_api_key:
            st.warning("OpenAI selected, but API key is missing.")
        else:
            st.success("OpenAI selected and API key is present.")
    elif st.session_state.selected_llm_provider == "Anthropic Claude":
        if not st.session_state.anthropic_api_key:
            st.warning("Anthropic Claude selected, but API key is missing.")
        else:
            st.success("Anthropic Claude selected and API key is present.")

# Determine if main content can be shown based on LLM config
can_proceed_with_llm = False
active_api_key_for_llm = None

if (
    st.session_state.selected_llm_provider == "OpenAI"
    and st.session_state.openai_api_key
):
    can_proceed_with_llm = True
    active_api_key_for_llm = st.session_state.openai_api_key
elif (
    st.session_state.selected_llm_provider == "Anthropic Claude"
    and st.session_state.anthropic_api_key
):
    can_proceed_with_llm = True
    active_api_key_for_llm = st.session_state.anthropic_api_key
elif st.session_state.selected_llm_provider == "None":
    # Allow proceeding without LLM for data upload and basic viewing
    pass
else:  # Provider selected but key missing
    st.sidebar.error(
        f"{st.session_state.selected_llm_provider} is selected, but the API key is missing. Please configure it."
    )

# File upload widget
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Preprocess and save the uploaded file
    temp_path, columns, df = preprocess_and_save(uploaded_file)

    if temp_path and columns and df is not None:
        # Display the uploaded data as a table
        st.write("Uploaded Data:")
        st.dataframe(df)  # Use st.dataframe for an interactive table

        st.session_state.df = df
        data_analyst_assistant = None  # Initialize to None

        if can_proceed_with_llm:
            if st.session_state.selected_llm_provider == "OpenAI":
                # Populate the dataframes dict of the persistent PandasTools instance
                st.session_state.pandas_tools_instance.dataframes["df"] = (
                    st.session_state.df
                )
                data_analyst_assistant = Assistant(
                    llm=OpenAIChat(model="gpt-4", api_key=active_api_key_for_llm),
                    tools=[st.session_state.pandas_tools_instance],
                    show_tool_calls=False,
                    markdown=True,
                    description="You are a world-class data analyst. You will help the user analyze their data.",
                    instructions=[
                        "First, get a general sense of the data.",
                        "Then, try to answer the user's question.",
                        f"The user has uploaded a file with the columns: {', '.join(st.session_state.df.columns)}.",
                        "The data is available in a pandas DataFrame named 'df'. You have direct access to it.",
                    ],
                )
            elif (
                st.session_state.selected_llm_provider == "Anthropic Claude"
                and st.session_state.anthropic_api_key
            ):
                # Use the Anthropic API key
                active_api_key_for_llm = st.session_state.anthropic_api_key

                # Check if anthropic package is available
                anthropic_available = is_anthropic_available()

                if anthropic_available:
                    # Use the native Claude class from phi-llm, but without tools due to schema compatibility issues
                    # Claude has different JSON schema requirements (draft 2020-12) than what phi-llm's PandasTools provides

                    # Create a DataFrame description for Claude to use
                    df_info = st.session_state.df.describe().to_string()
                    df_columns = ", ".join(st.session_state.df.columns.tolist())
                    df_shape = f"({st.session_state.df.shape[0]} rows, {st.session_state.df.shape[1]} columns)"
                    df_dtypes = st.session_state.df.dtypes.to_string()

                    data_analyst_assistant = Assistant(
                        llm=Claude(
                            model="claude-3-opus-20240229",  # You can adjust the model as needed
                            api_key=active_api_key_for_llm,
                            max_tokens=4096,
                        ),
                        # No tools for Claude due to schema incompatibility
                        tools=[],
                        show_tool_calls=False,
                        markdown=True,
                        description="You are a world-class data analyst using Claude. You will help the user analyze their data.",
                        instructions=[
                            "The user has uploaded a DataFrame with the following properties:",
                            "Name: 'df'",
                            f"Shape: {df_shape}",
                            f"Columns: {df_columns}",
                            f"Data types:\n{df_dtypes}",
                            f"Summary statistics:\n{df_info}",
                            "Answer the user's questions about this data without using tools.",
                            "Be concise and helpful in your responses.",
                        ],
                    )
                else:
                    # If anthropic package is not available, show an error and installation instructions
                    st.error(
                        "The 'anthropic' package is required for Claude integration."
                    )
                    with st.expander("Install the anthropic package"):
                        st.info("To use Claude, install the anthropic package:")
                        st.code("pip install anthropic", language="bash")
                    data_analyst_assistant = None

        # Initialize code storage in session state
        if "generated_code" not in st.session_state:
            st.session_state.generated_code = None

        # Main query input widget
        user_query = st.text_area("Ask a query about the data:")

        # No longer needed as we're hiding tool calls
        # st.info("💡 Check your terminal for a clearer output of the agent's response")

        if st.button("Submit Query"):
            if not user_query.strip():
                st.warning("Please enter a query.")
            elif st.session_state.selected_llm_provider == "None":
                st.info(
                    "No LLM provider selected. Please select a provider in the sidebar."
                )
            elif not data_analyst_assistant:
                st.error(
                    f"LLM assistant could not be initialized. Please check your {st.session_state.selected_llm_provider} API key."
                )
                if st.session_state.selected_llm_provider == "Anthropic Claude":
                    st.info("Make sure the 'anthropic' package is installed:")
                    st.code("pip install anthropic", language="bash")
            else:
                try:
                    # Process the query using the assistant
                    with st.spinner("Processing query..."):
                        # Handle streaming response properly
                        response_parts = []
                        for part in data_analyst_assistant.run(user_query):
                            response_parts.append(str(part))
                        response_content = "".join(response_parts)

                    # Display the response
                    st.markdown(response_content)
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
                    if st.session_state.selected_llm_provider == "Anthropic Claude":
                        st.info(
                            "If you're using Claude and seeing errors, make sure the 'anthropic' package is installed:"
                        )
                        st.code("pip install anthropic", language="bash")
