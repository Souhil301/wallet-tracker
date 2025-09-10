# pages/1_Expenses.py
import streamlit as st
from utils import pie_expenses, categorize_text
import pandas as pd

st.title("📊 Expenses")

st.markdown("This page shows your current expense breakdown and lets you add quick entries (text or voice file).")

income = st.session_state.get("income", 0)
expenses = st.session_state.get("expenses", {})

st.subheader("Expense breakdown")
fig = pie_expenses(expenses)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Add quick expense (text)")
with st.form("quick_exp"):
    desc = st.text_input("Description (e.g., 'Groceries 800')")
    amount = st.number_input("Amount (DA)", min_value=0.0, step=100.0)
    submitted = st.form_submit_button("Add")
    if submitted:
        if desc and amount > 0:
            cat = categorize_text(desc)
            st.session_state.expenses[cat] = st.session_state.expenses.get(cat, 0) + float(amount)
            st.success(f"Added {amount} DA to {cat}")
        else:
            st.error("Provide description and amount")

st.markdown("---")
st.subheader("Transcribe voice note (upload .wav/.mp3)")
st.markdown("Record on your phone/browser, then upload the audio file here. The app will try to transcribe and auto-categorize.")

upload = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a", "flac"])
from utils import transcribe_audio_file
if upload is not None:
    with st.spinner("Transcribing..."):
        text = transcribe_audio_file(upload)
    if text.startswith("ERROR"):
        st.error(text)
    else:
        st.success("Transcribed:")
        st.write(text)
        # Try extract amount from transcription
        import re
        m = re.search(r"(\d+[\.,]?\d*)", text.replace(",", ""))
        amount = float(m.group(1)) if m else 0.0
        cat = categorize_text(text)
        st.write(f"Detected category: **{cat}** | detected amount: **{amount} DA**")
        if st.button("Add transcribed expense"):
            if amount > 0:
                st.session_state.expenses[cat] = st.session_state.expenses.get(cat, 0) + amount
                st.success(f"Added {amount} DA to {cat}")
            else:
                st.error("No amount detected in transcription. Edit text or use manual entry.")
