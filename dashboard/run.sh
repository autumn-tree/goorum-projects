#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "Streamlit is not installed. Installing dependencies..."
    pip install xlrd openpyxl streamlit plotly pandas statsmodels
fi

# Run the streamlit app
echo "Starting Global Superstore Dashboard..."
streamlit run app.py
