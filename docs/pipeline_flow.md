# Pipeline Flow

## Execution Order

1. Silver Layer - Bookings
2. Silver Layer - Reviews
3. Silver Quality Checks
4. Gold Layer - Booking KPIs
5. Gold Layer - Review KPIs

---

## Data Flow

Raw →
Bronze →
Silver →
Gold →
Analytics Consumption

---

## Error Handling

- Pipeline fails if Silver validation fails
- Logs execution stages
- Ensures deterministic output

---

## Reproducibility

Running:

.venv/bin/python orchestration/run_pipeline.py

Rebuilds entire Silver and Gold layers from Bronze.
