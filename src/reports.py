"""Run the analytical reporting queries and print the results.

Run:  python -m src.reports
"""
from __future__ import annotations

import sqlite3

DB = "rentacar.db"

REPORTS = {
    "Revenue by category": """
        SELECT c.category, COUNT(r.rental_id) AS rentals,
               ROUND(SUM(r.total_cost),2) AS revenue
        FROM rentals r JOIN cars c ON c.car_id = r.car_id
        GROUP BY c.category ORDER BY revenue DESC;""",
    "Top 5 customers by spend": """
        SELECT cu.name, COUNT(r.rental_id) AS rentals,
               ROUND(SUM(r.total_cost),2) AS total_spent
        FROM customers cu JOIN rentals r ON r.customer_id = cu.customer_id
        GROUP BY cu.customer_id ORDER BY total_spent DESC LIMIT 5;""",
    "Cars never rented": """
        SELECT make, model, category FROM cars
        WHERE car_id NOT IN (SELECT DISTINCT car_id FROM rentals);""",
    "Average rental duration (days)": """
        SELECT ROUND(AVG(julianday(end_date)-julianday(start_date)),1) AS avg_days
        FROM rentals;""",
    "Monthly revenue": """
        SELECT substr(payment_date,1,7) AS month, ROUND(SUM(amount),2) AS revenue
        FROM payments GROUP BY month ORDER BY month;""",
}


def main() -> None:
    conn = sqlite3.connect(DB)
    for title, sql in REPORTS.items():
        print(f"\n=== {title} ===")
        for row in conn.execute(sql).fetchall():
            print("  " + " | ".join(str(x) for x in row))
    conn.close()


if __name__ == "__main__":
    main()
