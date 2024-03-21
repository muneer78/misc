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

# Categorize data
SELECT 
    SaleAmount,
    CASE 
        WHEN SaleAmount > 1000 THEN 'High'
        WHEN SaleAmount BETWEEN 500 AND 1000 THEN 'Medium'
        ELSE 'Low'
    END AS SaleLevel
FROM Sales;

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

# Advanced use of CASE WHEN
SELECT 
    CustomerID,
    PurchaseAmount,
    CASE 
        WHEN CustomerStatus = 'VIP' AND PurchaseAmount > 1000 THEN PurchaseAmount * 0.8
        WHEN CustomerStatus = 'Regular' AND PurchaseAmount > 1000 THEN PurchaseAmount * 0.9
        ELSE PurchaseAmount
    END AS FinalAmount
FROM Customers;

# Use numbers in Group By
SELECT DISTINCT rcdc."name", rcdc.account_rep__c
FROM crm.rpl_cadence_details__c rcdc
WHERE rcdc.account_rep__c IS NOT NULL
GROUP BY 1, 2
LIMIT 100
```
