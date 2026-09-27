import streamlit as st
import pandas as pd
import altair as alt

# ==============================================================================
# EXPRESSX FINGUIDE - PREMIUM UNIFIED COHESIVE THEME CODES
# ==============================================================================
st.set_page_config(page_title="ExpressX FinGuide v2", page_icon="📊", layout="centered")

# 🎨 Injecting your exact static/css/style.css properties into Streamlit's engine
st.markdown("""
    <style>
    /* 1. Global Background Canvas Overrides */
    .stApp, [data-testid="stAppViewContainer"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
        color: #2d3748 !important;
    }
    
    /* 2. Strips out default block layouts to mirror your centered wrapper cards */
    [data-testid="stVerticalBlock"] > div {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    }
    
    /* 3. Recreates your exact .auth-card-main and .container design */
    .auth-card-main, .container-card {
        width: 100%;
        max-width: 440px;
        background: #ffffff !important;
        padding: 40px 35px !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02) !important;
        border: 1px solid #e2e8f0 !important;
        text-align: center;
        margin: 0 auto;
        box-sizing: border-box;
    }
    
    /* 4. Custom Header Formats */
    h1 { font-size: 32px !important; font-weight: 800 !important; color: #1a202c !important; letter-spacing: -0.5px !important; margin-bottom: 4px !important; }
    h2 { font-size: 18px !important; font-weight: 600 !important; color: #4a5568 !important; margin-bottom: 10px !important; }
    p { font-size: 14px !important; color: #718096 !important; }
    
    /* 5. Left-Aligned Layouts for Inputs */
    .stTextInput, .stNumberInput {
        width: 100% !important;
        max-width: 370px !important;
        text-align: left !important;
    }
    
    label { font-size: 13px !important; font-weight: 600 !important; color: #4a5568 !important; }
    
    /* 6. Enforces your precise custom Input Field Spacing */
    div[data-baseweb="input"] {
        background: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="input"] input {
        color: #334155 !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
    }
    
    /* 7. Upgrades Streamlit buttons to match your bouncy physics code curves */
    .stButton > button {
        width: 100% !important;
        max-width: 370px !important;
        padding: 14px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        background: #1e293b !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    .stButton > button:hover {
        background: #0f172a !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* 8. Floating Asset Decorative Layout Symbols mapping */
    .coin-bg {
        position: absolute !important;
        font-size: 24px !important;
        opacity: 0.12 !important;
        pointer-events: none !important;
        z-index: 1 !important;
    }
    </style>
    
    <!-- 9. Floating Financial Elements Decoration Injection -->
    <div class="coin-bg" style="top: 12%; left: 8%;">💰</div>
    <div class="coin-bg" style="bottom: 15%; right: 8%;">💸</div>
    <div class="coin-bg" style="top: 22%; right: 6%;">💳</div>
    <div class="coin-bg" style="bottom: 22%; left: 6%;">🏦</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# APPLICATION PIPELINE VARIABLES & STATE MAPPING
# ------------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "welcome"
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
# VIEW 1: WELCOME SCREEN PORTAL
# ==============================================================================
if st.session_state.page == "welcome":
    st.markdown("<div class='auth-card-main'>", unsafe_allow_html=True)
    st.write("<p class='auth-badge'>ExpressX Security</p>", unsafe_allow_html=True)
    st.title("Express X FinGuide")
    st.write("Your personal structural guide to optimized budgeting and financial metrics tracking.")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    if st.button("📝 Create Account"):
        st.session_state.page = "signup"
        st.rerun()
    st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
    if st.button("🔐 Login Here →"):
        st.session_state.page = "login"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# VIEW 2: REGISTRATION ARCHITECTURE SCREEN
# ==============================================================================
elif st.session_state.page == "signup":
    st.markdown("<div class='auth-card-main'>", unsafe_allow_html=True)
    st.title("📝 Create Account")
    st.write("<p class='auth-card-subtitle'>Register your profile configuration variables</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    su_name = st.text_input("👤 Full Name", value="", placeholder="Enter full name")
    su_email = st.text_input("📧 Email Address", key="su_email", placeholder="Enter email")
    su_pass = st.text_input("🔒 Account Password", type="password", key="su_pass", placeholder="Create password")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Confirm Profile Registration →"):
        if su_email and su_pass:
            st.session_state.user_name = su_name if su_name else "User"
            st.session_state.page = "dashboard"
            st.rerun()
            
    if st.button("← Cancel and Back", key="back_su"):
        st.session_state.page = "welcome"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# VIEW 3: SECURE ACCESSIBILITY LOGIN PANEL
# ==============================================================================
elif st.session_state.page == "login":
    st.markdown("<div class='auth-card-main'>", unsafe_allow_html=True)
    st.title("🔐 Welcome Back!")
    st.write("<p class='auth-card-subtitle'>Login to manage your financial parameters</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    lin_email = st.text_input("📧 Email Address", key="lin_email", placeholder="Enter your email")
    lin_pass = st.text_input("🔒 Password", type="password", key="lin_pass", placeholder="Enter your password")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Login to FinGuide System →"):
        if lin_email and lin_pass:
            st.session_state.page = "dashboard"
            st.rerun()
            
    if st.button("← Back to Welcome", key="back_lin"):
        st.session_state.page = "welcome"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# VIEW 4: MAIN DASHBOARD OPTION GRID
# ==============================================================================
elif st.session_state.page == "dashboard":
    st.markdown("<div class='auth-card-main'>", unsafe_allow_html=True)
    st.title(f"👋 Welcome {st.session_state.user_name}")
    st.write("<h3>ExpressX Options Hub</h3>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    if st.button("🎯 Set Savings Goal First"):
        st.session_state.page = "step_savings"
        st.rerun()
    st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
    if st.button("💰 Add Monthly Income"):
        st.session_state.page = "step_income"
        st.rerun()
    st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
    if st.button("💸 Add Monthly Expenses"):
        st.session_state.page = "step_expenses"
        st.rerun()
    st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
    if st.button("📊 Financial Analysis Charts"):
        st.session_state.page = "step_analysis"
        st.rerun()
        
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🚪 Logout Systems Connection", key="logout_dash"):
        st.session_state.page = "welcome"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# WORKFLOW FORM: SAVINGS TARGET ENTRIES
# ==============================================================================
elif st.session_state.page == "step_savings":
    st.markdown("<div class='auth-card-main'>", unsafe_allow_html=True)
    st.title("🎯 Savings Goal")
    st.write("<p>Set aside a portion for your future security</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    goal_input = st.number_input("Desired Target Amount (₹)", min_value=0.0, step=500.0, value=st.session_state.savings_goal or 5000.0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Confirm Goal & Proceed →"):
        st.session_state.savings_goal = round(goal_input, 2)
        st.session_state.page = "step_income"
        st.rerun()
        
    if st.button("← Back to Hub"):
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# WORKFLOW FORM: INCOME DATA LOGGING & 5% VERIFIER
# ==============================================================================
elif st.session_state.page == "step_income":
    st.markdown("<div class='auth-card-main'>", unsafe_allow_html=True)
    st.title("💰 Add Income")
    st.write(f"<p>Target Savings Goal Stored: <b>₹{st.session_state.savings_goal:,.2f}</b></p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    source_input = st.text_input("Source Reference", value=st.session_state.income_source or "Salary")
    amount_input = st.number_input("Monthly Payload Amount (₹)", min_value=0.0, step=1000.0, value=st.session_state.income or 50000.0)
    
    # 5% Calculation Rule Logic Block
    min_saving_required = round(amount_input * 0.05, 2)
    is_valid = True
    
    st.markdown("<br>", unsafe_allow_html=True)
    if amount_input > 0 and st.session_state.savings_goal < min_saving_required:
        st.error(f"⚠️ Target Error! Your goal must be at least 5% of income. Minimum required: ₹{min_saving_required:.2f}")
        is_valid = False
    elif amount_input > 0:
        st.success("✅ Target verified and fully compliant.")

    if st.button("Next Step: Expenses →", disabled=not is_valid or amount_input <= 0):
        st.session_state.income = round(amount_input, 2)
        st.session_state.income_source = source_input
        st.session_state.page = "step_expenses"
        st.rerun()
        
    if st.button("← Back to Hub"):
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# WORKFLOW FORM: SEVEN EXPENSE FIELDS MAPPING
# ==============================================================================
elif st.session_state.page == "step_expenses":
    st.markdown("<div class='auth-card-main'>", unsafe_allow_html=True)
    st.title("💸 Monthly Expenses")
    st.write("<p>Input itemized spending category loops</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    food = st.number_input("🍏 Food Spending (₹)", min_value=0.0, value=st.session_state.expenses.get("Food", 0.0))
    travel = st.number_input("🚗 Travel Allowance (₹)", min_value=0.0, value=st.session_state.expenses.get("Travel", 0.0))
    fees = st.number_input("🏫 Education & Fees (₹)", min_value=0.0, value=st.session_state.expenses.get("Fees", 0.0))
    essentials = st.number_input("🛒 Daily Essentials (₹)", min_value=0.0, value=st.session_state.expenses.get("Daily Essentials", 0.0))
    medical = st.number_input("🏥 Medical Care (₹)", min_value=0.0, value=st.session_state.expenses.get("Medical", 0.0))
    entertainment = st.number_input("🎬 Entertainment (₹)", min_value=0.0, value=st.session_state.expenses.get("Entertainment", 0.0))
    others = st.number_input("📦 Other Logistics (₹)", min_value=0.0, value=st.session_state.expenses.get("Others", 0.0))
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Save & View Analysis Dashboard →"):
        st.session_state.expenses = {
            "Food": food, "Travel": travel, "Fees": fees, 
            "Daily Essentials": essentials, "Medical": medical, 
            "Entertainment": entertainment, "Others": others
        }
        st.session_state.page = "step_analysis"
        st.rerun()
        
    if st.button("← Back to Hub"):
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# WORKFLOW FORM: COMPREHENSIVE DATA ANALYSIS GRAPH ARRAYS
# ==============================================================================
elif st.session_state.page == "step_analysis":
    st.markdown("<div class='auth-card-main'>", unsafe_allow_html=True)
    st.title("📊 Financial Analysis")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    total_exp = sum(st.session_state.expenses.values())
    net_cash_left = st.session_state.income - st.session_state.savings_goal - total_exp
    
    st.write(f"💰 **Total Income:** ₹{st.session_state.income:,.0f}")
    st.write(f"🏦 **Planned Savings:** ₹{st.session_state.savings_goal:,.0f}")
    st.write(f"💸 **Total Expenses:** ₹{total_exp:,.0f}")
    
    if net_cash_left >= 0:
        st.markdown(f"💳 **Final Balance:** <span style='color:green;font-weight:700;'>₹{net_cash_left:,.0f}</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"💳 **Final Balance:** <span style='color:red;font-weight:700;'>₹{net_cash_left:,.0f}</span>", unsafe_allow_html=True)
        
    st.markdown("<hr>", unsafe_allow_html=True)
    
    active_expenses = {k: v for k, v in st.session_state.expenses.items() if v > 0}
    if active_expenses:
        st.write("### 🥧 Allocation Split Charts")
        df_exp = pd.DataFrame(list(active_expenses.items()), columns=["Category", "Amount"])
        
        chart = alt.Chart(df_exp).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6).encode(
            x=alt.X('Amount:Q', title="Amount (₹)"),
            y=alt.Y('Category:N', sort='-x', title="Spending Track"),
            color=alt.value('#1e293b')
        ).properties(width=340, height=200)
        st.altair_chart(chart, use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↩️ Back to Dashboard Main Menu"):
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

