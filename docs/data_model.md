# Data Model

## Silver Layer Schema

### stg_bookings.csv

| Column | Type | Description |
|---------|------|------------|
| booking_date | datetime | Date reservation was made |
| check_in | datetime | Check-in date |
| check_out | datetime | Check-out date |
| price | float | Booking value |
| status | string | OK / Cancelled |
| booker_country | string | Country code |
| cancelling_date | datetime | Cancellation date |
| source | string | booking / expedia |

---

### stg_reviews.csv

| Column | Type | Description |
|----------|------|------------|
| review_date | datetime | Date review was posted |
| review_rating | float | Rating (0–10 scale) |
| review_title | string | Review headline |
| review_text | string | Review content |
| review_response | string | Property response |
| source | string | booking / expedia |

---

## Gold Layer Outputs

### Booking KPIs
- kpi_bookings_summary.csv
- kpi_revenue_by_source.csv

### Review KPIs
- kpi_reviews_summary.csv
- kpi_reviews_count_by_source.csv
- kpi_reviews_avg_by_source.csv
- kpi_reviews_monthly_volume.csv
