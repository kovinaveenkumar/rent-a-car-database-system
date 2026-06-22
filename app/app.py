"""Streamlit front end for the Rent-A-Car database.

Run:  streamlit run app/app.py
(Make sure you've created the DB first: python -m src.init_db)
"""
from __future__ import annotations

import sqlite3

import pandas as pd
import streamlit as st

DB = "rentacar.db"


@st.cache_data
def q(sql: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


st.set_page_config(page_title="Rent-A-Car Dashboard", layout="wide")
st.title("🚗 Rent-A-Car — Reporting Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total rentals", int(q("SELECT COUNT(*) n FROM rentals")["n"][0]))
col2.metric("Total revenue", f"${q('SELECT SUM(total_cost) s FROM rentals')['s'][0]:,.0f}")
col3.metric("Fleet size", int(q("SELECT COUNT(*) n FROM cars")["n"][0]))

st.subheader("Revenue by category")
cat = q(
    "SELECT c.category, ROUND(SUM(r.total_cost),2) revenue "
    "FROM rentals r JOIN cars c ON c.car_id=r.car_id "
    "GROUP BY c.category ORDER BY revenue DESC"
)
st.bar_chart(cat, x="category", y="revenue")

st.subheader("Top customers")
st.dataframe(
    q(
        "SELECT cu.name, COUNT(r.rental_id) rentals, ROUND(SUM(r.total_cost),2) total_spent "
        "FROM customers cu JOIN rentals r ON r.customer_id=cu.customer_id "
        "GROUP BY cu.customer_id ORDER BY total_spent DESC"
    ),
    use_container_width=True,
)

st.subheader("Monthly revenue")
st.line_chart(
    q(
        "SELECT substr(payment_date,1,7) month, ROUND(SUM(amount),2) revenue "
        "FROM payments GROUP BY month ORDER BY month"
    ),
    x="month",
    y="revenue",
)
