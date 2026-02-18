# Project Plan: Streamlit Toy Project (Personal Finance Tracker)

## 1. Environment Setup
-   **Cloud**: Configure Gitpod environment using `.gitpod.yml`.
    -   Base Image: Python 3.9+
    -   Dependencies: `streamlit`, `pandas`
    -   Auto-start: `streamlit run app.py`
-   **Local/Colab**: Implement environment detection to show a welcome message only in local/Colab environments.

## 2. Basic Streamlit Elements
-   Implement the following widgets:
    -   `st.button`: For actions.
    -   `st.slider`: For numerical input.
    -   `st.text_input`: For text data.
    -   `st.checkbox`: For boolean toggles.

## 3. Toy Project: Simple Expense Tracker
-   **Goal**: A simple app to track personal expenses.
-   **Layout**:
    -   Use `st.sidebar` for navigation or global settings.
    -   Use `st.columns` to arrange form inputs.
    -   Use `st.container` to group related elements.
-   **Form**:
    -   `st.form`: Encapsulate inputs (Item Name, Category, Price) to prevent auto-reload on every keystroke.
    -   `st.form_submit_button`: To add the entry to the list.
-   **Data**: Display added expenses in a DataFrame/Table.

## 4. Components & Execution Results
-   **Metrics**: Use `st.metric` to display Total Expenses.
-   **Expander**: Use `st.expander` to hide/show raw data or help text.
-   **Feedback**: Use `st.balloons` or `st.success` upon successful form submission.
-   **Visualization**: Simple Bar Chart of expenses by category.

## 5. Execution
-   Run the application using `streamlit run app.py`.
-   Verify all features in the Gitpod preview or local browser.
