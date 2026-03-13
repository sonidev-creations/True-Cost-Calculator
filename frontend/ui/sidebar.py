import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 10px;">
            <div style="font-size:40px;margin-bottom:8px;">🛃</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
                 letter-spacing:3px;color:#F5C400;text-transform:uppercase;">
                True Cost Calculator
            </div>
            <div style="font-size:11px;color:#555;margin-top:4px;">
                v1.0 · India Import Intelligence
            </div>
        </div>
        <hr style="border-color:#222;margin:12px 0 20px"/>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
             letter-spacing:2px;color:#F5C400;text-transform:uppercase;margin-bottom:12px;">
            📋 Duty Rates (CBIC)
        </div>
        <table class="duty-table">
          <thead>
            <tr><th>Category</th><th>BCD</th><th>IGST</th><th>⚠️</th></tr>
          </thead>
          <tbody>
            <tr><td>Electronics</td><td><span class="rate-badge rate-medium">20%</span></td><td><span class="rate-badge rate-medium">18%</span></td><td><span class="restrict-no">No</span></td></tr>
            <tr><td>Clothing</td><td><span class="rate-badge rate-medium">20%</span></td><td><span class="rate-badge rate-low">12%</span></td><td><span class="restrict-no">No</span></td></tr>
            <tr><td>Footwear</td><td><span class="rate-badge rate-medium">25%</span></td><td><span class="rate-badge rate-medium">18%</span></td><td><span class="restrict-no">No</span></td></tr>
            <tr><td>Supplements</td><td><span class="rate-badge rate-low">10%</span></td><td><span class="rate-badge rate-medium">18%</span></td><td><span class="restrict-yes">FSSAI</span></td></tr>
            <tr><td>Cosmetics</td><td><span class="rate-badge rate-medium">20%</span></td><td><span class="rate-badge rate-high">28%</span></td><td><span class="restrict-no">No</span></td></tr>
            <tr><td>Books</td><td><span class="rate-badge rate-zero">0%</span></td><td><span class="rate-badge rate-zero">0%</span></td><td><span class="restrict-no">No</span></td></tr>
            <tr><td>Toys</td><td><span class="rate-badge rate-high">60%</span></td><td><span class="rate-badge rate-low">12%</span></td><td><span class="restrict-yes">BIS</span></td></tr>
            <tr><td>Food</td><td><span class="rate-badge rate-high">30%</span></td><td><span class="rate-badge rate-low">12%</span></td><td><span class="restrict-yes">FSSAI</span></td></tr>
            <tr><td>Watches</td><td><span class="rate-badge rate-medium">20%</span></td><td><span class="rate-badge rate-medium">18%</span></td><td><span class="restrict-no">No</span></td></tr>
            <tr><td>Jewelry</td><td><span class="rate-badge rate-low">15%</span></td><td><span class="rate-badge rate-zero">3%</span></td><td><span class="restrict-no">No</span></td></tr>
          </tbody>
        </table>
        <hr style="border-color:#222;margin:16px 0"/>
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
             letter-spacing:2px;color:#F5C400;text-transform:uppercase;margin-bottom:10px;">
            🧮 Duty Formula
        </div>
        <div style="background:#111;border:1px solid #222;border-radius:8px;
             padding:12px 14px;font-family:'JetBrains Mono',monospace;font-size:11px;
             color:#ccc;line-height:2;">
            <span style="color:#4A9EFF">AV</span>   = Price(INR) + Ship<br/>
            <span style="color:#F97316">BCD</span>  = AV × rate%<br/>
            <span style="color:#FB923C">SWS</span>  = BCD × 10%<br/>
            <span style="color:#A855F7">IGST</span> = (AV+BCD+SWS) × 18%<br/>
            <hr style="border-color:#333;margin:6px 0"/>
            <span style="color:#F5C400;font-weight:700">TOTAL = AV+BCD+SWS+IGST</span>
        </div>
        <hr style="border-color:#222;margin:16px 0"/>
        <div style="font-size:10px;color:#444;line-height:1.7;text-align:center;">
            Rates from CBIC tariff schedule.<br/>
            For estimation only.
        </div>
        """, unsafe_allow_html=True)
        
        # ── Live HS Code Search in Sidebar ────────────────────────────────
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
             letter-spacing:2px;color:#F5C400;text-transform:uppercase;margin-bottom:10px;">
            🔍 Search HS Code
        </div>
        """, unsafe_allow_html=True)

        search_term = st.text_input(
            "Search product",
            placeholder="e.g. headphones, shoes...",
            label_visibility="collapsed",
            key="sidebar_hs_search",
        )

        if search_term and len(search_term) >= 2:
            try:
                resp = requests.get(
                    "http://localhost:5000/hs-lookup",
                    params={"product": search_term},
                    timeout=3,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("match_found"):
                        st.markdown(f"""
                        <div style="background:rgba(245,196,0,0.08);border:1px solid rgba(245,196,0,0.2);
                             border-radius:8px;padding:10px 12px;margin-bottom:8px;">
                            <div style="font-family:'JetBrains Mono',monospace;font-size:14px;
                                 font-weight:700;color:#F5C400;">{data['hs_code']}</div>
                            <div style="font-size:11px;color:#aaa;margin-top:3px;">{data['description']}</div>
                            <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
                                 color:#F97316;margin-top:4px;">BCD {data['bcd_rate']:.0f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style="font-size:11px;color:#555;padding:6px 0;">
                            No exact match — try: headphones, shoes, laptop...
                        </div>
                        """, unsafe_allow_html=True)
            except Exception:
                st.markdown("""
                <div style="font-size:11px;color:#555;padding:6px 0;">
                    Backend offline
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#222;margin:16px 0'/>", unsafe_allow_html=True)

import streamlit as st
import requests

FLASK_URL = "http://localhost:5000"

# ── Local HS fallback (works even when backend is offline) ─────────────────
_LOCAL_HS = {
    "headphones":   {"hs_code": "8518.30", "description": "Headphones & Earphones",    "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "earbuds":      {"hs_code": "8518.30", "description": "Wireless Earbuds",           "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "earphones":    {"hs_code": "8518.30", "description": "Earphones",                  "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "laptop":       {"hs_code": "8471.30", "description": "Laptops & Notebooks",        "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "tablet":       {"hs_code": "8471.30", "description": "Tablets & iPads",            "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "phone":        {"hs_code": "8517.12", "description": "Mobile / Smart Phones",      "category": "mobile_phones", "bcd": "20%", "igst": "18%"},
    "mobile":       {"hs_code": "8517.12", "description": "Mobile Phones",              "category": "mobile_phones", "bcd": "20%", "igst": "18%"},
    "iphone":       {"hs_code": "8517.12", "description": "iPhone / Smartphones",       "category": "mobile_phones", "bcd": "20%", "igst": "18%"},
    "samsung":      {"hs_code": "8517.12", "description": "Samsung Smartphones",        "category": "mobile_phones", "bcd": "20%", "igst": "18%"},
    "smartwatch":   {"hs_code": "9102.12", "description": "Smart Watches",              "category": "watches",       "bcd": "20%", "igst": "18%"},
    "apple watch":  {"hs_code": "9102.12", "description": "Apple Watch / Smart Watch",  "category": "watches",       "bcd": "20%", "igst": "18%"},
    "watch":        {"hs_code": "9102.11", "description": "Wrist Watches",              "category": "watches",       "bcd": "20%", "igst": "18%"},
    "shoes":        {"hs_code": "6403.91", "description": "Leather Shoes",              "category": "footwear",      "bcd": "25%", "igst": "18%"},
    "sneakers":     {"hs_code": "6404.11", "description": "Sports Sneakers",            "category": "footwear",      "bcd": "25%", "igst": "18%"},
    "boots":        {"hs_code": "6403.12", "description": "Boots",                      "category": "footwear",      "bcd": "25%", "igst": "18%"},
    "nike":         {"hs_code": "6404.11", "description": "Sports Shoes",               "category": "footwear",      "bcd": "25%", "igst": "18%"},
    "adidas":       {"hs_code": "6404.11", "description": "Sports Shoes",               "category": "footwear",      "bcd": "25%", "igst": "18%"},
    "shirt":        {"hs_code": "6205.20", "description": "Men's Shirts",               "category": "clothing",      "bcd": "20%", "igst": "12%"},
    "tshirt":       {"hs_code": "6109.10", "description": "T-Shirts",                   "category": "clothing",      "bcd": "20%", "igst": "12%"},
    "jeans":        {"hs_code": "6203.42", "description": "Denim Jeans",                "category": "clothing",      "bcd": "20%", "igst": "12%"},
    "jacket":       {"hs_code": "6201.93", "description": "Jackets & Coats",            "category": "clothing",      "bcd": "20%", "igst": "12%"},
    "hoodie":       {"hs_code": "6110.20", "description": "Hoodies & Sweatshirts",      "category": "clothing",      "bcd": "20%", "igst": "12%"},
    "dress":        {"hs_code": "6204.41", "description": "Dresses",                    "category": "clothing",      "bcd": "20%", "igst": "12%"},
    "protein":      {"hs_code": "2106.10", "description": "Protein Supplements",        "category": "supplements",   "bcd": "10%", "igst": "18%"},
    "whey":         {"hs_code": "2106.10", "description": "Whey Protein",               "category": "supplements",   "bcd": "10%", "igst": "18%"},
    "vitamins":     {"hs_code": "2106.90", "description": "Vitamins & Minerals",        "category": "supplements",   "bcd": "10%", "igst": "18%"},
    "creatine":     {"hs_code": "2106.10", "description": "Creatine Supplements",       "category": "supplements",   "bcd": "10%", "igst": "18%"},
    "omega":        {"hs_code": "1504.20", "description": "Omega 3 / Fish Oil",         "category": "supplements",   "bcd": "10%", "igst": "18%"},
    "serum":        {"hs_code": "3304.99", "description": "Face Serums",                "category": "cosmetics",     "bcd": "20%", "igst": "28%"},
    "moisturizer":  {"hs_code": "3304.99", "description": "Moisturizers & Creams",      "category": "cosmetics",     "bcd": "20%", "igst": "28%"},
    "perfume":      {"hs_code": "3303.00", "description": "Perfumes & Fragrances",      "category": "cosmetics",     "bcd": "20%", "igst": "28%"},
    "lipstick":     {"hs_code": "3304.10", "description": "Lipstick & Lip Products",    "category": "cosmetics",     "bcd": "20%", "igst": "28%"},
    "shampoo":      {"hs_code": "3305.10", "description": "Shampoos & Hair Care",       "category": "cosmetics",     "bcd": "20%", "igst": "28%"},
    "sunscreen":    {"hs_code": "3304.99", "description": "Sunscreen & SPF Products",   "category": "cosmetics",     "bcd": "20%", "igst": "28%"},
    "book":         {"hs_code": "4901.99", "description": "Books & Publications",       "category": "books",         "bcd": "0%",  "igst": "0%"},
    "novel":        {"hs_code": "4901.99", "description": "Novels & Fiction Books",     "category": "books",         "bcd": "0%",  "igst": "0%"},
    "textbook":     {"hs_code": "4901.10", "description": "Textbooks & Educational",    "category": "books",         "bcd": "0%",  "igst": "0%"},
    "toy":          {"hs_code": "9503.00", "description": "Toys & Play Items",          "category": "toys",          "bcd": "60%", "igst": "12%"},
    "lego":         {"hs_code": "9503.00", "description": "LEGO Building Blocks",       "category": "toys",          "bcd": "60%", "igst": "12%"},
    "doll":         {"hs_code": "9502.10", "description": "Dolls & Accessories",        "category": "toys",          "bcd": "60%", "igst": "12%"},
    "puzzle":       {"hs_code": "9503.00", "description": "Puzzles & Brain Teasers",    "category": "toys",          "bcd": "60%", "igst": "12%"},
    "coffee":       {"hs_code": "0901.21", "description": "Coffee Beans / Ground",      "category": "food",          "bcd": "30%", "igst": "12%"},
    "chocolate":    {"hs_code": "1806.32", "description": "Chocolates & Confectionery", "category": "food",          "bcd": "30%", "igst": "12%"},
    "honey":        {"hs_code": "0409.00", "description": "Natural Honey",              "category": "food",          "bcd": "30%", "igst": "12%"},
    "nuts":         {"hs_code": "0802.32", "description": "Nuts & Dry Fruits",          "category": "food",          "bcd": "30%", "igst": "12%"},
    "necklace":     {"hs_code": "7117.19", "description": "Necklaces & Chains",         "category": "jewelry",       "bcd": "15%", "igst": "3%"},
    "ring":         {"hs_code": "7117.19", "description": "Rings & Bands",              "category": "jewelry",       "bcd": "15%", "igst": "3%"},
    "bracelet":     {"hs_code": "7117.19", "description": "Bracelets & Bangles",        "category": "jewelry",       "bcd": "15%", "igst": "3%"},
    "earrings":     {"hs_code": "7117.19", "description": "Earrings",                   "category": "jewelry",       "bcd": "15%", "igst": "3%"},
    "bag":          {"hs_code": "4202.22", "description": "Handbags & Purses",          "category": "bags",          "bcd": "20%", "igst": "18%"},
    "backpack":     {"hs_code": "4202.92", "description": "Backpacks",                  "category": "bags",          "bcd": "20%", "igst": "18%"},
    "suitcase":     {"hs_code": "4202.12", "description": "Suitcases & Luggage",        "category": "bags",          "bcd": "20%", "igst": "18%"},
    "wallet":       {"hs_code": "4202.31", "description": "Wallets & Cardholders",      "category": "bags",          "bcd": "20%", "igst": "18%"},
    "camera":       {"hs_code": "8525.80", "description": "Digital Cameras",            "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "drone":        {"hs_code": "8806.21", "description": "Unmanned Aircraft / Drones", "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "speaker":      {"hs_code": "8518.22", "description": "Loudspeakers",               "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "keyboard":     {"hs_code": "8471.60", "description": "Keyboards",                  "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "mouse":        {"hs_code": "8471.60", "description": "Computer Mouse",             "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "charger":      {"hs_code": "8504.40", "description": "Battery Chargers",           "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "power bank":   {"hs_code": "8507.60", "description": "Power Banks",                "category": "electronics",   "bcd": "20%", "igst": "18%"},
    "monitor":      {"hs_code": "8528.52", "description": "Computer Monitors",          "category": "electronics",   "bcd": "20%", "igst": "18%"},
}

RESTRICTION_TAGS = {
    "supplements": "⚠️ FSSAI",
    "food":        "⚠️ FSSAI",
    "toys":        "⚠️ BIS",
}


def _local_hs_search(query: str) -> list:
    query   = query.lower().strip()
    results = []
    seen    = set()
    for kw, info in _LOCAL_HS.items():
        if query in kw or query in info["description"].lower():
            if info["hs_code"] not in seen:
                seen.add(info["hs_code"])
                results.append(info)
        if len(results) >= 6:
            break
    return results


def _fetch_hs_results(query: str) -> list:
    """Try Flask backend first, fall back to local dict silently."""
    try:
        resp = requests.get(f"{FLASK_URL}/search-hs", params={"q": query}, timeout=3)
        if resp.status_code == 200:
            return resp.json().get("results", [])
    except Exception:
        pass
    return _local_hs_search(query)


def _render_hs_results(results: list):
    if not results:
        st.markdown(
            '<div style="font-size:11px;color:#555;padding:6px 2px">'
            'No results. Try: headphones, shoes, protein, lego…</div>',
            unsafe_allow_html=True,
        )
        return

    for r in results:
        bcd_val = int(r["bcd"].replace("%", ""))
        if bcd_val >= 30:
            bcd_color = "#EF4444"
        elif bcd_val >= 20:
            bcd_color = "#F97316"
        else:
            bcd_color = "#22C55E"

        restriction_tag  = RESTRICTION_TAGS.get(r["category"], "")
        restriction_html = (
            f'<span style="font-size:10px;background:rgba(239,68,68,0.15);'
            f'color:#EF4444;padding:2px 6px;border-radius:4px;margin-left:2px;'
            f'font-family:\'JetBrains Mono\',monospace;">{restriction_tag}</span>'
            if restriction_tag else ""
        )

        st.markdown(f"""
        <div style="background:#161600;border:1px solid #2A2A00;border-radius:8px;
             padding:10px 12px;margin-bottom:6px;">
            <div style="display:flex;justify-content:space-between;
                 align-items:center;margin-bottom:4px;flex-wrap:wrap;gap:4px;">
                <span style="font-family:'JetBrains Mono',monospace;font-size:12px;
                      color:#F5C400;font-weight:700;">{r['hs_code']}</span>
                <div style="display:flex;gap:4px;align-items:center;flex-wrap:wrap;">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                          background:rgba(239,68,68,0.12);color:{bcd_color};
                          padding:2px 6px;border-radius:4px;">BCD {r['bcd']}</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                          background:rgba(168,85,247,0.12);color:#A855F7;
                          padding:2px 6px;border-radius:4px;">IGST {r['igst']}</span>
                    {restriction_html}
                </div>
            </div>
            <div style="font-size:12px;color:#ccc;margin-bottom:2px;">{r['description']}</div>
            <div style="font-size:10px;color:#444;font-family:'JetBrains Mono',monospace;">
                {r['category'].upper().replace('_', ' ')}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:

        # ── Logo / Title ──────────────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center; padding:20px 0 10px;">
            <div style="font-size:40px; margin-bottom:8px;">🛃</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px;
                 letter-spacing:3px; color:#F5C400; text-transform:uppercase;">
                True Cost Calculator
            </div>
            <div style="font-size:11px; color:#555; margin-top:4px;">
                v1.0 · India Import Intelligence
            </div>
        </div>
        <hr style="border-color:#222; margin:12px 0 16px"/>
        """, unsafe_allow_html=True)

        # ── HS CODE SEARCH (NEW) ──────────────────────────────────────────
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:10px;
             letter-spacing:2px; color:#F5C400; text-transform:uppercase;
             margin-bottom:8px;">
            🔎 Search HS Code
        </div>
        """, unsafe_allow_html=True)

        query = st.text_input(
            label="hs_search_label",
            label_visibility="collapsed",
            placeholder="e.g. headphones, shoes, protein...",
            key="hs_search_input",
        )

        if query and len(query) >= 2:
            results = _fetch_hs_results(query)
            _render_hs_results(results)
        elif query:
            st.markdown(
                '<div style="font-size:11px;color:#555;padding:4px 2px">Keep typing…</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<hr style='border-color:#222; margin:16px 0'/>", unsafe_allow_html=True)

        # ── Duty Rates Reference ──────────────────────────────────────────
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:10px;
             letter-spacing:2px; color:#F5C400; text-transform:uppercase;
             margin-bottom:12px;">
            📋 Duty Rates (CBIC)
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <table class="duty-table">
            <thead>
                <tr>
                    <th>Category</th>
                    <th>BCD</th>
                    <th>IGST</th>
                    <th>⚠️</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Electronics</td>
                    <td><span class="rate-badge rate-medium">20%</span></td>
                    <td><span class="rate-badge rate-medium">18%</span></td>
                    <td><span class="restrict-no">No</span></td>
                </tr>
                <tr>
                    <td>Clothing</td>
                    <td><span class="rate-badge rate-medium">20%</span></td>
                    <td><span class="rate-badge rate-low">12%</span></td>
                    <td><span class="restrict-no">No</span></td>
                </tr>
                <tr>
                    <td>Footwear</td>
                    <td><span class="rate-badge rate-medium">25%</span></td>
                    <td><span class="rate-badge rate-medium">18%</span></td>
                    <td><span class="restrict-no">No</span></td>
                </tr>
                <tr>
                    <td>Supplements</td>
                    <td><span class="rate-badge rate-low">10%</span></td>
                    <td><span class="rate-badge rate-medium">18%</span></td>
                    <td><span class="restrict-yes">FSSAI</span></td>
                </tr>
                <tr>
                    <td>Cosmetics</td>
                    <td><span class="rate-badge rate-medium">20%</span></td>
                    <td><span class="rate-badge rate-high">28%</span></td>
                    <td><span class="restrict-no">No</span></td>
                </tr>
                <tr>
                    <td>Books</td>
                    <td><span class="rate-badge rate-zero">0%</span></td>
                    <td><span class="rate-badge rate-zero">0%</span></td>
                    <td><span class="restrict-no">No</span></td>
                </tr>
                <tr>
                    <td>Toys</td>
                    <td><span class="rate-badge rate-high">60%</span></td>
                    <td><span class="rate-badge rate-low">12%</span></td>
                    <td><span class="restrict-yes">BIS</span></td>
                </tr>
                <tr>
                    <td>Food</td>
                    <td><span class="rate-badge rate-high">30%</span></td>
                    <td><span class="rate-badge rate-low">12%</span></td>
                    <td><span class="restrict-yes">FSSAI</span></td>
                </tr>
                <tr>
                    <td>Watches</td>
                    <td><span class="rate-badge rate-medium">20%</span></td>
                    <td><span class="rate-badge rate-medium">18%</span></td>
                    <td><span class="restrict-no">No</span></td>
                </tr>
                <tr>
                    <td>Jewelry</td>
                    <td><span class="rate-badge rate-low">15%</span></td>
                    <td><span class="rate-badge rate-zero">3%</span></td>
                    <td><span class="restrict-no">No</span></td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#222; margin:18px 0'/>", unsafe_allow_html=True)

        # ── Formula Box ───────────────────────────────────────────────────
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:10px;
             letter-spacing:2px; color:#F5C400; text-transform:uppercase;
             margin-bottom:10px;">
            🧮 Duty Formula
        </div>
        <div style="background:#111; border:1px solid #222; border-radius:8px;
             padding:12px 14px; font-family:'JetBrains Mono',monospace; font-size:11px;
             color:#ccc; line-height:1.9;">
            <span style="color:#4A9EFF">AV</span>  = Price(INR) + Ship<br/>
            <span style="color:#F97316">BCD</span> = AV × rate%<br/>
            <span style="color:#FB923C">SWS</span> = BCD × 10%<br/>
            <span style="color:#A855F7">IGST</span>= (AV+BCD+SWS) × 18%<br/>
            <hr style="border-color:#333; margin:6px 0"/>
            <span style="color:#F5C400; font-weight:700">TOTAL = AV+BCD+SWS+IGST</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#222; margin:18px 0'/>", unsafe_allow_html=True)

        # ── Shipping Reference ────────────────────────────────────────────
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:10px;
             letter-spacing:2px; color:#F5C400; text-transform:uppercase;
             margin-bottom:10px;">
            🚢 Shipping Estimates
        </div>
        <div style="font-size:12px; color:#888; line-height:2;">
            🇨🇳 AliExpress — Free · 15–35 days<br/>
            🇺🇸 Amazon US — ₹1,200 · 10–20 days<br/>
            👗 SHEIN — Free · 12–25 days<br/>
            💊 iHerb — ₹600 · 8–15 days<br/>
            🌐 eBay — ₹900 · 14–30 days
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#222; margin:18px 0'/>", unsafe_allow_html=True)

        # ── Restriction Legend ────────────────────────────────────────────
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:10px;
             letter-spacing:2px; color:#F5C400; text-transform:uppercase;
             margin-bottom:10px;">
            ⚠️ Import Restrictions
        </div>
        <div style="font-size:12px; color:#888; line-height:2;">
            <span style="color:#EF4444; font-weight:700">FSSAI</span> — Food Safety permit required<br/>
            <span style="color:#EF4444; font-weight:700">BIS</span> — Quality certification needed<br/>
            <span style="color:#22C55E; font-weight:700">No restriction</span> — Standard clearance
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#222; margin:18px 0'/>", unsafe_allow_html=True)

        # ── Disclaimer ────────────────────────────────────────────────────
        st.markdown("""
        <div style="font-size:10px; color:#444; line-height:1.7; text-align:center;">
            Rates sourced from CBIC tariff schedule.<br/>
            For estimation only. Consult a customs<br/>
            broker for high-value imports.
        </div>
        """, unsafe_allow_html=True)