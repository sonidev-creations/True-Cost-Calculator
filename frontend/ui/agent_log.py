import streamlit as st
import time

AGENT_STEPS = [
    ("currency",      "🌐", "Fetching live USD → INR rate"),
    ("scraping",      "🕷️",  "Extracting product details from URL"),
    ("hsn_lookup",    "📋", "Looking up HSN code & duty category"),
    ("duty_calc",     "🏛️",  "Calculating BCD + SWS + IGST"),
    ("restrictions",  "⚠️",  "Checking import restrictions"),
    ("price_compare", "🔍", "Searching Amazon India / Flipkart"),
    ("ai_reasoning",  "🤖", "AGENT AI generating recommendation"),
]


def render_agent_log(steps_data=None):
    st.markdown("""
    <div class="agent-log-card">
        <div class="agent-log-title">⚙️ &nbsp; AI AGENT PIPELINE — LIVE</div>
    """, unsafe_allow_html=True)

    if steps_data:
        _render_from_data(steps_data)
    else:
        _render_animated()

    st.markdown("</div>", unsafe_allow_html=True)


def _render_from_data(steps_data):
    step_map = {s["step"]: s for s in steps_data}
    for key, icon, label in AGENT_STEPS:
        step   = step_map.get(key, {})
        status = step.get("status", "pending")
        msg    = step.get("message", "")

        if status == "done":
            html_val = f'<span class="step-value done">✅ {msg}</span>'
            css      = "done"
        elif status == "running":
            html_val = f'<span class="step-value running">⏳ {msg}</span>'
            css      = "running"
        else:
            html_val = '<span class="step-value pending">—</span>'
            css      = "pending"

        st.markdown(f"""
        <div class="agent-step {css}">
            <span class="step-icon">{icon}</span>
            <span class="step-label">{label}</span>
            {html_val}
        </div>
        """, unsafe_allow_html=True)


def _render_animated():
    placeholders = []
    for key, icon, label in AGENT_STEPS:
        ph = st.empty()
        ph.markdown(f"""
        <div class="agent-step pending">
            <span class="step-icon">{icon}</span>
            <span class="step-label">{label}</span>
            <span class="step-value pending">waiting...</span>
        </div>
        """, unsafe_allow_html=True)
        placeholders.append((ph, icon, label))

    for ph, icon, label in placeholders:
        ph.markdown(f"""
        <div class="agent-step running">
            <span class="step-icon">{icon}</span>
            <span class="step-label">{label}</span>
            <span class="step-value running">running...</span>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.5)
        ph.markdown(f"""
        <div class="agent-step done">
            <span class="step-icon">{icon}</span>
            <span class="step-label">{label}</span>
            <span class="step-value done">✅ done</span>
        </div>
        """, unsafe_allow_html=True)