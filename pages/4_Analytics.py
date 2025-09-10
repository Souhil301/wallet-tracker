# pages/4_Analytics.py
import streamlit as st
import pandas as pd
from utils import simple_forecast
import plotly.express as px

st.title("📊 Analytics & Forecasting")

st.markdown("This page shows trends, a simple forecast for the next 3 months, and compares your spending to a benchmark household (demo data).")

income = st.session_state.get("income", 0)
expenses = st.session_state.get("expenses", {})

# Create a simple series of last 6 month totals using randomness if not present
if "history_totals" not in st.session_state:
    base = sum(expenses.values())
    # make 6 months history (demo): slight noise around current total
    st.session_state.history_totals = [max(0, base * (0.8 + 0.08*i) ) for i in range(6)]

history = st.session_state.history_totals
st.write("Past 6 months expenses (demo)", history)

# Forecast next 3 months
preds = simple_forecast(history, n_forecast=3)
months = list(range(1, len(history)+1+len(preds)))
values = history + preds
df = pd.DataFrame({"Month": months, "Expense": values, "Type": ["history"]*len(history) + ["forecast"]*len(preds)})

fig = px.line(df, x="Month", y="Expense", color="Type", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Benchmarks (demo)")
# Dummy benchmark data (average household)
benchmark = {
    "Food": 15000,
    "Transport": 7000,
    "Housing": 20000,
    "Shopping": 8000,
    "Entertainment": 3000,
    "Other": 2000
}

user_df = pd.DataFrame({"Category": list(expenses.keys()), "User": list(expenses.values()), "Avg": [benchmark.get(k, 0) for k in expenses.keys()]})
st.data_editor(user_df)

# horizontal comparison chart
fig2 = px.bar(user_df, x="Category", y=["User", "Avg"], barmode="group")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("Insights:")
for cat in expenses.keys():
    user_val = expenses.get(cat, 0)
    avg_val = benchmark.get(cat, 0)
    if avg_val > 0:
        pct = (user_val - avg_val) / avg_val * 100
        if pct > 20:
            st.warning(f"You spend {pct:.0f}% more on **{cat}** than the benchmark.")
        elif pct < -20:
            st.info(f"You spend {abs(pct):.0f}% less on **{cat}** than the benchmark.")
