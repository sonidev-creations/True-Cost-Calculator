DUTY_RULES = {
    "electronics": {
        "bcd": 20.0, "igst": 18.0,
        "hs": "8471", "label": "Electronics & Gadgets"
    },
    "mobile_phones": {
        "bcd": 20.0, "igst": 18.0,
        "hs": "8517", "label": "Mobile Phones"
    },
    "clothing": {
        "bcd": 20.0, "igst": 12.0,
        "hs": "6109", "label": "Clothing & Apparel"
    },
    "footwear": {
        "bcd": 25.0, "igst": 18.0,
        "hs": "6403", "label": "Footwear & Shoes"
    },
    "supplements": {
        "bcd": 10.0, "igst": 18.0,
        "hs": "2106", "label": "Health Supplements"
    },
    "cosmetics": {
        "bcd": 20.0, "igst": 28.0,
        "hs": "3304", "label": "Cosmetics & Skincare"
    },
    "books": {
        "bcd": 0.0,  "igst": 0.0,
        "hs": "4901", "label": "Books & Printed Matter"
    },
    "toys": {
        "bcd": 60.0, "igst": 12.0,
        "hs": "9503", "label": "Toys & Games"
    },
    "watches": {
        "bcd": 20.0, "igst": 18.0,
        "hs": "9102", "label": "Watches"
    },
    "food": {
        "bcd": 30.0, "igst": 12.0,
        "hs": "2008", "label": "Food & Edibles"
    },
    "jewelry": {
        "bcd": 15.0, "igst": 3.0,
        "hs": "7113", "label": "Jewelry"
    },
    "bags": {
        "bcd": 20.0, "igst": 18.0,
        "hs": "4202", "label": "Bags & Luggage"
    },
}
 
SHIPPING_ESTIMATE_INR = 1200.0  # flat shipping estimate when not provided
 
 
def calculate(
    price_usd: float,
    category: str,
    currency_rate: float,
    shipping_inr: float = SHIPPING_ESTIMATE_INR,
) -> dict:
    """
    Calculates full India landed cost using the official CBIC formula:
 
        AV   = Price(INR) + Shipping              ← Assessable Value
        BCD  = AV × BCD_rate%                     ← Basic Customs Duty
        SWS  = BCD × 10%                          ← Social Welfare Surcharge
        IGST = (AV + BCD + SWS) × IGST_rate%     ← Integrated GST
        ──────────────────────────────────────────
        TOTAL LANDED = AV + BCD + SWS + IGST
 
    Args:
        price_usd      : Product price in US dollars
        category       : Product category key (from DUTY_RULES)
        currency_rate  : Current USD → INR exchange rate
        shipping_inr   : Estimated shipping cost in INR
 
    Returns:
        dict with all cost components and metadata
    """
    rules = DUTY_RULES.get(category, DUTY_RULES["electronics"])
 
    price_inr        = round(price_usd * currency_rate, 2)
    assessable_value = round(price_inr + shipping_inr, 2)
 
    bcd  = round(assessable_value * (rules["bcd"] / 100), 2)
    sws  = round(bcd * 0.10, 2)                               # 10% of BCD
 
    igst_base = assessable_value + bcd + sws
    igst      = round(igst_base * (rules["igst"] / 100), 2)
 
    total = round(assessable_value + bcd + sws + igst, 2)
 
    print(f"[duty] {category} | ₹{price_inr} + ship ₹{shipping_inr} | "
          f"BCD ₹{bcd} | SWS ₹{sws} | IGST ₹{igst} | TOTAL ₹{total}")
 
    return {
        "price_inr":                 price_inr,
        "assessable_value":          assessable_value,
        "basic_customs_duty":        bcd,
        "social_welfare_surcharge":  sws,
        "igst":                      igst,
        "shipping_cost":             shipping_inr,
        "total_landed_cost":         total,
        "duty_rate_percent":         rules["bcd"],
        "igst_rate_percent":         rules["igst"],
        "hs_code":                   rules["hs"],
        "category_label":            rules["label"],
    }
 