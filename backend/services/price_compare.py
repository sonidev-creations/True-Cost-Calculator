import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

PRICE_ESTIMATES = {
    "iphone 16 pro max": 159900, "iphone 16 pro": 119900,
    "iphone 16": 79900,   "iphone 15": 69900,
    "iphone 14": 59900,   "iphone 13": 49900,
    "macbook pro": 249900,"macbook air": 114900,
    "macbook": 114900,
    "samsung galaxy s24": 79999, "samsung galaxy s23": 59999,
    "oneplus 12": 64999,  "oneplus 11": 49999,
    "pixel 8 pro": 99999, "pixel 8": 75999,
    "sony wh1000xm5": 29990, "sony wh1000xm4": 24990,
    "airpods pro": 24900, "airpods": 14900,
    "apple watch ultra": 89900, "apple watch": 41900,
    "galaxy watch": 27999,
    "ipad pro": 99900,    "ipad air": 59900, "ipad": 34900,
    "samsung tab": 24999,
    "dell laptop": 65000, "hp laptop": 55000,
    "lenovo laptop": 50000, "asus laptop": 55000,
    "gaming laptop": 85000, "laptop": 55000,
    "rtx 4090": 200000,   "rtx 4080": 130000,
    "rtx 4070": 80000,    "rtx 3080": 70000,
    "ps5": 54990,         "xbox series x": 52990,
    "nintendo switch": 29999, "steam deck": 45000,
    "canon eos": 65000,   "sony alpha": 85000,
    "nikon": 55000,       "gopro": 35000,
    "dyson airwrap": 45000, "dyson v15": 52900,
    "kindle": 10999,      "echo dot": 4499,
    "apple tv": 18900,
    "monitor": 20000,     "webcam": 5000,
    "microphone": 8000,   "router": 5000,
    "powerbank": 3000,    "charger": 2000,
    "headphones": 15000,  "earbuds": 8000,
    "speaker": 8000,      "soundbar": 20000,
    "keyboard": 3000,     "mouse": 1500,
    "nike shoes": 8000,   "adidas shoes": 7000,
    "jordan": 12000,      "converse": 5000,
    "jeans": 2000,        "hoodie": 2500,
    "jacket": 4000,       "dress": 3000,
    "shirt": 1500,        "sneakers": 7000,
    "shoes": 5000,        "boots": 6000,
    "rolex": 800000,      "omega watch": 300000,
    "seiko": 15000,       "casio": 7000,
    "fossil watch": 10000,"watch": 8000,
    "louis vuitton": 200000, "gucci bag": 150000,
    "coach bag": 40000,   "backpack": 3000,
    "suitcase": 8000,     "wallet": 2000,
    "optimum nutrition whey": 4500, "myprotein": 3500,
    "whey protein": 3500, "creatine": 1500,
    "omega 3": 1200,      "multivitamin": 1000,
    "vitamin c": 500,     "vitamin d": 800,
    "protein": 3500,      "supplement": 2000,
    "perfume": 5000,      "moisturizer": 2000,
    "serum": 3000,        "shampoo": 800,
    "lipstick": 1500,     "sunscreen": 1000,
    "chocolate": 800,     "coffee": 1500,
    "nuts": 1500,         "snacks": 500,
    "book": 500,          "novel": 400,
    "textbook": 800,
    "lego": 5000,         "toy": 2000,
    "doll": 1500,         "puzzle": 1000,
    "necklace": 5000,     "ring": 8000,
    "bracelet": 3000,     "earring": 2000,
}


def search_india_price(product_name: str, provided_price: float = None) -> dict:
    if provided_price and float(provided_price) > 0:
        print(f"[price] User provided: Rs{provided_price:,.0f}")
        return {"indian_price": float(provided_price), "indian_source": "User Provided"}

    result = _try_amazon(product_name)
    if result:
        return result

    result = _try_flipkart(product_name)
    if result:
        return result

    result = _keyword_estimate(product_name)
    if result:
        return result

    return {"indian_price": None, "indian_source": None}


def _try_amazon(product_name: str) -> dict | None:
    try:
        query   = "+".join(product_name.split()[:5])
        url     = f"https://www.amazon.in/s?k={query}"
        session = requests.Session()
        session.headers.update({
            "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-IN,en;q=0.9,hi;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT":             "1",
            "Connection":      "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })
        resp = session.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "lxml")
        for selector in ["a-price-whole", "a-offscreen", "a-color-price"]:
            tags = soup.find_all("span", class_=selector)
            for tag in tags:
                raw    = tag.get_text(strip=True).replace(",","").replace(".","").replace("₹","").replace("Rs","").strip()
                digits = "".join(filter(str.isdigit, raw))
                if digits and 3 <= len(digits) <= 7:
                    price = float(digits)
                    if 100 < price < 2000000:
                        print(f"[price] Amazon India: Rs{price:,.0f}")
                        return {"indian_price": price, "indian_source": "Amazon India"}
    except Exception as e:
        print(f"[price] Amazon failed: {e}")
    return None


def _try_flipkart(product_name: str) -> dict | None:
    try:
        query = "%20".join(product_name.split()[:5])
        url   = f"https://www.flipkart.com/search?q={query}"
        resp  = requests.get(url, headers=HEADERS, timeout=8)
        soup  = BeautifulSoup(resp.text, "lxml")
        for cls in ["_30jeq3", "_1vC4OE", "Nx9bqj", "_4b5DiR", "hl05eU"]:
            tag = soup.find("div", class_=cls) or soup.find("span", class_=cls)
            if tag:
                raw    = tag.get_text(strip=True).replace("₹","").replace(",","").strip()
                digits = "".join(filter(str.isdigit, raw))
                if digits and 3 <= len(digits) <= 7:
                    price = float(digits)
                    if 100 < price < 2000000:
                        print(f"[price] Flipkart: Rs{price:,.0f}")
                        return {"indian_price": price, "indian_source": "Flipkart"}
    except Exception as e:
        print(f"[price] Flipkart failed: {e}")
    return None


def _keyword_estimate(product_name: str) -> dict | None:
    name_lower = product_name.lower()
    sorted_estimates = sorted(PRICE_ESTIMATES.items(), key=lambda x: len(x[0]), reverse=True)
    for keyword, price in sorted_estimates:
        if keyword in name_lower:
            print(f"[price] Keyword match '{keyword}': Rs{price:,.0f}")
            return {
                "indian_price":  float(price),
                "indian_source": "Estimated (India Market)",
            }
    return None