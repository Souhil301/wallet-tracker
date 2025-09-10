# pages/3_Investments.py
import streamlit as st
from utils import investment_line
import numpy as np

st.title("📈 Investments & Portfolio Simulation")

st.markdown("Enter sample investments (fake values). We'll simulate growth with simple compound interest assumptions.")

if "portfolio" not in st.session_state:
    st.session_state.portfolio = []

with st.form("add_inv"):
    name = st.text_input("Instrument name (e.g., Stocks - XYZ)")
    principal = st.number_input("Amount (DA)", min_value=0.0, step=100.0)
    ann_rate = st.number_input("Expected annual return (%)", min_value=0.0, max_value=100.0, value=6.0)
    years = st.number_input("Years to simulate", min_value=1, max_value=30, value=3)
    add = st.form_submit_button("Add to portfolio")
    if add:
        if name and principal > 0:
            st.session_state.portfolio.append({"name": name, "principal": principal, "rate": ann_rate, "years": int(years)})
            st.success("Added")

if st.session_state.portfolio:
    st.subheader("Portfolio items")
    for idx, item in enumerate(st.session_state.portfolio):
        st.write(f"- {item['name']}: {item['principal']} DA @ {item['rate']}% for {item['years']} years")

    # Combine simulation
    months = list(range(1, 12*max([p['years'] for p in st.session_state.portfolio]) + 1))
    combined = np.zeros(len(months))
    for p in st.session_state.portfolio:
        n = p['years'] * 12
        monthly_rate = (1 + p['rate']/100) ** (1/12) - 1
        values = []
        value = p['principal']
        for m in range(1, n+1):
            value = value * (1 + monthly_rate)
            values.append(value)
        # pad to full months length
        values = values + [values[-1]]*(len(months)-len(values))
        combined += np.array(values)
    fig = investment_line(months, combined.tolist())
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Animated growth")
    chart = st.line_chart([])
    import time
    for i in range(len(months)):
        chart.add_rows([[months[i], float(combined[i])]])
        time.sleep(0.02)
else:
    st.info("No portfolio items yet. Add one above to simulate.")
