import streamlit as st
import pandas as pd
import altair as alt

# ==============================================================================
# EXPRESSX FINGUIDE - COMPLETE ARTIFACT GENERATION (VERSION 2)
# ==============================================================================
st.set_page_config(page_title="ExpressX FinGuide v2", page_icon="📊", layout="centered")

# Custom App-wide styling matching your clean minimalist aesthetic
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: 600; padding: 10px; }
    .metric-card { background: white; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("👋 Welcome to ExpressX FinGuide")
st.caption("Sequential Budget Pipeline Engine • Version 2 (Backup Protected)")
st.markdown("---")

# Initialize persistent session tracking states to mimic your routes sequence
if "step" not in st.session_state:
    st.session_state.step = 1
if "savings_goal" not in st.session_state:
    st.session_state.savings_goal = 0.0
if "income" not in st.session_state:
    st.session_state.income = 0.0
if "income_source" not in st.session_state:
    st.session_state.income_source = ""
if "expenses" not in st.session_state:
    st.session_state.expenses = {}

# ==============================================================================
# ROUTE STEP 1: SET SAVINGS GOAL FIRST
# ==============================================================================
if st.session_state.step == 1:
    st.header("🎯 Step 1: Set Desired Savings Target")
    st.info("💡 FinGuide Rule: Specify your target savings allocation first. Income validation happens next.")
    
    goal_input = st.number_input("Desired Savings Target Amount (₹)", min_value=0.0, step=500.0, value=st.session_state.savings_goal or 5000.0)
    
    if st.button("Confirm Target & Proceed to Income →"):
        st.session_state.savings_goal = round(goal_input, 2)
        st.session_state.step = 2
        st.rerun()

# ==============================================================================
# ROUTE STEP 2: MONTHLY INCOME & 5% VALIDATION
# ==============================================================================
elif st.session_state.step == 2:
    st.header("💰 Step 2: Monthly Income Verification")
    st.metric(label="🎯 Cached Savings Target", value=f"₹{st.session_state.savings_goal:,.2f}")
    
    source_input = st.text_input("Income Source Reference", value=st.session_state.income_source or "Salary")
    amount_input = st.number_input("Monthly Revenue/Payload Amount (₹)", min_value=0.0, step=1000.0, value=st.session_state.income or 50000.0)
    
    # Live Evaluator Mechanics
    min_saving_required = round(amount_input * 0.05, 2)
    is_valid = True
    
    if amount_input > 0 and st.session_state.savings_goal < min_saving_required:
        st.warning(f"⚠️ Your pre-set savings goal (₹{st.session_state.savings_goal:.2f}) must be at least 5% of your income. Minimum target required for this income: ₹{min_saving_required:.2f}")
        is_valid = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Target"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Proceed to Expenses →", disabled=not is_valid or amount_input <= 0):
            st.session_state.income = round(amount_input, 2)
            st.session_state.income_source = source_input
            st.session_state.step = 3
            st.rerun()

# ==============================================================================
# ROUTE STEP 3: ITEMIZED EXPENSE INPUTS
# ==============================================================================
elif st.session_state.step == 3:
    st.header("💸 Step 3: Itemized Monthly Expenses")
    
    st.markdown("### Log Parameters Across Spending Tracks")
    food = st.number_input("🍏 Food Spending (₹)", min_value=0.0, step=100.0, value=st.session_state.expenses.get("Food", 0.0))
    travel = st.number_input("🚗 Travel Allowance (₹)", min_value=0.0, step=100.0, value=st.session_state.expenses.get("Travel", 0.0))
    fees = st.number_input("🏫 Education & Fees (₹)", min_value=0.0, step=100.0, value=st.session_state.expenses.get("Fees", 0.0))
    essentials = st.number_input("🛒 Daily Essentials (₹)", min_value=0.0, step=100.0, value=st.session_state.expenses.get("Daily Essentials", 0.0))
    medical = st.number_input("🏥 Medical Care (₹)", min_value=0.0, step=100.0, value=st.session_state.expenses.get("Medical", 0.0))
    entertainment = st.number_input("🎬 Entertainment (₹)", min_value=0.0, step=100.0, value=st.session_state.expenses.get("Entertainment", 0.0))
    others = st.number_input("📦 Other Logistics (₹)", min_value=0.0, step=100.0, value=st.session_state.expenses.get("Others", 0.0))
    
    # Check Realistic Savings Target Constraints
    necessary_spending = food + travel + fees + essentials + medical
    total_spending = necessary_spending + entertainment + others
    remaining_balance = st.session_state.income - st.session_state.savings_goal - total_spending
    
    if remaining_balance < 0:
        recommended_max = max(round(st.session_state.income * 0.05, 2), round(st.session_state.income - necessary_spending, 2))
        st.error(f"⚠️ Unrealistic Budget Target! Your necessary items (₹{necessary_spending:.2f}) and total spending leave a deficit. Recommended max target range: ₹{st.session_state.income * 0.05:.2f} - ₹{recommended_max:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Income"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Save Parameters & View Dashboard →"):
            st.session_state.expenses = {
                "Food": food, "Travel": travel, "Fees": fees, 
                "Daily Essentials": essentials, "Medical": medical, 
                "Entertainment": entertainment, "Others": others
            }
            st.session_state.step = 4
            st.rerun()

# ==============================================================================
# ROUTE STEP 4: INTERACTIVE FINANCIAL ANALYSIS DASHBOARD
# ==============================================================================
elif st.session_state.step == 4:
    st.header("📊 Step 4: Interactive Financial Analysis")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='metric-card'><p style='color:#64748b;margin:0;'>Logged Income</p><h2 style='margin:5px 0;'>₹{st.session_state.income:,.2f}</h2><small>{st.session_state.income_source}</small></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><p style='color:#64748b;margin:0;'>Savings Target</p><h2 style='margin:5px 0;color:#16a34a;'>₹{st.session_state.savings_goal:,.2f}</h2><small>Verified (≥5%)</small></div>", unsafe_allow_html=True)
    with m3:
        total_exp = sum(st.session_state.expenses.values())
        st.markdown(f"<div class='metric-card'><p style='color:#64748b;margin:0;'>Total Expenses</p><h2 style='margin:5px 0;color:#dc2626;'>₹{total_exp:,.2f}</h2><small>{len([v for v in st.session_state.expenses.values() if v > 0])} Active Tracks</small></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    active_expenses = {k: v for k, v in st.session_state.expenses.items() if v > 0}
    if active_expenses:
        st.subheader("🥧 Allocation Split Charts")
        df_exp = pd.DataFrame(list(active_expenses.items()), columns=["Category", "Amount"])
        
        chart = alt.Chart(df_exp).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6).encode(
            x=alt.X('Amount:Q', title="Amount (₹)"),
            y=alt.Y('Category:N', sort='-x', title="Spending Track"),
            color=alt.value('#1e293b')
        ).properties(height=300)
        
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("💡 No specific values were recorded under itemized spending tracks.")
        
    if st.button("🔄 Clear System & Reset Workflow Loop"):
        st.session_state.step = 1
        st.session_state.savings_goal = 0.0
        st.session_state.income = 0.0
        st.session_state.expenses = {}
        st.rerun()

