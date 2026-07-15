import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configure dashboard layout
st.set_page_config(layout="wide")

# -------------------------------
# Dashboard Header
# -------------------------------
st.title("📊 Financial Dashboard")
st.markdown("EMI Calculator + Salary Revision Simulator (Dynamic for Any Country)")

# -------------------------------
# Layout: Two Columns
# -------------------------------
col1, col2 = st.columns(2)

# --- EMI Calculator in Column 1 ---
with col1:
    st.subheader("EMI Calculator")
    P = st.number_input("Loan Amount", value=500000)
    R = st.number_input("Annual Interest Rate (%)", value=10.0)
    N = st.number_input("Tenure (months)", value=60)

    def calculate_emi(P, R, N):
        r = R / 12 / 100
        emi = (P * r * (1 + r)**N) / ((1 + r)**N - 1)
        total_payment = emi * N
        total_interest = total_payment - P
        return emi, total_payment, total_interest

    emi, total_payment, total_interest = calculate_emi(P, R, N)
    st.metric("Monthly EMI", f"₹{emi:.2f}")
    st.metric("Total Payment", f"₹{total_payment:.2f}")
    st.metric("Total Interest", f"₹{total_interest:.2f}")

# --- Salary Simulator in Column 2 ---
with col2:
    st.subheader("Salary Revision Simulator")

    country1 = st.text_input("Country 1", value="Qatar")
    country2 = st.text_input("Country 2", value="India")

    S1 = st.number_input(f"Current Salary in {country1}", value=100000)
    S2 = st.number_input(f"Proposed Salary in {country1}", value=120000)
    C1 = st.number_input(f"Living Cost {country1}", value=40000)
    C2 = st.number_input(f"Living Cost {country2}", value=25000)

    def salary_simulator(S1, S2, C1, C2):
        net_gain_country1 = S2 - C1
        net_gain_country2 = S2 - C2
        breakeven = (S2 - S1) / (C1 - C2) if (C1 - C2) != 0 else None
        return net_gain_country1, net_gain_country2, breakeven

    net_c1, net_c2, breakeven = salary_simulator(S1, S2, C1, C2)

    st.metric(f"Net Gain {country1}", f"₹{net_c1}")
    st.metric(f"Net Gain {country2}", f"₹{net_c2}")
    if breakeven is not None:
        st.metric("Breakeven Months", f"{breakeven:.2f}")

# -------------------------------
# Tabs for Charts
# -------------------------------
tab1, tab2 = st.tabs(["📉 EMI Comparison", "📈 Savings Growth"])

with tab1:
    loan_options = [
        {"amount": 500000, "rate": 10, "months": 60},
        {"amount": 500000, "rate": 12, "months": 60},
        {"amount": 500000, "rate": 8, "months": 60},
    ]
    emis = []
    labels = []
    for option in loan_options:
        emi_val, _, _ = calculate_emi(option["amount"], option["rate"], option["months"])
        emis.append(emi_val)
        labels.append(f"{option['rate']}%")

    fig, ax = plt.subplots()
    ax.bar(labels, emis)
    ax.set_title("EMI Comparison Across Interest Rates")
    ax.set_ylabel("Monthly EMI (₹)")
    st.pyplot(fig)

    # Insights
    min_emi = min(emis)
    max_emi = max(emis)
    best_rate = labels[emis.index(min_emi)]
    worst_rate = labels[emis.index(max_emi)]
    st.info(f"✅ Lowest EMI is at {best_rate}, saving ₹{max_emi - min_emi:.2f} per month compared to {worst_rate}.")

with tab2:
    years = list(range(1, 6))
    annual_savings_c1 = [net_c1 * 12 * y for y in years]
    annual_savings_c2 = [net_c2 * 12 * y for y in years]

    fig2, ax2 = plt.subplots()
    ax2.plot(years, annual_savings_c1, marker='o', label=country1)
    ax2.plot(years, annual_savings_c2, marker='o', label=country2)
    ax2.set_title("Savings Growth Over 5 Years")
    ax2.set_xlabel("Years")
    ax2.set_ylabel("Total Savings (₹)")
    ax2.legend()
    st.pyplot(fig2)

    # Insights
    if net_c1 > net_c2:
        st.info(f"💡 Relocating to {country1} increases savings by ₹{net_c1 - net_c2:.2f} per month compared to {country2}.")
    else:
        st.info(f"💡 Staying in {country2} provides higher monthly savings by ₹{net_c2 - net_c1:.2f} compared to {country1}.")
    if breakeven is not None:
        st.info(f"📊 Breakeven in about {breakeven:.1f} months.")
