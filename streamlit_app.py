import streamlit as st
import sqlite3
import pandas as pd

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Express X - FinGuide",
    page_icon="💰",
    layout="wide"
)

# ---------------- DATABASE ----------------

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    amount REAL,
    goal REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    amount REAL
)
""")

conn.commit()


# ---------------- SESSION ----------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""


# ---------------- HOME ----------------

if st.session_state.page == "home":

    st.title("💰 Express X")
    st.subheader("FinGuide - Your Personal Financial Advisor")

    st.write(
        "Track your income, expenses, savings and financial goals "
        "in one simple place."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Create Account", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()

    with col2:
        if st.button("Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()


# ---------------- SIGNUP ----------------

elif st.session_state.page == "signup":

    st.title("Create Your Express X Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account", use_container_width=True):

        if not email or not password:
            st.error("Email and password are required.")

        else:

            email = email.strip().lower()

            try:
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, password)
                )

                conn.commit()

                st.success("Account created successfully!")

                st.session_state.page = "login"
                st.rerun()

            except sqlite3.IntegrityError:
                st.error("Email already registered.")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ---------------- LOGIN ----------------

elif st.session_state.page == "login":

    st.title("Login to Express X")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        email = email.strip().lower()

        cursor.execute(
            "SELECT name FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        if user:

            st.session_state.logged_in = True
            st.session_state.user_name = user[0]
            st.session_state.page = "dashboard"

            st.rerun()

        else:
            st.error("Invalid Login")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ---------------- DASHBOARD ----------------

elif st.session_state.page == "dashboard":

    st.title("Express X - FinGuide")

    st.write(
        f"Welcome, **{st.session_state.user_name or 'User'}**!"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Add Monthly Income", use_container_width=True):
            st.session_state.page = "income"
            st.rerun()

    with col2:
        if st.button("Add Monthly Expenses", use_container_width=True):
            st.session_state.page = "expense"
            st.rerun()

    with col3:
        if st.button("Financial Analysis", use_container_width=True):
            st.session_state.page = "analysis"
            st.rerun()

    st.divider()

    st.subheader("Your Financial Overview")

    cursor.execute("SELECT amount, goal FROM income")
    income_data = cursor.fetchall()

    cursor.execute("SELECT amount FROM expenses")
    expense_data = cursor.fetchall()

    total_income = sum(row[0] for row in income_data)
    total_expense = sum(row[0] for row in expense_data)

    balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Income", f"₹{total_income:,.2f}")

    with col2:
        st.metric("Total Expenses", f"₹{total_expense:,.2f}")

    with col3:
        st.metric("Balance", f"₹{balance:,.2f}")

    st.divider()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.page = "home"
        st.rerun()


# ---------------- INCOME ----------------

elif st.session_state.page == "income":

    st.title("Add Monthly Income")

    source = st.selectbox(
        "Income Source",
        [
            "Salary",
            "Business",
            "Freelancing",
            "Investments",
            "Interest",
            "Scholarship",
            "Pocket Money",
            "Gift",
            "Rental Income",
            "Bonus",
            "Other"
        ]
    )

    amount = st.number_input(
        "Monthly Income",
        min_value=0.0,
        step=100.0
    )

    goal = st.number_input(
        "Monthly Savings Goal",
        min_value=0.0,
        step=100.0
    )

    if st.button("Save Income", use_container_width=True):

        cursor.execute("DELETE FROM income")

        cursor.execute(
            "INSERT INTO income (source, amount, goal) VALUES (?, ?, ?)",
            (source, amount, goal)
        )

        conn.commit()

        st.success("Income saved successfully!")

        st.session_state.page = "expense"
        st.rerun()

    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


# ---------------- EXPENSE ----------------

elif st.session_state.page == "expense":

    st.title("Add Monthly Expenses")

    categories = [
        "Food",
        "Clothing",
        "Travel",
        "Fees",
        "Daily Essentials",
        "Medical",
        "Entertainment",
        "Shopping",
        "Others"
    ]

    values = {}

    for category in categories:

        values[category] = st.number_input(
            category,
            min_value=0.0,
            step=50.0,
            key=category
        )

    if st.button("Save Expenses", use_container_width=True):

        cursor.execute("DELETE FROM expenses")

        for category, amount in values.items():

            if amount > 0:

                cursor.execute(
                    "INSERT INTO expenses (category, amount) VALUES (?, ?)",
                    (category, amount)
                )

        conn.commit()

        st.success("Expenses saved successfully!")

        st.session_state.page = "analysis"
        st.rerun()

    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


# ---------------- ANALYSIS ----------------

elif st.session_state.page == "analysis":

    st.title("Financial Analysis")

    cursor.execute("SELECT amount, goal FROM income")
    incomes = cursor.fetchall()

    cursor.execute(
        "SELECT category, amount FROM expenses"
    )

    expenses = cursor.fetchall()

    total_income = sum(row[0] for row in incomes)
    total_expense = sum(row[1] for row in expenses)

    balance = total_income - total_expense

    goal = incomes[0][1] if incomes else 0

    if total_income > 0:
        savings_percentage = (
            balance / total_income
        ) * 100
    else:
        savings_percentage = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Income",
            f"₹{total_income:,.2f}"
        )

    with col2:
        st.metric(
            "Total Expenses",
            f"₹{total_expense:,.2f}"
        )

    with col3:
        st.metric(
            "Balance",
            f"₹{balance:,.2f}"
        )

    st.divider()

    st.subheader("Savings")

    st.metric(
        "Savings Percentage",
        f"{savings_percentage:.2f}%"
    )

    if balance >= goal:

        st.success(
            "Congratulations! You achieved your monthly savings goal."
        )

    else:

        st.info(
            f"You need ₹{goal - balance:,.2f} more "
            "to reach your savings goal."
        )

    st.subheader("Expense Breakdown")

    if expenses:

        df = pd.DataFrame(
            expenses,
            columns=["Category", "Amount"]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        highest = max(
            expenses,
            key=lambda x: x[1]
        )

        st.write(
            f"**Highest Expense:** {highest[0]} "
            f"— ₹{highest[1]:,.2f}"
        )

        st.subheader("Expense Chart")

        chart_df = df.set_index("Category")

        st.bar_chart(chart_df["Amount"])

    else:
        st.info("No expenses added yet.")

    st.subheader("Smart Suggestion")

    if savings_percentage >= 50:

        suggestion = (
            "Excellent! You are saving a large portion "
            "of your income."
        )

    elif savings_percentage >= 30:

        suggestion = (
            "Good! Your finances are under control."
        )

    elif savings_percentage >= 10:

        suggestion = (
            "Try reducing unnecessary expenses "
            "to save more."
        )

    else:

        suggestion = (
            "Your expenses are very high. "
            "Consider reviewing your spending."
        )

    st.info(suggestion)

    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()