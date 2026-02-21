Moniepoint! Code Challenge - DreamDev 2026

Welcome, Future Engineers!

At Moniepoint, we're building Africa's leading business payments and financial services platform. Our ecosystem powers millions of merchants with POS terminals, savings accounts, airtime & bills, card payments, and business management tools.

This hackathon tests your ability to work with real-world multi-product data, build production-quality APIs, and extract actionable insights. We're evaluating accuracy, API design, code quality, architecture, and performance.

IMPORTANT: Your submission must be a working REST API that reviewers can call. Follow the API specification exactly—incomplete or non-runnable submissions cannot be evaluated.


PROBLEM STATEMENT

Moniepoint's Growth & Intelligence team needs to understand merchant behavior across the entire product ecosystem. Merchants interact with multiple products: they process POS transactions, sell airtime, pay bills, accept card payments, manage inventory with MonieBook, save funds, and go through KYC verification for account upgrades.

The platform logs all merchant activities across these products. Your task is to build an Analytics API that processes a year's worth of activity logs and exposes key business insights through REST endpoints.

DATA SOURCE
Your data source is CSV files containing daily merchant activity records.

Location:  /data/activities_YYYYMMDD.csv 
Your first task is to import the CSV data into a PostgreSQL database before processing for analytics. 

DATA SCHEMA
event_id (UUID) - Unique event identifier
merchant_id (VARCHAR) - Merchant identifier (format: MRC-XXXXXX)
event_timestamp (TIMESTAMP) - When the event occurred (ISO 8601 format)
product (VARCHAR) - Product category: POS, AIRTIME, BILLS, CARD_PAYMENT, SAVINGS, MONIEBOOK, KYC
event_type (VARCHAR) - Type of activity
amount (DECIMAL) - Transaction amount in NGN (0 for non-monetary)
status (VARCHAR) - One of: SUCCESS, FAILED, PENDING
channel (VARCHAR) - One of: POS, APP, USSD, WEB, OFFLINE
region (VARCHAR) - Merchant's operating region
merchant_tier (VARCHAR) - KYC tier: STARTER, VERIFIED, PREMIUM
PRODUCT TYPES
POS: POS terminal card transactions (payments received by merchant)
AIRTIME: Airtime vending for customers
BILLS: Bill payments (electricity, cable TV, internet, etc.)
CARD_PAYMENT: Merchant's own card payments to suppliers
SAVINGS: Merchant savings account (deposits, withdrawals, interest)
MONIEBOOK: Inventory and sales tracking for offline businesses
KYC: Know Your Customer verification and tier upgrades
EVENT TYPES BY PRODUCT
POS: CARD_TRANSACTION, CASH_WITHDRAWAL, TRANSFER
AIRTIME: AIRTIME_PURCHASE, DATA_PURCHASE
BILLS: ELECTRICITY, CABLE_TV, INTERNET, WATER, BETTING
CARD_PAYMENT: SUPPLIER_PAYMENT, INVOICE_PAYMENT
SAVINGS: DEPOSIT, WITHDRAWAL, INTEREST_CREDIT, AUTO_SAVE
MONIEBOOK: SALE_RECORDED, INVENTORY_UPDATE, EXPENSE_LOGGED
KYC: DOCUMENT_SUBMITTED, VERIFICATION_COMPLETED, TIER_UPGRADE

API SPECIFICATION

Your API must expose the following endpoints on port 8080. All responses must be JSON.

Base URL:http://localhost:8080 
GET /analytics/top-merchant
Returns the merchant with the highest total successful transaction amount across ALL products.
Response:{"merchant_id": "MRC-001234", "total_volume": 98765432.10} 
GET /analytics/monthly-active-merchants
Returns the count of unique merchants with at least one successful event per month.
Response:{"2024-01": 8234, "2024-02": 8456, ... "2024-12": 9102} 
GET /analytics/product-adoption
Returns unique merchant count per product (sorted by count, highest first).
Response:{"POS": 15234, "AIRTIME": 12456, "BILLS": 10234, ...} 
GET /analytics/kyc-funnel
Returns the KYC conversion funnel (unique merchants at each stage, successful events only).
Response:{"documents_submitted": 5432, "verifications_completed": 4521, "tier_upgrades": 3890} 
GET /analytics/failure-rates
Returns failure rate per product: (FAILED / (SUCCESS + FAILED)) x 100. Exclude PENDING. Sort by rate descending.
Response:[{"product": "BILLS", "failure_rate": 5.2}, {"product": "AIRTIME", "failure_rate": 4.1}, ...] 
EVALUATION CRITERIA
Correctness (30%) - All 5 endpoints return accurate data
Code Quality (25%) - Clean, readable code with meaningful names
Architecture (20%) - Sensible organization, separation of concerns
Performance (15%) - API responds quickly; startup within 5 minutes
API Design (10%) - Proper HTTP methods, status codes, JSON responses
IMPORTANT NOTES
Some records may have malformed data—handle these gracefully
Monetary values: 2 decimal places. Percentages: 1 decimal place
Your API will be tested against a different dataset
Use any framework—we evaluate results, not framework choice
Document any assumptions in your README
PRE-SUBMISSION CHECKLIST
Repository is public on GitHub
API responds on port 8080
All 5 endpoints return valid JSON
README.md includes your name, assumptions and set up instruction for the reviewer
Repository URL submitted before deadline

Candidate Starter Pack
Here is a link to your candidate starter package https://drive.google.com/file/d/1wOBfiRf-uCTobaPr1XAb6xOCa1zAAUm1/view?usp=sharing.

The candidate package contains everything you need to get started:
Extract data.zip to get the sample CSV files
Read the README.md carefully for setup instructions
The README contains detailed instructions for database setup, API testing, and submission requirements. Make sure to read it thoroughly before starting.

SUPPORTED LANGUAGES
You may use any of the following languages with any framework of your choice:
Python (FastAPI)