# Data Model

## Silver Table: stg_bookings

| Column | Type | Description |
|--------|------|------------|
| booking_date | datetime | Reservation creation timestamp |
| check_in | datetime | Guest check-in date |
| check_out | datetime | Guest check-out date |
| price | float | Booking revenue amount |
| status | string | OK or Cancelled |
| booker_country | string | ISO country code (nullable for Expedia) |
| cancelling_date | datetime | Cancellation timestamp (nullable) |
| source | string | booking or expedia |

---

## Gold Table: kpi_bookings

| Metric | Description |
|--------|------------|
| total_bookings | Total number of bookings |
| total_revenue | Sum of revenue for status = OK |
| cancelled_bookings | Total cancelled bookings |
| cancellation_rate_percent | Cancelled / Total |
| avg_booking_value | Average revenue per confirmed booking |
| revenue_by_source | Revenue per OTA |
