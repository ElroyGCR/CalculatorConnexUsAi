import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO

# —— Page Setup ——
st.set_page_config(page_title="AI vs Human ROI Calculator", layout="wide")

# —— Load Logo & Watermark ——
def load_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# Paths to logo and watermark
logo_path = "connexus_logo.png"
watermark_path = "connexus_logo_watermark.png"

# Watermark CSS injection
watermark_b64 = load_base64_image(watermark_path)
if watermark_b64:
    st.markdown(f"""
        <style>
        .watermark {{
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 600px;
          height: 600px;
          opacity: 0.05;
          background: url("data:image/png;base64,{watermark_b64}") no-repeat center/contain;
          pointer-events: none;
          z-index: 0;
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
        <div style='text-align:center; margin-bottom: 20px;'>
            <img src='data:image/png;base64,{logo_b64}' style='max-height: 50px; width: auto;'>
        </div>
    """, unsafe_allow_html=True)

# —— Sidebar Inputs ——
st.sidebar.header("🔧 Input Parameters")
human_hourly = st.sidebar.number_input("Human Hourly Rate ($)", value=19.5, min_value=0.0)
hours_day = st.sidebar.number_input("Working Hours per Day", value=8.0, min_value=0.0)
efficiency = st.sidebar.slider("Human Agent Utilization (%)", min_value=0, max_value=100, value=65) / 100
ai_cost_per_minute = st.sidebar.number_input("AI Cost per Minute ($)", value=0.35, min_value=0.0)

# —— Core Calculations ——
ai_hourly = ai_cost_per_minute * 60
cost_day = human_hourly * hours_day
worked_hours = hours_day * efficiency
cost_per_eff_hour = cost_day / worked_hours if worked_hours else float('inf')
savings_per_hour = cost_per_eff_hour - ai_hourly
savings_pct = (savings_per_hour / cost_per_eff_hour * 100) if cost_per_eff_hour else 0

# —— Savings Row ———
st.markdown("### 💰 Savings Summary")
s1, s2 = st.columns(2)
with s1:
    st.markdown("""
        <div style='background-color:#1E4620; padding: 20px; border-radius:12px; font-size:28px; font-weight:700; color:#C8E6C9;'>
        💵 Saving per Hour: ${:.2f}
        </div>
    """.format(savings_per_hour), unsafe_allow_html=True)
with s2:
    st.markdown("""
        <div style='background-color:#1E4620; padding: 20px; border-radius:12px; font-size:28px; font-weight:700; color:#C8E6C9;'>
        📉 Saving Percentage: {:.1f}%
        </div>
    """.format(savings_pct), unsafe_allow_html=True)

# —— Visual Charts ——
st.markdown("### 🌐 Visual Comparison")
labels = ['Human', 'AI']
costs = [cost_per_eff_hour, ai_hourly]
colors = ['#FF6B6B', '#4D96FF']

fig, ax = plt.subplots(figsize=(6, 4), facecolor='none')
bars = ax.bar(labels, costs, color=colors, width=0.6, edgecolor='black')

for bar in bars:
    height = bar.get_height()
    ax.annotate(f"${height:.2f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 8),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=10, weight='bold')

mid_y = (costs[0] + costs[1]) / 2
ax.annotate(f"Savings:\n${savings_per_hour:.2f}\n({savings_pct:.1f}%)",
            xy=(0.5, mid_y),
            xytext=(0.5, mid_y + 10),
            ha='center', va='center',
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", fc="lightgreen", ec="green", lw=2))

ax.set_facecolor('none')
fig.patch.set_facecolor('none')
ax.set_ylabel("Cost per Effective Hour ($)")
ax.set_ylim(0, max(costs[0], costs[1]) * 1.3)
ax.set_title("Cost Comparison: Human vs AI", fontsize=14, weight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

# —— Footer ——
st.markdown("---")
st.caption("AI vs Human Cost Calculator by ConnexUS. Built with Streamlit & Plotly.")
