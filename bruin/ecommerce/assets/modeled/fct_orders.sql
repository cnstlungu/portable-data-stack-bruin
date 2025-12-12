/* @bruin
name: fct_orders
type: duckdb.sql
materialization:
   type: table
depends:
   - raw.orders
   - fct_order_items

columns:
  - name: order_id
    type: varchar
    checks:
      - name: not_null
      - name: unique
  - name: customer_id
    type: varchar
    checks:
      - name: not_null
  - name: status
    type: varchar
    checks:
      - name: not_null
      - name: accepted_values
        value: ["pending", "processing", "shipped", "delivered", "cancelled"]
  - name: total_amount
    type: decimal
    checks:
      - name: not_null
      - name: positive

custom_checks:
  - name: order_total_matches_line_items
    query: |
      SELECT COUNT(*) as issue_count
      FROM fct_orders o
      LEFT JOIN (
        SELECT order_id, SUM(total_item_amount) as calculated_total
        FROM fct_order_items
        GROUP BY order_id
      ) oi ON o.order_id = oi.order_id
      WHERE ABS(COALESCE(o.total_amount, 0) - COALESCE(oi.calculated_total, 0)) > 0.01
    value: 0

@bruin */

SELECT 
    id AS order_id,
    customer_id,
    status,
    total_amount,
    created_at,
    updated_at
FROM raw.orders
