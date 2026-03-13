from fastapi import FastAPI
from scraper import scrape_product

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI running"}

@app.get("/scrape")
def scrape(url: str):
    result = scrape_product(url)
    return result

import streamlit as st
import requests
from ui.styles     import inject_css
from ui.header     import render_header
from ui.input_form import render_input_form
from ui.agent_log  import render_agent_log
from ui.results    import render_results
from ui.sidebar    import render_sidebar

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="True Cost Calculator",
    page_icon="🛃",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Country duty rates (mirrors backend COUNTRY_RATES) ───────────────────────
COUNTRY_RATES = {
    "India":     {"bcd": 20,  "gst": 18,  "symbol": "₹",   "fx": 83.5,  "flag": "🇮🇳"},
    "USA":       {"bcd": 0,   "gst": 8,   "symbol": "$",   "fx": 1.0,   "flag": "🇺🇸"},
    "UK":        {"bcd": 4,   "gst": 20,  "symbol": "£",   "fx": 1.27,  "flag": "🇬🇧"},
    "UAE":       {"bcd": 5,   "gst": 5,   "symbol": "د.إ", "fx": 3.67,  "flag": "🇦🇪"},
    "Singapore": {"bcd": 0,   "gst": 9,   "symbol": "S$",  "fx": 1.35,  "flag": "🇸🇬"},
    "Germany":   {"bcd": 3.7, "gst": 19,  "symbol": "€",   "fx": 1.08,  "flag": "🇩🇪"},
    "Australia": {"bcd": 5,   "gst": 10,  "symbol": "A$",  "fx": 0.65,  "flag": "🇦🇺"},
    "Canada":    {"bcd": 0,   "gst": 13,  "symbol": "C$",  "fx": 0.74,  "flag": "🇨🇦"},
    "Japan":     {"bcd": 0,   "gst": 10,  "symbol": "¥",   "fx": 0.0067,"flag": "🇯🇵"},
    "China":     {"bcd": 7,   "gst": 13,  "symbol": "¥",   "fx": 7.24,  "flag": "🇨🇳"},
}


def _compute_country_costs(price_usd: float, india_bcd: float, india_igst: float) -> list[dict]:
    results = []
    for country, info in COUNTRY_RATES.items():
        b = india_bcd  if country == "India" else info["bcd"]
        g = india_igst if country == "India" else info["gst"]
        price_local = price_usd * info["fx"]
        bcd         = price_local * (b / 100)
        gst         = (price_local + bcd) * (g / 100)
        total_local = price_local + bcd + gst
        total_usd   = total_local / info["fx"]
        results.append({
            "country":     country,
            "flag":        info["flag"],
            "symbol":      info["symbol"],
            "bcd_pct":     b,
            "gst_pct":     g,
            "total_usd":   round(total_usd, 2),
            "total_local": round(total_local, 2),
        })
    results.sort(key=lambda x: x["total_usd"])
    return results


def _render_country_comparison(comparison: list[dict]) -> None:
    st.markdown("### 🌍 Country-wise Cost Comparison")
    cheapest = comparison[0]

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a3a1a, #0d2b0d);
        border: 1px solid #00ff88;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 16px;
        text-align: center;
    ">
        <div style="font-size: 0.75rem; color: #888; letter-spacing: 2px; margin-bottom: 4px;">CHEAPEST TO BUY</div>
        <div style="font-size: 2rem;">{cheapest['flag']}</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #00ff88;">{cheapest['country']}</div>
        <div style="font-size: 1rem; color: #ccc;">
            {cheapest['symbol']}{cheapest['total_local']:,.0f}
            &nbsp;·&nbsp; ~${cheapest['total_usd']:.2f} USD
        </div>
    </div>
    """, unsafe_allow_html=True)

    rows_html = ""
    for i, c in enumerate(comparison):
        is_best    = i == 0
        bar_pct    = int((c["total_usd"] / comparison[-1]["total_usd"]) * 100)
        rank_color = "#00ff88" if is_best else ("#ffd700" if i == 1 else "#aaa")
        rows_html += f"""
        <div style="
            display: flex; align-items: center; gap: 10px;
            padding: 8px 0; border-bottom: 1px solid #222;
        ">
            <div style="width: 26px; text-align: center; font-size: 1.1rem;">{c['flag']}</div>
            <div style="flex: 1;">
                <div style="font-size: 0.85rem; color: {rank_color}; font-weight: {'700' if is_best else '400'};">
                    {c['country']}
                    {'&nbsp;🏆' if is_best else ''}
                </div>
                <div style="
                    height: 4px; border-radius: 2px;
                    background: linear-gradient(90deg, {rank_color} {bar_pct}%, #333 {bar_pct}%);
                    margin-top: 4px;
                "></div>
            </div>
            <div style="text-align: right; font-size: 0.8rem; color: #ccc; min-width: 90px;">
                {c['symbol']}{c['total_local']:,.0f}<br/>
                <span style="color: #666; font-size: 0.7rem;">${c['total_usd']:.2f}</span>
            </div>
        </div>
        """

    st.markdown(f"""
    <div style="
        background: #111;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 12px 16px;
    ">{rows_html}</div>
    """, unsafe_allow_html=True)


# ─── Mock result (backend-offline fallback) ───────────────────────────────────
def _mock_result(form_data: dict) -> dict:
    price_usd = form_data.get("price_usd", 100)

    cat_rates = {
        "electronics":   (20, 18), "mobile_phones": (20, 18),
        "clothing":      (20, 12), "footwear":      (25, 18),
        "supplements":   (10, 18), "cosmetics":     (20, 28),
        "books":         (0,   0), "toys":          (60, 12),
        "food":          (30, 12), "watches":       (20, 18),
        "jewelry":       (15,  3), "bags":          (20, 18),
    }
    bcd_pct, igst_pct = cat_rates.get(form_data.get("category", "electronics"), (20, 18))

    rate      = 83.5
    price_inr = price_usd * rate
    bcd       = price_inr * (bcd_pct / 100)
    sws       = bcd * 0.10
    igst      = (price_inr + bcd + sws) * (igst_pct / 100)
    shipping  = 1200
    total     = price_inr + bcd + sws + igst + shipping
    indian    = form_data.get("indian_price_inr") or (total * 0.85)

    restricted      = form_data.get("category") in ("supplements", "food", "toys")
    restriction_map = {
        "supplements": "FSSAI import permit required.",
        "food":        "FSSAI import permit required.",
        "toys":        "BIS certification required.",
    }

    hs_display  = "8471.30"
    cat_label   = form_data.get("category", "electronics").replace("_", " ").title()
    comparison  = _compute_country_costs(price_usd, bcd_pct, igst_pct)

    return {
        "product_name":   form_data.get("product_name") or "Sample Product",
        "source_site":    form_data.get("source_site", "amazon_us"),
        "currency_rate":  rate,
        "price_usd":      price_usd,
        "cost_breakdown": {
            "price_inr":                round(price_inr, 2),
            "assessable_value":         round(price_inr + shipping, 2),
            "basic_customs_duty":       round(bcd,   2),
            "social_welfare_surcharge": round(sws,   2),
            "igst":                     round(igst,  2),
            "shipping_cost":            shipping,
            "total_landed_cost":        round(total, 2),
            "duty_rate_percent":        bcd_pct,
            "igst_rate_percent":        igst_pct,
            "hs_code":                  hs_display,
            "category_label":           cat_label,
        },
        "indian_price":      round(indian, 2),
        "indian_source":     "Amazon India (estimated)",
        "verdict":           "BUY_LOCAL" if indian < total else "BUY_ABROAD",
        "savings":           round(indian - total, 2),
        "restricted":        restricted,
        "restriction_note":  restriction_map.get(form_data.get("category", ""), ""),
        "delivery_estimate": "10–20 days",
        "country_comparison": comparison,
        "ai_reasoning": (
            f"Total landed cost is ₹{total:,.0f} after {bcd_pct}% BCD and {igst_pct}% IGST "
            f"(HS {hs_display}). "
            + (f"Buy locally — you save ₹{abs(indian-total):,.0f}." if indian < total
               else f"Buying abroad saves you ₹{abs(indian-total):,.0f}.")
        ),
        "agent_steps": [
            {"step": "currency",       "status": "done", "message": "Rate: $1 = ₹83.5 (fallback)"},
            {"step": "scraping",       "status": "done", "message": "Using entered product name"},
            {"step": "hsn_lookup",     "status": "done", "message": f"HS {hs_display} — {cat_label}"},
            {"step": "duty_calc",      "status": "done", "message": f"BCD {bcd_pct}% + SWS 10% + IGST {igst_pct}%"},
            {"step": "restrictions",   "status": "done", "message": "BIS/FSSAI check complete" if restricted else "No restrictions"},
            {"step": "price_compare",  "status": "done", "message": f"India estimate: ₹{indian:,.0f}"},
            {"step": "country_compare","status": "done", "message": f"Best: {comparison[0]['country']} @ ${comparison[0]['total_usd']:.2f}"},
            {"step": "ai_reasoning",   "status": "done", "message": "Recommendation generated"},
        ],
    }


# ─── CSS + Layout ─────────────────────────────────────────────────────────────
inject_css()
render_sidebar()
render_header()

for key, default in [("result", None), ("error", None), ("loading", False)]:
    if key not in st.session_state:
        st.session_state[key] = default

col_form, col_results = st.columns([1, 1.3], gap="large")

with col_form:
    form_data = render_input_form()

    if form_data:
        st.session_state.result  = None
        st.session_state.error   = None
        st.session_state.loading = True

        try:
            resp = requests.post("http://localhost:5000/analyze", json=form_data, timeout=30)
            if resp.status_code == 200:
                st.session_state.result = resp.json()
            else:
                st.session_state.error = f"Backend error {resp.status_code}"
        except requests.exceptions.ConnectionError:
            st.session_state.result = _mock_result(form_data)
        except Exception as e:
            st.session_state.error = str(e)

        st.session_state.loading = False
        st.rerun()

with col_results:
    result = st.session_state.result
    if result:
        render_results(result)

        # ── Country Comparison (below main results) ──────────────────────────
        comparison = result.get("country_comparison")
        if not comparison:
            # Build locally if backend didn't include it
            cb       = result.get("cost_breakdown", {})
            bcd_pct  = cb.get("duty_rate_percent", 20)
            igst_pct = cb.get("igst_rate_percent", 18)
            price_u  = result.get("price_usd") or result.get("cost_breakdown", {}).get("price_inr", 0) / 83.5
            comparison = _compute_country_costs(float(price_u), bcd_pct, igst_pct)

        _render_country_comparison(comparison)

    elif st.session_state.error:
        st.error(f"❌ {st.session_state.error}")
    else:
        st.markdown("""
        <div class="placeholder-box">
            <div class="placeholder-icon">🛃</div>
            <div class="placeholder-title">Your Analysis Will Appear Here</div>
            <div class="placeholder-desc">
                Fill in the product details on the left and click<br/>
                <strong>Calculate True Cost</strong> to get started.
            </div>
            <div class="placeholder-features">
                <div class="feat-item">💰 Total landed cost in ₹</div>
                <div class="feat-item">🏛️ Customs duty breakdown</div>
                <div class="feat-item">🇮🇳 Indian price comparison</div>
                <div class="feat-item">⚠️ Import restrictions check</div>
                <div class="feat-item">🌍 Country-wise cost ranking</div>
                <div class="feat-item">🤖 AI recommendation</div>
            </div>
        </div>
        """, unsafe_allow_html=True)