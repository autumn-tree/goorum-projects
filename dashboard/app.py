import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# Set page config
st.set_page_config(page_title="Global Superstore Dashboard", layout="wide")

# Constants
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, 'data', 'Global Superstore.xls')
LOGO_PATH = os.path.join(BASE_DIR, 'data', 'logo.png')

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel(DATA_PATH)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        st.image(logo, use_container_width=True)
    
    st.title("Global Superstore Analytics")
    st.markdown("---")
    
    # Filters
    st.header("Filters")
    regions = sorted(df['Region'].unique().tolist())
    selected_regions = st.multiselect("Select Regions", options=regions, default=regions)
    
    categories = sorted(df['Category'].unique().tolist())
    selected_categories = st.multiselect("Select Categories", options=categories, default=categories)

# Filter data
filtered_df = df[
    (df['Region'].isin(selected_regions)) & 
    (df['Category'].isin(selected_categories))
]

# Dashboard Main Content
tab1, tab2 = st.tabs(["📦 Category Analysis", "🌍 Regional Analysis"])

with tab1:
    st.header("Sales Distribution by Category")
    if not filtered_df.empty:
        fig_box = px.box(
            filtered_df, 
            x="Category", 
            y="Sales", 
            color="Category",
            title="Sales Distribution per Category",
            template="plotly_dark"
        )
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

with tab2:
    st.header("Sales vs Profit by Region")
    if not filtered_df.empty:
        fig_scatter = px.scatter(
            filtered_df,
            x="Sales",
            y="Profit",
            color="Region",
            hover_data=["Product Name", "Country"],
            title="Sales vs Profit Relationship",
            template="plotly_dark",
            trendline="ols" if filtered_df.shape[0] > 1 else None
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# Metrics
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
with col2:
    st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
with col3:
    st.metric("Total Quantity", f"{filtered_df['Quantity'].sum():,}")
