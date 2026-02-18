import streamlit as st
import pandas as pd
import os

# Security/reliability guardrails for local usage
MAX_BASIC_NAME_LENGTH = 80
MAX_ITEM_NAME_LENGTH = 100
MAX_EXPENSE_ROWS = 1000

# --- Page Config ---
st.set_page_config(page_title="Streamlit Toy Project", layout="wide")

# --- Environment Check & Welcome Message ---
# Simple heuristic: Check for Gitpod-specific environment variables or default to Local/Colab
if "GITPOD_WORKSPACE_ID" not in os.environ:
    st.balloons()
    st.title("👋 Welcome to the Local/Colab Streamlit App!")
    st.info("You are running this application locally or in Colab.")
else:
    st.title("☁️ Running in Gitpod Environment")

st.divider()

# --- Basic Elements Section ---
st.header("1. Basic Streamlit Elements")
st.markdown("Here we demonstrate some fundamental Streamlit widgets.")

col1, col2 = st.columns(2)

with col1:
    # Button
    if st.button("Click me!", key="basic_btn"):
        st.write("Button was clicked!")
    
    # Checkbox
    show_text = st.checkbox("Show hidden text", key="basic_checkbox")
    if show_text:
        st.write("This text is toggled by the checkbox.")

with col2:
    # Slider
    slider_val = st.slider("Select a value", 0, 100, 50, key="basic_slider")
    st.write(f"Current Value: {slider_val}")

    # Text Input
    user_input = st.text_input(
        "Enter your name",
        key="basic_input",
        max_chars=MAX_BASIC_NAME_LENGTH,
    )
    if user_input:
        st.write(f"Hello, {user_input.strip()}!")

st.divider()

# --- Toy Project: Simple Expense Tracker ---
st.header("2. Toy Project: Simple Expense Tracker")
st.markdown("A demonstration of **Layouts, Forms, and Data Display**.")

# Initialize session state for data persistence within the session
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Item", "Category", "Amount"])
elif len(st.session_state.expenses) > MAX_EXPENSE_ROWS:
    st.session_state.expenses = (
        st.session_state.expenses.tail(MAX_EXPENSE_ROWS).reset_index(drop=True)
    )

# Layout: Sidebar for Summary, Main area for Input and List
with st.sidebar:
    st.header("Tracker Summary")
    if not st.session_state.expenses.empty:
        total_expense = st.session_state.expenses["Amount"].sum()
        st.metric(label="Total Spent", value=f"${total_expense:.2f}")
        
        # Simple Chart
        st.subheader("Expenses by Category")
        category_data = st.session_state.expenses.groupby("Category")["Amount"].sum()
        st.bar_chart(category_data)
    else:
        st.info("No expenses added yet.")

# Main Content: Form
with st.container():
    st.subheader("Add New Expense")
    
    with st.form("expense_form", clear_on_submit=True):
        f_col1, f_col2, f_col3 = st.columns(3)
        
        with f_col1:
            item_name = st.text_input("Item Name", max_chars=MAX_ITEM_NAME_LENGTH)
        with f_col2:
            category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Other"])
        with f_col3:
            amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
            
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            clean_item_name = item_name.strip()
            if clean_item_name and len(clean_item_name) <= MAX_ITEM_NAME_LENGTH and amount > 0:
                new_expense = pd.DataFrame(
                    [[clean_item_name, category, amount]],
                    columns=["Item", "Category", "Amount"],
                )
                st.session_state.expenses = pd.concat(
                    [st.session_state.expenses, new_expense], ignore_index=True
                ).tail(MAX_EXPENSE_ROWS).reset_index(drop=True)
                st.success(f"Added **{clean_item_name}** (${amount}) to list!")
                st.balloons()
            else:
                st.error(
                    "Please enter a valid item name (1-100 chars) and amount greater than 0."
                )

# Display Data
st.subheader("Expense List")
with st.expander("View Details", expanded=True):
    if not st.session_state.expenses.empty:
        st.dataframe(st.session_state.expenses, use_container_width=True)
    else:
        st.write("No expenses to display.")
