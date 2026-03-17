-- Hospitality Data Platform
-- Analytical SQL Queries
-- Author: Francisco Cunha
-- Purpose: Demonstrate warehouse-level analytics using SQL

SELECT source, 
SUM(price) AS total_revenue
FROM silver.bookings
WHERE status = 'OK'
GROUP BY source;

SELECT source,
total_bookings,
total_cancelled,
ROUND((total_cancelled * 100.0) / total_bookings,2) AS cancellation_rate
FROM (
SELECT source,
COUNT(*) FILTER(WHERE status = 'Cancelled') AS total_cancelled,
COUNT(status) AS total_bookings
FROM silver.bookings
GROUP BY source
) t
ORDER BY cancellation_rate DESC;


SELECT source,
ROUND(AVG(price) FILTER(WHERE status = 'OK'),2) AS avg_booking_value
FROM silver.bookings
GROUP BY source
ORDER by avg_booking_value DESC;


SELECT
DATE_TRUNC('month', booking_date) AS month,
SUM(price) AS month_revenue
FROM silver.bookings
WHERE status = 'OK'
GROUP BY month
ORDER BY month;

SELECT
ROUND((revenue_booking * 100.0) / revenue_total, 2) AS booking_rate,
ROUND((revenue_expedia * 100.0) / revenue_total, 2) AS expedia_rate
FROM (
SELECT
SUM(price) FILTER (WHERE source = 'booking' AND status = 'OK') AS revenue_booking,
SUM(price) FILTER (WHERE source = 'expedia' AND status = 'OK') AS revenue_expedia,
SUM(price) FILTER (WHERE status = 'OK') AS revenue_total
FROM silver.bookings
) r;

SELECT source,
ROUND(AVG(review_rating),2) AS avg_rating
FROM silver.reviews
GROUP BY source;

SELECT
DATE_TRUNC ('month', review_date) AS month,
COUNT(*) AS number_of_reviews
FROM silver.reviews
GROUP BY month 
ORDER BY month;


SELECT 
COALESCE(booker_country, 'Expedia Unknown') as country,
ROUND(SUM(price),2) as revenue
FROM silver.bookings
WHERE status = 'OK'
GROUP BY booker_country
ORDER BY revenue DESC



