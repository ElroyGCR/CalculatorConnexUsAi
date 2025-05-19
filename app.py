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

# —— CSS Styling ——
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
    
    /* Section headings */
    .section-heading {
        color: #00FFAA;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        padding-left: 10px;
        border-left: 4px solid #FF6700;
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

# —— Breakdown Table ——
st.markdown("<div class='section-heading'>📊 Breakdown Table</div>", unsafe_allow_html=True)

# Create a cleaner table with borders and exact styling from the screenshot, but without the last two rows
table_html = f"""
<div style="display: flex; justify-content: center; margin-bottom: 30px;">
  <table style="background-color: rgba(0, 0, 0, 0.2); border-collapse: collapse; width: 80%; border: 1px solid #333;">
    <tr style="border-bottom: 1px solid #333;">
      <th style="padding: 12px; text-align: left; color: #00FFAA; border-right: 1px solid #333;"></th>
      <th style="padding: 12px; text-align: center; color: #00FFAA; border-right: 1px solid #333;">Human</th>
      <th style="padding: 12px; text-align: center; color: #00FFAA;">AI</th>
    </tr>
    <tr style="border-bottom: 1px solid #333;">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #333;">Cost per minute</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #333;">${human_hourly/60:.2f}</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">${ai_cost_per_minute:.2f}</td>
    </tr>
    <tr style="border-bottom: 1px solid #333;">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #333;">Hourly Rate</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #333;">${human_hourly:.2f}</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">${ai_hourly:.2f}</td>
    </tr>
    <tr style="border-bottom: 1px solid #333;">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #333;">Working hours per day</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #333;">{hours_day}</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">{hours_day}</td>
    </tr>
    <tr style="border-bottom: 1px solid #333;">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #333;">Utilization</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #333;">{efficiency*100:.0f}%</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">100%</td>
    </tr>
    <tr style="border-bottom: 1px solid #333;">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #333;">Cost per day</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #333;">${cost_day:.2f}</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">${ai_hourly * hours_day:.2f}</td>
    </tr>
    <tr style="border-bottom: 1px solid #333;">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #333;">Effective hours worked</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #333;">{worked_hours:.2f}</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">{hours_day}</td>
    </tr>
    <tr>
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #333;">Cost per effective hour</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #333;">${cost_per_eff_hour:.2f}</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">${ai_hourly:.2f}</td>
    </tr>
  </table>
</div>
"""
st.markdown(table_html, unsafe_allow_html=True)

# —— Visual Comparison - Centered and Smaller ——
st.markdown("<div class='section-heading'>🌐 Visual Comparison</div>", unsafe_allow_html=True)

# Create a centered container for the chart
st.markdown("""
<div style="display: flex; justify-content: center; align-items: center;">
    <div style="width: 75%;">
        <div id="chart-container"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Create a smaller, centered chart
fig, ax = plt.subplots(figsize=(8, 5))
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
            fontsize=20, fontweight='bold', color='white')

mid_y = (costs[0] + costs[1]) / 2
ax.annotate(f"Savings:\n${savings_per_hour:.2f}\n({savings_pct:.1f}%)",
            xy=(0.5, (costs[0] + costs[1])/1.5),
            xytext=(0.5, costs[0] * 0.8),
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

# —— Savings Row ———
st.markdown("<div class='section-heading'>💰 Savings Summary</div>", unsafe_allow_html=True)
s1, s2 = st.columns(2)
with s1:
    st.markdown(f"""
        <div style="background-color: rgba(30, 70, 32, 0.8); padding: 20px; border-radius: 12px; font-size: 28px; font-weight: 700; color: #C8E6C9; margin-bottom: 20px; text-align: center;">
        💵 Saving per Hour: ${savings_per_hour:.2f}
        </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown(f"""
        <div style="background-color: rgba(30, 70, 32, 0.8); padding: 20px; border-radius: 12px; font-size: 28px; font-weight: 700; color: #C8E6C9; margin-bottom: 20px; text-align: center;">
        📉 Saving Percentage: {savings_pct:.1f}%
        </div>
    """, unsafe_allow_html=True)

# Add monthly and yearly projections
st.markdown("<div class='section-heading'>📆 Cost Projections</div>", unsafe_allow_html=True)
days_month = 22  # Average working days per month
months_year = 12

# Calculate projections
monthly_human_cost = cost_day * days_month
monthly_ai_cost = ai_hourly * hours_day * days_month
monthly_savings = (savings_per_hour * hours_day) * days_month

yearly_human_cost = monthly_human_cost * months_year
yearly_ai_cost = monthly_ai_cost * months_year
yearly_savings = monthly_savings * months_year

# Create columns for projections with transparent backgrounds
proj1, proj2, proj3 = st.columns(3)

with proj1:
    st.markdown(f"""
        <div style="background-color: rgba(42, 62, 104, 0.8); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
            <h4 style="color: #8BB8F8; margin: 0; font-size: 18px; font-weight: bold;">Daily</h4>
            <p style="font-size: 22px; margin: 10px 0 5px;">
                <span style='color:#FF6B6B;'>Human: ${cost_day:.2f}</span><br>
                <span style='color:#4D96FF;'>AI: ${ai_hourly * hours_day:.2f}</span><br>
                <span style='color:#C8E6C9;'>Savings: ${savings_per_hour * hours_day:.2f}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

with proj2:
    st.markdown(f"""
        <div style="background-color: rgba(42, 62, 104, 0.8); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
            <h4 style="color: #8BB8F8; margin: 0; font-size: 18px; font-weight: bold;">Monthly (22 days)</h4>
            <p style="font-size: 22px; margin: 10px 0 5px;">
                <span style='color:#FF6B6B;'>Human: ${monthly_human_cost:.2f}</span><br>
                <span style='color:#4D96FF;'>AI: ${monthly_ai_cost:.2f}</span><br>
                <span style='color:#C8E6C9;'>Savings: ${monthly_savings:.2f}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

with proj3:
    st.markdown(f"""
        <div style="background-color: rgba(42, 62, 104, 0.8); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
            <h4 style="color: #8BB8F8; margin: 0; font-size: 18px; font-weight: bold;">Yearly</h4>
            <p style="font-size: 22px; margin: 10px 0 5px;">
                <span style='color:#FF6B6B;'>Human: ${yearly_human_cost:,.2f}</span><br>
                <span style='color:#4D96FF;'>AI: ${yearly_ai_cost:,.2f}</span><br>
                <span style='color:#C8E6C9;'>Savings: ${yearly_savings:,.2f}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

# —— Footer ——
st.markdown("---")
st.caption("AI vs Human Cost Calculator by ConnexUS. Built with Streamlit & Plotly.")
