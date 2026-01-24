# Global Superstore Dashboard

A modern, interactive retail analytics dashboard built with Python, Streamlit, and Plotly Express.

## Features
- **Logo & Branding**: Professional retail analytics theme.
- **Interactive Filtering**: Filter by Region and Category from the sidebar.
- **Data Visualizations**:
    - **Category Analysis**: Sales distribution across product categories.
    - **Regional Analysis**: Sales vs. Profit scatter plot with trendlines.
- **Top-level Metrics**: Live summaries of Sales, Profit, and Quantity.

## Local Setup

### Prerequisites
Ensure you have Python 3.8+ installed on your system.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/autumn-tree/goorum-projects.git
   cd goorum-projects/dashboard
   ```

2. Install the required dependencies:
   ```bash
   pip install xlrd openpyxl streamlit plotly pandas statsmodels
   ```

## How to Run

### Option 1: Using the Script (Recommended)
Run the convenience script, which also verifies dependencies:
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Using Streamlit Directly
```bash
streamlit run app.py
```

## Tech Stack
- **Dashboard**: Streamlit
- **Visualizations**: Plotly Express
- **Analysis**: Pandas, Statsmodels
- **Excel Support**: xlrd, openpyxl
