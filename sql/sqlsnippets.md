# Data cleaning

```
# Filtering Out Rows with Missing Values
SELECT order_id, order_status, order_delivered_carrier_date
FROM orders
WHERE order_delivered_carrier_date IS NULL;

# Replacing Missing Values
SELECT order_id, order_status, COALESCE(order_delivered_carrier_date, 'Unknown') AS filled_column
FROM orders;

# Finding duplicate records
SELECT order_id, customer_id, COUNT(*)
FROM orders
GROUP BY order_id, customer_id
HAVING COUNT(*) > 1;
```

# Data analysis

```
# Window function to rank categorical variable
SELECT * , ROW_NUMBER() OVER(PARTITION BY position ORDER BY salary DESC) AS employee_rank
FROM employees;

# Categorize data with CASE statements
SELECT 
    SaleAmount,
    CASE 
        WHEN SaleAmount > 1000 THEN 'High'
        WHEN SaleAmount BETWEEN 500 AND 1000 THEN 'Medium'
        ELSE 'Low'
    END AS SaleLevel
FROM Sales;

# Window function to find duplicate rows
WHERE id IN (
SELECT id
ROW NUMBER() OVER(PARTITIon by VAR1, VAR2) as rownum
FROM table) as sub
WHERE rownum >1
);

# Categorizing with CASE WHEN
SELECT 
    CustomerID,
    PurchaseAmount,
    CASE 
        WHEN CustomerStatus = 'VIP' AND PurchaseAmount > 1000 THEN PurchaseAmount * 0.8
        WHEN CustomerStatus = 'Regular' AND PurchaseAmount > 1000 THEN PurchaseAmount * 0.9
        ELSE PurchaseAmount
    END AS FinalAmount
FROM Customers;

# Using CASE in WHERE Clause
SELECT *
FROM customers
WHERE CASE
    WHEN country = 'USA' THEN sales_region = 'North America'
    WHEN country = 'UK' THEN sales_region = 'Europe'
    ELSE FALSE
END;

# Using CASE with Aggregate Functions
SELECT
    department,
    COUNT(CASE WHEN salary > 50000 THEN 1 END) AS high_salary_count,
    COUNT(CASE WHEN salary <= 50000 THEN 1 END) AS low_salary_count
FROM employees
GROUP BY department;

# Nesting CASE Statements
SELECT
    order_id,
    CASE
        WHEN payment_status = 'paid' THEN
            CASE
                WHEN shipping_status = 'shipped' THEN 'Delivered'
                ELSE 'Processing'
            END
        ELSE 'Pending'
    END AS order_status
FROM orders;

# Using CASE in JOIN Conditions
SELECT
    o.order_id,
    o.order_date,
    c.customer_name
FROM orders o
JOIN customers c
ON CASE
    WHEN o.customer_id = 1 THEN c.customer_id = o.customer_id
    WHEN o.customer_id = 2 THEN c.country = 'USA'
    ELSE c.country = 'UK'
END;

# IN operator filters records based on a specified set of values
SELECT column1 FROM your_table WHERE column1 IN ('value1', 'value2');

# Subquery with IN Clause
SELECT *
FROM employees
WHERE department_id IN (SELECT department_id FROM departments WHERE department_name = 'Sales');

# COALESCE() returns the first non-NULL value in a list
SELECT COALESCE(column1, 'default_value') FROM your_table;

# Self-Join for Hierarchy
SELECT e.employee_name, m.employee_name AS manager_name
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id;

# Window function
SELECT order_date, sales_amount, SUM(sales_amount) OVER (ORDER BY order_date) AS running_total
FROM sales;

# Pivot data
SELECT *
FROM (
    SELECT TO_CHAR(order_date, 'YYYY-MM') AS month, product_category, sales_amount
    FROM sales
) AS pivoted
PIVOT (
    SUM(sales_amount)
    FOR product_category IN ('Electronics', 'Clothing', 'Books')
) AS pivoted_sales;

# ROLLUP for Hierarchical Aggregation
SELECT region, MONTH(order_date) AS month, SUM(total_sales) AS monthly_sales
FROM sales
GROUP BY ROLLUP(region, MONTH(order_date));

# Recursive query example
WITH RECURSIVE employee_hierarchy AS (
  SELECT employee_id, first_name, last_name, manager_id, 1 AS level
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  SELECT e.employee_id, e.first_name, e.last_name, e.manager_id, eh.level + 1
  FROM employees e
  JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT first_name, last_name, level
FROM employee_hierarchy;

# Subquery factoring
WITH cte_product_sales AS (
  SELECT product_id, SUM(quantity * unit_price) AS total_sales
  FROM order_items oi
  JOIN orders o ON oi.order_id = o.order_id
  WHERE o.order_date >= '2022-01-01' AND o.order_date < '2023-01-01'
  GROUP BY product_id
)
SELECT p.product_name, coalesce(ps.total_sales, 0) AS total_sales
FROM products p
LEFT JOIN cte_product_sales ps ON p.product_id = ps.product_id;

# Lateral join
SELECT p.product_name, p.category_id,
  (SELECT category_name
   FROM categories c
   WHERE c.category_id = p.category_id) AS category_name,
  (SELECT array_agg(tag_name ORDER BY tag_name)
   FROM product_tags pt
   JOIN tags t ON pt.tag_id = t.tag_id
   WHERE pt.product_id = p.product_id) AS tags
FROM products p;
```
# Dates
```
# Calculating the difference between two timestamps
SELECT TIMESTAMPDIFF(MINUTE, start_time, end_time) AS duration_minutes;


```
# Redshift specific
```
# Pivot
SELECT
  id, 
  has_homepage::boolean, 
  has_contacts_page::boolean, 
  has_about_page::boolean
FROM (SELECT id, page_type FROM user_pages WHERE is_active) 
PIVOT(COUNT(*) FOR page_type IN ('home' AS has_homepage, 'contact' AS has_contact_page, 'about' AS has_about_page))

# LTRIM allows you to trim a specified string from the beginning of a text field
SELECT
  LTRIM('airbyte_', source_id) AS source_id,
  LTRIM('airbyte_', source_name) AS source_name 
FROM source_data

# NVL2 allows you to specify a column name, a value to return if the column’s value is NOT NULL, and a value to return if the column’s value is NULL.
SELECT 
  user_id, 
  NVL2(user_email, user_email, account_email) AS email_address 
FROM users

# JSON_EXTRACT_PATH_TEXT allows you to extract the value of a specified key, with the option of returning NULL for records that may not have that key
SELECT
  user_id,
  JSON_EXTRACT_PATH_TEXT(user_contact_info, email, TRUE) AS user_email 
FROM users

# NULLIF allows you to compare two arguments and return NULL if they are equal
SELECT
  user_id, 
  user_email, 
  account_email
FROM users
WHERE NULLIF(user_email, account_email) IS NOT NULL

```
