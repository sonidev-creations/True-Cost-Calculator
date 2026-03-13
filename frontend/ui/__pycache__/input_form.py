import streamlit as st
import requests

SOURCES = {
    "amazon_us":  "🇺🇸 Amazon US",
    "aliexpress": "🇨🇳 AliExpress",
    "shein":      "👗 SHEIN",
    "iherb":      "💊 iHerb",
    "ebay":       "🌐 eBay",
    "walmart":    "🇺🇸 Walmart US",
    "other":      "🌍 Other Site",
}

CATEGORIES = {
    "electronics":   "📱 Electronics & Gadgets",
    "mobile_phones": "📲 Mobile Phones",
    "clothing":      "👕 Clothing & Apparel",
    "footwear":      "👟 Footwear & Shoes",
    "supplements":   "💊 Health Supplements",
    "cosmetics":     "💄 Cosmetics & Skincare",
    "books":         "📚 Books & Printed Matter",
    "toys":          "🧸 Toys & Games",
    "watches":       "⌚ Watches",
    "food":          "🍎 Food & Edibles",
    "jewelry":       "💍 Jewelry",
    "bags":          "👜 Bags & Luggage",
}

BACKEND_URL = "http://localhost:5000"


def fetch_hs_code(product_name: str) -> dict | None:
    """
    Calls backend /hs-lookup and returns HS code result.
    Returns None if backend is offline or product name is empty.
    """
    if not product_name or len(product_name.strip()) < 3:
        return None
    try:
        resp = requests.get(
            f"{BACKEND_URL}/hs-lookup",
            params={"product": product_name},
            timeout=5,
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None


def render_input_form():
    st.markdown('<div class="form-section-title">📦 Product Details</div>',
                unsafe_allow_html=True)

    # ── Live HS Code lookup outside the form ──────────────────────────────────
    product_name_input = st.text_input(
        "Product Name",
        placeholder="e.g. Sony WH-1000XM5 Headphones",
        key="product_name_live",
    )

    # Show HS code badge live as user types
    if product_name_input and len(product_name_input.strip()) >= 3:
        hs_data = fetch_hs_code(product_name_input)
        if hs_data and hs_data.get("match_found"):
            st.markdown(f"""
            <div style="background:rgba(245,196,0,0.08);border:1px solid rgba(245,196,0,0.25);
                 border-radius:10px;padding:10px 16px;margin:4px 0 12px;
                 display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                          color:#888;letter-spacing:2px;text-transform:uppercase;">
                          HS CODE DETECTED
                    </span><br/>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:16px;
                          font-weight:700;color:#F5C400;">
                          {hs_data['hs_code']}
                    </span>
                    <span style="font-size:12px;color:#aaa;margin-left:10px;">
                          {hs_data['description']}
                    </span>
                </div>
                <div style="text-align:right;">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:13px;
                          font-weight:700;color:#F97316;">
                          BCD {hs_data['bcd_rate']:.0f}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif hs_data and not hs_data.get("match_found"):
            st.markdown("""
            <div style="background:rgba(255,255,255,0.03);border:1px solid #333;
                 border-radius:10px;padding:8px 16px;margin:4px 0 12px;
                 font-family:'JetBrains Mono',monospace;font-size:11px;color:#555;">
                 HS Code: Auto-detecting... (will use category default)
            </div>
            """, unsafe_allow_html=True)

    with st.form(key="product_form", clear_on_submit=False):

        product_url = st.text_input(
            "Product URL (optional)",
            placeholder="https://amazon.com/dp/... or https://aliexpress.com/...",
        )

        price_usd = st.number_input(
            "Price in USD ($)  ★ Required",
            min_value=0.01,
            max_value=100000.0,
            value=None,
            step=0.01,
            format="%.2f",
            placeholder="Enter price in USD",
        )

        col1, col2 = st.columns(2)
        with col1:
            source_key = st.selectbox(
                "Buying From",
                options=list(SOURCES.keys()),
                format_func=lambda k: SOURCES[k],
            )
        with col2:
            category_key = st.selectbox(
                "Product Category",
                options=list(CATEGORIES.keys()),
                format_func=lambda k: CATEGORIES[k],
            )

        indian_price = st.number_input(
            "Indian Price ₹ (optional — for comparison)",
            min_value=0.0,
            max_value=10000000.0,
            value=None,
            step=1.0,
            format="%.0f",
            placeholder="Check Amazon India / Flipkart",
        )

        st.markdown("""
        <div style="background:rgba(245,196,0,0.06);border:1px solid rgba(245,196,0,0.15);
             border-radius:8px;padding:10px 14px;margin:8px 0 16px;
             font-size:12px;color:#888;font-family:'JetBrains Mono',monospace;">
            💱 Rate: $1 ≈ ₹83.5 (live) &nbsp;·&nbsp; IGST: 18% &nbsp;·&nbsp; Source: CBIC Tariff
        </div>
        """, unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "🔍  Calculate True Cost",
            use_container_width=True,
            type="primary",
        )

        if submitted:
            if not price_usd or price_usd <= 0:
                st.error("❌ Please enter the product price in USD.")
                return None

            return {
                "product_name":     product_name_input.strip() if product_name_input else "Unknown Product",
                "url":              product_url.strip() if product_url else "",
                "price_usd":        float(price_usd),
                "source_site":      source_key,
                "category":         category_key,
                "indian_price_inr": float(indian_price) if indian_price and indian_price > 0 else None,
            }

    return None