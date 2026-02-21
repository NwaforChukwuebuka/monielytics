"""Analytics REST endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.services import analytics_service

router = APIRouter(prefix="/anaytics", tags=["analytics"])


@router.get("/top-merchant")
def get_top_merchant(db: Session = Depends(get_db)):
    """Merchant with highest total successful transaction amount across all products."""
    return analytics_service.get_top_merchant(db)


@router.get("/monthly-active-merchants")
def get_monthly_active_merchants(db: Session = Depends(get_db)):
    """Count of unique merchants with at least one successful event per month."""
    return analytics_service.get_monthly_active_merchants(db)


@router.get("/product-adoption")
def get_product_adoption(db: Session = Depends(get_db)):
    """Unique merchant count per product (successful events), sorted by count descending."""
    return analytics_service.get_product_adoption(db)


@router.get("/kyc-funnel")
def get_kyc_funnel(db: Session = Depends(get_db)):
    """KYC conversion funnel: unique merchants at each stage (successful events only)."""
    return analytics_service.get_kyc_funnel(db)


@router.get("/failure-rates")
def get_failure_rates(db: Session = Depends(get_db)):
    """Failure rate per product; exclude PENDING; sort by rate descending."""
    return analytics_service.get_failure_rates(db)
