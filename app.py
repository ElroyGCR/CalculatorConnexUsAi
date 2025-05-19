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
          top: 10px;
          left: 50%;
          transform: translateX(-50%);
          width: 800px;
          height: 800px;
          opacity: 0.08;
          background: url("data:image/png;base64,{watermark_b64}") no-repeat center/contain;
          pointer-events: none;
          z-index: -1;
        }}
        </style>
        <div class="watermark"></div>
    """, unsafe_allow_html=True)

# Logo in sidebar
logo_b64 = load_base64_image(logo_path)
if logo_b64:
    st.sidebar.markdown(f"""
        <div style='text-align:center;'>
            <img src='data:image/png;base64,{logo_b64}' style='height:80px;'>
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

# —— Metrics Layout ——
st.markdown("## 💼 AI vs Human Cost Breakdown")
st.markdown("### Metrics Summary")
st.markdown("<style>div.metric-block { background-color: rgba(0,0,0,0.25); padding: 15px; border-radius: 10px; margin-bottom: 10px; font-size: 20px; color: #00BFFF; }</style>", unsafe_allow_html=True)

cols = st.columns(2)
with cols[0]:
    st.markdown("<div class='metric-block'><b>Cost per Minute (Human)</b><br>${:.2f}</div>".format(human_hourly / 60), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Hourly Rate (Human)</b><br>${:.2f}</div>".format(human_hourly), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Working Hours per Day</b><br>{}</div>".format(hours_day), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Utilization (Human)</b><br>{:.0f}%</div>".format(efficiency*100), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Cost per Day (Human)</b><br>${:.2f}</div>".format(cost_day), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Effective Hours Worked</b><br>{:.2f}</div>".format(worked_hours), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Cost per Effective Hour</b><br>${:.2f}</div>".format(cost_per_eff_hour), unsafe_allow_html=True)

with cols[1]:
    st.markdown("<div class='metric-block'><b>Cost per Minute (AI)</b><br>${:.2f}</div>".format(ai_cost_per_minute), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Hourly Rate (AI)</b><br>${:.2f}</div>".format(ai_hourly), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Working Hours per Day</b><br>{}</div>".format(hours_day), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Utilization (AI)</b><br>100%</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Cost per Day (AI)</b><br>${:.2f}</div>".format(ai_hourly * hours_day), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Effective Hours Worked</b><br>{:.2f}</div>".format(hours_day), unsafe_allow_html=True)
    st.markdown("<div class='metric-block'><b>Cost per Effective Hour</b><br>${:.2f}</div>".format(ai_hourly), unsafe_allow_html=True)

# —— Savings Row ——
st.markdown("---")
st.markdown("### 💰 Savings Summary")
s1, s2 = st.columns(2)
with s1:
    st.success(f"💵 **Saving per Hour:** ${savings_per_hour:.2f}")
with s2:
    st.success(f"📉 **Saving Percentage:** {savings_pct:.1f}%")

# —— Visual Charts ——
st.markdown("---")
st.markdown("### 🌐 Visual Comparison")
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

mid_y = (costs[0] + costs[1]) / 2
ax.annotate(f"Savings:\n${savings_per_hour:.2f}\n({savings_pct:.1f}%)",
            xy=(0.5, mid_y),
            xytext=(0.5, mid_y + 10),
            ha='center', va='center',
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", fc="lightgreen", ec="green", lw=2))

ax.set_ylabel("Cost per Effective Hour ($)")
ax.set_ylim(0, max(costs[0], costs[1]) * 1.3)
ax.set_title("Cost Comparison: Human vs AI", fontsize=14, weight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

# —— Footer ——
st.markdown("---")
st.caption("AI vs Human Cost Calculator by ConnexUS. Built with Streamlit & Plotly.")
