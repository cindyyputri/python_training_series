import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    
    # Visualize data for the current month
    st.subheader("Expense Visualization")

    # Filter data for the current month
    current_date = pd.Timestamp.now()
    start_of_month = current_date.replace(day=1)
    end_of_month = (start_of_month + pd.DateOffset(months=1)) - pd.DateOffset(days=1)
    
    convert_date_column()
    
    # Filter the DataFrame for the current month
    monthly_expenses = st.session_state.expenses[
        (st.session_state.expenses['Date'].dt.date >= start_of_month.date()) & 
        (st.session_state.expenses['Date'].dt.date <= end_of_month.date())
    ]
    
    if not monthly_expenses.empty:
        # Group by date and sum the amounts
        daily_expenses = monthly_expenses.groupby('Date').agg({'Amount': 'sum'}).reset_index()

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(daily_expenses['Date'], daily_expenses['Amount'], marker='o')
        ax.set_xlabel('Date')
        ax.set_ylabel('Amount')
        ax.set_title('Daily Expenses for the Current Month')
        plt.xticks(rotation=45)

        st.pyplot(fig)
    else:
        st.write("No expenses found for the current month.")
