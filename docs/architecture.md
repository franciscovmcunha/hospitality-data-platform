# Architecture

## Overview

The Hospitality Data Platform follows a Medallion Architecture pattern:

Raw → Bronze → Silver → Gold

This layered structure ensures separation of concerns, data reliability, and scalability.

---

## Raw Layer

Purpose:
- Immutable source data
- No transformation applied
- Acts as system of record

Contains:
- OTA exports (Booking, Expedia)
- Original review data

---

## Bronze Layer

Purpose:
- Light cleaning
- Structural standardization
- Anonymization
- Preserve original business meaning

Characteristics:
- Minimal transformation
- Column normalization
- Hashing of personal identifiers

---

## Silver Layer

Purpose:
- Schema unification across sources
- Type enforcement (datetime, float, string)
- Business rule normalization
- Quality validation

Includes:

### Bookings
- Unified status (OK / Cancelled)
- Price normalization
- Automatic date corrections
- Source tagging

### Reviews
- Unified rating scale (0–10 float)
- Unified review schema
- Multilingual text preserved
- Source normalization

---

## Gold Layer

Purpose:
- Business-ready aggregated metrics
- Revenue intelligence
- Reputation intelligence

Includes:

### Booking KPIs
- Total revenue
- Cancellation rate
- Average booking value
- Revenue by source

### Review KPIs
- Total reviews
- Average rating
- Rating by source
- Monthly review volume

---

## Orchestration

Centralized pipeline execution:

orchestration/run_pipeline.py

Executes:

1. Silver bookings
2. Silver reviews
3. Silver quality checks
4. Gold booking KPIs
5. Gold review KPIs

---

## Design Principles

- Modularity
- Deterministic transformations
- Explicit business logic
- Reproducibility
- Analytics-ready output
