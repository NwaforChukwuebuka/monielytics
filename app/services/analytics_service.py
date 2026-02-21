"""SQL-backed analytics for merchant activity data."""
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


def get_top_merchant(db: Session) -> dict[str, Any]:
    """Merchant with highest total successful transaction amount across all products."""
    row = db.execute(
        text("""
            SELECT merchant_id, SUM(amount) AS total_volume
            FROM activities
            WHERE status = 'SUCCESS'
            GROUP BY merchant_id
            ORDER BY total_volume DESC
            LIMIT 1
        """)
    ).fetchone()
    if not row:
        return {"merchant_id": "MRC-000000", "total_volume": 0.00}
    vol = float(row[1]) if row[1] is not None else 0.0
    return {"merchant_id": row[0], "total_volume": round(vol, 2)}


def get_monthly_active_merchants(db: Session) -> dict[str, int]:
    """Count of unique merchants with at least one successful event per month."""
    rows = db.execute(
        text("""
            SELECT to_char(event_timestamp, 'YYYY-MM') AS month, COUNT(DISTINCT merchant_id) AS cnt
            FROM activities
            WHERE status = 'SUCCESS' AND event_timestamp IS NOT NULL
            GROUP BY to_char(event_timestamp, 'YYYY-MM')
            ORDER BY month
        """)
    ).fetchall()
    return {str(r[0]): int(r[1]) for r in rows}


def get_product_adoption(db: Session) -> dict[str, int]:
    """Unique merchant count per product, sorted by count descending."""
    rows = db.execute(
        text("""
            SELECT product, COUNT(DISTINCT merchant_id) AS cnt
            FROM activities
            GROUP BY product
            ORDER BY cnt DESC
        """)
    ).fetchall()
    return {str(r[0]): int(r[1]) for r in rows}


def get_kyc_funnel(db: Session) -> dict[str, int]:
    """KYC conversion funnel: unique merchants at each stage (successful events only)."""
    docs = db.execute(
        text("""
            SELECT COUNT(DISTINCT merchant_id) FROM activities
            WHERE product = 'KYC' AND status = 'SUCCESS' AND event_type = 'DOCUMENT_SUBMITTED'
        """)
    ).scalar() or 0
    verif = db.execute(
        text("""
            SELECT COUNT(DISTINCT merchant_id) FROM activities
            WHERE product = 'KYC' AND status = 'SUCCESS' AND event_type = 'VERIFICATION_COMPLETED'
        """)
    ).scalar() or 0
    tier = db.execute(
        text("""
            SELECT COUNT(DISTINCT merchant_id) FROM activities
            WHERE product = 'KYC' AND status = 'SUCCESS' AND event_type = 'TIER_UPGRADE'
        """)
    ).scalar() or 0
    return {
        "documents_submitted": int(docs),
        "verifications_completed": int(verif),
        "tier_upgrades": int(tier),
    }


def get_failure_rates(db: Session) -> list[dict[str, Any]]:
    """Failure rate per product: FAILED/(SUCCESS+FAILED)*100, exclude PENDING, sort by rate desc."""
    rows = db.execute(
        text("""
            SELECT product,
                   COUNT(*) FILTER (WHERE status = 'FAILED') AS failed,
                   COUNT(*) FILTER (WHERE status = 'SUCCESS') AS success
            FROM activities
            WHERE status IN ('SUCCESS', 'FAILED')
            GROUP BY product
            HAVING (COUNT(*) FILTER (WHERE status = 'FAILED') + COUNT(*) FILTER (WHERE status = 'SUCCESS')) > 0
        """)
    ).fetchall()
    out = []
    for r in rows:
        product, failed, success = r[0], int(r[1] or 0), int(r[2] or 0)
        total = failed + success
        rate = (failed / total * 100) if total else 0
        out.append({"product": product, "failure_rate": round(rate, 1)})
    out.sort(key=lambda x: x["failure_rate"], reverse=True)
    return out
