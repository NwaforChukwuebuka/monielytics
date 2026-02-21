"""SQLAlchemy model for merchant activity events."""
from sqlalchemy import Column, DECIMAL, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Activity(Base):
    """Single merchant activity event (one row per CSV record)."""

    __tablename__ = "activities"

    event_id = Column(PG_UUID(as_uuid=True), primary_key=True)
    merchant_id = Column(String(32), nullable=False, index=True)  # MRC-XXXXXX
    event_timestamp = Column(DateTime(timezone=True), nullable=True, index=True)
    product = Column(String(32), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    amount = Column(DECIMAL(18, 2), nullable=False, default=0)
    status = Column(String(16), nullable=False, index=True)  # SUCCESS, FAILED, PENDING
    channel = Column(String(16), nullable=True)
    region = Column(String(64), nullable=True)
    merchant_tier = Column(String(16), nullable=True)
