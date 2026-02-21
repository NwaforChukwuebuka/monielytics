# Moniepoint Analytics API

REST API to analyze merchant activity logs. Data are loaded into a PostgreSQL backend from CSV and exposed via five analytical endpoints.

**Candidate:** Nwafor Chukwuebuka Samuel

---

## Prerequisites

- **Python** 3.10+
- **PostgreSQL**

---

## Setup

1. **Clone and enter the project**
   ```bash
   cd monielytics
   ```

2. **Environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set `DATABASE_URL`, e.g.:
   ```text
   DATABASE_URL=postgresql://user:password@localhost:5432/monielytics
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional — load activity data from CSV**
   ```bash
   python scripts/import_data.py
   ```

5. **Run the API**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080
   ```
   Docs: [http://localhost:8080/api/docs](http://localhost:8080/api/docs)

---

## API summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/top-merchant` | Merchant with highest total successful transaction amount |
| GET | `/analytics/monthly-active-merchants` | Unique merchants with ≥1 success per month |
| GET | `/analytics/product-adoption` | Unique merchant count per product (successful events) |
| GET | `/analytics/kyc-funnel` | KYC funnel: documents submitted → verification → tier upgrade |
| GET | `/analytics/failure-rates` | Failure rate per product (excludes PENDING) |

Root: `GET /` returns API info and links to docs.
