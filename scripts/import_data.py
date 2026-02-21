"""
Import CSV activity files into PostgreSQL.
Handles malformed rows by skipping them and logging counts per file.
Uses batched inserts for performance.
"""
import csv
import logging
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from uuid import UUID

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import delete

from app.config import DATA_DIR, DATA_FILE_PATTERN
from app.db import db_session
from app.models import Activity

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

VALID_PRODUCTS = frozenset(
    {"POS", "AIRTIME", "BILLS", "CARD_PAYMENT", "SAVINGS", "MONIEBOOK", "KYC"}
)
VALID_STATUS = frozenset({"SUCCESS", "FAILED", "PENDING"})
BATCH_SIZE = 10_000


def parse_timestamp(value: str):
    """Parse ISO 8601 timestamp; return None if empty or invalid."""
    if not value or not value.strip():
        return None
    value = value.strip()
    if value.upper() in ("NOT-A-DATE", "INVALID", "N/A"):
        return None
    try:
        from datetime import datetime
        # Handle optional 'Z' and fractional seconds
        s = value.replace("Z", "+00:00")
        if "." in s and "+" not in s and "Z" not in value:
            s = s  # no TZ
        return datetime.fromisoformat(s)
    except Exception:
        return None


def parse_amount(value: str) -> Decimal | None:
    """Parse amount; return None if invalid."""
    if not value or not value.strip():
        return Decimal("0")
    value = value.strip().upper()
    if value in ("INVALID", "N/A", ""):
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def parse_uuid(value: str) -> UUID | None:
    """Parse UUID; return None if invalid."""
    if not value or not value.strip():
        return None
    try:
        return UUID(value.strip())
    except (ValueError, TypeError):
        return None


def validate_row(row: dict) -> tuple[bool, str]:
    """
    Validate required fields. Returns (ok, reason).
    """
    if not row.get("merchant_id") or not str(row["merchant_id"]).strip():
        return False, "missing merchant_id"
    if not row.get("product") or str(row["product"]).strip() not in VALID_PRODUCTS:
        return False, "missing or invalid product"
    if not row.get("status") or str(row["status"]).strip() not in VALID_STATUS:
        return False, "missing or invalid status"
    event_id = parse_uuid(row.get("event_id", ""))
    if event_id is None:
        return False, "invalid event_id"
    amount = parse_amount(row.get("amount", "0"))
    if amount is None:
        return False, "invalid amount"
    return True, ""


def row_to_activity(row: dict) -> Activity | None:
    """Build Activity model from CSV row; return None if invalid."""
    ok, _ = validate_row(row)
    if not ok:
        return None
    event_id = parse_uuid(row["event_id"])
    amount = parse_amount(row.get("amount", "0")) or Decimal("0")
    ts = parse_timestamp(row.get("event_timestamp", ""))
    return Activity(
        event_id=event_id,
        merchant_id=str(row["merchant_id"]).strip(),
        event_timestamp=ts,
        product=str(row["product"]).strip(),
        event_type=str(row.get("event_type", "") or "").strip() or "UNKNOWN",
        amount=amount,
        status=str(row["status"]).strip(),
        channel=str(row.get("channel", "") or "").strip() or None,
        region=str(row.get("region", "") or "").strip() or None,
        merchant_tier=str(row.get("merchant_tier", "") or "").strip() or None,
    )


def import_file(path: Path, db, batch: list) -> tuple[int, int]:
    """Process one CSV file; return (inserted, skipped)."""
    inserted = 0
    skipped = 0
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            activity = row_to_activity(row)
            if activity is None:
                skipped += 1
                continue
            batch.append(activity)
            inserted += 1
            if len(batch) >= BATCH_SIZE:
                db.bulk_save_objects(batch)
                db.flush()
                batch.clear()
    return inserted, skipped


def main():
    if not DATA_DIR.is_dir():
        logger.error("Data directory not found: %s", DATA_DIR)
        sys.exit(1)
    files = sorted(DATA_DIR.glob(DATA_FILE_PATTERN))
    if not files:
        logger.error("No CSV files found in %s matching %s", DATA_DIR, DATA_FILE_PATTERN)
        sys.exit(1)
    logger.info("Found %d CSV files", len(files))
    total_inserted = 0
    total_skipped = 0
    with db_session() as db:
        # Clear existing data so re-runs are idempotent
        db.execute(delete(Activity))
        batch: list[Activity] = []
        for path in files:
            inserted, skipped = import_file(path, db, batch)
            total_inserted += inserted
            total_skipped += skipped
            logger.info("%s: inserted=%d skipped=%d", path.name, inserted, skipped)
        if batch:
            db.bulk_save_objects(batch)
            db.flush()
    logger.info("Done. Total inserted=%d total skipped=%d", total_inserted, total_skipped)


if __name__ == "__main__":
    main()
