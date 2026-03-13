import requests
from bs4 import BeautifulSoup
 
# ── Browser-like headers to avoid bot detection ───────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
 
 
def scrape_product(url: str) -> dict:
    """
    Attempts to scrape the product title from a given URL.
    Frontend-provided data always takes priority over scraped data.
 
    Supported sites:
        - Amazon US  (amazon.com)
        - AliExpress (aliexpress.com)
        - SHEIN      (shein.com)
        - iHerb      (iherb.com)
        - eBay       (ebay.com)
        - Walmart    (walmart.com)
        - Generic    (any other URL — uses <title> tag)
 
    Args:
        url : Full product URL string
 
    Returns:
        dict with 'scraped_title' and 'source', or empty dict on failure
    """
    if not url or not url.startswith("http"):
        return {}
 
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
 
        # ── Amazon US ─────────────────────────────────────────────────────────
        if "amazon.com" in url:
            tag = soup.find(id="productTitle")
            if tag:
                title = tag.get_text(strip=True)
                print(f"[scraper] Amazon US → {title[:60]}")
                return {"scraped_title": title, "source": "amazon_us"}
 
        # ── AliExpress ────────────────────────────────────────────────────────
        elif "aliexpress.com" in url:
            tag = (
                soup.find("h1", class_="product-title-text")
                or soup.find("h1")
            )
            if tag:
                title = tag.get_text(strip=True)
                print(f"[scraper] AliExpress → {title[:60]}")
                return {"scraped_title": title, "source": "aliexpress"}
 
        # ── SHEIN ─────────────────────────────────────────────────────────────
        elif "shein.com" in url:
            tag = soup.find("h1", class_="product-intro__head-name")
            if tag:
                title = tag.get_text(strip=True)
                print(f"[scraper] SHEIN → {title[:60]}")
                return {"scraped_title": title, "source": "shein"}
 
        # ── iHerb ─────────────────────────────────────────────────────────────
        elif "iherb.com" in url:
            tag = soup.find("h1", itemprop="name")
            if tag:
                title = tag.get_text(strip=True)
                print(f"[scraper] iHerb → {title[:60]}")
                return {"scraped_title": title, "source": "iherb"}
 
        # ── eBay ──────────────────────────────────────────────────────────────
        elif "ebay.com" in url:
            tag = soup.find("h1", class_="x-item-title__mainTitle")
            if tag:
                title = tag.get_text(strip=True)
                print(f"[scraper] eBay → {title[:60]}")
                return {"scraped_title": title, "source": "ebay"}
 
        # ── Walmart ───────────────────────────────────────────────────────────
        elif "walmart.com" in url:
            tag = soup.find("h1", itemprop="name") or soup.find("h1")
            if tag:
                title = tag.get_text(strip=True)
                print(f"[scraper] Walmart → {title[:60]}")
                return {"scraped_title": title, "source": "walmart"}
 
        # ── Generic fallback — grab <title> tag ───────────────────────────────
        page_title = soup.find("title")
        if page_title:
            title = page_title.get_text(strip=True)
            print(f"[scraper] Generic → {title[:60]}")
            return {"scraped_title": title, "source": "generic"}
 
    except requests.exceptions.Timeout:
        print(f"[scraper] Timeout fetching: {url[:60]}")
    except requests.exceptions.RequestException as e:
        print(f"[scraper] Request error: {e}")
    except Exception as e:
        print(f"[scraper] Parse error: {e}")
 
    return {}