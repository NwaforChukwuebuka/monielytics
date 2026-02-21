"""Analytics REST endpoints."""
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.services import analytics_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/top-merchant")
def get_top_merchant(db: Session = Depends(get_db)):
    """Merchant with highest total successful transaction amount across all products."""
    logger.debug("get_top_merchant")
    return analytics_service.get_top_merchant(db)


@router.get("/monthly-active-merchants")
def get_monthly_active_merchants(db: Session = Depends(get_db)):
    """Count of unique merchants with at least one successful event per month."""
    logger.debug("get_monthly_active_merchants")
    return analytics_service.get_monthly_active_merchants(db)


@router.get("/product-adoption")
def get_product_adoption(db: Session = Depends(get_db)):
    """Unique merchant count per product, sorted by count descending."""
    logger.debug("get_product_adoption")
    return analytics_service.get_product_adoption(db)


@router.get("/kyc-funnel")
def get_kyc_funnel(db: Session = Depends(get_db)):
    """KYC conversion funnel: unique merchants at each stage (successful events only)."""
    logger.debug("get_kyc_funnel")
    return analytics_service.get_kyc_funnel(db)


@router.get("/failure-rates")
def get_failure_rates(db: Session = Depends(get_db)):
    """Failure rate per product; exclude PENDING; sort by rate descending."""
    logger.debug("get_failure_rates")
    return analytics_service.get_failure_rates(db)
