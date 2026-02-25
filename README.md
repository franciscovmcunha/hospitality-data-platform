# Hospitality Data Platform

End-to-end Data Engineering project implementing a Medallion Architecture (Bronze / Silver / Gold) for hospitality booking and review data.

This project simulates a real-world data platform ingesting data from multiple OTA sources (Booking & Expedia), anonymizing sensitive fields, standardizing schemas, and preparing business-ready datasets.

---

## Architecture

This project follows the Medallion Architecture pattern:

Raw → Bronze → Silver → Gold

### Raw
- Original source files
- Not versioned (sensitive data)
- Stored locally only

### Bronze
- Cleaned and anonymized datasets
- Standardized date formats
- Personally identifiable information hashed (SHA-256)

### Silver (In Progress)
- Unified schema across sources
- Structured and validated datasets
- Ready for transformation

### Gold (Planned)
- Business-level aggregated metrics
- Revenue KPIs
- Booking & review performance indicators

---

## Project Structure

hospitality-data-platform/

data/
- raw/
- bronze/
- silver/
- gold/

scripts/
- anonymization/

transformations/
- staging/
- marts/

quality/
ingestion/
orchestration/
docs/

---

## Data Privacy

All personally identifiable information (PII) such as:

- Guest names  
- Reservation IDs  
- Confirmation numbers  
- Review author names  

is hashed before being stored in the Bronze layer.

Raw sensitive data is never versioned in Git.

---

## Tech Stack

- Python
- Pandas
- Git
- CSV ingestion
- Hash-based anonymization
- Medallion Architecture

Planned:
- SQL (DuckDB / SQLite)
- Data Quality validation
- Orchestration layer
- BI layer

---

## How to Run

1. Place raw CSV files inside data/raw/
2. Run:

python scripts/anonymization/anonymize_booking.py  
python scripts/anonymization/anonymize_expedia.py  

Bronze files will be generated in data/bronze/

---

## Roadmap

[x] Bronze Layer (Anonymization & Standardization)  
[ ] Bronze Data Quality Checks  
[ ] Silver Unified Schema  
[ ] Gold Business Metrics  
[ ] SQL Layer  
[ ] BI / Dashboard  

---

## Project Goal

This repository demonstrates practical Data Engineering concepts applied to a hospitality business context, simulating a real-world data platform design from ingestion to analytics-ready datasets.
