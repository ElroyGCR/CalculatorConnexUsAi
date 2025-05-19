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
        st.warning(f"Error loading image {image_path}: {str(e)}")
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
    
    /* Table styling */
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
        background-color: rgba(30, 70, 32, 0.8);
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
        background-color: rgba(42, 62, 104, 0.8);
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
        width: 800px;
        height: 800px;
        opacity: 0.08;
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        pointer-events: none;
        z-index: -1;
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

# —— Breakdown Table - avoiding format() method ——
st.markdown("### 📊 Breakdown Table")

# Pre-format values to avoid using str.format() method
human_cost_per_min = f"${human_hourly/60:.2f}"
ai_cost_per_min = f"${ai_cost_per_minute:.2f}"
human_hourly_fmt = f"${human_hourly:.2f}"
ai_hourly_fmt = f"${ai_hourly:.2f}"
hours_day_fmt = f"{hours_day}"
efficiency_fmt = f"{efficiency*100:.0f}%"
human_cost_day = f"${cost_day:.2f}"
ai_cost_day = f"${ai_hourly * hours_day:.2f}"
worked_hours_fmt = f"{worked_hours:.2f}"
hours_day_str = f"{hours_day}"
cost_per_eff_hour_fmt = f"${cost_per_eff_hour:.2f}"
ai_hourly_fmt2 = f"${ai_hourly:.2f}"
savings_per_hour_fmt = f"${savings_per_hour:.2f}"
savings_pct_fmt = f"{savings_pct:.1f}%"

# Create HTML table without using format()
table_html = f"""
<div class='table-container'>
  <table>
    <tr><th></th><th>Human</th><th>AI</th></tr>
    <tr><td>Cost per minute</td><td>{human_cost_per_min}</td><td>{ai_cost_per_min}</td></tr>
    <tr><td>Hourly Rate</td><td>{human_hourly_fmt}</td><td>{ai_hourly_fmt}</td></tr>
    <tr><td>Working hours per day</td><td>{hours_day_fmt}</td><td>{hours_day_fmt}</td></tr>
    <tr><td>Utilization</td><td>{efficiency_fmt}</td><td>100%</td></tr>
    <tr><td>Cost per day</td><td>{human_cost_day}</td><td>{ai_cost_day}</td></tr>
    <tr><td>Effective hours worked</td><td>{worked_hours_fmt}</td><td>{hours_day_str}</td></tr>
    <tr><td>Cost per effective hour</td><td>{cost_per_eff_hour_fmt}</td><td>{ai_hourly_fmt2}</td></tr>
    <tr><td><b>Saving per hour</b></td><td colspan="2"><b>{savings_per_hour_fmt}</b></td></tr>
    <tr><td><b>Saving %</b></td><td colspan="2"><b>{savings_pct_fmt}</b></td></tr>
  </table>
</div>
"""
st.markdown(table_html, unsafe_allow_html=True)

# —— Metrics Layout ——
st.markdown("## 💼 AI vs Human Cost Breakdown")

# Use columns for the metrics display
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"<div class='metric-block'><b>Cost per Minute (Human)</b><br>${human_hourly/60:.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-block'><b>Hourly Rate (Human)</b><br>${human_hourly:.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-block'><b>Working Hours per Day</b><br>{hours_day}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-block'><b>Utilization (Human)</b><br>{efficiency*100:.0f}%</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-block'><b>Cost per Day (Human)</b><br>${cost_day:.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-block'><b>Effective Hours Worked</b><br>{worked_hours:.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-block'><b>Cost per Effective Hour</b><br>${cost_per_eff_hour:.2f}</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='metric-block'><b>Cost per Minute (AI)</b><br>${ai_cost_per_minute:.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-block'><b>Hourly Rate (AI)</b><br>${ai_hourly:.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-block'><b>Working Hours per Day</b><br>{hours_day}</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Utilization (AI)</b><br>100%</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-block'><b>Cost per Day (AI)</b><br>${ai_hourly * hours_day:.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-block'><b>Effective Hours Worked</b><br>{hours_day:.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-block'><b>Cost per Effective Hour</b><br>${ai_hourly:.2f}</div>", unsafe_allow_html=True)

# —— Savings Row ———
st.markdown("### 💰 Savings Summary")
s1, s2 = st.columns(2)
with s1:
    st.markdown(f"""
        <div class="savings-card">
        💵 Saving per Hour: ${savings_per_hour:.2f}
        </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown(f"""
        <div class="savings-card">
        📉 Saving Percentage: {savings_pct:.1f}%
        </div>
    """, unsafe_allow_html=True)

# —— Visual Charts ——
st.markdown("### 🌐 Visual Comparison")

# Only show one chart - the simpler matplotlib one
fig, ax = plt.subplots(figsize=(10, 5))
# Set transparent background
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)

labels = ['Human', 'AI']
costs = [cost_per_eff_hour, ai_hourly]
colors = ['#FF6B6B', '#4D96FF']

bars = ax.bar(labels, costs, color=colors, width=0.6, edgecolor='#FF6700', linewidth=2)

# Add cost labels in the middle of the bars with larger text
for i, bar in enumerate(bars):
    height = bar.get_height()
    # Centered cost values with larger font
    ax.text(bar.get_x() + bar.get_width()/2, height/2,
            f"${height:.2f}",
            ha='center', va='center',
            fontsize=16, fontweight='bold', color='white')

mid_y = (costs[0] + costs[1]) / 2
ax.annotate(f"Savings:\n${savings_per_hour:.2f}\n({savings_pct:.1f}%)",
            xy=(0.5, mid_y),
            xytext=(0.5, mid_y + 10),
            ha='center', va='center',
            fontsize=14, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", fc="lightgreen", ec="green", lw=2))

ax.set_ylabel("Cost per Effective Hour ($)", fontsize=14)
ax.set_ylim(0, max(costs[0], costs[1]) * 1.3)
ax.set_title("Cost Comparison: Human vs AI", fontsize=18, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Set text color to white for better visibility
ax.title.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white', labelsize=14)
ax.tick_params(axis='y', colors='white', labelsize=14)
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')

st.pyplot(fig)

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
    st.markdown(f"""
        <div class="projection-card">
            <h4 class="projection-title">Daily</h4>
            <p class="projection-value">
                <span style='color:#FF6B6B;'>Human: ${cost_day:.2f}</span><br>
                <span style='color:#4D96FF;'>AI: ${ai_hourly * hours_day:.2f}</span><br>
                <span style='color:#C8E6C9;'>Savings: ${savings_per_hour * hours_day:.2f}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

with proj2:
    st.markdown(f"""
        <div class="projection-card">
            <h4 class="projection-title">Monthly (22 days)</h4>
            <p class="projection-value">
                <span style='color:#FF6B6B;'>Human: ${monthly_human_cost:.2f}</span><br>
                <span style='color:#4D96FF;'>AI: ${monthly_ai_cost:.2f}</span><br>
                <span style='color:#C8E6C9;'>Savings: ${monthly_savings:.2f}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

with proj3:
    st.markdown(f"""
        <div class="projection-card">
            <h4 class="projection-title">Yearly</h4>
            <p class="projection-value">
                <span style='color:#FF6B6B;'>Human: ${yearly_human_cost:,.2f}</span><br>
                <span style='color:#4D96FF;'>AI: ${yearly_ai_cost:,.2f}</span><br>
                <span style='color:#C8E6C9;'>Savings: ${yearly_savings:,.2f}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

# —— Footer ——
st.markdown("---")
st.caption("AI vs Human Cost Calculator by ConnexUS. Built with Streamlit & Plotly.")
