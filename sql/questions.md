# Window function practice

Setup: `sqlite3 practice.db < sql/dataset.sql` then `sqlite3 -header -column practice.db`

Tables: `departments(dept_id, dept_name)`,
`employees(emp_id, emp_name, dept_id, hire_date, salary, manager_id)`,
`sales(sale_id, emp_id, sale_date, region, amount)`

## Ranking (ROW_NUMBER / RANK / DENSE_RANK / NTILE)
1. Rank all employees by salary, highest first. Show ROW_NUMBER, RANK and DENSE_RANK side by side. Why do they differ?
2. Top 2 highest-paid employees in each department (use DENSE_RANK; then try ROW_NUMBER and compare).
3. Split employees into 4 salary quartiles with NTILE.
4. Find the 2nd highest salary in each department.
5. Show each employee's most recent sale only (one row per employee).

## Aggregates over a window (SUM / AVG / COUNT ... OVER)
6. For each employee, show salary and the department's average salary on the same row.
7. Show each employee's salary as a % of their department's total payroll.
8. Show employees earning more than their department average.
9. Running total of `amount` across all sales ordered by date (break ties with sale_id).
10. Running total of sales per employee.

## Offset functions (LAG / LEAD / FIRST_VALUE / LAST_VALUE)
11. For each sale, show the previous sale amount for the same employee and the difference.
12. Number of days between each employee's consecutive sales.
13. Month-over-month change in total sales (aggregate by month first, then LAG).
14. For each department, show the lowest-paid employee's name next to every row (FIRST_VALUE).
15. Show each employee's hire order within their department and the name of the person hired right before them.

## Frames (ROWS / RANGE BETWEEN)
16. 3-sale moving average of `amount` (current + 2 preceding, ordered by date).
17. Rolling 30-day total of sales (RANGE or a self-join; note SQLite's RANGE limits).
18. Cumulative sales per region ordered by date.
19. Why does LAST_VALUE return the current row by default? Fix it with an explicit frame.

## Challenges
20. For each month, find the top salesperson and their share of that month's total.
21. Identify "gaps and islands": streaks of consecutive months in which an employee made at least one sale.
22. Find employees whose salary is within 10% of their department's maximum.
23. Use `manager_id` to show each employee's salary next to their manager's salary and the diff (self-join + window avg of the manager's team).
24. Percentile: use PERCENT_RANK and CUME_DIST on salary within each department.
