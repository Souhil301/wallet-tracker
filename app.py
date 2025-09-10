# app.py
import streamlit as st
from utils import DEFAULT_CATEGORIES

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2e2e 0%, #0a192f 50%, #142d4c 100%);
        color: #e6f1f5;
    }
    .stSidebar {
        background: #1c2541 !important;
    }
    </style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Wallet Tracker", layout="wide")

# ---------- Accessibility settings ----------
if "accessibility" not in st.session_state:
    st.session_state.accessibility = {"big_font": False, "high_contrast": False}

def apply_accessibility():
    css = ""
    if st.session_state.accessibility["big_font"]:
        css += """
        html, body, [class*="css"]  {
            font-size: 18px !important;
        }
        """
    if st.session_state.accessibility["high_contrast"]:
        css += """
        .stApp {
            background-color: #000 !important;
            color: #fff !important;
        }
        .stButton>button, .stMetric {
            background-color: #111 !important;
            color: #fff !important;
        }
        """
    if css:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.title("💰 Wallet Tracker & Portfolio Analytics")
st.markdown("Simple demo for the event — **enter data once** in Home, then explore pages for Expenses, Savings, Investments, Analytics, and Reports.")

with st.sidebar:
    st.header("Settings & Accessibility")
    big = st.checkbox("Big fonts", value=st.session_state.accessibility["big_font"])
    highc = st.checkbox("High contrast", value=st.session_state.accessibility["high_contrast"])
    st.session_state.accessibility["big_font"] = big
    st.session_state.accessibility["high_contrast"] = highc
    apply_accessibility()

# Initialize session_storage for inputs
if "income" not in st.session_state:
    st.session_state.income = 50000
if "expenses" not in st.session_state:
    st.session_state.expenses = {cat: 0.0 for cat in DEFAULT_CATEGORIES}
if "notes" not in st.session_state:
    st.session_state.notes = []

st.header("Enter monthly financial data (fake data is fine)")
st.session_state.income = st.number_input("Monthly income (DA)", min_value=0, value=int(st.session_state.income), step=1000)

st.markdown("**Expenses by category**")
cols = st.columns(3)
i = 0
for cat in st.session_state.expenses.keys():
    with cols[i % 3]:
        val = st.number_input(f"{cat}", min_value=0.0, value=float(st.session_state.expenses[cat]), step=500.0, format="%f")
        st.session_state.expenses[cat] = float(val)
    i += 1

st.markdown("---")
st.markdown("**Quick expense entry / note** (type or upload voice note on Expenses page)")
note = st.text_input("Add short note (e.g., 'Bought groceries 800')", value="")
if st.button("Add note"):
    if note.strip():
        st.session_state.notes.append(note.strip())
        st.success("Note added")
    else:
        st.error("Note is empty")

st.success("Data saved. Use Pages (left) to navigate: Expenses, Savings, Investments, Analytics, Reports.")
