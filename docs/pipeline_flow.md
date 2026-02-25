# Pipeline Execution Flow

The pipeline is orchestrated through:

python orchestration/run_pipeline.py

Execution steps:

1. Silver Layer (stg_bookings.py)
   - Unifies schemas
   - Normalizes status
   - Converts to proper datatypes
   - Fixes inverted dates

2. Silver Quality Checks (silver_checks.py)
   - Validates booking_date for active bookings
   - Validates check_out >= check_in
   - Validates allowed status values

3. Gold Layer (kpi_bookings.py)
   - Aggregates KPIs
   - Calculates revenue
   - Calculates cancellation rate
   - Generates final metrics

Pipeline exits with failure if validations fail.
