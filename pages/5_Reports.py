# pages/5_Reports.py
import streamlit as st
import pandas as pd
from utils import df_to_csv_bytes, df_to_excel_bytes, create_pdf_report

st.title("🗂 Reports & Exports")

income = st.session_state.get("income", 0)
expenses = st.session_state.get("expenses", {})
portfolio = st.session_state.get("portfolio", [])
notes = st.session_state.get("notes", [])

st.subheader("Download data")

summary_df = pd.DataFrame({"Category": list(expenses.keys()), "Amount": list(expenses.values())})
summary_df_totals = pd.DataFrame([{"Income": income, "Total Expenses": sum(expenses.values()), "Savings": income - sum(expenses.values())}])

csv = df_to_csv_bytes(summary_df)
excel = df_to_excel_bytes(summary_df)

st.download_button("Download expenses CSV", data=csv, file_name="expenses.csv", mime="text/csv")
st.download_button("Download expenses XLSX", data=excel, file_name="expenses.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown("---")
st.subheader("Simple PDF report")
summary_text = f"Monthly Summary\nIncome: {income:.0f} DA\nTotal expenses: {sum(expenses.values()):.0f} DA\nSavings: {income - sum(expenses.values()):.0f} DA\n\nNotes:\n" + "\n".join(notes)
pdf_bytes = create_pdf_report(summary_text)
st.download_button("Download PDF summary", data=pdf_bytes, file_name="wallet_report.pdf", mime="application/pdf")
