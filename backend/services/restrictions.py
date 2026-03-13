RESTRICTIONS = {
    "supplements": {
        "restricted": True,
        "note": (
            "⚠️ Health supplements require FSSAI import clearance under the Food Safety "
            "and Standards Act 2006. Products must carry a valid FSSAI license number. "
            "Personal imports of up to 3 months' supply are generally allowed without "
            "a formal license under the personal use exemption. Commercial imports "
            "require a No Objection Certificate (NOC) from FSSAI."
        ),
    },
    "food": {
        "restricted": True,
        "note": (
            "⚠️ Food items require FSSAI import permit and must comply with the Food "
            "Safety and Standards (Import) Regulations 2017. All packaged foods must "
            "carry FSSAI-compliant labeling including ingredients, allergens, and "
            "nutritional info in English. Perishables require cold-chain compliance "
            "and may be subject to phytosanitary inspection."
        ),
    },
    "toys": {
        "restricted": True,
        "note": (
            "⚠️ Toys for children under 14 years require BIS (Bureau of Indian Standards) "
            "certification under IS 9873 / IS 15644. Non-BIS certified toys are banned "
            "from import since January 2021 under the Toys (Quality Control) Order 2020. "
            "Adult collectibles and hobby items above age 14 are generally exempt. "
            "Seized non-compliant toys may be destroyed at the importer's cost."
        ),
    },
    "mobile_phones": {
        "restricted": False,
        "note": (
            "✅ Mobile phones have no major import restrictions. Standard customs duty "
            "and IGST apply. Ensure the device supports Indian frequency bands (4G LTE "
            "Band 3/5/40) for full network compatibility. Warranty may be void outside "
            "country of purchase."
        ),
    },
    "cosmetics": {
        "restricted": False,
        "note": (
            "✅ Cosmetics are generally unrestricted for personal import. Products "
            "containing certain restricted ingredients (e.g., hydroquinone above 2%, "
            "tretinoin) may require a prescription. Import of animal-tested cosmetics "
            "from cruelty-free certified brands is preferred under BIS guidelines."
        ),
    },
    "electronics": {
        "restricted": False,
        "note": (
            "✅ Electronics have no major import restrictions for personal use. "
            "Commercial imports of certain items (drones, radio equipment) may require "
            "WPC (Wireless Planning & Coordination) type approval. "
            "BIS certification required for some products under CRS scheme."
        ),
    },
    "clothing": {
        "restricted": False,
        "note": "✅ No import restrictions on clothing and apparel. Standard customs clearance applies.",
    },
    "footwear": {
        "restricted": False,
        "note": "✅ No import restrictions on footwear. Standard customs clearance applies.",
    },
    "books": {
        "restricted": False,
        "note": (
            "✅ Books and printed matter are freely importable with zero BCD and zero IGST. "
            "Obscene or seditious publications are prohibited under the Customs Act."
        ),
    },
    "watches": {
        "restricted": False,
        "note": "✅ No import restrictions on watches. Standard duty and customs clearance applies.",
    },
    "jewelry": {
        "restricted": False,
        "note": (
            "✅ Jewelry can be imported with standard duty. Passengers arriving in India "
            "can carry jewelry duty-free up to ₹50,000 (men) or ₹1,00,000 (women) "
            "under the baggage rules. Courier/mail imports are subject to full duty."
        ),
    },
    "bags": {
        "restricted": False,
        "note": "✅ No import restrictions on bags and luggage. Standard customs clearance applies.",
    },
}
 
 
def check(category: str) -> dict:
    """
    Returns import restriction status and advisory note for a product category.
 
    Args:
        category : Product category key
 
    Returns:
        dict with 'restricted' (bool) and 'restriction_note' (str)
    """
    info = RESTRICTIONS.get(
        category,
        {
            "restricted": False,
            "note": "✅ No known import restrictions — standard customs clearance applies.",
        },
    )
 
    print(f"[restrictions] {category} → restricted={info['restricted']}")
 
    return {
        "restricted":       info["restricted"],
        "restriction_note": info["note"],
    }
 