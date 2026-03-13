import streamlit as st

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


def render_input_form():
    st.markdown('<div class="form-section-title">📦 Product Details</div>',
                unsafe_allow_html=True)

    with st.form(key="product_form", clear_on_submit=False):

        product_name = st.text_input(
            "Product Name",
            placeholder="e.g. Sony WH-1000XM5 Headphones",
        )

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
                "product_name":     product_name.strip() if product_name else "Unknown Product",
                "url":              product_url.strip() if product_url else "",
                "price_usd":        float(price_usd),
                "source_site":      source_key,
                "category":         category_key,
                "indian_price_inr": float(indian_price) if indian_price and indian_price > 0 else None,
            }

    return None
import streamlit as st

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

# ── Same HS database as sidebar — keyword → category + hs_code ─────────────
_HS_MAP = {
    # Electronics
    "laptop":        ("electronics",   "8471.30"),
    "computer":      ("electronics",   "8471.30"),
    "headphones":    ("electronics",   "8518.30"),
    "earphones":     ("electronics",   "8518.30"),
    "earbuds":       ("electronics",   "8518.30"),
    "speaker":       ("electronics",   "8518.22"),
    "keyboard":      ("electronics",   "8471.60"),
    "mouse":         ("electronics",   "8471.60"),
    "monitor":       ("electronics",   "8528.52"),
    "tablet":        ("electronics",   "8471.30"),
    "ipad":          ("electronics",   "8471.30"),
    "camera":        ("electronics",   "8525.80"),
    "drone":         ("electronics",   "8806.21"),
    "router":        ("electronics",   "8517.62"),
    "hard disk":     ("electronics",   "8471.70"),
    "ssd":           ("electronics",   "8471.70"),
    "charger":       ("electronics",   "8504.40"),
    "power bank":    ("electronics",   "8507.60"),
    "printer":       ("electronics",   "8443.32"),
    "projector":     ("electronics",   "9008.60"),
    "tv":            ("electronics",   "8528.72"),
    "television":    ("electronics",   "8528.72"),
    # Mobile
    "phone":         ("mobile_phones", "8517.12"),
    "mobile":        ("mobile_phones", "8517.12"),
    "smartphone":    ("mobile_phones", "8517.12"),
    "iphone":        ("mobile_phones", "8517.12"),
    "samsung":       ("mobile_phones", "8517.12"),
    "oneplus":       ("mobile_phones", "8517.12"),
    # Watches
    "smartwatch":    ("watches",       "9102.12"),
    "apple watch":   ("watches",       "9102.12"),
    "watch":         ("watches",       "9102.11"),
    "fitness tracker":("watches",      "9102.12"),
    "casio":         ("watches",       "9102.11"),
    "fossil":        ("watches",       "9102.11"),
    # Gaming (toys category)
    "gaming console":("toys",          "9504.50"),
    "playstation":   ("toys",          "9504.50"),
    "xbox":          ("toys",          "9504.50"),
    "ps5":           ("toys",          "9504.50"),
    # Clothing
    "shirt":         ("clothing",      "6205.20"),
    "t-shirt":       ("clothing",      "6109.10"),
    "tshirt":        ("clothing",      "6109.10"),
    "jeans":         ("clothing",      "6203.42"),
    "dress":         ("clothing",      "6204.41"),
    "jacket":        ("clothing",      "6201.93"),
    "hoodie":        ("clothing",      "6110.20"),
    "sweater":       ("clothing",      "6110.20"),
    "leggings":      ("clothing",      "6104.62"),
    "socks":         ("clothing",      "6115.95"),
    "cap":           ("clothing",      "6505.00"),
    "hat":           ("clothing",      "6505.00"),
    "scarf":         ("clothing",      "6214.20"),
    "gloves":        ("clothing",      "6216.00"),
    # Footwear
    "shoes":         ("footwear",      "6403.91"),
    "sneakers":      ("footwear",      "6404.11"),
    "boots":         ("footwear",      "6403.12"),
    "sandals":       ("footwear",      "6402.20"),
    "heels":         ("footwear",      "6403.51"),
    "nike":          ("footwear",      "6404.11"),
    "adidas":        ("footwear",      "6404.11"),
    "flip flops":    ("footwear",      "6402.20"),
    # Supplements
    "protein":       ("supplements",   "2106.10"),
    "whey":          ("supplements",   "2106.10"),
    "creatine":      ("supplements",   "2106.10"),
    "vitamins":      ("supplements",   "2106.90"),
    "vitamin":       ("supplements",   "2106.90"),
    "omega":         ("supplements",   "1504.20"),
    "probiotic":     ("supplements",   "2106.90"),
    "collagen":      ("supplements",   "3504.00"),
    "melatonin":     ("supplements",   "2932.99"),
    "supplement":    ("supplements",   "2106.90"),
    "pre workout":   ("supplements",   "2106.90"),
    # Cosmetics
    "serum":         ("cosmetics",     "3304.99"),
    "moisturizer":   ("cosmetics",     "3304.99"),
    "sunscreen":     ("cosmetics",     "3304.99"),
    "lipstick":      ("cosmetics",     "3304.10"),
    "foundation":    ("cosmetics",     "3304.30"),
    "mascara":       ("cosmetics",     "3304.20"),
    "perfume":       ("cosmetics",     "3303.00"),
    "shampoo":       ("cosmetics",     "3305.10"),
    "conditioner":   ("cosmetics",     "3305.90"),
    "face wash":     ("cosmetics",     "3401.19"),
    "toner":         ("cosmetics",     "3304.99"),
    "retinol":       ("cosmetics",     "3304.99"),
    "niacinamide":   ("cosmetics",     "3304.99"),
    "skincare":      ("cosmetics",     "3304.99"),
    "makeup":        ("cosmetics",     "3304.30"),
    # Books
    "book":          ("books",         "4901.99"),
    "novel":         ("books",         "4901.99"),
    "textbook":      ("books",         "4901.10"),
    "comic":         ("books",         "4901.99"),
    "magazine":      ("books",         "4902.90"),
    # Toys
    "lego":          ("toys",          "9503.00"),
    "toy":           ("toys",          "9503.00"),
    "doll":          ("toys",          "9502.10"),
    "board game":    ("toys",          "9504.40"),
    "puzzle":        ("toys",          "9503.00"),
    "rc car":        ("toys",          "9503.00"),
    "action figure": ("toys",          "9502.10"),
    # Food
    "coffee":        ("food",          "0901.21"),
    "chocolate":     ("food",          "1806.32"),
    "nuts":          ("food",          "0802.32"),
    "tea":           ("food",          "0902.30"),
    "honey":         ("food",          "0409.00"),
    "snacks":        ("food",          "1905.90"),
    "olive oil":     ("food",          "1509.10"),
    # Jewelry
    "necklace":      ("jewelry",       "7117.19"),
    "ring":          ("jewelry",       "7117.19"),
    "bracelet":      ("jewelry",       "7117.19"),
    "earrings":      ("jewelry",       "7117.19"),
    "gold":          ("jewelry",       "7108.12"),
    "silver":        ("jewelry",       "7113.11"),
    # Bags
    "bag":           ("bags",          "4202.22"),
    "backpack":      ("bags",          "4202.92"),
    "suitcase":      ("bags",          "4202.12"),
    "wallet":        ("bags",          "4202.31"),
    "handbag":       ("bags",          "4202.22"),
    "tote":          ("bags",          "4202.22"),
    "purse":         ("bags",          "4202.31"),
    "luggage":       ("bags",          "4202.12"),
}

# Restriction warnings shown inline
_RESTRICTION_WARN = {
    "supplements": "⚠️ FSSAI permit required for supplements",
    "food":        "⚠️ FSSAI permit required for food items",
    "toys":        "⚠️ BIS certification required for toys",
}


def _detect_from_name(name: str):
    """
    Scans product name against HS map keywords.
    Returns (category_key, hs_code, matched_keyword) or (None, None, None).
    """
    name_lower = name.lower().strip()
    # Longest keyword match first for accuracy
    for kw in sorted(_HS_MAP.keys(), key=len, reverse=True):
        if kw in name_lower:
            cat, hs = _HS_MAP[kw]
            return cat, hs, kw
    return None, None, None


def render_input_form():
    """Renders the product input form. Returns form data dict on submit, else None."""

    st.markdown(
        '<div class="form-section-title">📦 Product Details</div>',
        unsafe_allow_html=True,
    )

    # ── Live HS detection OUTSIDE form (reacts as user types) ──────────────
    product_name_live = st.text_input(
        "Product Name",
        placeholder="e.g. Sony WH-1000XM5 Headphones",
        key="product_name_live",
        help="Type product name — HS code & category auto-detected instantly",
    )

    # Run detection on every keystroke
    detected_cat, detected_hs, matched_kw = _detect_from_name(product_name_live)

    # Show HS detection badge when found
    if detected_hs:
        cat_label   = CATEGORIES.get(detected_cat, detected_cat)
        warn        = _RESTRICTION_WARN.get(detected_cat, "")
        warn_html   = (
            f'<span style="margin-left:8px;font-size:11px;color:#EF4444;">{warn}</span>'
            if warn else ""
        )
        st.markdown(f"""
        <div style="background:rgba(245,196,0,0.07);border:1px solid rgba(245,196,0,0.25);
             border-radius:8px;padding:9px 14px;margin:-4px 0 10px;
             display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:11px;
                  color:#F5C400;font-weight:700;">🔍 HS {detected_hs}</span>
            <span style="font-size:12px;color:#ccc;">{cat_label}</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                  color:#555;">matched: "{matched_kw}"</span>
            {warn_html}
        </div>
        """, unsafe_allow_html=True)

    # ── Rest of form ────────────────────────────────────────────────────────
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
            # Auto-select detected category, fallback to electronics
            cat_keys    = list(CATEGORIES.keys())
            default_idx = cat_keys.index(detected_cat) if detected_cat in cat_keys else 0
            category_key = st.selectbox(
                "Product Category",
                options=cat_keys,
                format_func=lambda k: CATEGORIES[k],
                index=default_idx,
                help="Auto-filled from product name — change if needed",
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

        # Info bar — shows detected HS or default message
        if detected_hs:
            info_text = f"🔍 HS {detected_hs} detected &nbsp;·&nbsp; BCD + IGST auto-applied &nbsp;·&nbsp; CBIC Tariff"
        else:
            info_text = "💱 Rate: $1 ≈ ₹83.5 (live) &nbsp;·&nbsp; IGST: 18% &nbsp;·&nbsp; Source: CBIC Tariff"

        st.markdown(f"""
        <div style="background:rgba(245,196,0,0.06);border:1px solid rgba(245,196,0,0.15);
             border-radius:8px;padding:10px 14px;margin:8px 0 16px;
             font-size:12px;color:#888;font-family:'JetBrains Mono',monospace;">
            {info_text}
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

            final_name = product_name_live.strip() if product_name_live else "Unknown Product"

            return {
                "product_name":     final_name,
                "url":              product_url.strip() if product_url else "",
                "price_usd":        float(price_usd),
                "source_site":      source_key,
                "category":         category_key,
                "detected_hs":      detected_hs or "",
                "indian_price_inr": float(indian_price) if indian_price and indian_price > 0 else None,
            }

    return None