# Use a more recent, stable Python version
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the working directory
COPY app/ .

# Expose the port Streamlit will run on
EXPOSE 8501

# Set the headless environment variable for Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true

# Run the Streamlit app when the container launches
CMD ["streamlit", "run", "ai_data_analyst.py", "--server.address=0.0.0.0", "--server.port=8501"]
