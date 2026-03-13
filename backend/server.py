import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from services.duty_table   import calculate_landed_cost, search_hs_code, get_duty_info
from services.restrictions import check_restrictions
from services.currency     import get_usd_to_inr
from services.scraper      import scrape_product
from agents.duty_agent     import get_recommendation
from agents.price_agent    import get_indian_price

app = Flask(__name__)
CORS(app)


# ─────────────────────────────────────────────────────────────────────────────
# POST /analyze  — Main calculation endpoint
# ─────────────────────────────────────────────────────────────────────────────
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    product_name     = data.get("product_name", "Unknown Product")
    url              = data.get("url", "")
    price_usd        = float(data.get("price_usd", 0))
    source_site      = data.get("source_site", "amazon_us")
    category         = data.get("category", "electronics")
    detected_hs      = data.get("detected_hs", "")
    indian_price_inp = data.get("indian_price_inr")

    steps = []

    # ── Step 1: Currency ─────────────────────────────────────────────────────
    fx_rate = get_usd_to_inr()
    steps.append({"step": "currency", "status": "done",
                  "message": f"$1 = ₹{fx_rate:.2f} (live)"})

    # ── Step 2: Scraping ─────────────────────────────────────────────────────
    scraped    = scrape_product(url, product_name)
    final_name = scraped["name"]
    steps.append({"step": "scraping", "status": "done",
                  "message": f"Using {scraped['source']} product name"})

    # ── Step 3: HSN Lookup ───────────────────────────────────────────────────
    duty_info = get_duty_info(category)
    if detected_hs:
        duty_info["hs_code"] = detected_hs
    steps.append({"step": "hsn_lookup", "status": "done",
                  "message": f"HS {duty_info['hs_code']} — {duty_info['label']}"})

    # ── Step 4: Duty Calculation ─────────────────────────────────────────────
    price_inr   = price_usd * fx_rate
    cost        = calculate_landed_cost(price_inr, category)
    steps.append({"step": "duty_calc", "status": "done",
                  "message": f"BCD {cost['duty_rate_percent']:.0f}% + SWS 10% + IGST {cost['igst_rate_percent']:.0f}%"})

    # ── Step 5: Restrictions ─────────────────────────────────────────────────
    restriction = check_restrictions(category)
    steps.append({"step": "restrictions", "status": "done",
                  "message": "Restriction found ⚠️" if restriction["restricted"] else "No restrictions"})

    # ── Step 6: Indian Price ─────────────────────────────────────────────────
    india_result = get_indian_price(final_name, indian_price_inp)
    indian_price = india_result["price"]
    indian_src   = india_result["source"]
    if indian_price:
        steps.append({"step": "price_compare", "status": "done",
                      "message": f"₹{indian_price:,.0f} on {indian_src}"})
    else:
        steps.append({"step": "price_compare", "status": "done",
                      "message": "Not found — add manually for comparison"})

    # ── Step 7: AI Recommendation ────────────────────────────────────────────
    ai_text = get_recommendation(
        final_name,
        cost["total_landed_cost"],
        indian_price,
        category,
        restriction["restricted"],
        restriction["note"],
    )
    steps.append({"step": "ai_reasoning", "status": "done",
                  "message": "Recommendation ready"})

    # ── Verdict ──────────────────────────────────────────────────────────────
    total   = cost["total_landed_cost"]
    savings = None
    verdict = "NEUTRAL"

    if indian_price:
        savings = round(indian_price - total, 2)
        if savings > 500:
            verdict = "BUY_ABROAD"
        elif savings < -500:
            verdict = "BUY_LOCAL"
        else:
            verdict = "CLOSE_CALL"

    return jsonify({
        "product_name":      final_name,
        "source_site":       source_site,
        "currency_rate":     fx_rate,
        "price_usd":         price_usd,
        "cost_breakdown":    cost,
        "indian_price":      indian_price,
        "indian_source":     indian_src,
        "verdict":           verdict,
        "savings":           savings,
        "restricted":        restriction["restricted"],
        "restriction_note":  restriction["note"],
        "delivery_estimate": cost.get("delivery", "10–20 days"),
        "ai_reasoning":      ai_text,
        "agent_steps":       steps,
    })


# ─────────────────────────────────────────────────────────────────────────────
# GET /search-hs?q=headphones  — HS Code search endpoint
# ─────────────────────────────────────────────────────────────────────────────
@app.route("/search-hs", methods=["GET"])
def search_hs():
    query   = request.args.get("q", "").strip()
    if not query or len(query) < 2:
        return jsonify({"results": []})

    results = search_hs_code(query)
    return jsonify({"query": query, "results": results})


# ─────────────────────────────────────────────────────────────────────────────
# GET /health  — Health check
# ─────────────────────────────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "True Cost Calculator API running"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)