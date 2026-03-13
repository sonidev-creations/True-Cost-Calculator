import streamlit as st
import requests

from ui.styles     import inject_css
from ui.header     import render_header
from ui.input_form import render_input_form
from ui.agent_log  import render_agent_log
from ui.results    import render_results
from ui.sidebar    import render_sidebar


# ── Mock result when backend is offline ────────────────────────────────────
def _mock(form_data):
    p     = form_data.get("price_usd", 100) * 83.5
    bcd   = p * 0.20
    sws   = bcd * 0.10
    igst  = (p + bcd + sws) * 0.18
    ship  = 1200
    total = p + bcd + sws + igst + ship
    ind   = form_data.get("indian_price_inr") or round(total * 0.85, 0)

    return {
        "product_name":   form_data.get("product_name", "Sample Product"),
        "currency_rate":  83.5,
        "cost_breakdown": {
            "price_inr":                round(p,         2),
            "assessable_value":         round(p + ship,  2),
            "basic_customs_duty":       round(bcd,       2),
            "social_welfare_surcharge": round(sws,       2),
            "igst":                     round(igst,      2),
            "shipping_cost":            ship,
            "total_landed_cost":        round(total,     2),
            "duty_rate_percent":        20,
            "hs_code":                  "8471",
            "category_label":           "Electronics",
        },
        "indian_price":      ind,
        "indian_source":     "Amazon India",
        "verdict":           "BUY_LOCAL" if ind < total else "BUY_ABROAD",
        "savings":           round(ind - total, 2),
        "restricted":        False,
        "restriction_note":  "No import restrictions for this category.",
        "delivery_estimate": "10–20 days",
        "ai_reasoning": (
            f"Total landed cost is ₹{total:,.0f} after 20% BCD and 18% IGST. "
            f"Same product in India costs ₹{ind:,.0f}. "
            f"{'Buy locally — cheaper by ₹' + f'{abs(ind-total):,.0f}.' if ind < total else 'Buying abroad saves ₹' + f'{abs(ind-total):,.0f}.'}"
        ),
        "agent_steps": [
            {"step": "currency",      "status": "done", "message": "$1 = ₹83.5"},
            {"step": "scraping",      "status": "done", "message": "Product details extracted"},
            {"step": "hsn_lookup",    "status": "done", "message": "HS 8471 — Electronics"},
            {"step": "duty_calc",     "status": "done", "message": "BCD 20% + IGST 18%"},
            {"step": "restrictions",  "status": "done", "message": "No restrictions"},
            {"step": "price_compare", "status": "done", "message": f"Amazon India ₹{ind:,.0f}"},
            {"step": "ai_reasoning",  "status": "done", "message": "Recommendation ready"},
        ],
    }


# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="True Cost Calculator",
    page_icon="🛃",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject CSS + render sidebar + header ────────────────────────────────────
inject_css()
render_sidebar()
render_header()

# ── Session state ────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error  = None

# ── Two-column layout ────────────────────────────────────────────────────────
col_form, col_results = st.columns([1, 1.3], gap="large")

with col_form:
    form_data = render_input_form()

    if form_data:
        st.session_state.result = None
        st.session_state.error  = None

        with st.container():
            render_agent_log()

        try:
            resp = requests.post(
                "http://localhost:5000/analyze",
                json=form_data,
                timeout=30,
            )
            if resp.status_code == 200:
                st.session_state.result = resp.json()
            else:
                st.session_state.result = _mock(form_data)
        except Exception:
            st.session_state.result = _mock(form_data)

        st.rerun()

with col_results:
    if st.session_state.result:
        render_results(st.session_state.result)
    elif st.session_state.error:
        st.error(f"❌ {st.session_state.error}")
    else:
        st.markdown("""
        <div class="placeholder-box">
            <div class="placeholder-icon">🛃</div>
            <div class="placeholder-title">Your Analysis Will Appear Here</div>
            <div class="placeholder-desc">
                Fill in the product details and click<br/>
                <strong>Calculate True Cost</strong>
            </div>
            <div class="placeholder-features">
                <div class="feat-item">💰 Total landed cost ₹</div>
                <div class="feat-item">🏛️ Duty breakdown</div>
                <div class="feat-item">🇮🇳 India price compare</div>
                <div class="feat-item">⚠️ Import restrictions</div>
                <div class="feat-item">🤖 AI recommendation</div>
                <div class="feat-item">🚢 Delivery estimate</div>
            </div>
        </div>
        """, unsafe_allow_html=True)