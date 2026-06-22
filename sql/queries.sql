-- Analytical / reporting queries (joins, GROUP BY, subqueries)

-- 1) Revenue by car category (JOIN + GROUP BY)
SELECT c.category,
       COUNT(r.rental_id)      AS rentals,
       ROUND(SUM(r.total_cost),2) AS revenue
FROM rentals r
JOIN cars c ON c.car_id = r.car_id
GROUP BY c.category
ORDER BY revenue DESC;

-- 2) Top customers by total spend (JOIN + GROUP BY + ORDER + LIMIT)
SELECT cu.name,
       COUNT(r.rental_id)         AS rentals,
       ROUND(SUM(r.total_cost),2) AS total_spent
FROM customers cu
JOIN rentals r ON r.customer_id = cu.customer_id
GROUP BY cu.customer_id
ORDER BY total_spent DESC
LIMIT 5;

-- 3) Cars that have never been rented (subquery)
SELECT make, model, category
FROM cars
WHERE car_id NOT IN (SELECT DISTINCT car_id FROM rentals);

-- 4) Average rental duration in days (date math)
SELECT ROUND(AVG(julianday(end_date) - julianday(start_date)), 1) AS avg_days
FROM rentals;

-- 5) Monthly revenue from payments (GROUP BY on derived month)
SELECT substr(payment_date, 1, 7) AS month,
       ROUND(SUM(amount), 2)      AS revenue
FROM payments
GROUP BY month
ORDER BY month;
