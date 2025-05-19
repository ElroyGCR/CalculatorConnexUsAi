import streamlit as st
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="AI vs Human ROI Calculator", layout="wide")

# Sidebar: Input Parameters
with st.sidebar:
    st.markdown("## 🔧 Input Parameters")

    human_hourly_rate = st.number_input("Human Hourly Rate ($)", value=19.50, step=0.5, format="%.2f")
    working_hours_per_day = st.number_input("Working Hours per Day", value=8.0, step=0.5, format="%.2f")
    human_efficiency = st.slider("Human Agent Utilization (%)", min_value=0, max_value=100, value=40, step=5)
    ai_cost_per_minute = st.number_input("AI Cost per Minute ($)", value=0.35, step=0.01, format="%.2f")

# --- Calculations ---
ai_hourly_rate = ai_cost_per_minute * 60
effective_hours_worked = working_hours_per_day * (human_efficiency / 100)
human_cost_per_day = human_hourly_rate * working_hours_per_day
human_cost_per_effective_hour = (
    human_cost_per_day / effective_hours_worked if effective_hours_worked > 0 else 0
)
ai_cost_per_effective_hour = ai_hourly_rate
savings_per_hour = human_cost_per_effective_hour - ai_cost_per_effective_hour
savings_percentage = (
    (savings_per_hour / human_cost_per_effective_hour) * 100 if human_cost_per_effective_hour > 0 else 0
)

# Right column layout
left_col, right_col = st.columns([0.05, 0.95])

with right_col:
    # 📋 Assumptions Box
    with st.container():
        st.markdown("### 📋 Input Assumptions")
        st.markdown("---")
        st.markdown(f"**Human Hourly Rate:** ${human_hourly_rate:.2f}")
        st.markdown(f"**Working Hours per Day:** {working_hours_per_day}")
        st.markdown(f"**Human Utilization:** {human_efficiency}%")
        st.markdown(f"**AI Cost per Minute:** ${ai_cost_per_minute:.2f}")
        st.markdown(f"**AI Hourly Rate:** ${ai_hourly_rate:.2f}")

    st.markdown("---")  # Separator

    # 📊 Calculated Output Box
    with st.container():
        st.markdown("### 📊 Calculated Output")

        # Human Section
        st.subheader("🧍 Human Agent Stats")
        st.write(f"**Human Cost per Day:** ${human_cost_per_day:.2f}")
        st.write(f"**Effective Hours Worked:** {effective_hours_worked:.2f}")
        st.write(f"**Human Cost per Effective Hour:** ${human_cost_per_effective_hour:.2f}")

        # AI Section
        st.subheader("🤖 AI Agent Stats")
        st.write(f"**AI Cost per Effective Hour:** ${ai_cost_per_effective_hour:.2f}")

        # Savings Section
        st.subheader("💰 Savings")
        st.success(f"**Savings per Hour:** ${savings_per_hour:.2f}")
        st.success(f"**Savings Percentage:** {savings_percentage:.1f}%")

    st.markdown("---")

    # 🌐 Visual Comparison
    st.markdown("### 🌐 Visual Comparison")

    # Create visual bar comparison
    labels = ['Human', 'AI']
    costs = [human_cost_per_effective_hour, ai_cost_per_effective_hour]
    colors = ['#FF6B6B', '#4D96FF']

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, costs, color=colors, width=0.6, edgecolor='black')

    # Annotate bars with cost labels
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"${height:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 8),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10, weight='bold')

    # Add savings annotation
    mid_x = 0.5
    mid_y = (costs[0] + costs[1]) / 2
    ax.annotate(f"Savings:\n${savings_per_hour:.2f}\n({savings_percentage:.1f}%)",
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
