import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --yellow:       #F5C400;
        --yellow-light: #FFF4B8;
        --yellow-dark:  #C49A00;
        --black:        #0A0A0A;
        --dark1:        #111111;
        --dark2:        #1A1A1A;
        --dark3:        #222222;
        --dark4:        #2E2E2E;
        --gray:         #888888;
        --gray-light:   #CCCCCC;
        --white:        #F5F5F5;
        --green:        #22C55E;
        --red:          #EF4444;
        --orange:       #F97316;
        --blue:         #3B82F6;
        --purple:       #A855F7;
        --teal:         #14B8A6;
        --font-main:    'Syne', sans-serif;
        --font-mono:    'JetBrains Mono', monospace;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: var(--black) !important;
        color: var(--white) !important;
        font-family: var(--font-main) !important;
    }

    [data-testid="stAppViewContainer"] {
        background: radial-gradient(ellipse at top left, #1A1500 0%, var(--black) 60%) !important;
    }

    [data-testid="stSidebar"] {
        background: var(--dark1) !important;
        border-right: 1px solid #2A2A00 !important;
    }
    [data-testid="stSidebar"] * { color: var(--gray-light) !important; }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: var(--yellow) !important; }

    .main-header {
        background: linear-gradient(135deg, #1A1500 0%, #0D0D00 60%, #0A0A0A 100%);
        border: 1px solid #3A3000;
        border-radius: 16px;
        padding: 32px 40px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 240px; height: 240px;
        background: radial-gradient(circle, rgba(245,196,0,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .header-badge {
        display: inline-block;
        background: rgba(245,196,0,0.12);
        border: 1px solid rgba(245,196,0,0.3);
        color: var(--yellow) !important;
        font-family: var(--font-mono) !important;
        font-size: 11px;
        letter-spacing: 3px;
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 14px;
    }
    .header-title {
        font-family: var(--font-main) !important;
        font-size: 38px;
        font-weight: 800;
        color: var(--white) !important;
        line-height: 1.1;
        margin: 0 0 6px;
    }
    .header-title span { color: var(--yellow) !important; }
    .header-subtitle {
        font-family: var(--font-mono) !important;
        font-size: 12px;
        color: var(--gray) !important;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }
    .header-tags { display: flex; flex-wrap: wrap; gap: 8px; }
    .header-tag {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        color: var(--gray-light) !important;
        font-family: var(--font-mono) !important;
        font-size: 11px;
        padding: 4px 12px;
        border-radius: 20px;
    }

    .form-card {
        background: var(--dark1);
        border: 1px solid #2A2A00;
        border-radius: 16px;
        padding: 28px 24px;
        margin-bottom: 16px;
    }
    .form-section-title {
        font-family: var(--font-mono) !important;
        font-size: 10px;
        letter-spacing: 3px;
        color: var(--yellow) !important;
        text-transform: uppercase;
        margin-bottom: 16px;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        background: var(--dark2) !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        color: var(--white) !important;
        font-family: var(--font-main) !important;
    }
    label, .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: var(--gray-light) !important;
        font-family: var(--font-main) !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    .stButton > button {
        background: var(--yellow) !important;
        color: var(--black) !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: var(--font-main) !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        padding: 14px 28px !important;
        width: 100% !important;
        letter-spacing: 0.5px !important;
        transition: all 0.2s !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background: #FFD700 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 24px rgba(245,196,0,0.35) !important;
    }

    .reset-btn > button {
        background: var(--dark3) !important;
        color: var(--gray-light) !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        border: 1px solid #333 !important;
        padding: 10px !important;
    }

    .agent-log-card {
        background: var(--dark1);
        border: 1px solid #2A2A00;
        border-radius: 16px;
        padding: 24px;
        margin-top: 16px;
    }
    .agent-log-title {
        font-family: var(--font-mono) !important;
        font-size: 10px;
        letter-spacing: 3px;
        color: var(--yellow) !important;
        text-transform: uppercase;
        margin-bottom: 16px;
    }
    .agent-step {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 6px;
    }
    .agent-step.done    { background: rgba(34,197,94,0.06);  border: 1px solid rgba(34,197,94,0.15); }
    .agent-step.running { background: rgba(245,196,0,0.06);  border: 1px solid rgba(245,196,0,0.2); }
    .agent-step.pending { background: rgba(255,255,255,0.02);border: 1px solid rgba(255,255,255,0.06); opacity:0.4; }
    .step-icon  { font-size: 18px; width: 28px; text-align: center; flex-shrink: 0; }
    .step-label { font-size: 13px; color: var(--gray-light) !important; flex: 1; }
    .step-value { font-family: var(--font-mono) !important; font-size: 11px; }
    .step-value.done    { color: var(--green)  !important; }
    .step-value.running { color: var(--yellow) !important; }
    .step-value.pending { color: var(--gray)   !important; }

    .verdict-banner {
        border-radius: 16px;
        padding: 28px 24px;
        text-align: center;
        margin-bottom: 16px;
    }
    .verdict-banner.buy-abroad {
        background: linear-gradient(135deg, #052010 0%, #0A2A18 100%);
        border: 2px solid var(--green);
        box-shadow: 0 0 40px rgba(34,197,94,0.12);
    }
    .verdict-banner.buy-local {
        background: linear-gradient(135deg, #1A0505 0%, #2A0A0A 100%);
        border: 2px solid var(--red);
        box-shadow: 0 0 40px rgba(239,68,68,0.12);
    }
    .verdict-banner.close-call {
        background: linear-gradient(135deg, #1A1500 0%, #2A2000 100%);
        border: 2px solid var(--yellow);
        box-shadow: 0 0 40px rgba(245,196,0,0.12);
    }
    .verdict-emoji  { font-size: 52px; margin-bottom: 10px; display: block; }
    .verdict-label  { font-family: var(--font-mono) !important; font-size: 10px; letter-spacing: 3px; color: var(--gray) !important; margin-bottom: 6px; text-transform: uppercase; }
    .verdict-text   { font-family: var(--font-main) !important; font-size: 26px; font-weight: 800; margin-bottom: 8px; }
    .verdict-text.green  { color: var(--green)  !important; }
    .verdict-text.red    { color: var(--red)    !important; }
    .verdict-text.yellow { color: var(--yellow) !important; }
    .verdict-savings  { font-size: 14px; color: var(--gray-light) !important; }
    .verdict-delivery { font-family: var(--font-mono) !important; font-size: 11px; color: var(--gray) !important; margin-top: 8px; }

    .breakdown-card {
        background: var(--dark1);
        border: 1px solid #2A2A00;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .breakdown-title {
        font-family: var(--font-mono) !important;
        font-size: 10px;
        letter-spacing: 3px;
        color: var(--yellow) !important;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .total-row {
        background: rgba(245,196,0,0.06);
        border: 1px solid rgba(245,196,0,0.2);
        border-radius: 10px;
        padding: 14px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 12px;
    }
    .total-label { font-size: 14px; font-weight: 700; color: var(--white) !important; }
    .total-value { font-family: var(--font-mono) !important; font-size: 24px; font-weight: 700; color: var(--yellow) !important; }
    .india-row {
        background: rgba(34,197,94,0.05);
        border: 1px solid rgba(34,197,94,0.15);
        border-radius: 10px;
        padding: 12px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 8px;
    }
    .india-label { font-size: 14px; color: var(--gray-light) !important; }
    .india-value { font-family: var(--font-mono) !important; font-size: 20px; font-weight: 700; color: var(--green) !important; }

    .restriction-box {
        background: rgba(239,68,68,0.06);
        border: 1px solid rgba(239,68,68,0.3);
        border-left: 4px solid var(--red);
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 16px;
        display: flex;
        gap: 14px;
        align-items: flex-start;
    }
    .restriction-icon  { font-size: 22px; flex-shrink: 0; }
    .restriction-title { font-size: 14px; font-weight: 700; color: var(--red) !important; margin-bottom: 4px; }
    .restriction-text  { font-size: 12px; color: var(--gray-light) !important; line-height: 1.6; }

    .safe-box {
        background: rgba(34,197,94,0.05);
        border: 1px solid rgba(34,197,94,0.2);
        border-left: 4px solid var(--green);
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 16px;
        display: flex;
        gap: 14px;
        align-items: center;
    }
    .safe-text { font-size: 13px; color: var(--green) !important; font-weight: 600; }

    .ai-box {
        background: rgba(59,130,246,0.05);
        border: 1px solid rgba(59,130,246,0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .ai-box-title {
        font-family: var(--font-mono) !important;
        font-size: 10px;
        letter-spacing: 3px;
        color: #60A5FA !important;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .ai-text { font-size: 14px; color: var(--gray-light) !important; line-height: 1.8; }

    .duty-table { width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 8px; }
    .duty-table th {
        background: rgba(245,196,0,0.1);
        color: var(--yellow) !important;
        font-family: var(--font-mono) !important;
        font-size: 9px;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 8px 10px;
        text-align: left;
    }
    .duty-table td { padding: 8px 10px; color: var(--gray-light) !important; border-bottom: 1px solid rgba(255,255,255,0.04); }
    .duty-table tr:last-child td { border-bottom: none; }
    .rate-badge { font-family: var(--font-mono) !important; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: 600; }
    .rate-high   { background: rgba(239,68,68,0.15);  color: var(--red)    !important; }
    .rate-medium { background: rgba(249,115,22,0.15); color: var(--orange) !important; }
    .rate-low    { background: rgba(34,197,94,0.15);  color: var(--green)  !important; }
    .rate-zero   { background: rgba(255,255,255,0.08);color: var(--gray-light) !important; }
    .restrict-yes { color: var(--red)   !important; font-weight: 700; font-size: 11px; }
    .restrict-no  { color: var(--green) !important; font-size: 11px; }

    .placeholder-box {
        border: 2px dashed #2A2A00;
        border-radius: 20px;
        padding: 60px 32px;
        text-align: center;
        background: rgba(245,196,0,0.02);
        min-height: 420px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .placeholder-icon  { font-size: 56px; margin-bottom: 16px; }
    .placeholder-title { font-size: 20px; font-weight: 700; color: var(--white) !important; margin-bottom: 10px; }
    .placeholder-desc  { font-size: 14px; color: var(--gray) !important; line-height: 1.7; margin-bottom: 24px; }
    .placeholder-features { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; max-width: 340px; }
    .feat-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 12px;
        color: var(--gray-light) !important;
        text-align: left;
    }

    [data-testid="metric-container"] {
        background: var(--dark2);
        border: 1px solid #2A2A00;
        border-radius: 12px;
        padding: 16px !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        color: var(--gray) !important;
        font-family: var(--font-mono) !important;
        font-size: 11px !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: var(--yellow) !important;
        font-family: var(--font-mono) !important;
    }

    hr { border-color: #222 !important; margin: 20px 0 !important; }
    #MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
    .stSpinner > div { border-top-color: var(--yellow) !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--dark1); }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)