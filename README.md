# Hospitality Data Platform

A modular Data Engineering project implementing a Medallion Architecture
for hospitality booking and review analytics.

This project simulates a production-ready data backbone for OTA data,
covering ingestion, transformation, validation, aggregation, and orchestration.

---

# Architecture

Raw → Bronze → Silver → Gold

Designed to:

- Unify heterogeneous OTA data
- Normalize business logic
- Enforce data quality
- Deliver analytics-ready KPIs

---

# Data Domains

## Bookings
- Revenue metrics
- Cancellation analysis
- Channel comparison
- Booking value analysis

## Reviews
- Reputation monitoring
- Rating normalization
- Channel rating comparison
- Review volume trends

---

# Pipeline

Central orchestration:

orchestration/run_pipeline.py

Executes full rebuild:

1. Silver bookings
2. Silver reviews
3. Quality validation
4. Gold booking KPIs
5. Gold review KPIs

---

# Engineering Highlights

- Multi-source schema unification
- Rating normalization (text → numeric)
- Defensive data engineering
- Structured modular transformations
- Deterministic pipeline execution
- Medallion architecture implementation

---

# Output KPIs

## Revenue
- Total revenue
- Average booking value
- Cancellation rate
- Revenue by source

## Reputation
- Average rating
- Rating by source
- Monthly review volume
- Review count by source

---

# Technologies

- Python
- Pandas
- Modular ETL architecture
- Layered data modeling

---

# Strategic Positioning

This project serves as:

- Hospitality data backbone
- Foundation for revenue optimization engines
- Base layer for advanced analytics systems

---

# Author

Fracisco Cunha
Data Engineering Portfolio Project  
Hospitality Analytics & Revenue Intelligence
