"""Minimal API tests for analytics endpoints (response shape and types)."""
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_top_merchant():
    r = client.get("/analytics/top-merchant")
    assert r.status_code == 200
    data = r.json()
    assert "merchant_id" in data
    assert "total_volume" in data
    assert isinstance(data["total_volume"], (int, float))


def test_monthly_active_merchants():
    r = client.get("/analytics/monthly-active-merchants")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    for k, v in data.items():
        assert isinstance(k, str)
        assert isinstance(v, int)


def test_product_adoption():
    r = client.get("/analytics/product-adoption")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    for k, v in data.items():
        assert isinstance(k, str)
        assert isinstance(v, int)


def test_kyc_funnel():
    r = client.get("/analytics/kyc-funnel")
    assert r.status_code == 200
    data = r.json()
    assert "documents_submitted" in data
    assert "verifications_completed" in data
    assert "tier_upgrades" in data
    for k in ("documents_submitted", "verifications_completed", "tier_upgrades"):
        assert isinstance(data[k], int)


def test_failure_rates():
    r = client.get("/analytics/failure-rates")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    for item in data:
        assert "product" in item
        assert "failure_rate" in item
        assert isinstance(item["failure_rate"], (int, float))
