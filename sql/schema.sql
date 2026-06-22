-- Rent-A-Car — normalized (3NF) relational schema
-- Works with SQLite (demo) and is portable to MySQL with minor type tweaks
-- (e.g., INTEGER PRIMARY KEY AUTOINCREMENT -> INT AUTO_INCREMENT PRIMARY KEY).

PRAGMA foreign_keys = ON;

CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    phone         TEXT,
    license_no    TEXT    NOT NULL UNIQUE
);

CREATE TABLE cars (
    car_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    make          TEXT    NOT NULL,
    model         TEXT    NOT NULL,
    year          INTEGER NOT NULL,
    category      TEXT    NOT NULL,           -- Economy, SUV, Luxury, ...
    daily_rate    REAL    NOT NULL,
    status        TEXT    NOT NULL DEFAULT 'available'  -- available / rented
);

CREATE TABLE rentals (
    rental_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id   INTEGER NOT NULL,
    car_id        INTEGER NOT NULL,
    start_date    TEXT    NOT NULL,
    end_date      TEXT    NOT NULL,
    total_cost    REAL    NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (car_id)      REFERENCES cars(car_id)
);

CREATE TABLE payments (
    payment_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    rental_id     INTEGER NOT NULL,
    amount        REAL    NOT NULL,
    payment_date  TEXT    NOT NULL,
    method        TEXT    NOT NULL,           -- card / cash / upi
    FOREIGN KEY (rental_id) REFERENCES rentals(rental_id)
);

-- Indexes to speed up frequent reporting joins/filters
CREATE INDEX idx_rentals_customer ON rentals(customer_id);
CREATE INDEX idx_rentals_car      ON rentals(car_id);
CREATE INDEX idx_payments_rental  ON payments(rental_id);
CREATE INDEX idx_cars_category    ON cars(category);
