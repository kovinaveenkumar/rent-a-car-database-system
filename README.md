# Rent-A-Car Database Management System

> A relational database system for car rentals — normalized 3NF schema, indexed analytical SQL, and an interactive Streamlit reporting dashboard.

![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

A full database-driven application for a car-rental business covering the complete data lifecycle: **ER design → normalized (3NF) schema → seed data → analytical SQL (joins, GROUP BY, subqueries) → indexed performance → a Streamlit dashboard**. It ships with **SQLite** so it runs with zero setup, and the schema is **portable to MySQL** with minor type tweaks.

## Key Features

- **3NF relational schema** — `customers`, `cars`, `rentals`, `payments` with primary/foreign keys
- **Indexes** on common join/filter columns for faster reporting
- **Analytical SQL** — revenue by category, top customers, cars never rented (subquery), average rental duration, monthly revenue
- **Seed script** generating realistic sample data
- **Streamlit dashboard** with KPI metrics, bar/line charts, and tables

## Sample Output

```
=== Revenue by category ===
  SUV | 14 | 7990.0
  Economy | 21 | 5430.0
  Luxury | 5 | 3780.0

=== Cars never rented ===   (subquery)
  Tesla | Model 3 | Luxury

=== Average rental duration (days) ===
  5.8
```

## Tech Stack

SQL (SQLite / MySQL-portable) · Python · Streamlit · pandas

## Schema

```
customers ──< rentals >── cars
                 │
                 ▼
              payments
```

## Project Structure

```
.
├── sql/
│   ├── schema.sql       # 3NF tables, keys, indexes
│   └── queries.sql      # analytical/reporting queries
├── src/
│   ├── init_db.py       # build DB from schema + seed sample data
│   └── reports.py       # run reporting queries (CLI)
├── app/
│   └── app.py           # Streamlit dashboard
├── requirements.txt
└── README.md
```

## Getting Started

```bash
pip install -r requirements.txt

# 1. Create and seed the database (writes rentacar.db)
python -m src.init_db

# 2a. Run text reports
python -m src.reports

# 2b. Or launch the dashboard
streamlit run app/app.py
```

## Porting to MySQL

Use `sql/schema.sql` as a base; change `INTEGER PRIMARY KEY AUTOINCREMENT` to
`INT AUTO_INCREMENT PRIMARY KEY`, point a MySQL connector at your server, and the
queries in `sql/queries.sql` run with minimal changes (replace the SQLite
`julianday()` / `substr()` date helpers with `DATEDIFF()` / `DATE_FORMAT()`).

## License

MIT
