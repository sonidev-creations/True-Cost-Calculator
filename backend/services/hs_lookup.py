
import re   
# ─── Comprehensive HS Code Database (CBIC India) ──────────────────────────────
HS_DATABASE: list[dict] = [
    # Electronics & Gadgets
    {"hs_code": "8471.30", "description": "Laptops / Portable Computers",      "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["laptop", "notebook", "macbook", "chromebook", "ultrabook", "computer"]},
    {"hs_code": "8517.12", "description": "Mobile Phones / Smartphones",        "bcd_rate": 20, "igst_rate": 18, "category": "mobile_phones",  "keywords": ["phone", "smartphone", "iphone", "android", "mobile", "pixel", "samsung galaxy", "oneplus"]},
    {"hs_code": "8518.30", "description": "Headphones / Earphones",             "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["headphone", "earphone", "earbud", "airpod", "headset", "tws", "in-ear", "over-ear"]},
    {"hs_code": "8519.81", "description": "Bluetooth Speakers",                 "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["speaker", "bluetooth speaker", "soundbar", "subwoofer", "jbl", "bose speaker"]},
    {"hs_code": "8528.72", "description": "Monitors / Display Screens",         "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["monitor", "display", "screen", "lcd", "led monitor", "4k monitor"]},
    {"hs_code": "8521.90", "description": "Streaming Devices / Media Players",  "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["fire stick", "chromecast", "roku", "apple tv", "streaming", "media player"]},
    {"hs_code": "8543.70", "description": "Smart Home Devices / IoT",           "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["smart home", "echo dot", "alexa", "google home", "smart plug", "iot"]},
    {"hs_code": "8471.60", "description": "Input Devices (Mouse/Keyboard)",     "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["mouse", "keyboard", "trackpad", "input device", "wireless mouse", "mechanical keyboard"]},
    {"hs_code": "8504.40", "description": "Power Banks / Chargers",             "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["power bank", "charger", "fast charger", "usb charger", "gan charger", "wireless charger"]},
    {"hs_code": "8525.80", "description": "Cameras / Webcams",                  "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["camera", "webcam", "dslr", "mirrorless", "action camera", "gopro", "dashcam"]},
    {"hs_code": "8473.30", "description": "Computer Accessories / Parts",       "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["ssd", "hard drive", "ram", "graphics card", "gpu", "cpu", "motherboard", "computer part"]},
    {"hs_code": "8513.10", "description": "Flashlights / Portable Lamps",       "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["flashlight", "torch", "led light", "portable lamp"]},

    # Wearables
    {"hs_code": "9102.11", "description": "Wrist Watches (Digital)",            "bcd_rate": 20, "igst_rate": 18, "category": "watches",       "keywords": ["watch", "smartwatch", "apple watch", "garmin", "fitbit", "wristwatch", "samsung watch"]},
    {"hs_code": "9101.11", "description": "Wrist Watches (Luxury/Analog)",      "bcd_rate": 20, "igst_rate": 18, "category": "watches",       "keywords": ["rolex", "omega watch", "seiko", "casio", "fossil watch", "analog watch", "luxury watch"]},
    {"hs_code": "8479.89", "description": "Fitness Trackers / Smart Bands",     "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["fitness tracker", "mi band", "smart band", "activity tracker", "health band"]},

    # Clothing & Apparel
    {"hs_code": "6109.10", "description": "T-Shirts / Cotton Tops",             "bcd_rate": 20, "igst_rate": 12, "category": "clothing",      "keywords": ["t-shirt", "tshirt", "tee", "polo", "cotton top", "shirt"]},
    {"hs_code": "6203.42", "description": "Trousers / Jeans / Pants",           "bcd_rate": 20, "igst_rate": 12, "category": "clothing",      "keywords": ["jeans", "trousers", "pants", "chinos", "denim", "leggings"]},
    {"hs_code": "6201.93", "description": "Jackets / Coats / Outerwear",        "bcd_rate": 20, "igst_rate": 12, "category": "clothing",      "keywords": ["jacket", "coat", "hoodie", "sweatshirt", "parka", "windbreaker", "bomber"]},
    {"hs_code": "6212.10", "description": "Innerwear / Undergarments",          "bcd_rate": 20, "igst_rate": 12, "category": "clothing",      "keywords": ["underwear", "innerwear", "bra", "panty", "boxer", "brief", "lingerie"]},
    {"hs_code": "6217.10", "description": "Clothing Accessories (Belts/Ties)",  "bcd_rate": 20, "igst_rate": 12, "category": "clothing",      "keywords": ["belt", "tie", "scarf", "hat", "cap", "gloves", "socks", "beanie"]},

    # Footwear
    {"hs_code": "6403.91", "description": "Leather Shoes / Formal Footwear",   "bcd_rate": 25, "igst_rate": 18, "category": "footwear",      "keywords": ["leather shoes", "formal shoes", "oxford", "derby", "loafer", "boot"]},
    {"hs_code": "6404.11", "description": "Sports Shoes / Sneakers",            "bcd_rate": 25, "igst_rate": 18, "category": "footwear",      "keywords": ["sneakers", "running shoes", "nike", "adidas", "sports shoes", "trainers", "converse"]},
    {"hs_code": "6402.99", "description": "Casual Footwear / Sandals",          "bcd_rate": 25, "igst_rate": 18, "category": "footwear",      "keywords": ["sandals", "slippers", "flip flops", "casual shoes", "crocs", "slides"]},

    # Bags & Luggage
    {"hs_code": "4202.12", "description": "Backpacks / Laptop Bags",            "bcd_rate": 20, "igst_rate": 18, "category": "bags",          "keywords": ["backpack", "laptop bag", "school bag", "rucksack", "daypack"]},
    {"hs_code": "4202.22", "description": "Handbags / Purses",                  "bcd_rate": 20, "igst_rate": 18, "category": "bags",          "keywords": ["handbag", "purse", "tote", "clutch", "shoulder bag", "crossbody"]},
    {"hs_code": "4202.92", "description": "Travel Bags / Duffel Bags",          "bcd_rate": 20, "igst_rate": 18, "category": "bags",          "keywords": ["duffel", "travel bag", "gym bag", "sports bag", "weekender"]},
    {"hs_code": "4202.11", "description": "Suitcases / Trolley Bags",           "bcd_rate": 20, "igst_rate": 18, "category": "bags",          "keywords": ["suitcase", "trolley", "luggage", "cabin bag", "hard case"]},

    # Supplements & Health
    {"hs_code": "2106.90", "description": "Protein Supplements / Whey",        "bcd_rate": 10, "igst_rate": 18, "category": "supplements",   "keywords": ["whey", "protein powder", "supplement", "creatine", "bcaa", "pre-workout", "mass gainer"]},
    {"hs_code": "3004.50", "description": "Vitamins / Minerals",                "bcd_rate": 10, "igst_rate": 18, "category": "supplements",   "keywords": ["vitamin", "omega-3", "fish oil", "multivitamin", "zinc", "magnesium", "calcium"]},
    {"hs_code": "2106.10", "description": "Protein Concentrates / Isolates",    "bcd_rate": 10, "igst_rate": 18, "category": "supplements",   "keywords": ["isolate", "concentrate", "casein", "plant protein", "vegan protein"]},

    # Cosmetics & Beauty
    {"hs_code": "3304.99", "description": "Face Care / Skincare Products",      "bcd_rate": 20, "igst_rate": 28, "category": "cosmetics",     "keywords": ["serum", "moisturizer", "sunscreen", "face wash", "cleanser", "toner", "retinol", "skincare"]},
    {"hs_code": "3305.10", "description": "Hair Care Products",                 "bcd_rate": 20, "igst_rate": 28, "category": "cosmetics",     "keywords": ["shampoo", "conditioner", "hair oil", "hair mask", "hair care", "hair serum"]},
    {"hs_code": "3304.10", "description": "Lipstick / Lip Products",            "bcd_rate": 20, "igst_rate": 28, "category": "cosmetics",     "keywords": ["lipstick", "lip balm", "lip gloss", "lip liner", "lip care"]},
    {"hs_code": "3303.00", "description": "Perfumes / Fragrances",              "bcd_rate": 20, "igst_rate": 28, "category": "cosmetics",     "keywords": ["perfume", "cologne", "fragrance", "eau de parfum", "deodorant", "body spray"]},
    {"hs_code": "3401.11", "description": "Personal Care / Soap / Body Wash",  "bcd_rate": 20, "igst_rate": 28, "category": "cosmetics",     "keywords": ["soap", "body wash", "shower gel", "face soap", "hand wash"]},

    # Food & Beverages
    {"hs_code": "0901.21", "description": "Coffee / Coffee Beans",              "bcd_rate": 30, "igst_rate": 12, "category": "food",          "keywords": ["coffee", "espresso", "coffee beans", "ground coffee", "instant coffee"]},
    {"hs_code": "2101.12", "description": "Tea / Herbal Tea",                   "bcd_rate": 30, "igst_rate": 12, "category": "food",          "keywords": ["tea", "green tea", "herbal tea", "matcha", "chamomile"]},
    {"hs_code": "1806.32", "description": "Chocolates / Confectionery",         "bcd_rate": 30, "igst_rate": 28, "category": "food",          "keywords": ["chocolate", "candy", "confectionery", "gummies", "sweet", "snack"]},
    {"hs_code": "2008.19", "description": "Dry Fruits / Nuts",                  "bcd_rate": 30, "igst_rate": 12, "category": "food",          "keywords": ["almonds", "cashews", "walnuts", "dry fruits", "nuts", "pistachios"]},

    # Books & Media
    {"hs_code": "4901.99", "description": "Books / Printed Matter",             "bcd_rate":  0, "igst_rate":  0, "category": "books",         "keywords": ["book", "novel", "textbook", "printed", "publication", "comic", "manga"]},
    {"hs_code": "8523.49", "description": "Software / Digital Media",           "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["software", "game disc", "dvd", "blu-ray", "cd"]},

    # Toys & Games
    {"hs_code": "9503.00", "description": "Toys / Children's Games",            "bcd_rate": 60, "igst_rate": 12, "category": "toys",          "keywords": ["toy", "lego", "doll", "action figure", "board game", "puzzle", "kids", "children"]},
    {"hs_code": "9504.50", "description": "Video Game Consoles / Controllers",  "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["playstation", "xbox", "nintendo", "ps5", "gaming console", "controller", "gamepad"]},

    # Jewelry
    {"hs_code": "7113.19", "description": "Jewelry (Gold / Silver)",            "bcd_rate": 15, "igst_rate":  3, "category": "jewelry",       "keywords": ["jewelry", "jewellery", "necklace", "bracelet", "ring", "earring", "pendant", "gold", "silver"]},
    {"hs_code": "7116.20", "description": "Imitation / Fashion Jewelry",        "bcd_rate": 20, "igst_rate": 18, "category": "jewelry",       "keywords": ["fashion jewelry", "imitation", "costume jewelry", "artificial jewelry"]},

    # Sports & Fitness
    {"hs_code": "9506.91", "description": "Sports Equipment / Gym Equipment",  "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["dumbbell", "barbell", "gym equipment", "resistance band", "yoga mat", "sports equipment"]},
    {"hs_code": "9506.62", "description": "Sports Balls / Equipment",          "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["football", "basketball", "cricket bat", "tennis racket", "badminton"]},

    # Home & Kitchen
    {"hs_code": "8516.60", "description": "Kitchen Appliances (Small)",         "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["blender", "mixer", "toaster", "air fryer", "instant pot", "coffee maker", "juicer"]},
    {"hs_code": "7323.99", "description": "Kitchen Utensils / Cookware",        "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["pan", "pot", "cookware", "knife", "cutting board", "utensil", "cast iron"]},
    {"hs_code": "9403.20", "description": "Furniture / Home Furnishing",        "bcd_rate": 20, "igst_rate": 18, "category": "electronics",   "keywords": ["chair", "desk", "table", "shelf", "furniture", "sofa", "bed frame"]},

    # Automotive
    {"hs_code": "8708.99", "description": "Car Accessories / Auto Parts",       "bcd_rate": 15, "igst_rate": 28, "category": "electronics",   "keywords": ["car accessory", "dash cam", "car charger", "seat cover", "car organizer"]},
]


# ─── Lookup Function ──────────────────────────────────────────────────────────
def lookup_by_name(product_name: str) -> dict:
    """
    Match a product name to the best HS code entry.
    Returns match details including hs_code, description, rates, and match info.
    """
    if not product_name:
        return _default_result()

    name_lower = product_name.lower()
    name_lower = re.sub(r"[^a-z0-9\s\-]", " ", name_lower)
    words      = name_lower.split()

    best_match  = None
    best_score  = 0

    for entry in HS_DATABASE:
        score        = 0
        matched_kw   = None

        for kw in entry["keywords"]:
            kw_words = kw.split()
            if all(w in name_lower for w in kw_words):
                kw_score = len(kw_words) * 10 + len(kw)   # longer = better match
                if kw_score > score:
                    score      = kw_score
                    matched_kw = kw

        if score > best_score:
            best_score = score
            best_match = {**entry, "matched_keyword": matched_kw}

    if best_match and best_score > 0:
        return {
            "match_found":     True,
            "hs_code":         best_match["hs_code"],
            "description":     best_match["description"],
            "bcd_rate":        best_match["bcd_rate"],
            "igst_rate":       best_match["igst_rate"],
            "category":        best_match["category"],
            "matched_keyword": best_match["matched_keyword"],
        }

    return _default_result()


def get_all_codes() -> list[dict]:
    """Return the full HS code database."""
    return [
        {
            "hs_code":     e["hs_code"],
            "description": e["description"],
            "bcd_rate":    e["bcd_rate"],
            "igst_rate":   e["igst_rate"],
            "category":    e["category"],
            "keywords":    e["keywords"],
        }
        for e in HS_DATABASE
    ]


def _default_result() -> dict:
    return {
        "match_found":     False,
        "hs_code":         "9999.99",
        "description":     "General Merchandise",
        "bcd_rate":        20,
        "igst_rate":       18,
        "category":        "general",
        "matched_keyword": None,
    }