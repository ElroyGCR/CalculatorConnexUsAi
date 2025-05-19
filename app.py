import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO
import os

# —— Page Setup ——
st.set_page_config(page_title="ConnexUS AI vs Human ROI Calculator", layout="wide", page_icon=None)

# —— Load Logo & Watermark ——
def load_base64_image(image_path):
    try:
        if not os.path.exists(image_path):
            st.warning(f"Image file not found: {image_path}")
            return None
        
        img = Image.open(image_path)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        st.warning(f"Error loading image {path}: {str(e)}")
        return None

# Paths to logo and watermark
logo_path = "connexus_logo.png"
watermark_path = "connexus_logo_watermark.png"

# CSS Styling
st.markdown("""
<style>
    /* Main container styling */
    .block-container {
        padding-top: 1rem !important;
    }
    
    /* Logo styling */
    .sidebar-logo {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .sidebar-logo img {
        max-height: 60px;
        width: auto;
        object-fit: contain;
    }
    
    /* Metric styling */
    .metric-block {
        background-color: rgba(0,0,0,0.25);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        font-size: 20px;
        color: #00BFFF;
    }
    
    /* Savings card styling */
    .savings-card {
        background-color: #1E4620;
        padding: 20px;
        border-radius: 12px;
        font-size: 28px;
        font-weight: 700;
        color: #C8E6C9;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Projections card styling */
    .projection-card {
        background-color: #2A3E68;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
    }
    .projection-title {
        color: #8BB8F8;
        margin: 0;
        font-size: 18px;
        font-weight: bold;
    }
    .projection-value {
        font-size: 22px;
        margin: 10px 0 5px;
    }
    
    /* Watermark */
    .watermark {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 600px;
        height: 600px;
        opacity: 0.05;
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        pointer-events: none;
        z-index: 0;
    }
</style>
""", unsafe_allow_html=True)

# Watermark CSS injection
watermark_b64 = load_base64_image(watermark_path)
if watermark_b64:
    st.markdown(f"""
        <style>
        .watermark {{
          background-image: url("data:image/png;base64,{watermark_b64}");
        }}
        </style>
        <div class="watermark"></div>
    """, unsafe_allow_html=True)

# —— Header Title ——
st.markdown("""
    <div style='text-align:center; font-size:40px; font-weight:bold; color:#00FFAA; margin-bottom:20px;'>
        🤖 ConnexUS AI vs Human ROI Calculator
    </div>
""", unsafe_allow_html=True)

# —— Logo in sidebar ——
logo_b64 = load_base64_image(logo_path)
if logo_b64:
    st.sidebar.markdown(f"""
        <div class="sidebar-logo">
            <img src='data:image/png;base64,{logo_b64}'>
        </div>
    """, unsafe_allow_html=True)

# —— Sidebar Inputs ——
st.sidebar.header("🔧 Input Parameters")
human_hourly = st.sidebar.number_input("Human Hourly Rate ($)", value=19.5, min_value=0.0, step=0.1)
hours_day = st.sidebar.number_input("Working Hours per Day", value=8.0, min_value=0.0, step=0.5)
efficiency = st.sidebar.slider("Human Agent Utilization (%)", min_value=0, max_value=100, value=65) / 100
ai_cost_per_minute = st.sidebar.number_input("AI Cost per Minute ($)", value=0.35, min_value=0.0, step=0.01)

# —— Core Calculations ——
ai_hourly = ai_cost_per_minute * 60
cost_day = human_hourly * hours_day
worked_hours = hours_day * efficiency
# Fix division by zero error
cost_per_eff_hour = cost_day / worked_hours if worked_hours > 0 else 0
savings_per_hour = cost_per_eff_hour - ai_hourly
savings_pct = (savings_per_hour / cost_per_eff_hour * 100) if cost_per_eff_hour > 0 else 0

# —— Metrics Layout ——
st.markdown("## 💼 AI vs Human Cost Breakdown")

# Add the Breakdown Table section
st.markdown("### 📊 Breakdown Table")
st.markdown("""
<style>
.table-container {
  font-size: 18px;
  background-color: rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  padding: 20px;
  color: #EEE;
  margin-bottom: 30px;
}
.table-container th {
  text-align: left;
  padding-right: 20px;
  color: #00FFAA;
}
.table-container td {
  padding-bottom: 8px;
}
</style>
<div class='table-container'>
  <table>
    <tr><th></th><th>Human</th><th>AI</th></tr>
    <tr><td>Cost per minute</td><td>${0:.2f}</td><td>${1:.2f}</td></tr>
    <tr><td>Hourly Rate</td><td>${2:.2f}</td><td>${3:.2f}</td></tr>
    <tr><td>Working hours per day</td><td>{4}</td><td>{5}</td></tr>
    <tr><td>Utilization</td><td>{6:.0f}%</td><td>100%</td></tr>
    <tr><td>Cost per day</td><td>${7:.2f}</td><td>${8:.2f}</td></tr>
    <tr><td>Effective hours worked</td><td>{9:.2f}</td><td>{10}</td></tr>
    <tr><td>Cost per effective hour</td><td>${11:.2f}</td><td>${12:.2f}</td></tr>
    <tr><td><b>Saving per hour</b></td><td colspan="2"><b>${13:.2f}</b></td></tr>
    <tr><td><b>Saving %</b></td><td colspan="2"><b>{14:.1f}%</b></td></tr>
  </table>
</div>
""".format(
    human_hourly/60, ai_cost_per_minute,
    human_hourly, ai_hourly,
    hours_day, hours_day,
    efficiency*100,
    cost_day, ai_hourly * hours_day,
    worked_hours, hours_day,
    cost_per_eff_hour, ai_hourly,
    savings_per_hour, savings_pct
), unsafe_allow_html=True)

# Use columns for the detailed metrics display
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='metric-block'><b>Cost per Minute (Human)</b><br>${0:.2f}</div>".format(human_hourly / 60), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Hourly Rate (Human)</b><br>${0:.2f}</div>".format(human_hourly), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Working Hours per Day</b><br>{0}</div>".format(hours_day), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Utilization (Human)</b><br>{0:.0f}%</div>".format(efficiency*100), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Cost per Day (Human)</b><br>${0:.2f}</div>".format(cost_day), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Effective Hours Worked</b><br>{0:.2f}</div>".format(worked_hours), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Cost per Effective Hour</b><br>${0:.2f}</div>".format(cost_per_eff_hour), unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-block'><b>Cost per Minute (AI)</b><br>${0:.2f}</div>".format(ai_cost_per_minute), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Hourly Rate (AI)</b><br>${0:.2f}</div>".format(ai_hourly), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Working Hours per Day</b><br>{0}</div>".format(hours_day), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Utilization (AI)</b><br>100%</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Cost per Day (AI)</b><br>${0:.2f}</div>".format(ai_hourly * hours_day), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Effective Hours Worked</b><br>{0:.2f}</div>".format(hours_day), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Cost per Effective Hour</b><br>${0:.2f}</div>".format(ai_hourly), unsafe_allow_html=True)

# —— Savings Row ———
st.markdown("### 💰 Savings Summary")
s1, s2 = st.columns(2)
with s1:
    st.markdown("""
        <div class="savings-card">
        💵 Saving per Hour: ${0:.2f}
        </div>
    """.format(savings_per_hour), unsafe_allow_html=True)
with s2:
    st.markdown("""
        <div class="savings-card">
        📉 Saving Percentage: {0:.1f}%
        </div>
    """.format(savings_pct), unsafe_allow_html=True)

# —— Visual Charts ——
st.markdown("### 🌐 Visual Comparison")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    # Bar Chart with Matplotlib
    labels = ['Human', 'AI']
    costs = [cost_per_eff_hour, ai_hourly]
    colors = ['#FF6B6B', '#4D96FF']

    fig, ax = plt.subplots(figsize=(6, 4))
    # Set transparent background
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    
    bars = ax.bar(labels, costs, color=colors, width=0.6, edgecolor='black')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"${height:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 8),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12, weight='bold')

    mid_y = (costs[0] + costs[1]) / 2
    ax.annotate(f"Savings:\n${savings_per_hour:.2f}\n({savings_pct:.1f}%)",
                xy=(0.5, mid_y),
                xytext=(0.5, mid_y + 10),
                ha='center', va='center',
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.5", fc="lightgreen", ec="green", lw=2))

    ax.set_ylabel("Cost per Effective Hour ($)", fontsize=12)
    ax.set_ylim(0, max(costs[0], costs[1]) * 1.3)
    ax.set_title("Cost Comparison: Human vs AI", fontsize=14, weight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Set text color to white for better visibility
    ax.title.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    
    st.pyplot(fig)

with col2:
    # Adding a Plotly interactive chart
    fig = go.Figure()
    
    # Bar chart for comparison
    fig.add_trace(go.Bar(
        x=labels,
        y=costs,
        text=[f"${cost:.2f}" for cost in costs],
        textposition='auto',
        marker_color=colors,
        hoverinfo='y+name'
    ))
    
    # Add annotation for savings
    fig.add_annotation(
        x=0.5,
        y=max(costs) * 0.7,
        text=f"Savings: ${savings_per_hour:.2f} ({savings_pct:.1f}%)",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40,
        bgcolor="rgba(144, 238, 144, 0.6)",
        bordercolor="green",
        borderwidth=2,
        borderpad=4,
        font=dict(color="black", size=14)
    )
    
    # Update layout with transparent background
    fig.update_layout(
        title="Interactive Cost Comparison",
        xaxis_title="",
        yaxis_title="Cost per Effective Hour ($)",
        height=400,
        margin=dict(l=40, r=40, t=60, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font_size=18
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Add monthly and yearly projections
st.markdown("### 📆 Cost Projections")
days_month = 22  # Average working days per month
months_year = 12

# Calculate projections
monthly_human_cost = cost_day * days_month
monthly_ai_cost = ai_hourly * hours_day * days_month
monthly_savings = (savings_per_hour * hours_day) * days_month

yearly_human_cost = monthly_human_cost * months_year
yearly_ai_cost = monthly_ai_cost * months_year
yearly_savings = monthly_savings * months_year

# Create columns for projections
proj1, proj2, proj3 = st.columns(3)

with proj1:
    st.markdown("""
        <div class="projection-card">
            <h4 class="projection-title">Daily</h4>
            <p class="projection-value">
                <span style='color:#FF6B6B;'>Human: ${0:.2f}</span><br>
                <span style='color:#4D96FF;'>AI: ${1:.2f}</span><br>
                <span style='color:#C8E6C9;'>Savings: ${2:.2f}</span>
            </p>
        </div>
    """.format(cost_day, ai_hourly * hours_day, savings_per_hour * hours_day), unsafe_allow_html=True)

with proj2:
    st.markdown("""
        <div class="projection-card">
            <h4 class="projection-title">Monthly (22 days)</h4>
            <p class="projection-value">
                <span style='color:#FF6B6B;'>Human: ${0:.2f}</span><br>
                <span style='color:#4D96FF;'>AI: ${1:.2f}</span><br>
                <span style='color:#C8E6C9;'>Savings: ${2:.2f}</span>
            </p>
        </div>
    """.format(monthly_human_cost, monthly_ai_cost, monthly_savings), unsafe_allow_html=True)

with proj3:
    st.markdown("""
        <div class="projection-card">
            <h4 class="projection-title">Yearly</h4>
            <p class="projection-value">
                <span style='color:#FF6B6B;'>Human: ${0:,.2f}</span><br>
                <span style='color:#4D96FF;'>AI: ${1:,.2f}</span><br>
                <span style='color:#C8E6C9;'>Savings: ${2:,.2f}</span>
            </p>
        </div>
    """.format(yearly_human_cost, yearly_ai_cost, yearly_savings), unsafe_allow_html=True)

# —— Footer ——
st.markdown("---")
st.caption("AI vs Human Cost Calculator by ConnexUS. Built with Streamlit & Plotly.")
