import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# —— Page Setup ——
st.set_page_config(page_title="AI vs Human ROI Calculator", layout="wide")

# —— Sidebar Inputs ——
st.sidebar.header("🔧 Input Parameters")
human_hourly = st.sidebar.number_input("Human Hourly Rate ($)", value=19.5, min_value=0.0)
hours_day = st.sidebar.number_input("Working Hours per Day", value=8.0, min_value=0.0)
efficiency = st.sidebar.slider("Human Agent Utilization (%)", min_value=0, max_value=100, value=40) / 100
ai_cost_per_minute = st.sidebar.number_input("AI Cost per Minute ($)", value=0.35, min_value=0.0)

# —— Core Calculations ——
ai_hourly = ai_cost_per_minute * 60
cost_day = human_hourly * hours_day
worked_hours = hours_day * efficiency
cost_per_eff_hour = cost_day / worked_hours if worked_hours else float('inf')
savings_per_hour = cost_per_eff_hour - ai_hourly
savings_pct = (savings_per_hour / cost_per_eff_hour * 100) if cost_per_eff_hour else 0

# —— Layout ——
col1, col2 = st.columns([0.05, 0.95])

with col2:
    st.markdown("### 📋 Input Assumptions")
    st.markdown("---")
    st.markdown(f"**Human Hourly Rate:** ${human_hourly:.2f}")
    st.markdown(f"**Working Hours per Day:** {hours_day}")
    st.markdown(f"**Human Utilization:** {efficiency*100:.0f}%")
    st.markdown(f"**AI Cost per Minute:** ${ai_cost_per_minute:.2f}")
    st.markdown(f"**AI Hourly Rate:** ${ai_hourly:.2f}")

    st.markdown("---")
    st.markdown("### 📊 Calculated Output")
    st.subheader("🧍 Human Agent Stats")
    st.markdown(f"<div style='background-color: rgba(0,0,0,0.25); padding: 10px; border-radius: 8px;'>**Human Cost per Day:** ${cost_day:.2f}<br>**Effective Hours Worked:** {worked_hours:.2f}<br>**Human Cost per Effective Hour:** ${cost_per_eff_hour:.2f}</div>", unsafe_allow_html=True)

    st.subheader("🤖 AI Agent Stats")
    st.markdown(f"<div style='background-color: rgba(0,0,0,0.25); padding: 10px; border-radius: 8px;'>**AI Cost per Effective Hour:** ${ai_hourly:.2f}</div>", unsafe_allow_html=True)

    st.subheader("💰 Savings")
    st.markdown(f"<div style='background-color: rgba(0,0,0,0.25); padding: 10px; border-radius: 8px; color: #00FFAA; font-weight: bold;'>Savings per Hour: ${savings_per_hour:.2f}<br>Savings Percentage: {savings_pct:.1f}%</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🌐 Visual Comparison (Matplotlib)")
    labels = ['Human', 'AI']
    costs = [cost_per_eff_hour, ai_hourly]
    colors = ['#FF6B6B', '#4D96FF']

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, costs, color=colors, width=0.6, edgecolor='black')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"${height:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 8),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10, weight='bold')

    mid_x = 0.5
    mid_y = (costs[0] + costs[1]) / 2
    ax.annotate(f"Savings:\n${savings_per_hour:.2f}\n({savings_pct:.1f}%)",
                xy=(mid_x, mid_y),
                xytext=(mid_x, mid_y + 10),
                ha='center', va='center',
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.5", fc="lightgreen", ec="green", lw=2))

    ax.set_ylabel("Cost per Effective Hour ($)")
    ax.set_ylim(0, max(costs[0], costs[1]) * 1.3)
    ax.set_title("Cost Comparison: Human vs AI", fontsize=14, weight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)

    st.markdown("---")
    st.markdown("### 🌐 Visual Comparison (Plotly)")
    fig2 = go.Figure(data=[
        go.Bar(name="Human Cost/hr", x=["Human"], y=[cost_per_eff_hour], marker_color="#EF5350"),
        go.Bar(name="AI Cost/hr", x=["AI"], y=[ai_hourly], marker_color="#66BB6A"),
    ])
    fig2.update_layout(
        yaxis_title="Cost per Effective Hour ($)",
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=40)
    )
    st.plotly_chart(fig2, use_container_width=True)

# —— Footer ——
st.markdown("---")
st.caption("AI vs Human Cost Calculator by ConnexUS. Built with Streamlit & Plotly.")
