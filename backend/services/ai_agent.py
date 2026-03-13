import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def get_reasoning(
    product_name: str,
    category: str,
    cost_breakdown: dict,
    indian_price: float,
    restricted: bool,
) -> str:
    """Groq AI reasoning with strong fallback."""

    api_key = os.getenv("GROQ_API_KEY", "")
    if api_key and api_key != "your_groq_apikey":
        result = _call_groq(api_key, product_name, category,
                            cost_breakdown, indian_price, restricted)
        if result:
            return result

    return _fallback_reasoning(cost_breakdown, indian_price, restricted)


def _call_groq(api_key, product_name, category, cost, indian_price, restricted):
    try:
        total = cost.get("total_landed_cost", 0)
        bcd   = cost.get("basic_customs_duty", 0)
        sws   = cost.get("social_welfare_surcharge", 0)
        igst  = cost.get("igst", 0)
        rate  = cost.get("duty_rate_percent", 20)
        hs    = cost.get("hs_code", "")

        if indian_price and indian_price > 0:
            diff         = indian_price - total
            compare_line = (
                f"Indian market price is ₹{indian_price:,.0f}. "
                f"{'Importing saves ₹' + f'{diff:,.0f}.' if diff > 0 else 'Buying locally saves ₹' + f'{abs(diff):,.0f}.'}"
            )
        else:
            compare_line = "Indian market price not available."

        prompt = f"""You are an India customs and import expert advisor.

Product: {product_name}
HS Code: {hs}
Category: {category}
Price after all import duties: ₹{total:,.0f}
  Basic Customs Duty ({rate:.0f}%): ₹{bcd:,.0f}
  Social Welfare Surcharge: ₹{sws:,.0f}
  IGST: ₹{igst:,.0f}
{compare_line}
Import restrictions: {"YES - clearance needed" if restricted else "None"}

Give a clear 2-3 sentence buying recommendation for an Indian consumer.
Mention specific rupee amounts. Be direct. No bullet points. Plain text only."""

        client   = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model       = "llama3-8b-8192",
            messages    = [{"role": "user", "content": prompt}],
            max_tokens  = 200,
            temperature = 0.4,
        )
        text = response.choices[0].message.content.strip()
        print(f"[ai_agent] Groq OK: {text[:60]}...")
        return text

    except Exception as e:
        print(f"[ai_agent] Groq failed: {e}")
        return None


def _fallback_reasoning(cost_breakdown, indian_price, restricted=False):
    """Rule-based reasoning when Groq is unavailable."""
    total = cost_breakdown.get("total_landed_cost", 0)
    bcd   = cost_breakdown.get("basic_customs_duty", 0)
    rate  = cost_breakdown.get("duty_rate_percent", 20)
    igst  = cost_breakdown.get("igst", 0)
    label = cost_breakdown.get("category_label", "this product")
    hs    = cost_breakdown.get("hs_code", "")

    restriction_note = (
        " ⚠️ Note: Import restrictions apply — check FSSAI/BIS requirements before ordering."
        if restricted else ""
    )

    if indian_price and indian_price > 0:
        diff = indian_price - total

        if diff > 1000:
            return (
                f"Buying abroad is the better deal for {label} (HS {hs}). "
                f"After paying ₹{bcd:,.0f} BCD ({rate:.0f}%) and ₹{igst:,.0f} IGST, "
                f"the total landed cost is ₹{total:,.0f} — saving you ₹{diff:,.0f} "
                f"compared to the Indian price of ₹{indian_price:,.0f}.{restriction_note}"
            )
        elif diff < -1000:
            return (
                f"Buy locally in India — it is cheaper by ₹{abs(diff):,.0f}. "
                f"Import duties add ₹{bcd:,.0f} BCD ({rate:.0f}%) and ₹{igst:,.0f} IGST, "
                f"pushing the landed cost to ₹{total:,.0f} versus ₹{indian_price:,.0f} locally. "
                f"You also avoid customs delays and warranty issues.{restriction_note}"
            )
        else:
            return (
                f"This is a close call — only ₹{abs(diff):,.0f} difference. "
                f"Importing costs ₹{total:,.0f} (after {rate:.0f}% BCD + 18% IGST) "
                f"versus ₹{indian_price:,.0f} locally. "
                f"Factor in delivery time, warranty, and after-sales service.{restriction_note}"
            )

    return (
        f"Total landed cost for {label} (HS {hs}) is ₹{total:,.0f} "
        f"including {rate:.0f}% BCD (₹{bcd:,.0f}) and 18% IGST (₹{igst:,.0f}). "
        f"Search Amazon India or Flipkart to compare before deciding.{restriction_note}"
    )