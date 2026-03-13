import requests

FALLBACK_RATE = 92.0   # ← change from 83.5 to 92.0


def get_usd_to_inr() -> float:

    # ── API 1: Wise ───────────────────────────────────────────────────────
    try:
        url  = "https://wise.com/rates/live?source=USD&target=INR"   # ← paste here
        resp = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        data = resp.json()
        rate = float(data["value"])
        print(f"[currency] Wise: $1 = Rs{rate:.2f}")
        return rate
    except Exception as e:
        print(f"[currency] Wise failed: {e}")

    # ── API 2: open.er-api ────────────────────────────────────────────────
    try:
        url  = "https://open.er-api.com/v6/latest/USD"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get("result") == "success":
            rate = float(data["rates"]["INR"])
            print(f"[currency] open.er-api: $1 = Rs{rate:.2f}")
            return rate
    except Exception as e:
        print(f"[currency] open.er-api failed: {e}")

    # ── API 3: Frankfurter ────────────────────────────────────────────────
    try:
        url  = "https://api.frankfurter.app/latest?from=USD&to=INR"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        rate = float(data["rates"]["INR"])
        print(f"[currency] Frankfurter: $1 = Rs{rate:.2f}")
        return rate
    except Exception as e:
        print(f"[currency] Frankfurter failed: {e}")

    # ── API 4: fawazahmed0 ────────────────────────────────────────────────
    try:
        url  = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        rate = float(data["usd"]["inr"])
        print(f"[currency] fawazahmed0: $1 = Rs{rate:.2f}")
        return rate
    except Exception as e:
        print(f"[currency] fawazahmed0 failed: {e}")

    # ── All failed ────────────────────────────────────────────────────────
    print(f"[currency] All APIs failed — using fallback Rs{FALLBACK_RATE}")
    return FALLBACK_RATE
