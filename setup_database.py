# filename: setup_database.py

import sqlite3
from pathlib import Path


database_path = Path(__file__).resolve().parent / "data" / "database.sqlite"
database_path.parent.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(database_path) as connection:
    cursor = connection.cursor()

    cursor.executescript(
        """
        DROP TABLE IF EXISTS sales;
        DROP TABLE IF EXISTS customer_employee;
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS employees;

        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            department TEXT NOT NULL,
            satisfaction_score REAL NOT NULL CHECK (satisfaction_score BETWEEN 0 AND 5),
            tenure_years REAL NOT NULL CHECK (tenure_years >= 0)
        );

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            industry TEXT NOT NULL,
            churn_date TEXT,
            satisfaction_score REAL NOT NULL CHECK (satisfaction_score BETWEEN 0 AND 5)
        );

        CREATE TABLE customer_employee (
            customer_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            assigned_date TEXT NOT NULL,

            PRIMARY KEY (customer_id, employee_id),

            FOREIGN KEY (customer_id)
                REFERENCES customers(id)
                ON DELETE CASCADE,

            FOREIGN KEY (employee_id)
                REFERENCES employees(id)
                ON DELETE RESTRICT
        );

        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            region TEXT NOT NULL,
            product TEXT NOT NULL,
            revenue REAL NOT NULL CHECK (revenue >= 0),
            date TEXT NOT NULL,
            units_sold INTEGER NOT NULL CHECK (units_sold >= 0),

            FOREIGN KEY (customer_id)
                REFERENCES customers(id)
                ON DELETE RESTRICT,

            FOREIGN KEY (employee_id)
                REFERENCES employees(id)
                ON DELETE RESTRICT,

            FOREIGN KEY (customer_id, employee_id)
                REFERENCES customer_employee(customer_id, employee_id)
                ON DELETE RESTRICT
        );

        INSERT INTO employees
            (id, department, satisfaction_score, tenure_years)
        VALUES
            (1, 'Consulting', 4.4, 3.5),
            (2, 'Audit', 4.1, 6.0),
            (3, 'Tax', 4.6, 2.0),
            (4, 'Technology', 3.9, 4.5),
            (5, 'Consulting', 4.7, 5.2),
            (6, 'Audit', 4.3, 2.8),
            (7, 'Tax', 4.0, 7.1),
            (8, 'Technology', 4.5, 1.8),
            (9, 'Consulting', 4.2, 1.2);

        INSERT INTO customers
            (id, name, industry, churn_date, satisfaction_score)
        VALUES
            (1, 'Acme Corporation', 'Manufacturing', NULL, 4.6),
            (2, 'Beacon Health', 'Healthcare', NULL, 4.2),
            (3, 'Meridian Home Products', 'Retail', '2026-02-14', 2.8),
            (4, 'Delta Financial', 'Financial Services', NULL, 4.8),
            (5, 'Horizon Logistics', 'Transportation', NULL, 4.1),
            (6, 'Southstar Energy', 'Energy', NULL, 4.5),
            (7, 'Pinecrest University', 'Education', NULL, 4.0),
            (8, 'Silverline Media', 'Media', NULL, 3.7),
            (9, 'Summit Telecom', 'Telecommunications', NULL, 4.3),
            (10, 'Greenfield Foods', 'Food and Beverage', NULL, 4.4);

        INSERT INTO customer_employee
            (customer_id, employee_id, role, assigned_date)
        VALUES
            (1, 1, 'Account Lead', '2026-01-05'),
            (1, 4, 'Technology Specialist', '2026-01-06'),
            (2, 3, 'Account Lead', '2026-01-08'),
            (2, 8, 'Technology Specialist', '2026-01-09'),
            (3, 5, 'Account Lead', '2026-01-10'),
            (3, 2, 'Audit Specialist', '2026-01-11'),
            (4, 3, 'Account Lead', '2026-01-12'),
            (4, 8, 'Technology Specialist', '2026-01-13'),
            (5, 1, 'Account Lead', '2026-01-15'),
            (5, 4, 'Technology Specialist', '2026-01-16'),
            (6, 5, 'Account Lead', '2026-01-18'),
            (6, 9, 'Consulting Specialist', '2026-01-19'),
            (7, 1, 'Account Lead', '2026-01-21'),
            (7, 2, 'Audit Specialist', '2026-01-22'),
            (8, 9, 'Account Lead', '2026-01-24'),
            (8, 4, 'Technology Specialist', '2026-01-25'),
            (9, 5, 'Account Lead', '2026-01-27'),
            (9, 8, 'Technology Specialist', '2026-01-28'),
            (10, 3, 'Account Lead', '2026-01-30'),
            (10, 6, 'Audit Specialist', '2026-01-31');

        INSERT INTO sales
            (id, customer_id, employee_id, region, product, revenue, date, units_sold)
        VALUES
            (1, 1, 1, 'East', 'Analytics Platform', 125000.00, '2026-01-15', 42),
            (2, 1, 4, 'East', 'Cloud Services', 112500.00, '2026-02-03', 18),
            (3, 2, 3, 'West', 'Cybersecurity', 98000.00, '2026-02-10', 31),
            (4, 2, 8, 'West', 'Analytics Platform', 76500.00, '2026-03-12', 24),
            (5, 3, 5, 'South', 'Analytics Platform', 143500.00, '2026-02-22', 55),
            (6, 3, 2, 'South', 'Tax Advisory', 42000.00, '2026-01-30', 12),
            (7, 4, 3, 'North', 'Cybersecurity', 87500.00, '2026-03-05', 27),
            (8, 4, 8, 'North', 'Cloud Services', 131000.00, '2026-04-11', 39),
            (9, 5, 1, 'East', 'Analytics Platform', 119500.00, '2026-03-18', 36),
            (10, 5, 4, 'East', 'Cloud Services', 104000.00, '2026-04-02', 22),
            (11, 6, 5, 'West', 'Cybersecurity', 157500.00, '2026-04-19', 44),
            (12, 6, 9, 'West', 'Analytics Platform', 128000.00, '2026-05-07', 41),
            (13, 7, 1, 'South', 'Cloud Services', 91000.00, '2026-05-14', 29),
            (14, 7, 2, 'South', 'Audit Readiness', 68000.00, '2026-05-21', 17),
            (15, 8, 9, 'North', 'Analytics Platform', 73500.00, '2026-04-28', 23),
            (16, 8, 4, 'North', 'Cloud Services', 84500.00, '2026-05-03', 26),
            (17, 9, 5, 'East', 'Cybersecurity', 146000.00, '2026-06-09', 38),
            (18, 9, 8, 'East', 'Cloud Services', 99000.00, '2026-06-17', 30),
            (19, 10, 3, 'South', 'Tax Advisory', 62500.00, '2026-06-24', 15),
            (20, 10, 6, 'South', 'Analytics Platform', 108500.00, '2026-07-02', 33);
        """
    )

print(f"Database created at: {database_path}")
print("Tables created: sales, customers, employees")
