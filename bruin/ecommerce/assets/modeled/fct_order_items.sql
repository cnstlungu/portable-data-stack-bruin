/* @bruin
name: fct_order_items
type: duckdb.sql
materialization:
   type: table
   strategy: merge
depends:
   - raw.order_items

columns:
  - name: order_item_id
    type: varchar
    primary_key: true
    checks:
      - name: not_null
      - name: unique
  - name: order_id
    type: varchar
    checks:
      - name: not_null
  - name: product_id
    type: varchar
    checks:
      - name: not_null
  - name: quantity
    type: bigint
    checks:
      - name: not_null
      - name: positive
  - name: price_at_purchase
    type: decimal
    checks:
      - name: not_null
      - name: positive
  - name: total_item_amount
    type: decimal
    checks:
      - name: not_null
      - name: positive

custom_checks:
  - name: total_amount_calculation_correct
    query: |
      SELECT COUNT(*) as issue_count
      FROM fct_order_items
      WHERE ABS(total_item_amount - (quantity * price_at_purchase)) > 0.01
    value: 0

@bruin */

SELECT 
    id AS order_item_id,
    order_id,
    product_id,
    quantity,
    price_at_purchase,
    quantity * price_at_purchase AS total_item_amount,
    updated_at
FROM raw.order_items
