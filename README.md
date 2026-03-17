# Hospitality Data Platform

A modular **Data Engineering project** implementing a **Medallion Architecture** for hospitality booking and review analytics.

This project simulates a **production-style data backbone for OTA (Online Travel Agency) data**, covering ingestion, transformation, validation, aggregation, and analytical querying.

The platform integrates **multi-source booking and review datasets**, normalizes schemas, and produces **analytics-ready metrics for revenue and reputation monitoring**.

---

# Architecture

This project follows a **Medallion Data Architecture**, commonly used in modern data platforms.

```
Raw → Bronze → Silver → Gold
```

Each layer progressively improves data quality, structure, and analytical usability.

---

# Raw Layer

The **Raw layer** represents the original data exported from external OTA platforms.

Sources used in this project:

- Booking.com  
- Expedia  

Characteristics:

- Original schema preserved  
- No transformations applied  
- Data stored exactly as received from the source systems  

⚠️ **Raw datasets are not included in the public repository.**

The original OTA exports contain **personally identifiable information (PII)** such as:

- guest names  
- email addresses  
- reservation identifiers  

To ensure **data privacy and responsible data handling**, raw files are stored **only in the local development environment** and are excluded from version control via `.gitignore`.

---

# Bronze Layer

The **Bronze layer** performs the first transformation stage.

Objectives:

- Initial data cleaning  
- PII anonymization  
- Structural normalization  

Examples of transformations:

- Hashing personal identifiers (guest names, emails, reservation IDs)  
- Normalizing column formats  
- Cleaning currency values  
- Standardizing date formats  

This layer ensures **sensitive information is protected** while maintaining the operational structure of the data.

---

# Silver Layer

The **Silver layer** standardizes business schemas across multiple data sources.

In this layer:

- Booking.com and Expedia datasets are unified  
- Business fields are normalized  
- Booking status values are standardized  
- Review ratings are converted into comparable numeric values  

The Silver layer produces **analysis-ready structured tables**.

Examples:

- unified bookings dataset  
- unified reviews dataset  

---

# Gold Layer

The **Gold layer** contains aggregated business metrics and KPIs.

These datasets support analytical use cases such as:

- revenue monitoring  
- cancellation analysis  
- OTA performance comparison  
- reputation tracking  
- review volume trends  

Examples of generated KPIs:

- total revenue  
- average booking value  
- cancellation rate  
- revenue share by OTA  
- average review rating  
- monthly review volume  

The Gold layer represents **business-ready analytical outputs**.

---

# Data Domains

## Bookings

Booking datasets are unified across OTAs and standardized into a single schema.

Analytical use cases include:

- revenue analysis  
- cancellation monitoring  
- channel performance comparison  
- guest origin analysis  
- monthly revenue trends  

---

## Reviews

Review data from multiple OTAs is normalized to support reputation analytics.

Analytical use cases include:

- average rating monitoring  
- rating comparison across platforms  
- review volume trends  
- reputation monitoring  
- review response analysis  

---

# Pipeline

The pipeline is orchestrated through:

```
orchestration/run_pipeline.py
```

Pipeline execution performs:

1. Silver bookings transformation  
2. Silver reviews transformation  
3. Data quality validation  
4. Gold booking KPIs generation  
5. Gold review KPIs generation  

This ensures a **deterministic rebuild of the analytical dataset**.

---

# SQL Analytics Layer

Analytical SQL queries are included to demonstrate **warehouse-level analysis**.

Location:

```
analytics/sql/analysis_queries.sql
```

Queries included:

- revenue by OTA  
- cancellation rate by platform  
- average booking value  
- revenue share by OTA  
- monthly revenue trends  
- average review rating by platform  
- monthly review volume  
- revenue by guest country  

These queries simulate **analytical exploration typically performed on data warehouses**.

---

# Project Structure

```
hospitality-data-platform

analytics/
└── sql/
    └── analysis_queries.sql

data/
├── raw/        (local only – excluded from repository)
├── bronze/
├── silver/
└── gold/

docs/
├── architecture.md
├── data_model.md
├── pipeline_flow.md
└── business_use_cases.md

orchestration/
└── run_pipeline.py

quality/
├── bronze_checks.py
└── silver_checks.py

scripts/
└── anonymization/

transformations/
├── staging/
└── marts/

README.md
```

---

# Engineering Highlights

Key engineering concepts implemented in this project:

- Medallion Data Architecture  
- Multi-source schema unification  
- PII anonymization pipeline  
- Defensive data engineering  
- Deterministic orchestration  
- Modular ETL architecture  
- Data quality validation  
- Business KPI generation  

---

# Example KPIs

## Revenue Analytics

- total revenue  
- average booking value  
- cancellation rate  
- revenue share by OTA  
- revenue by guest country  
- monthly revenue trends  

---

## Reputation Analytics

- average review rating  
- rating comparison by platform  
- review volume over time  
- review count by OTA  
- reputation monitoring metrics  

---

# Technologies

Core stack used in this project:

- Python  
- Pandas  
- SQL  
- Modular ETL architecture  
- Medallion data modeling  

---

# Strategic Positioning

This project represents a **hospitality analytics data backbone**.

It can serve as the foundation for:

- revenue optimization engines  
- hospitality analytics platforms  
- reputation monitoring systems  
- pricing intelligence tools  
- OTA performance monitoring  

---

# Author

**Francisco Cunha**  
Data Engineering Portfolio Project  
Hospitality Analytics & Revenue Intelligence
