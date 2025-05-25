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
    
    /* Chart container styling for better fit */
    .chart-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        max-height: 50vh;
        margin: 20px 0;
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
efficiency = st.sidebar.slider("Human Agent Utilization (%)", min_value=0, max_value=100, value=65, step=5) / 100

# Add AI Automation slider
automation_pct = st.sidebar.slider("AI Automation Level (%)", min_value=0, max_value=100, value=50, step=5) / 100

# Replace the AI cost per minute slider with a dropdown
ai_tier_data = {
    "Tier 1 (1,000-4,999 min) - $0.25": {"client_rate": 0.25, "ai_telephony": 0.20, "mgmt_fee": 0.05},
    "Tier 2 (5,000-9,999 min) - $0.22": {"client_rate": 0.22, "ai_telephony": 0.18, "mgmt_fee": 0.04},
    "Tier 3 (10,000-24,999 min) - $0.18": {"client_rate": 0.18, "ai_telephony": 0.15, "mgmt_fee": 0.03},
    "Tier 4 (25,000-49,999 min) - $0.16": {"client_rate": 0.16, "ai_telephony": 0.14, "mgmt_fee": 0.02},
    "Tier 5 (≥50,000 min) - $0.14": {"client_rate": 0.14, "ai_telephony": 0.12, "mgmt_fee": 0.02}
}

selected_tier = st.sidebar.selectbox("AI Cost per Minute", list(ai_tier_data.keys()), index=2)  # Default to Tier 3
ai_cost_per_minute = ai_tier_data[selected_tier]["client_rate"]

# —— Core Calculations ——
ai_hourly = ai_cost_per_minute * 60
cost_day = human_hourly * hours_day
worked_hours = hours_day * efficiency

# Calculate blended cost based on automation level
human_portion = 1 - automation_pct  # Percentage still handled by humans
ai_portion = automation_pct  # Percentage handled by AI

# Blended hourly cost calculation
cost_per_eff_hour = cost_day / worked_hours if worked_hours > 0 else 0
blended_hourly_cost = (human_portion * cost_per_eff_hour) + (ai_portion * ai_hourly)

# Calculate savings comparing 100% human vs blended approach
savings_per_hour = cost_per_eff_hour - blended_hourly_cost
savings_pct = (savings_per_hour / cost_per_eff_hour * 100) if cost_per_eff_hour > 0 else 0

# —— Breakdown Table ——
st.markdown("<div class='section-heading'>📊 Breakdown Table</div>", unsafe_allow_html=True)

# Create a cleaner, prettier table with better styling
table_html = f"""
<div style="display: flex; justify-content: center; margin-bottom: 30px;">
  <table style="background-color: rgba(0, 0, 0, 0.2); border-collapse: collapse; width: 80%; border: 2px solid #333; border-radius: 4px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    <tr style="border-bottom: 2px solid #333; background-color: rgba(0, 0, 0, 0.3);">
      <th style="padding: 14px; text-align: left; color: #00FFAA; border-right: 1px solid #444; font-size: 18px;"></th>
      <th style="padding: 14px; text-align: center; color: #00FFAA; border-right: 1px solid #444; font-size: 18px;">Human</th>
      <th style="padding: 14px; text-align: center; color: #00FFAA; font-size: 18px;">AI</th>
    </tr>
    <tr style="border-bottom: 1px solid #333; transition: background-color 0.2s;">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #444; font-weight: 500;">Cost per minute</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #444;">${human_hourly/60:.2f}</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">${ai_cost_per_minute:.2f}</td>
    </tr>
    <tr style="border-bottom: 1px solid #333; background-color: rgba(0, 0, 0, 0.1);">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #444; font-weight: 500;">Hourly Rate</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #444;">${human_hourly:.2f}</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">${ai_hourly:.2f}</td>
    </tr>
    <tr style="border-bottom: 1px solid #333;">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #444; font-weight: 500;">Working hours per day</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #444;">{hours_day}</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">{hours_day}</td>
    </tr>
    <tr style="border-bottom: 1px solid #333; background-color: rgba(0, 0, 0, 0.1);">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #444; font-weight: 500;">Utilization</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #444;">{efficiency*100:.0f}%</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">100%</td>
    </tr>
    <tr style="border-bottom: 1px solid #333;">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #444; font-weight: 500;">Cost per day</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #444;">${cost_day:.2f}</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">${ai_hourly * hours_day:.2f}</td>
    </tr>
    <tr style="border-bottom: 1px solid #333; background-color: rgba(0, 0, 0, 0.1);">
      <td style="padding: 12px; text-align: left; color: #EEE; border-right: 1px solid #444; font-weight: 500;">Effective hours worked</td>
      <td style="padding: 12px; text-align: center; color: #EEE; border-right: 1px solid #444;">{worked_hours:.2f}</td>
      <td style="padding: 12px; text-align: center; color: #EEE;">{hours_day}</td>
    </tr>
    <tr style="background-color: rgba(0,0,0,0.2);">
      <td style="padding: 14px; text-align: left; color: #EEE; border-right: 1px solid #444; font-weight: bold;">Cost per effective hour</td>
      <td style="padding: 14px; text-align: center; color: #EEE; border-right: 1px solid #444; font-weight: bold; font-size: 18px;">${cost_per_eff_hour:.2f}</td>
      <td style="padding: 14px; text-align: center; color: #EEE; font-weight: bold; font-size: 18px;">${ai_hourly:.2f}</td>
    </tr>
  </table>
</div>
"""
st.markdown(table_html, unsafe_allow_html=True)

# —— Visual Comparison - Properly Sized for 15.6" Screen ——
st.markdown("<div class='section-heading'>🌐 Visual Comparison</div>", unsafe_allow_html=True)

# Create a container that fits well on a 15.6" screen
col1, col2, col3 = st.columns([1, 2, 1])  # Center the chart with padding on sides

with col2:
    # Create appropriately sized chart for 15.6" screen (about 75% of screen height)
    fig, ax = plt.subplots(figsize=(8, 6))  # Adjusted size for better fit
    # Set transparent background
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    labels = ['100% Human', f'{human_portion*100:.0f}% Human +\n{ai_portion*100:.0f}% AI']
    costs = [cost_per_eff_hour, blended_hourly_cost]
    colors = ['#FF6B6B', '#4D96FF']

    bars = ax.bar(labels, costs, color=colors, width=0.6, edgecolor='#FF6700', linewidth=2)

    # Add cost labels in the middle of the bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        # Centered cost values
        ax.text(bar.get_x() + bar.get_width()/2, height/2,
                f"${height:.2f}",
                ha='center', va='center',
                fontsize=16, fontweight='bold', color='white')

    # Position savings box between the bars
    if len(bars) >= 2:
        savings_x = (bars[0].get_x() + bars[0].get_width() + bars[1].get_x()) / 2
        savings_y = max(costs) * 0.8
        
        ax.annotate(f"Savings:\n${savings_per_hour:.2f}\n({savings_pct:.1f}%)",
                    xy=(savings_x, savings_y),
                    ha='center', va='center',
                    fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.5", fc="#90EE90", ec="#228B22", lw=2))

    # Styling improvements
    ax.set_ylabel("Cost per Effective Hour ($)", fontsize=14)
    ax.set_ylim(0, max(costs[0], costs[1]) * 1.1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_axisbelow(True)

    # Set text color to white for better visibility
    ax.tick_params(axis='x', colors='white', labelsize=12)
    ax.tick_params(axis='y', colors='white', labelsize=11)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.yaxis.label.set_color('white')

    # Improve spacing
    plt.tight_layout()
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
days_month = 22  # Average working days per month
months_year = 12

# Calculate projections for blended approach
monthly_human_cost = cost_day * days_month
monthly_blended_cost = blended_hourly_cost * hours_day * days_month
monthly_savings = (savings_per_hour * hours_day) * days_month

yearly_human_cost = monthly_human_cost * months_year
yearly_blended_cost = monthly_blended_cost * months_year
yearly_savings = monthly_savings * months_year

# Create columns for projections with transparent backgrounds
proj1, proj2, proj3 = st.columns(3)

with proj1:
    st.markdown(f"""
        <div style="background-color: rgba(42, 62, 104, 0.8); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
            <h4 style="color: #8BB8F8; margin: 0; font-size: 18px; font-weight: bold;">Daily</h4>
            <p style="font-size: 22px; margin: 10px 0 5px;">
                <span style='color:#C8E6C9;'>Savings: ${savings_per_hour * hours_day:.2f}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

with proj2:
    st.markdown(f"""
        <div style="background-color: rgba(42, 62, 104, 0.8); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
            <h4 style="color: #8BB8F8; margin: 0; font-size: 18px; font-weight: bold;">Monthly</h4>
            <p style="font-size: 22px; margin: 10px 0 5px;">
                <span style='color:#C8E6C9;'>Savings: ${monthly_savings:.2f}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

with proj3:
    st.markdown(f"""
        <div style="background-color: rgba(42, 62, 104, 0.8); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
            <h4 style="color: #8BB8F8; margin: 0; font-size: 18px; font-weight: bold;">Yearly</h4>
            <p style="font-size: 22px; margin: 10px 0 5px;">
                <span style='color:#C8E6C9;'>Savings: ${yearly_savings:,.2f}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

# —— Footer ——
st.markdown("---")

# ─── Improved FAQ Section - With Tabs for Organization ────────────────────
st.write("## Frequently Asked Questions")

# Simple text description with larger font
st.write("#### Common questions about AI automation and how it can benefit your contact center operations.")

# Use tabs to organize FAQs without nesting expanders
faq_tabs = st.tabs([
    "Why Choose AI", 
    "Cost Savings", 
    "Implementation", 
    "Capabilities",
    "Getting Started"
])

# Tab 1: Why Choose AI
with faq_tabs[0]:
    st.write("### Why Businesses Are Switching to AI Voice Agents")
    
    st.write("**What exactly is an AI Voice Representative?**")
    st.write("""
    AI Voice Representatives are cutting-edge virtual agents that revolutionize how businesses handle communications. They conduct remarkably natural phone conversations, answer complex questions, process requests, and deliver consistent excellence 24/7/365.
    
    Unlike human agents who need breaks, vacations, and sick days, our AI Voice Representatives work around the clock with zero downtime, zero turnover, and zero training requirements—transforming your customer service from a cost center into a competitive advantage.
    """)
    
    st.write("**How do AI Voice Agents differ from traditional IVR systems?**")
    st.write("""
    Unlike traditional IVR systems that force callers through rigid menu trees, our AI Voice Agents engage in natural conversations. They don't just recognize keywords—they understand intent, can handle complex inquiries, and provide personalized responses that sound human, creating a dramatically improved customer experience.
    """)

# Tab 2: Cost & Efficiency
with faq_tabs[1]:
    st.write("### Cost Savings & Operational Efficiency")
    
    st.write("**What kind of cost savings can I expect?**")
    st.write("""
    Businesses typically slash communication costs by 50-70% when implementing AI Voice Agents. Beyond the obvious savings on salaries and benefits, you'll eliminate costly overhead from:

    - Recruitment & Turnover Costs: No more spending thousands on hiring replacements for the average 30-45% annual call center attrition
    - Training Expenses: Eliminate the 2-6 weeks of paid training for each new agent
    - Absenteeism & No-Shows: The average call center loses 7-15% of scheduled hours to unexpected absences and no-shows
    - Management Overhead: Reduce supervisory staff needed for scheduling, quality monitoring, and performance management
    
    Use our ROI calculator above to see your specific savings potential.
    """)
    
    st.write("**How do AI Voice Agents improve operational efficiency?**")
    st.write("""
    Our AI Voice Agents transform your operation with:

    - 24/7/365 Availability: Never miss another call, even at 3 AM or during holidays
    - Infinite Scalability: Handle sudden call spikes without scrambling to staff up
    - Zero Ramp-Up Time: Deploy additional capacity instantly during seasonal peaks
    - Perfect Consistency: Every caller receives the same high-quality experience
    - Zero Burnout: Unlike humans, AI agents maintain peak performance regardless of call volume or complexity
    - Instant Knowledge Updates: New information is available across all AI agents simultaneously without training sessions
    """)
    
    st.write("**What happens to my business when calls go unanswered?**")
    st.write("""
    Every missed call is potentially thousands in lost revenue. Studies show:

    - 85% of customers whose calls go unanswered will not call back
    - 75% of callers will form a negative impression of your business from unanswered calls
    - The average missed sales call represents $1,200-$4,800 in lost potential revenue
    
    Our AI Voice Agents ensure every call is answered promptly, even during peak hours, nights, weekends, and holidays – capturing revenue that would otherwise be lost.
    """)

# Tab 3: Implementation & Integration
with faq_tabs[2]:
    st.write("### Implementation & Integration")
    
    st.write("**How long does it take to implement AI Voice Agents?**")
    st.write("""
    Implementation timelines depend on the specific product type you choose and your business requirements. Many of our solutions can be deployed rapidly with minimal setup time.
    
    Typical implementation timelines:
    - Basic phone automation: 2-3 weeks
    - Complex integrations: 4-8 weeks
    - Enterprise-wide deployment: 8-12 weeks
    
    We work closely with your team to ensure a smooth transition with minimal disruption to your operations.
    """)
    
    st.write("**Will AI Voice Agents integrate with my existing systems?**")
    st.write("""
    Absolutely! Our flexible integration framework connects with virtually any business system you're currently using. Whether it's a popular CRM like Salesforce, your proprietary databases, or legacy phone systems, we design custom integration pathways that make implementation smooth and non-disruptive.
    
    Our system works with:
    - All major CRM platforms (Salesforce, Microsoft Dynamics, HubSpot, etc.)
    - Custom databases and legacy systems
    - VoIP and traditional phone systems
    - Ticketing systems (Zendesk, ServiceNow, etc.)
    - Knowledge bases and information repositories
    """)

# Tab 4: Capabilities & Limitations
with faq_tabs[3]:
    st.write("### Capabilities & Customer Experience")
    
    st.write("**What types of calls can AI Voice Agents handle effectively?**")
    st.write("""
    Our AI Voice Agents excel at handling appointment scheduling, customer service inquiries, order status updates, product information requests, lead qualification, and routine transactions. They're particularly effective for high-volume, repetitive call types that follow predictable patterns.
    """)
    
    st.write("**How do AI Voice Agents handle complex or unusual customer requests?**")
    st.write("""
    Our AI Voice Agents are designed to recognize when a conversation exceeds their capabilities. In these situations, they seamlessly transfer the call to a human agent, providing a complete transcript and summary of the conversation so the human agent can pick up exactly where the AI left off—creating a smooth customer experience.
    """)
    
    st.write("**Can AI Voice Agents make outbound calls too?**")
    st.write("""
    Absolutely! Our AI Voice Agents can conduct outbound calling campaigns for appointment reminders, payment collection, satisfaction surveys, lead qualification, and promotional offers. They can reach hundreds of customers simultaneously with personalized conversations that drive results.
    """)
    
    st.write("**How natural do the AI Voice Agents sound?**")
    st.write("""
    Our advanced AI technology produces remarkably natural-sounding voices that many callers cannot distinguish from humans. The agents understand context, respond to emotional cues, adjust their tone appropriately, and can even insert thoughtful pauses and conversational fillers for an authentic experience.
    """)
    
    st.write("**What languages do your AI Voice Agents support?**")
    st.write("""
    Our AI Voice Agents currently support over 25 languages including English, Spanish, French, German, Italian, Portuguese, Mandarin, Japanese, and Arabic. Each language version maintains natural intonation and cultural nuances for an authentic experience regardless of region.
    """)

# Tab 5: Getting Started
with faq_tabs[4]:
    st.write("### Getting Started & Pricing")
    
    st.write("**How is pricing structured for AI Voice Agents?**")
    st.write("""
    Our pricing models are designed to provide predictability and transparency:

    - Monthly subscription based on usage volume
    - Per-minute rates for active AI conversation time
    - One-time implementation and integration fee
    
    Most clients see ROI within the first month of deployment. The calculator above demonstrates how the savings typically far exceed the investment.
    """)
    
    st.write("**What's the first step in getting started with AI Voice Agents?**")
    st.write("""
    The process begins with a consultation where we:
    
    1. Assess your current call operations
    2. Identify opportunities for AI implementation
    3. Provide a customized proposal with expected cost savings
    4. Create an implementation timeline
    5. Develop an integration plan for your existing systems
    
    We typically begin with a pilot program focused on a specific call type to demonstrate value before expanding to additional use cases.
    """)
    
    st.write("**How can I see your AI Voice Agents in action?**")
    st.write("""
    We offer several ways to experience our AI Voice Agents firsthand:
    
    - Live demonstration with your specific use cases
    - Sample recordings of AI conversations
    - Pilot program with limited scope to prove the concept
    - References from existing clients in your industry
    
    This gives you the opportunity to evaluate the technology with your own requirements before making a decision.
    """)

# Add some spacing at the bottom
st.write("")
