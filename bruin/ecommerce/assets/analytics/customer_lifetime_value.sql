/* @bruin
name: analytics.customer_lifetime_value
type: duckdb.sql
materialization:
   type: table
depends:
   - fct_orders
   - dim_customers

columns:
  - name: customer_id
    type: varchar
    description: "Unique customer identifier"
    checks:
      - name: not_null
      - name: unique
  - name: email
    type: varchar
    description: "Customer email address"
    checks:
      - name: not_null
      - name: pattern
        value: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
  - name: total_lifetime_value
    type: decimal
    description: "Total amount spent by customer across all orders"
    checks:
      - name: not_null
  - name: order_count
    type: bigint
    description: "Total number of orders placed by customer"
    checks:
      - name: not_null
  - name: avg_order_value
    type: decimal
    description: "Average order value for this customer"

custom_checks:
  - name: avg_order_value_matches_calculation
    query: |
      SELECT COUNT(*) as issue_count
      FROM analytics.customer_lifetime_value
      WHERE ABS(avg_order_value - (total_lifetime_value / NULLIF(order_count, 0))) > 0.01
      AND order_count > 0
    value: 0
    
  - name: all_customers_have_clv_record
    query: |
      SELECT COUNT(*) as missing_count
      FROM dim_customers c
      LEFT JOIN analytics.customer_lifetime_value clv ON c.customer_id = clv.customer_id
      WHERE clv.customer_id IS NULL
    value: 0

@bruin */

SELECT 
    c.customer_id,
    c.email,
    c.name,
    c.country,
    c.city,
    COALESCE(SUM(o.total_amount), 0) AS total_lifetime_value,
    COUNT(o.order_id) AS order_count,
    COALESCE(AVG(o.total_amount), 0) AS avg_order_value,
    MIN(o.created_at) AS first_order_date,
    MAX(o.created_at) AS last_order_date,
    DATEDIFF('day', MIN(o.created_at), MAX(o.created_at)) AS customer_tenure_days
FROM dim_customers c
LEFT JOIN fct_orders o ON c.customer_id = o.customer_id
GROUP BY 
    c.customer_id,
    c.email,
    c.name,
    c.country,
    c.city
