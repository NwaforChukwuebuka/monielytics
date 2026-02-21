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
   DATABASE_URL=postgresql://user:password@localhost:5432/<datebase_name>
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the API**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080
   ```
   Docs: [http://localhost:8080/api/docs](http://localhost:8080/api/docs)

5. **Load activity data from CSV**
   ```bash
   python scripts/import_data.py
   ```

---

## API summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/top-merchant` | Merchant with highest total successful transaction amount |
| GET | `/analytics/monthly-active-merchants` | Unique merchants with ≥1 success per month |
| GET | `/analytics/product-adoption` | Unique merchant count per product |
| GET | `/analytics/kyc-funnel` | KYC funnel: documents submitted → verification → tier upgrade |
| GET | `/analytics/failure-rates` | Failure rate per product (excludes PENDING) |

Root: `GET /` returns API info and links to docs.

---

## Assumptions

- **Data path:** CSV files live under `data/` with pattern `activities_YYYYMMDD.csv`. The importer runs from the project root.
- **Malformed rows:** Rows with invalid `event_id` (non-UUID), missing/empty `merchant_id`, invalid `amount` (e.g. "INVALID"), or invalid/missing `product`/`status` are skipped during import. Empty or "NOT-A-DATE" timestamps are stored as NULL; they do not contribute to monthly-active-merchants.
- **Idempotent import:** Running the import script again truncates the `activities` table and reloads from CSV.
- **Monetary values:** Rounded to 2 decimal places in responses; percentages to 1 decimal place.
- **KYC funnel:** Counts distinct merchants with at least one successful KYC event of type `DOCUMENT_SUBMITTED`, `VERIFICATION_COMPLETED`, or `TIER_UPGRADE` respectively.
