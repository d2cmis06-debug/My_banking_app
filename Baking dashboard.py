import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Bharosa Bank Pro", layout="wide")

st.markdown("""
    <style>
    /* Background Dark */
    .stApp { background-color: #0e1117; }
    
    /* Title Gold */
    h1 { color: #ffd700 !important; text-align: center; font-size: 45px !important; font-weight: bold; }
    
    /* Sabhi Labels aur Text ko Bright White karne ke liye */
    label, p, .stMarkdown, .stSelectbox label, .stNumberInput label, .stTextInput label {
        color: #ffffff !important; 
        font-size: 18px !important; 
        font-weight: 600 !important;
    }

    /* Tabs ka color white */
    .stTabs [data-baseweb="tab"] p {
        color: #ffffff !important;
    }

    /* Input boxes ke andar ka text black (padhne ke liye) */
    input { color: #000000 !important; font-weight: bold !important; background-color: #ffffff !important; }
    
    /* Table headers white */
    thead tr th { color: #ffffff !important; background-color: #1f2937 !important; }
    
    .card { background-color: #1f2937; padding: 20px; border-radius: 15px; border: 1px solid #4b5563; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA INITIALIZATION ---
if "accounts" not in st.session_state:
    st.session_state.accounts = {
        "Admin": {"balance": 50000.0, "type": "Savings"},
        "Rahul": {"balance": 10000.0, "type": "Current"}
    }
if "history" not in st.session_state:
    st.session_state.history = []

# --- 3. HEADER ---
st.markdown("<h1>🏦 Bharosa Bank Management</h1>", unsafe_allow_html=True)

# --- 4. MAIN FEATURES ---
tab1, tab2, tab3, tab4 = st.tabs(["💰 Transactions", "👤 Manage Accounts", "📜 History", "📋 Services"])

# --- TAB 1: TRANSACTIONS ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Deposit Money (Credit)")
        user_to_credit = st.selectbox("Select Account to Credit:", list(st.session_state.accounts.keys()), key="credit_user")
        credit_amt = st.number_input("Amount to Deposit (₹):", min_value=0.0, step=500.0, key="c_amt")
        if st.button("Deposit Cash 📥"):
            if credit_amt > 0:
                st.session_state.accounts[user_to_credit]["balance"] += credit_amt
                st.session_state.history.append({"Date": datetime.now().strftime("%d-%m-%Y %H:%M"), "Account": user_to_credit, "Type": "CREDIT", "Amount": f"+₹{credit_amt}"})
                st.success(f"₹{credit_amt} credited successfully!")
                st.rerun()

    with col2:
        st.markdown("### Transfer Money (Debit)")
        sender = st.selectbox("From Account:", list(st.session_state.accounts.keys()), key="debit_user")
        receiver = st.text_input("Receiver Name:")
        debit_amt = st.number_input("Amount to Transfer (₹):", min_value=0.0, step=500.0, key="d_amt")
        if st.button("Send Money 📤"):
            if debit_amt > st.session_state.accounts[sender]["balance"]:
                st.error("Insufficient Funds!")
            elif debit_amt > 0:
                st.session_state.accounts[sender]["balance"] -= debit_amt
                st.session_state.history.append({"Date": datetime.now().strftime("%d-%m-%Y %H:%M"), "Account": sender, "Type": "DEBIT", "Amount": f"-₹{debit_amt}"})
                st.success("Sent Successfully!")
                st.rerun()

# --- TAB 2: ACCOUNT MANAGEMENT ---
with tab2:
    st.markdown("### Bank Administration")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Add New Account")
        new_name = st.text_input("Enter Full Name:")
        acc_type = st.selectbox("Account Type:", ["Savings", "Current", "Salary"])
        init_dep = st.number_input("Initial Deposit (₹):", min_value=0.0)
        if st.button("Create Account ✅"):
            if new_name and new_name not in st.session_state.accounts:
                st.session_state.accounts[new_name] = {"balance": init_dep, "type": acc_type}
                st.success(f"Account created!")
                st.rerun()

    with c2:
        st.markdown("#### Delete Account")
        user_to_del = st.selectbox("Select Account to Remove:", ["Select--"] + list(st.session_state.accounts.keys()))
        if st.button("Delete Permanently 🗑️"):
            if user_to_del != "Select--" and user_to_del != "Admin":
                del st.session_state.accounts[user_to_del]
                st.warning(f"Account closed.")
                st.rerun()

    st.markdown("### Current Customer Database")
    st.table(pd.DataFrame.from_dict(st.session_state.accounts, orient='index'))

# --- TAB 3: HISTORY ---
with tab3:
    st.markdown("### Transaction Records")
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history))