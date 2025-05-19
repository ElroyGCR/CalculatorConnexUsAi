import streamlit as st
import plotly.graph_objects as go
from decimal import Decimal, ROUND_HALF_UP

# —— Page Setup ——
st.set_page_config(page_title="AI vs Human Cost Calculator", layout="wide")

# —— Sidebar Inputs ——
st.sidebar.header("🔧 Input Parameters")
human_hourly = st.sidebar.number_input("Human Hourly Rate ($)", value=19.5, min_value=0.0)
hours_day = st.sidebar.number_input("Working Hours per Day", value=8.0, min_value=0.0)
efficiency = st.sidebar.slider("Human Agent Efficiency (%)", min_value=0, max_value=100, value=65) / 100
ai_hourly = st.sidebar.number_input("AI Cost per Hour ($)", value=21.0, min_value=0.0)

# —— Core Calculations ——
cost_day = human_hourly * hours_day
worked_hours = hours_day * efficiency
cost_per_eff_hour = cost_day / worked_hours if worked_hours else float('inf')
savings_per_hour = cost_per_eff_hour - ai_hourly
savings_pct = (savings_per_hour / cost_per_eff_hour * 100) if cost_per_eff_hour else 0

# —— Layout ——
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📉 Input Assumptions")
    st.write(f"**Human Hourly Rate:** ${human_hourly:,.2f}")
    st.write(f"**Hours per Day:** {hours_day:,.2f}")
    st.write(f"**Efficiency:** {efficiency*100:.0f}%")
    st.write(f"**AI Hourly Rate:** ${ai_hourly:,.2f}")

with col2:
    st.markdown("### 🌊 Calculated Output")
    st.success(f"**Human Cost per Day:** ${cost_day:,.2f}")
    st.success(f"**Effective Hours Worked:** {worked_hours:,.2f}")
    st.success(f"**Human Cost per Effective Hour:** ${cost_per_eff_hour:,.2f}")
    st.success(f"**AI Cost per Effective Hour:** ${ai_hourly:,.2f}")
    st.success(f"**Savings per Hour:** ${savings_per_hour:,.2f}")
    st.success(f"**Savings Percentage:** {savings_pct:,.1f}%")

# —— Chart ——
st.markdown("### 🌐 Visual Comparison")
fig = go.Figure(data=[
    go.Bar(name="Human Cost/hr", x=["Human"], y=[cost_per_eff_hour], marker_color="#EF5350"),
    go.Bar(name="AI Cost/hr", x=["AI"], y=[ai_hourly], marker_color="#66BB6A"),
])
fig.update_layout(
    yaxis_title="Cost per Effective Hour ($)",
    barmode='group',
    height=400,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=40, b=40)
)
st.plotly_chart(fig, use_container_width=True)

# —— Footer ——
st.markdown("---")
st.caption("AI vs Human Cost Calculator by ConnexUS. Built with Streamlit & Plotly.")
