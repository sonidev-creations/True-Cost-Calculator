import streamlit as st
from ui.agent_log import render_agent_log


def render_results(result: dict):
    verdict          = result.get("verdict", "NEUTRAL")
    cost             = result.get("cost_breakdown", {})
    ai_text          = result.get("ai_reasoning", "")
    indian_price     = result.get("indian_price")
    indian_source    = result.get("indian_source", "Indian Marketplace")
    restricted       = result.get("restricted", False)
    restriction_note = result.get("restriction_note", "")
    delivery         = result.get("delivery_estimate", "—")
    savings          = result.get("savings")
    agent_steps      = result.get("agent_steps", [])
    hs_info          = result.get("hs_lookup", {})

    if agent_steps:
        render_agent_log(steps_data=agent_steps)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    _verdict_banner(verdict, savings, delivery)
    _hs_banner(hs_info)
    _cost_breakdown(cost, indian_price, indian_source)
    _restriction_box(restricted, restriction_note)
    _ai_box(ai_text)
    _metrics(cost, indian_price, delivery, indian_source)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("← Calculate Another Product", use_container_width=True):
        st.session_state.result = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def _verdict_banner(verdict, savings, delivery):
    cfgs = {
        "BUY_ABROAD": ("buy-abroad", "✈️",  "✅ Buy From Abroad",        "green"),
        "BUY_LOCAL":  ("buy-local",  "🏪",  "🇮🇳 Buy Locally in India",  "red"),
        "CLOSE_CALL": ("close-call", "⚖️",  "Close Call — Your Choice",  "yellow"),
        "NEUTRAL":    ("close-call", "📊",  "Check Indian Prices First", "yellow"),
    }
    cls, emoji, text, tcls = cfgs.get(verdict, ("close-call", "❓", "Unknown", "yellow"))

    savings_html = ""
    if savings is not None:
        amt = abs(round(savings))
        if savings > 500:
            savings_html = f'<div class="verdict-savings">Save <strong>₹{amt:,}</strong> buying abroad</div>'
        elif savings < -500:
            savings_html = f'<div class="verdict-savings">Save <strong>₹{amt:,}</strong> buying locally</div>'
        else:
            savings_html = f'<div class="verdict-savings">Difference is only ₹{amt:,} — almost the same</div>'

    st.markdown(f"""
    <div class="verdict-banner {cls}">
        <span class="verdict-emoji">{emoji}</span>
        <div class="verdict-label">Recommendation</div>
        <div class="verdict-text {tcls}">{text}</div>
        {savings_html}
        <div class="verdict-delivery">🚢 Estimated delivery: {delivery}</div>
    </div>
    """, unsafe_allow_html=True)


def _hs_banner(hs_info: dict):
    if not hs_info or not hs_info.get("hs_code"):
        return

    hs_code    = hs_info.get("hs_code", "")
    desc       = hs_info.get("description", "")
    bcd        = hs_info.get("bcd_rate", 0)
    igst       = hs_info.get("igst_rate", 18)
    matched    = hs_info.get("matched_keyword", "")
    found      = hs_info.get("match_found", False)

    match_badge = (
        f'<span style="background:rgba(34,197,94,0.15);color:#22C55E;'
        f'font-family:JetBrains Mono,monospace;font-size:10px;padding:2px 8px;'
        f'border-radius:4px;margin-left:8px;">✅ matched: {matched}</span>'
        if found and matched
        else
        f'<span style="background:rgba(255,255,255,0.06);color:#666;'
        f'font-family:JetBrains Mono,monospace;font-size:10px;padding:2px 8px;'
        f'border-radius:4px;margin-left:8px;">category default</span>'
    )

    st.markdown(f"""
    <div style="background:rgba(245,196,0,0.06);border:1px solid rgba(245,196,0,0.2);
         border-radius:12px;padding:14px 18px;margin-bottom:14px;
         display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
        <div>
            <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                  color:#888;letter-spacing:2px;text-transform:uppercase;">HS CODE</span>
            <br/>
            <span style="font-family:'JetBrains Mono',monospace;font-size:20px;
                  font-weight:700;color:#F5C400;">{hs_code}</span>
            <span style="font-size:13px;color:#aaa;margin-left:10px;">{desc}</span>
            {match_badge}
        </div>
        <div style="display:flex;gap:12px;">
            <div style="text-align:center;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:18px;
                     font-weight:700;color:#F97316;">{bcd:.0f}%</div>
                <div style="font-size:10px;color:#666;letter-spacing:1px;">BCD</div>
            </div>
            <div style="text-align:center;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:18px;
                     font-weight:700;color:#A855F7;">{igst:.0f}%</div>
                <div style="font-size:10px;color:#666;letter-spacing:1px;">IGST</div>
            </div>
            <div style="text-align:center;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:18px;
                     font-weight:700;color:#FB923C;">10%</div>
                <div style="font-size:10px;color:#666;letter-spacing:1px;">SWS</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _cost_breakdown(cost, indian_price, indian_source):
    total = cost.get("total_landed_cost", 0)
    if total == 0:
        return

    def bar(label, value, color):
        pct = min(int((value / total) * 100), 100) if total > 0 else 0
        st.markdown(f"""
        <div style="margin-bottom:14px">
            <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                <span style="font-size:13px;color:#ccc">{label}</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:13px;
                      font-weight:600;color:{color}">₹{value:,.0f}</span>
            </div>
            <div style="background:rgba(255,255,255,0.05);border-radius:4px;height:7px;overflow:hidden">
                <div style="width:{pct}%;height:100%;background:{color};border-radius:4px"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="breakdown-card">', unsafe_allow_html=True)
    st.markdown('<div class="breakdown-title">💰 Cost Breakdown</div>', unsafe_allow_html=True)

    bar("Product Price (USD → INR)",             cost.get("price_inr", 0),                "#4A9EFF")
    bar(f"Basic Customs Duty (BCD {cost.get('duty_rate_percent',0):.0f}%)",
                                                 cost.get("basic_customs_duty", 0),        "#F97316")
    bar("Social Welfare Surcharge (10% of BCD)", cost.get("social_welfare_surcharge", 0),  "#FB923C")
    bar(f"IGST ({cost.get('igst_rate_percent',18):.0f}%)",
                                                 cost.get("igst", 0),                      "#A855F7")
    if cost.get("shipping_cost", 0) > 0:
        bar("Shipping Cost",                     cost.get("shipping_cost", 0),             "#14B8A6")

    st.markdown(f"""
    <div class="total-row">
        <span class="total-label">Total Landed Cost</span>
        <span class="total-value">₹{total:,.0f}</span>
    </div>
    """, unsafe_allow_html=True)

    if indian_price:
        # Source badge color
        src_color = "#22C55E" if indian_source == "User Provided" else \
                    "#F59E0B" if "Estimated" in indian_source else "#4A9EFF"
        st.markdown(f"""
        <div class="india-row">
            <div>
                <span class="india-label">🇮🇳 India Price</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                      background:rgba(255,255,255,0.06);color:{src_color};
                      padding:2px 8px;border-radius:4px;margin-left:8px;">
                      {indian_source}
                </span>
            </div>
            <span class="india-value">₹{indian_price:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def _restriction_box(restricted, note):
    if restricted:
        st.markdown(f"""
        <div class="restriction-box">
            <div class="restriction-icon">🚨</div>
            <div>
                <div class="restriction-title">Import Restriction Alert</div>
                <div class="restriction-text">{note}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="safe-box">
            <span style="font-size:20px">✅</span>
            <span class="safe-text">No import restrictions — standard customs clearance applies.</span>
        </div>
        """, unsafe_allow_html=True)


def _ai_box(ai_text):
    if not ai_text:
        return
    st.markdown(f"""
    <div class="ai-box">
        <div class="ai-box-title">🤖 &nbsp; AI Agent Reasoning</div>
        <div class="ai-text">{ai_text}</div>
    </div>
    """, unsafe_allow_html=True)


def _metrics(cost, indian_price, delivery, indian_source):
    total      = cost.get("total_landed_cost", 0)
    duty_total = (cost.get("basic_customs_duty", 0)
                + cost.get("social_welfare_surcharge", 0)
                + cost.get("igst", 0))
    duty_pct   = (duty_total / cost.get("price_inr", 1)) * 100 if cost.get("price_inr", 0) > 0 else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("💰 Landed Cost", f"₹{total:,.0f}")
    with c2:
        st.metric("🏛️ Duty Added",  f"₹{duty_total:,.0f}", f"+{duty_pct:.0f}%")
    with c3:
        if indian_price:
            diff = total - indian_price
            sign = "+" if diff > 0 else ""
            label = f"🇮🇳 vs {indian_source[:12]}"
            st.metric(label, f"₹{indian_price:,.0f}", f"{sign}₹{diff:,.0f}")
        else:
            st.metric("🚢 Delivery", delivery)