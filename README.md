# Hospitality Data Platform

A modular Data Engineering project implementing a Medallion Architecture
for OTA (Online Travel Agency) booking analytics.

This project simulates a production-ready data platform for hotel booking data,
covering ingestion, transformation, validation, aggregation, and orchestration.

---

# Project Overview

The platform processes booking data from multiple OTA sources:

- Booking.com
- Expedia

It standardizes schemas, applies business rules, validates data integrity,
and produces aggregated KPIs for revenue and performance monitoring.

Architecture follows the Medallion pattern:

Raw → Bronze → Silver → Gold

---

# Architecture

## Raw Layer
- Original source data
- Immutable input
- Not version-controlled (sensitive data)

## Bronze Layer
- Light cleaning
- Anonymization
- Standardized structure
- Preserves original semantics

## Silver Layer
- Unified schema across OTAs
- Strong typing (datetime, float, string)
- Status normalization
- Automatic correction of inverted dates
- Data quality validation

Final Silver schema:

- booking_date (datetime)
- check_in (datetime)
- check_out (datetime)
- price (float)
- status (OK / Cancelled)
- booker_country (nullable)
- cancelling_date (nullable)
- source (booking / expedia)

## Gold Layer
Aggregated business metrics:

- total_bookings
- total_revenue
- cancelled_bookings
- cancellation_rate_percent
- avg_booking_value
- revenue_by_source

---

# Folder Structure

hospitality-data-platform/
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── transformations/
│   ├── staging/
│   │   └── stg_bookings.py
│   └── marts/
│       └── kpi_bookings.py
│
├── quality/
│   ├── bronze_checks.py
│   └── silver_checks.py
│
├── orchestration/
│   └── run_pipeline.py
│
├── analytics/
│   └── sql/
│
├── docs/
│   ├── architecture.md
│   ├── data_model.md
│   ├── business_use_cases.md
│   └── pipeline_flow.md
│
├── scripts/
│   └── anonymization/
│
└── README.md

---

# Data Flow

1. Raw ingestion
2. Bronze transformation
3. Silver standardization
4. Silver quality checks
5. Gold KPI generation
6. Orchestration via run_pipeline.py

---

# Business Logic

## Status Normalization

Booking:
- ok → OK
- inhouse → OK
- cancelled_by_guest → Cancelled
- cancelled_by_hotel → Cancelled
- no_show → Cancelled

Expedia:
- postStay → OK
- cancelled → Cancelled

---

## Automatic Data Corrections

To ensure data consistency:

- Inverted dates are automatically swapped (check_out < check_in)
- Missing booking_date for confirmed bookings is filled using check_in

These corrections prevent pipeline failure while maintaining data integrity.

---

# Data Quality Validation

Silver checks validate:

- booking_date not null for active bookings
- check_out >= check_in
- Valid status values only (OK / Cancelled)

Pipeline fails if validations fail.

---

# KPIs Produced

Example metrics:

- Total Bookings
- Total Revenue
- Cancelled Bookings
- Cancellation Rate
- Average Booking Value
- Revenue by Source

---

# How to Run

Create virtual environment (if needed):

python -m venv .venv

Activate environment:

source .venv/bin/activate

Install dependency:

pip install pandas

Run full pipeline:

.venv/bin/python orchestration/run_pipeline.py

---

# Technologies Used

- Python
- Pandas
- Modular Architecture
- Medallion Pattern
- Data Validation Logic

---

# Engineering Concepts Demonstrated

- Schema unification across heterogeneous sources
- Business rule normalization
- Automated data validation
- Modular transformation design
- Layered architecture (Raw → Bronze → Silver → Gold)
- Centralized orchestration
- Defensive data engineering

---

# Future Improvements

- Incremental data loading
- Docker containerization
- Structured logging
- Unit testing with pytest
- Cloud deployment (AWS / Azure)
- Dashboard layer (Power BI / Tableau)
- Automated quality reporting

---

# Author

Francisco Cunha  
Data Engineering Track  
Hospitality Analytics & Revenue Intelligence
