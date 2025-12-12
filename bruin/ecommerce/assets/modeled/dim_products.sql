/* @bruin
name: dim_products
type: duckdb.sql
materialization:
   type: table
depends:
   - raw.products

columns:
  - name: product_id
    type: varchar
    description: "Unique product identifier"
    checks:
      - name: not_null
      - name: unique
  - name: current_price
    type: decimal
    description: "Current product price"
    checks:
      - name: not_null
      - name: positive
  - name: category
    type: varchar
    checks:
      - name: not_null
      - name: accepted_values
        value: ["Electronics", "Books", "Clothing", "Home & Garden", "Toys"]

@bruin */

SELECT 
    id AS product_id,
    name,
    category,
    price AS current_price,
    created_at,
    updated_at
FROM raw.products
