"""
services/database.py
=====================
SQLite database for True Cost Calculator.
Stores search history and HS code lookups.
No server needed — creates truecost.db file automatically.
"""

from __future__ import annotations
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ─── Table 1: Search History ──────────────────────────────────────────────────
class Calculation(db.Model):
    """Every product search + result is saved here."""
    __tablename__ = "calculations"

    id               = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    product_name     = db.Column(db.String(200), nullable=False)
    price_usd        = db.Column(db.Float,       nullable=False)
    category         = db.Column(db.String(100))
    source_site      = db.Column(db.String(100))

    # HS Code info
    hs_code          = db.Column(db.String(20))
    hs_description   = db.Column(db.String(200))

    # Cost breakdown
    price_inr        = db.Column(db.Float)
    bcd              = db.Column(db.Float)
    sws              = db.Column(db.Float)
    igst             = db.Column(db.Float)
    shipping_cost    = db.Column(db.Float)
    total_landed     = db.Column(db.Float)
    duty_rate_pct    = db.Column(db.Float)
    igst_rate_pct    = db.Column(db.Float)
    currency_rate    = db.Column(db.Float)

    # Comparison result
    indian_price     = db.Column(db.Float)
    indian_source    = db.Column(db.String(200))
    verdict          = db.Column(db.String(20))
    savings          = db.Column(db.Float)

    # Restrictions
    restricted       = db.Column(db.Boolean, default=False)
    restriction_note = db.Column(db.Text)

    # Timestamp
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id":               self.id,
            "product_name":     self.product_name,
            "price_usd":        self.price_usd,
            "category":         self.category,
            "source_site":      self.source_site,
            "hs_code":          self.hs_code,
            "hs_description":   self.hs_description,
            "price_inr":        self.price_inr,
            "bcd":              self.bcd,
            "sws":              self.sws,
            "igst":             self.igst,
            "shipping_cost":    self.shipping_cost,
            "total_landed":     self.total_landed,
            "duty_rate_pct":    self.duty_rate_pct,
            "igst_rate_pct":    self.igst_rate_pct,
            "currency_rate":    self.currency_rate,
            "indian_price":     self.indian_price,
            "indian_source":    self.indian_source,
            "verdict":          self.verdict,
            "savings":          self.savings,
            "restricted":       self.restricted,
            "restriction_note": self.restriction_note,
            "created_at":       self.created_at.isoformat() if self.created_at else None,
        }


# ─── Table 2: HS Code Search Log ──────────────────────────────────────────────
class HSSearchLog(db.Model):
    """Logs every HS code lookup."""
    __tablename__ = "hs_search_log"

    id              = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    search_query    = db.Column(db.String(200), nullable=False)
    matched_hs_code = db.Column(db.String(20))
    matched_desc    = db.Column(db.String(200))
    matched_keyword = db.Column(db.String(100))
    match_found     = db.Column(db.Boolean, default=False)
    bcd_rate        = db.Column(db.Float)
    igst_rate       = db.Column(db.Float)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id":               self.id,
            "search_query":     self.search_query,
            "matched_hs_code":  self.matched_hs_code,
            "matched_desc":     self.matched_desc,
            "matched_keyword":  self.matched_keyword,
            "match_found":      self.match_found,
            "bcd_rate":         self.bcd_rate,
            "igst_rate":        self.igst_rate,
            "created_at":       self.created_at.isoformat() if self.created_at else None,
        }


# ─── Helpers ──────────────────────────────────────────────────────────────────
def save_calculation(response: dict, price_usd: float, category: str,
                     source_site: str, currency_rate: float) -> Calculation:
    cb = response.get("cost_breakdown", {})
    record = Calculation(
        product_name     = response.get("product_name", "Unknown"),
        price_usd        = price_usd,
        category         = category,
        source_site      = source_site,
        hs_code          = cb.get("hs_code"),
        hs_description   = cb.get("category_label"),
        price_inr        = cb.get("price_inr"),
        bcd              = cb.get("basic_customs_duty"),
        sws              = cb.get("social_welfare_surcharge"),
        igst             = cb.get("igst"),
        shipping_cost    = cb.get("shipping_cost"),
        total_landed     = cb.get("total_landed_cost"),
        duty_rate_pct    = cb.get("duty_rate_percent"),
        igst_rate_pct    = cb.get("igst_rate_percent"),
        currency_rate    = currency_rate,
        indian_price     = response.get("indian_price"),
        indian_source    = response.get("indian_source"),
        verdict          = response.get("verdict"),
        savings          = response.get("savings"),
        restricted       = response.get("restricted", False),
        restriction_note = response.get("restriction_note", ""),
    )
    db.session.add(record)
    db.session.commit()
    return record


def save_hs_log(query: str, hs_result: dict) -> HSSearchLog:
    log = HSSearchLog(
        search_query    = query,
        matched_hs_code = hs_result.get("hs_code"),
        matched_desc    = hs_result.get("description"),
        matched_keyword = hs_result.get("matched_keyword"),
        match_found     = hs_result.get("match_found", False),
        bcd_rate        = hs_result.get("bcd_rate"),
        igst_rate       = hs_result.get("igst_rate"),
    )
    db.session.add(log)
    db.session.commit()
    return log