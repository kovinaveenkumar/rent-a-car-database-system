"""Create the SQLite database from schema.sql and seed sample data.

Run:  python -m src.init_db   (creates rentacar.db)
"""
from __future__ import annotations

import os
import random
import sqlite3
from datetime import date, timedelta

DB = "rentacar.db"
SCHEMA = os.path.join("sql", "schema.sql")


def seed(conn: sqlite3.Connection, seed_val: int = 42) -> None:
    random.seed(seed_val)
    cur = conn.cursor()

    customers = [
        ("Aarav Sharma", "aarav@example.com", "201-555-0101", "DL1001"),
        ("Bianca Lopez", "bianca@example.com", "201-555-0102", "DL1002"),
        ("Chen Wei", "chen@example.com", "201-555-0103", "DL1003"),
        ("Diana Patel", "diana@example.com", "201-555-0104", "DL1004"),
        ("Ethan Brown", "ethan@example.com", "201-555-0105", "DL1005"),
    ]
    cur.executemany(
        "INSERT INTO customers(name,email,phone,license_no) VALUES (?,?,?,?)", customers
    )

    cars = [
        ("Toyota", "Corolla", 2022, "Economy", 45.0),
        ("Honda", "Civic", 2021, "Economy", 48.0),
        ("Ford", "Explorer", 2023, "SUV", 85.0),
        ("Jeep", "Wrangler", 2022, "SUV", 95.0),
        ("BMW", "5 Series", 2023, "Luxury", 140.0),
        ("Tesla", "Model 3", 2023, "Luxury", 130.0),
    ]
    cur.executemany(
        "INSERT INTO cars(make,model,year,category,daily_rate) VALUES (?,?,?,?,?)", cars
    )

    methods = ["card", "cash", "upi"]
    start = date(2026, 1, 1)
    # Note: car_id 6 (Tesla) intentionally left un-rented to demo the subquery.
    for _ in range(40):
        cust = random.randint(1, 5)
        car = random.randint(1, 5)
        s = start + timedelta(days=random.randint(0, 150))
        days = random.randint(1, 10)
        e = s + timedelta(days=days)
        rate = dict(enumerate([45, 48, 85, 95, 140, 130], start=1))[car]
        cost = round(rate * days, 2)
        cur.execute(
            "INSERT INTO rentals(customer_id,car_id,start_date,end_date,total_cost) "
            "VALUES (?,?,?,?,?)",
            (cust, car, s.isoformat(), e.isoformat(), cost),
        )
        rid = cur.lastrowid
        cur.execute(
            "INSERT INTO payments(rental_id,amount,payment_date,method) VALUES (?,?,?,?)",
            (rid, cost, e.isoformat(), random.choice(methods)),
        )
    conn.commit()


def main() -> None:
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    with open(SCHEMA, encoding="utf-8") as f:
        conn.executescript(f.read())
    seed(conn)
    n = conn.execute("SELECT COUNT(*) FROM rentals").fetchone()[0]
    print(f"Created {DB} with {n} rentals seeded.")
    conn.close()


if __name__ == "__main__":
    main()
