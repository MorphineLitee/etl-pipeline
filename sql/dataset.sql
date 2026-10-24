-- Practice dataset for window functions (SQLite / Spark SQL / Postgres friendly)
-- Load:  sqlite3 practice.db < dataset.sql

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    dept_id   INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL
);

CREATE TABLE employees (
    emp_id     INTEGER PRIMARY KEY,
    emp_name   TEXT NOT NULL,
    dept_id    INTEGER REFERENCES departments(dept_id),
    hire_date  TEXT NOT NULL,      -- YYYY-MM-DD
    salary     INTEGER NOT NULL,
    manager_id INTEGER             -- NULL for the CEO-level person
);

CREATE TABLE sales (
    sale_id   INTEGER PRIMARY KEY,
    emp_id    INTEGER REFERENCES employees(emp_id),
    sale_date TEXT NOT NULL,       -- YYYY-MM-DD
    region    TEXT NOT NULL,       -- North / South / East / West
    amount    INTEGER NOT NULL
);

INSERT INTO departments VALUES
 (1, 'Engineering'),
 (2, 'Sales'),
 (3, 'Marketing'),
 (4, 'HR');

-- Note: deliberate salary ties inside departments (good for RANK vs DENSE_RANK vs ROW_NUMBER)
INSERT INTO employees VALUES
 (1,  'Asha Rao',      1, '2018-03-12', 150000, NULL),
 (2,  'Ben Carter',    1, '2019-07-01', 120000, 1),
 (3,  'Chitra Nair',   1, '2020-01-15', 120000, 1),
 (4,  'Dev Malhotra',  1, '2021-09-20',  95000, 2),
 (5,  'Elena Petrov',  1, '2022-04-04',  90000, 2),
 (6,  'Farah Khan',    1, '2023-02-27',  90000, 3),
 (7,  'Gita Sharma',   2, '2017-05-30', 110000, 1),
 (8,  'Hiro Tanaka',   2, '2019-11-11',  80000, 7),
 (9,  'Isha Verma',    2, '2020-06-08',  80000, 7),
 (10, 'Jack Miller',   2, '2021-03-22',  72000, 7),
 (11, 'Kiran Das',     2, '2022-08-16',  65000, 8),
 (12, 'Lena Schmidt',  3, '2018-10-05',  85000, 1),
 (13, 'Mohan Iyer',    3, '2020-12-01',  70000, 12),
 (14, 'Nina Lopez',    3, '2022-01-10',  70000, 12),
 (15, 'Omar Ali',      4, '2019-04-18',  68000, 1),
 (16, 'Priya Menon',   4, '2023-06-05',  55000, 15);

-- Sales: only the Sales team (7-11) plus two marketing reps (13, 14).
-- Dates span Jan-Jun 2024 with gaps; some same-day sales and repeated amounts.
INSERT INTO sales VALUES
 (1,  7,  '2024-01-05', 'North', 5000),
 (2,  8,  '2024-01-09', 'South', 3200),
 (3,  9,  '2024-01-15', 'East',  4100),
 (4,  10, '2024-01-20', 'West',  2800),
 (5,  11, '2024-01-28', 'North', 1500),
 (6,  7,  '2024-02-02', 'South', 6200),
 (7,  8,  '2024-02-10', 'East',  3200),
 (8,  9,  '2024-02-10', 'West',  4800),
 (9,  10, '2024-02-18', 'North', 2900),
 (10, 11, '2024-02-25', 'South', 1800),
 (11, 13, '2024-02-26', 'East',  2200),
 (12, 7,  '2024-03-03', 'West',  7000),
 (13, 8,  '2024-03-08', 'North', 3900),
 (14, 9,  '2024-03-12', 'South', 4100),
 (15, 10, '2024-03-19', 'East',  3300),
 (16, 11, '2024-03-27', 'West',  2100),
 (17, 14, '2024-03-30', 'North', 2600),
 (18, 7,  '2024-04-04', 'East',  5500),
 (19, 8,  '2024-04-11', 'West',  4400),
 (20, 9,  '2024-04-11', 'North', 5200),
 (21, 10, '2024-04-22', 'South', 3000),
 (22, 11, '2024-04-29', 'East',  2400),
 (23, 13, '2024-04-30', 'West',  1900),
 (24, 7,  '2024-05-06', 'North', 6800),
 (25, 8,  '2024-05-14', 'South', 3600),
 (26, 9,  '2024-05-20', 'East',  4100),
 (27, 10, '2024-05-23', 'West',  3500),
 (28, 11, '2024-05-31', 'North', 2700),
 (29, 14, '2024-06-02', 'South', 3100),
 (30, 7,  '2024-06-07', 'East',  7500),
 (31, 8,  '2024-06-13', 'West',  4200),
 (32, 9,  '2024-06-18', 'North', 5900),
 (33, 10, '2024-06-21', 'South', 3300),
 (34, 11, '2024-06-28', 'East',  3000);
