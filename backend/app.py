"""
True Cost Calculator — Flask Backend
=====================================
Runs on: http://localhost:5000

Endpoints:
    GET  /health            → health check
    POST /analyze           → full cost analysis pipeline
    GET  /hs-lookup         → lookup HS code by product name
    GET  /hs-codes          → get all HS codes database
    POST /compare-countries → compare import costs across countries
    GET  /history           → get past calculations
    GET  /history/stats     → summary stats
"""

# ── ADDED: import os for SQLite path ──
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from services.currency        import get_usd_to_inr
from services.duty_calculator import calculate
from services.restrictions    import check as check_restrictions
from services.scraper         import scrape_product
from services.price_compare   import search_india_price
from services.ai_agent        import get_reasoning
from services.hs_lookup       import lookup_by_name, get_all_codes
# ── ADDED: database imports ──
from services.database        import db, Calculation, HSSearchLog, save_calculation, save_hs_log

load_dotenv()

app = Flask(__name__)
CORS(app)

# ── ADDED: SQLite config ──
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'truecost.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    print("[db] SQLite tables ready  ->  truecost.db")

# ─── Constants ────────────────────────────────────────────────────────────────
DELIVERY_MAP = {
    "amazon_us":  "7-14 days",
    "aliexpress": "15-30 days",
    "shein":      "10-20 days",
    "iherb":      "7-14 days",
    "ebay":       "10-25 days",
    "walmart":    "10-20 days",
    "other":      "10-25 days",
}

# Country-specific duty/tax rates for comparison
COUNTRY_RATES = {
    "India":     {"bcd": 20,  "gst": 18,  "symbol": "₹",   "fx_to_usd": 83.5,   "flag": "🇮🇳"},
    "USA":       {"bcd": 0,   "gst": 8,   "symbol": "$",   "fx_to_usd": 1.0,    "flag": "🇺🇸"},
    "UK":        {"bcd": 4,   "gst": 20,  "symbol": "£",   "fx_to_usd": 1.27,   "flag": "🇬🇧"},
    "UAE":       {"bcd": 5,   "gst": 5,   "symbol": "د.إ", "fx_to_usd": 3.67,   "flag": "🇦🇪"},
    "Singapore": {"bcd": 0,   "gst": 9,   "symbol": "S$",  "fx_to_usd": 1.35,   "flag": "🇸🇬"},
    "Germany":   {"bcd": 3.7, "gst": 19,  "symbol": "€",   "fx_to_usd": 1.08,   "flag": "🇩🇪"},
    "Australia": {"bcd": 5,   "gst": 10,  "symbol": "A$",  "fx_to_usd": 0.65,   "flag": "🇦🇺"},
    "Canada":    {"bcd": 0,   "gst": 13,  "symbol": "C$",  "fx_to_usd": 0.74,   "flag": "🇨🇦"},
    "Japan":     {"bcd": 0,   "gst": 10,  "symbol": "¥",   "fx_to_usd": 0.0067, "flag": "🇯🇵"},
    "China":     {"bcd": 7,   "gst": 13,  "symbol": "¥",   "fx_to_usd": 7.24,   "flag": "🇨🇳"},
}


# ─── Helpers ──────────────────────────────────────────────────────────────────
def _parse_price(value, field="price_usd"):
    try:
        v = float(value)
        if v <= 0:
            raise ValueError
        return v, None
    except (TypeError, ValueError):
        return None, {"error": f"Invalid {field}"}


def _compute_landed_cost(price_usd: float, bcd_pct: float, gst_pct: float, fx: float) -> dict:
    """Generic landed-cost formula (no SWS — that's India-specific)."""
    price_local = price_usd * fx
    bcd         = price_local * (bcd_pct / 100)
    gst         = (price_local + bcd) * (gst_pct / 100)
    total       = price_local + bcd + gst
    return {
        "price_local": round(price_local, 2),
        "bcd":         round(bcd, 2),
        "gst":         round(gst, 2),
        "total_usd":   round(total / fx, 2),
        "total_local": round(total, 2),
    }


def _build_country_comparison(price_usd: float, bcd_pct: float, gst_pct: float) -> list:
    """Build a ranked list of countries by total landed cost in USD."""
    results = []
    for country, info in COUNTRY_RATES.items():
        b = bcd_pct if country == "India" else info["bcd"]
        g = gst_pct if country == "India" else info["gst"]
        breakdown = _compute_landed_cost(price_usd, b, g, info["fx_to_usd"])
        results.append({
            "country":     country,
            "flag":        info["flag"],
            "symbol":      info["symbol"],
            "bcd_pct":     b,
            "gst_pct":     g,
            "total_usd":   breakdown["total_usd"],
            "total_local": breakdown["total_local"],
            "breakdown":   breakdown,
        })
    results.sort(key=lambda x: x["total_usd"])
    return results


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    # ── ADDED: show DB status ──
    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"

    return jsonify({
        "status":    "ok",
        "message":   "True Cost Calculator API is running",
        "version":   "1.2.0",
        "database":  db_status,
        "endpoints": ["/health", "/analyze", "/hs-lookup", "/hs-codes",
                      "/compare-countries", "/history", "/history/stats"],
    })


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    product_name     = str(data.get("product_name", "Unknown Product")).strip()
    price_usd        = data.get("price_usd")
    category         = str(data.get("category", "electronics")).strip()
    source_site      = str(data.get("source_site", "other")).strip()
    url              = str(data.get("url", "")).strip()
    indian_price_inr = data.get("indian_price_inr")

    price_usd, err = _parse_price(price_usd)
    if err:
        return jsonify(err), 400

    agent_steps = []

    # STEP 1 - Currency
    agent_steps.append({"step": "currency", "status": "running", "message": "Fetching..."})
    rate = get_usd_to_inr()
    agent_steps[-1] = {
        "step": "currency", "status": "done",
        "message": f"$1 = Rs{rate:.2f} (live)"
    }

    # STEP 2 - Scrape
    agent_steps.append({"step": "scraping", "status": "running", "message": "Extracting details..."})
    scraped = scrape_product(url)
    if scraped.get("scraped_title"):
        product_name = scraped["scraped_title"][:80]
        scrape_msg   = "Title extracted from URL"
    else:
        scrape_msg = "Using provided product name"
    agent_steps[-1] = {"step": "scraping", "status": "done", "message": scrape_msg}

    # STEP 3 - HSN Lookup
    agent_steps.append({"step": "hsn_lookup", "status": "running", "message": "Looking up HSN..."})
    hs_result = lookup_by_name(product_name)
    cost      = calculate(price_usd, category, rate)

    if hs_result["match_found"]:
        cost["hs_code"]        = hs_result["hs_code"]
        cost["category_label"] = hs_result["description"]
        if hs_result.get("bcd_rate") is not None:
            cost["duty_rate_percent"] = hs_result["bcd_rate"]
        if hs_result.get("igst_rate") is not None:
            cost["igst_rate_percent"] = hs_result["igst_rate"]

    # ── ADDED: log HS lookup to DB ──
    try:
        save_hs_log(product_name, hs_result)
    except Exception as e:
        print(f"[db] HS log warning: {e}")

    agent_steps[-1] = {
        "step": "hsn_lookup", "status": "done",
        "message": f"HS {cost['hs_code']} - {cost['category_label']}"
    }

    # STEP 4 - Duty Calculation
    agent_steps.append({"step": "duty_calc", "status": "running", "message": "Calculating duties..."})
    agent_steps[-1] = {
        "step": "duty_calc", "status": "done",
        "message": f"BCD {cost['duty_rate_percent']:.0f}% + SWS 10% + IGST {cost['igst_rate_percent']:.0f}%"
    }

    # STEP 5 - Restrictions
    agent_steps.append({"step": "restrictions", "status": "running", "message": "Checking rules..."})
    restriction_info = check_restrictions(category)
    agent_steps[-1] = {
        "step": "restrictions", "status": "done",
        "message": "Restrictions found!" if restriction_info["restricted"] else "No restrictions"
    }

    # STEP 6 - India Price
    agent_steps.append({"step": "price_compare", "status": "running", "message": "Searching India prices..."})
    india_info    = search_india_price(product_name, indian_price_inr)
    indian_price  = india_info.get("indian_price")
    indian_source = india_info.get("indian_source", "Indian Marketplace")
    agent_steps[-1] = {
        "step": "price_compare", "status": "done",
        "message": f"Rs{indian_price:,.0f} on {indian_source}" if indian_price else "Not found"
    }

    # STEP 7 - Country Comparison
    agent_steps.append({"step": "country_compare", "status": "running", "message": "Comparing countries..."})
    country_comparison = _build_country_comparison(
        price_usd, cost["duty_rate_percent"], cost["igst_rate_percent"]
    )
    agent_steps[-1] = {
        "step": "country_compare", "status": "done",
        "message": f"Best: {country_comparison[0]['country']} @ ${country_comparison[0]['total_usd']:.2f}"
    }

    # STEP 8 - AI Reasoning
    agent_steps.append({"step": "ai_reasoning", "status": "running", "message": "Generating advice..."})
    ai_text = get_reasoning(
        product_name   = product_name,
        category       = category,
        cost_breakdown = cost,
        indian_price   = indian_price,
        restricted     = restriction_info["restricted"],
    )
    agent_steps[-1] = {"step": "ai_reasoning", "status": "done", "message": "Recommendation ready"}

    # Verdict
    total   = cost["total_landed_cost"]
    verdict = "NEUTRAL"
    savings = None

    if indian_price and indian_price > 0:
        savings = indian_price - total
        if savings > 500:
            verdict = "BUY_ABROAD"
        elif savings < -500:
            verdict = "BUY_LOCAL"
        else:
            verdict = "CLOSE_CALL"

    response = {
        "product_name":       product_name,
        "currency_rate":      rate,
        "cost_breakdown":     cost,
        "indian_price":       indian_price,
        "indian_source":      indian_source,
        "verdict":            verdict,
        "savings":            savings,
        "restricted":         restriction_info["restricted"],
        "restriction_note":   restriction_info["restriction_note"],
        "delivery_estimate":  DELIVERY_MAP.get(source_site, "10-25 days"),
        "ai_reasoning":       ai_text,
        "agent_steps":        agent_steps,
        "country_comparison": country_comparison,
        "hs_lookup": {
            "hs_code":         cost["hs_code"],
            "description":     cost["category_label"],
            "matched_keyword": hs_result.get("matched_keyword"),
            "match_found":     hs_result.get("match_found", False),
        },
    }

    # ── ADDED: save full result to SQLite ──
    try:
        record = save_calculation(
            response      = response,
            price_usd     = price_usd,
            category      = category,
            source_site   = source_site,
            currency_rate = rate,
        )
        response["history_id"] = record.id
        print(f"[db] Saved  id={record.id}  product='{product_name}'  verdict={verdict}")
    except Exception as e:
        print(f"[db] WARNING: could not save — {e}")

    print(f"\n[app] Analysis complete for '{product_name}' | Total Rs{total:,.0f} | Verdict: {verdict}\n")
    return jsonify(response), 200


@app.route("/compare-countries", methods=["POST"])
def compare_countries():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    price_usd, err = _parse_price(data.get("price_usd"))
    if err:
        return jsonify(err), 400

    bcd_pct    = float(data.get("bcd_pct", 20))
    gst_pct    = float(data.get("gst_pct", 18))
    comparison = _build_country_comparison(price_usd, bcd_pct, gst_pct)
    return jsonify({
        "price_usd":  price_usd,
        "bcd_pct":    bcd_pct,
        "gst_pct":    gst_pct,
        "comparison": comparison,
        "cheapest":   comparison[0] if comparison else None,
    }), 200


@app.route("/hs-lookup", methods=["GET"])
def hs_lookup():
    product = request.args.get("product", "").strip()
    if not product:
        return jsonify({
            "error":    "Missing product name",
            "usage":    "/hs-lookup?product=your+product+name",
            "examples": [
                "/hs-lookup?product=sony headphones",
                "/hs-lookup?product=whey protein",
                "/hs-lookup?product=nike shoes",
            ]
        }), 400

    result = lookup_by_name(product)
    return jsonify({
        "query":           product,
        "hs_code":         result["hs_code"],
        "description":     result["description"],
        "bcd_rate":        result["bcd_rate"],
        "igst_rate":       result["igst_rate"],
        "matched_keyword": result["matched_keyword"],
        "match_found":     result["match_found"],
        "source":          "CBIC India Tariff Schedule",
    }), 200


@app.route("/hs-codes", methods=["GET"])
def all_hs_codes():
    category_filter = request.args.get("category", "").strip().lower()
    codes = get_all_codes()
    if category_filter:
        codes = [c for c in codes if category_filter in c["description"].lower()]
    return jsonify({
        "total":  len(codes),
        "filter": category_filter or "none",
        "codes":  codes,
        "source": "CBIC India Tariff Schedule",
    }), 200


# ── ADDED: history routes ──────────────────────────────────────────────────────
@app.route("/history", methods=["GET"])
def history():
    limit    = min(int(request.args.get("limit", 50)), 200)
    offset   = int(request.args.get("offset", 0))
    verdict  = request.args.get("verdict", "").upper()
    category = request.args.get("category", "").lower()

    query = Calculation.query
    if verdict in ("BUY_ABROAD", "BUY_LOCAL", "CLOSE_CALL", "NEUTRAL"):
        query = query.filter(Calculation.verdict == verdict)
    if category:
        query = query.filter(Calculation.category == category)

    total   = query.count()
    records = query.order_by(Calculation.created_at.desc()).offset(offset).limit(limit).all()
    return jsonify({
        "total":   total,
        "limit":   limit,
        "offset":  offset,
        "results": [r.to_dict() for r in records],
    }), 200


@app.route("/history/stats", methods=["GET"])
def history_stats():
    from sqlalchemy import func
    total       = Calculation.query.count()
    hs_total    = HSSearchLog.query.count()
    avg_savings = db.session.query(func.avg(Calculation.savings)).scalar() or 0
    avg_total   = db.session.query(func.avg(Calculation.total_landed)).scalar() or 0
    verdict_counts = dict(
        db.session.query(Calculation.verdict, func.count(Calculation.id))
        .group_by(Calculation.verdict).all()
    )
    top_cats = db.session.query(
        Calculation.category, func.count(Calculation.id).label("n")
    ).group_by(Calculation.category).order_by(db.text("n DESC")).limit(5).all()
    top_hs = db.session.query(
        HSSearchLog.matched_hs_code, HSSearchLog.matched_desc,
        func.count(HSSearchLog.id).label("n")
    ).group_by(HSSearchLog.matched_hs_code).order_by(db.text("n DESC")).limit(5).all()
    return jsonify({
        "total_calculations": total,
        "total_hs_lookups":   hs_total,
        "avg_savings_inr":    round(float(avg_savings), 2),
        "avg_total_landed":   round(float(avg_total), 2),
        "verdict_breakdown":  verdict_counts,
        "top_categories":     [{"category": c, "count": n} for c, n in top_cats],
        "top_hs_codes":       [{"hs_code": h, "description": d, "count": n} for h, d, n in top_hs],
    }), 200


@app.route("/history/<int:record_id>", methods=["GET"])
def history_detail(record_id):
    record = Calculation.query.get_or_404(record_id)
    return jsonify(record.to_dict()), 200


@app.route("/history/<int:record_id>", methods=["DELETE"])
def history_delete(record_id):
    record = Calculation.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"deleted": True, "id": record_id}), 200


# ─── Error Handlers ───────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error":     "Endpoint not found",
        "available": ["/health", "/analyze", "/hs-lookup", "/hs-codes",
                      "/compare-countries", "/history", "/history/stats"],
    }), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  True Cost Calculator - Backend API  v1.2.0")
    print("  Running on     : http://localhost:5000")
    print("  Health check   : http://localhost:5000/health")
    print("  HS Lookup      : http://localhost:5000/hs-lookup?product=headphones")
    print("  All HS Codes   : http://localhost:5000/hs-codes")
    print("  Country Compare: http://localhost:5000/compare-countries")
    print("  History        : http://localhost:5000/history")
    print("  Stats          : http://localhost:5000/history/stats")
    print("=" * 55 + "\n")
    app.run(debug=True, port=5000, host="0.0.0.0")