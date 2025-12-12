/* @bruin
name: analytics.unsold_products
type: duckdb.sql
materialization:
   type: view
depends:
   - dim_products
   - fct_order_items

columns:
  - name: product_id
    type: varchar
    description: "Product ID that has never been sold"
    checks:
      - name: not_null
      - name: unique

custom_checks:
  - name: unsold_products_have_no_sales
    query: |
      SELECT COUNT(*) as issue_count
      FROM analytics.unsold_products up
      INNER JOIN fct_order_items oi ON up.product_id = oi.product_id
    value: 0

@bruin */

-- Identify products that have never been sold
SELECT 
    p.product_id,
    p.name AS product_name,
    p.category,
    p.current_price,
    p.created_at AS product_created_at,
    DATEDIFF('day', p.created_at, CAST(CURRENT_TIMESTAMP AS TIMESTAMP)) AS days_since_creation
FROM dim_products p
LEFT JOIN fct_order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL

