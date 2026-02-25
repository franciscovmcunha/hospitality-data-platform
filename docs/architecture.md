# Architecture Overview

## Medallion Architecture

This project follows the Medallion Architecture pattern:

Raw → Bronze → Silver → Gold

### Raw Layer
- Contains original source data (Booking.com and Expedia)
- Not versioned (sensitive data)
- Acts as immutable input

### Bronze Layer
- Basic cleaning and anonymization
- Preserves original structure
- Standardizes column names where needed
- Light data normalization

### Silver Layer
- Unified schema across sources
- Strong typing (datetime, float, string)
- Business rule normalization (status mapping)
- Automatic correction of inverted dates
- Data quality validations

Final Silver schema:

- booking_date (datetime)
- check_in (datetime)
- check_out (datetime)
- price (float)
- status (OK / Cancelled)
- booker_country (string, nullable)
- cancelling_date (datetime, nullable)
- source (booking / expedia)

### Gold Layer
- Aggregated KPIs
- Revenue metrics
- Cancellation metrics
- Channel comparison metrics

## Data Flow

1. Raw data ingested
2. Bronze transformation
3. Silver standardization
4. Quality checks
5. Gold KPI generation
6. Orchestration via run_pipeline.py
