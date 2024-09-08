import streamlit as st
import pandas as pd

# Initialize the expense data
def initialize_expenses():
    if 'expenses' not in st.session_state:
        st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

# Add an expense entry
def add_expense(date, category, amount, description):
    new_entry = pd.DataFrame([[pd.Timestamp(date), category, amount, description]], columns=['Date', 'Category', 'Amount', 'Description'])
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_entry], ignore_index=True)

# Remove an expense entry
def remove_expense(index):
    st.session_state.expenses = st.session_state.expenses.drop(index).reset_index(drop=True)

# Convert 'Date' column to datetime
def convert_date_column():
    st.session_state.expenses['Date'] = pd.to_datetime(st.session_state.expenses['Date'])

# Initialize expense tracker
initialize_expenses()

# Title of the app
st.title("Simple Expense Tracker")

# Input fields for new expense
date = st.date_input("Date")
categories = ['Food', 'Transportation', 'Entertainment', 'Utilities', 'Other']
category = st.selectbox("Category", categories)
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
description = st.text_input("Description")

# Button to add a new expense
if st.button("Add Expense"):
    add_expense(date, category, amount, description)

# Display the expense tracker
if not st.session_state.expenses.empty:
    st.subheader("Your Expenses")
    st.dataframe(st.session_state.expenses)
    
    # Remove expense
    index_to_remove = st.number_input("Index of expense to remove", min_value=0, max_value=len(st.session_state.expenses)-1, step=1)
    if st.button("Remove Expense"):
        remove_expense(index_to_remove)
        st.success(f"Removed expense at index {index_to_remove}")
