# pages/2_Savings.py
import streamlit as st
from utils import bar_summary
import pandas as pd

st.title("💡 Savings & Monthly Summary")

income = st.session_state.get("income", 0)
expenses = st.session_state.get("expenses", {})
notes = st.session_state.get("notes", [])

total_expenses = sum(expenses.values())
savings = income - total_expenses

st.metric("Monthly Income (DA)", f"{income:,.0f}")
st.metric("Total Expenses (DA)", f"{total_expenses:,.0f}")
st.metric("Estimated Savings (DA)", f"{savings:,.0f}")

st.markdown("### Simple monthly summary")
st.write(f"This month you spent **{total_expenses:,.0f} DA** and saved **{savings:,.0f} DA**.")

# Simulate last month totals using a simple shift (for demo)
# If you had stored historical months, you'd pull them. We'll create a fake 'last month'
last_month_total = st.session_state.get("last_month_total", max(total_expenses * 0.8, 1))
st.session_state["last_month_total"] = total_expenses  # update for next time

delta_pct = ((last_month_total - total_expenses) / last_month_total * 100) if last_month_total else 0

if delta_pct > 0:
    st.success(f"Good job — spending decreased by {abs(delta_pct):.1f}% vs last month.")
elif delta_pct < 0:
    st.warning(f"Spending increased by {abs(delta_pct):.1f}% vs last month.")
else:
    st.info("Spending is unchanged vs last month.")

fig = bar_summary(income, total_expenses, savings)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("Friendly tips & alerts")
# simple rule-based alerts
if total_expenses > income:
    st.error("⚠️ Warning: Your expenses are higher than income. Consider reducing discretionary spending.")
elif total_expenses > 0.9 * income:
    st.warning("⚠️ You are close to your income limit. Review expenses.")
else:
    st.success("✅ Your spending looks within your income range.")

# Example personalized tip
if expenses.get("Shopping", 0) > 0.3 * total_expenses and total_expenses>0:
    st.info("💡Tip: Shopping is a large part of your spending. Consider a 10% cut and see the monthly savings.")
