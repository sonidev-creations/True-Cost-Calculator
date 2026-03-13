import streamlit as st


def render_header():
    st.markdown("""
    <div class="main-header">
        <div class="header-badge">🛃 INDIA IMPORT INTELLIGENCE</div>
        <div class="header-title">
            <span>True Cost</span> Calculator
        </div>
        <div class="header-subtitle">
            CUSTOMS × DUTIES × GST × PRICE COMPARISON × IMPORT INTELLIGENCE
        </div>
        <div class="header-tags">
            <span class="header-tag">🇨🇳 AliExpress</span>
            <span class="header-tag">🇺🇸 Amazon US</span>
            <span class="header-tag">👗 SHEIN</span>
            <span class="header-tag">💊 iHerb</span>
            <span class="header-tag">🛒 eBay</span>
            <span class="header-tag">🏬 Walmart US</span>
        </div>
    </div>
    """, unsafe_allow_html=True)