import streamlit as st
import pandas as pd
import altair as alt

# ==============================================================================
# EXPRESSX FINGUIDE - PREMIUM STREAMLIT PIPELINE WITH AUTH (VERSION 2)
# ==============================================================================
st.set_page_config(page_title="ExpressX FinGuide v2", page_icon="📊", layout="centered")

# Custom App-wide styling matching your clean minimalist aesthetic
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: 600; padding: 10px; }
    .auth-card { background: white; padding: 35px 30px; border-radius: 20px; border: 1px solid #e2e8f0; box-shadow: 0 10px 30px rgba(0,0,0,0.02); text-align: center; }
    .metric-card { background: white; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Initialize global navigation state loops
if "page" not in st.session_state:
    st.session_state.page = "welcome"  # Starts fresh at your landing card!
if "savings_goal" not in st.session_state:
    st.session_state.savings_goal = 0.0
if "income" not in st.session_state:
    st.session_state.income = 0.0
if "income_source" not in st.session_state:
    st.session_state.income_source = ""
if "expenses" not in st.session_state:
    st.session_state.expenses = {}
if "user_name" not in st.session_state:
    st.session_state.user_name = "User"

# ==============================================================================
# PAGE 1: WELCOME SCREEN & CORE BRANDING
# ==============================================================================
if st.session_state.page == "welcome":
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.subheader("SMART FINANCIAL MANAGEMENT")
    st.title("Express X FinGuide")
    st.write("Your Personal Guide to Smarter Money Decisions")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Create Account"):
            st.session_state.page = "signup"
            st.rerun()
    with col2:
        if st.button("🔐 Login Here"):
            st.session_state.page = "login"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# PAGE 2: SIGN UP CARD
# ==============================================================================
elif st.session_state.page == "signup":
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.title("📝 Create Account")
    st.caption("Start your journey towards smarter money management")
    
    su_name = st.text_input("👤 Full Name", value="")
    su_email = st.text_input("📧 Email Address", key="su_email")
    su_pass = st.text_input("🔒 Password", type="password", key="su_pass")
    
    if st.button("Create Account & Login"):
        if su_email and su_pass:
            st.session_state.user_name = su_name if su_name else "User"
            st.session_state.page = "dashboard"
            st.rerun()
    
    if st.button("← Back to Welcome"):
        st.session_state.page = "welcome"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# PAGE 3: LOGIN CARD
# ==============================================================================
elif st.session_state.page == "login":
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.title("🔐 Welcome Back!")
    st.caption("Login to continue managing your finances")
    
    lin_email = st.text_input("📧 Email Address", key="lin_email")
    lin_pass = st.text_input("🔒 Password", type="password", key="lin_pass")
    
    if st.button("Login to FinGuide →"):
        if lin_email and lin_pass:
            st.session_state.page = "dashboard"
            st.rerun()
            
    if st.button("← Back to Welcome"):
        st.session_state.page = "welcome"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# PAGE 4: INTERACTIVE MENU DASHBOARD PANEL
# ==============================================================================
elif st.session_state.page == "dashboard":
    st.title(f"👋 Welcome {st.session_state.user_name}")
    st.caption("ExpressX FinGuide • Main Management Hub")
    st.markdown("---")
    
    st.write("### Choose an Option")
    
    if st.button("🎯 Set Savings Target & Start Pipeline"):
        st.session_state.page = "step_savings"
        st.rerun()
        
    if st.button("💰 Log Income"):
        st.session_state.page = "step_income"
        st.rerun()
        
    if st.button("💸 Log Expenses"):
        st.session_state.page = "step_expenses"
        st.rerun()
        
    if st.button("📊 View Analysis Graphs"):
        st.session_state.page = "step_analysis"
        st.rerun()
        
    st.markdown("---")
    if st.button("🚪 Logout", key="logout_dashboard"):
        st.session_state.page = "welcome"
        st.rerun()

# ==============================================================================
# WORKFLOW STEP: SAVINGS TARGET
# ==============================================================================
elif st.session_state.page == "step_savings":
    st.header("🎯 Step 1: Set Desired Savings Target")
    goal_input = st.number_input("Desired Savings Target Amount (₹)", min_value=0.0, step=500.0, value=st.session_state.savings_goal or 5000.0)
    
    if st.button("Confirm Target & Proceed to Income →"):
        st.session_state.savings_goal = round(goal_input, 2)
        st.session_state.page = "step_income"
        st.rerun()
        
    if st.button("← Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

# ==============================================================================
# WORKFLOW STEP: INCOME & 5% SAFETY CHECK
# ==============================================================================
elif st.session_state.page == "step_income":
    st.header("💰 Step 2: Monthly Income Verification")
    st.metric(label="🎯 Cached Savings Target", value=f"₹{st.session_state.savings_goal:,.2f}")
    
    source_input = st.text_input("Income Source Reference", value=st.session_state.income_source or "Salary")
    amount_input = st.number_input("Monthly Revenue Amount (₹)", min_value=0.0, step=1000.0, value=st.session_state.income or 50000.0)
    
    min_saving_required = round(amount_input * 0.05, 2)
    is_valid = True
    
    if amount_input > 0 and st.session_state.savings_goal < min_saving_required:
        st.warning(f"⚠️ Savings goal must be at least 5% of income. Minimum target required: ₹{min_saving_required:.2f}")
        is_valid = False

    if st.button("Proceed to Expenses →", disabled=not is_valid or amount_input <= 0):
        st.session_state.income = round(amount_input, 2)
        st.session_state.income_source = source_input
        st.session_state.page = "step_expenses"
        st.rerun()
        
    if st.button("← Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

# ==============================================================================
# WORKFLOW STEP: EXPENSES LOG
# ==============================================================================
elif st.session_state.page == "step_expenses":
    st.header("💸 Step 3: Itemized Monthly Expenses")
    
    food = st.number_input("🍏 Food Spending (₹)", min_value=0.0, value=st.session_state.expenses.get("Food", 0.0))
    travel = st.number_input("🚗 Travel Allowance (₹)", min_value=0.0, value=st.session_state.expenses.get("Travel", 0.0))
    fees = st.number_input("🏫 Education & Fees (₹)", min_value=0.0, value=st.session_state.expenses.get("Fees", 0.0))
    essentials = st.number_input("🛒 Daily Essentials (₹)", min_value=0.0, value=st.session_state.expenses.get("Daily Essentials", 0.0))
    medical = st.number_input("🏥 Medical Care (₹)", min_value=0.0, value=st.session_state.expenses.get("Medical", 0.0))
    entertainment = st.number_input("🎬 Entertainment (₹)", min_value=0.0, value=st.session_state.expenses.get("Entertainment", 0.0))
    others = st.number_input("📦 Other Logistics (₹)", min_value=0.0, value=st.session_state.expenses.get("Others", 0.0))
    
    if st.button("Save Parameters & View Analysis Charts →"):
        st.session_state.expenses = {
            "Food": food, "Travel": travel, "Fees": fees, 
            "Daily Essentials": essentials, "Medical": medical, 
            "Entertainment": entertainment, "Others": others
        }
        st.session_state.page = "step_analysis"
        st.rerun()

# ==============================================================================
# WORKFLOW STEP: FINAL INTERACTIVE VISUAL ANALYSIS
# ==============================================================================
elif st.session_state.page == "step_analysis":
    st.header("📊 Step 4: Interactive Financial Analysis")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='metric-card'><p style='color:#64748b;margin:0;'>Income</p><h2>₹{st.session_state.income:,.2f}</h2></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><p style='color:#64748b;margin:0;'>Savings Goal</p><h2 style='color:#16a34a;'>₹{st.session_state.savings_goal:,.2f}</h2></div>", unsafe_allow_html=True)
    with m3:
        total_exp = sum(st.session_state.expenses.values())
        st.markdown(f"<div class='metric-card'><p style='color:#64748b;margin:0;'>Expenses</p><h2 style='color:#dc2626;'>₹{total_exp:,.2f}</h2></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    active_expenses = {k: v for k, v in st.session_state.expenses.items() if v > 0}
    if active_expenses:
