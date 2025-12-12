# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "psycopg2-binary",
#     "faker",
# ]
# ///

import argparse
import os
import random
import uuid
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import execute_values
from faker import Faker

# Initialize Faker
fake = Faker()

def get_db_connection():
    return psycopg2.connect(
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
        database=os.environ.get("POSTGRES_DB")
    )

def create_tables(conn):
    with conn.cursor() as cur:
        print("Creating tables...")
        cur.execute("DROP TABLE IF EXISTS order_items CASCADE")
        cur.execute("DROP TABLE IF EXISTS orders CASCADE")
        cur.execute("DROP TABLE IF EXISTS products CASCADE")
        cur.execute("DROP TABLE IF EXISTS customers CASCADE")

        cur.execute("""
            CREATE TABLE customers (
                id VARCHAR(36) PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                country VARCHAR(100),
                city VARCHAR(100),
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE products (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE orders (
                id VARCHAR(36) PRIMARY KEY,
                customer_id VARCHAR(36) REFERENCES customers(id),
                status VARCHAR(50) NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE order_items (
                id VARCHAR(36) PRIMARY KEY,
                order_id VARCHAR(36) REFERENCES orders(id),
                product_id VARCHAR(36) REFERENCES products(id),
                quantity INTEGER NOT NULL,
                price_at_purchase DECIMAL(10, 2) NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """)
    conn.commit()

def generate_data(num_customers, num_orders, num_products):
    print(f"Generating {num_customers} customers, {num_products} products, {num_orders} orders...")
    
    # --- Customers ---
    customers = []
    for _ in range(num_customers):
        created_at = fake.date_time_between(start_date='-2y', end_date='-1y')
        updated_at = created_at
        
        # Simulate updates for 10% of customers
        if random.random() < 0.1:
            updated_at = fake.date_time_between(start_date=created_at, end_date='now')

        customers.append({
            'id': str(uuid.uuid4()),
            'email': fake.email(),
            'name': fake.name(),
            'country': fake.country(),
            'city': fake.city(),
            'created_at': created_at,
            'updated_at': updated_at
        })

    # --- Products ---
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Toys']
    products = []
    for _ in range(num_products):
        created_at = fake.date_time_between(start_date='-2y', end_date='-1y')
        updated_at = created_at
        
        # Simulate price updates for 20% of products
        if random.random() < 0.2:
            updated_at = fake.date_time_between(start_date=created_at, end_date='now')

        products.append({
            'id': str(uuid.uuid4()),
            'name': fake.catch_phrase(),
            'category': random.choice(categories),
            'price': round(random.uniform(10.0, 1000.0), 2),
            'created_at': created_at,
            'updated_at': updated_at
        })

    # --- Orders ---
    orders = []
    order_items = []
    
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    # Ensure some customers have NO orders (Inactive Customers)
    active_customers = random.sample(customers, k=int(num_customers * 0.8))
    
    # Ensure some products have NO sales (Unsold Products)
    active_products = random.sample(products, k=int(num_products * 0.9))

    for _ in range(num_orders):
        customer = random.choice(active_customers)
        order_id = str(uuid.uuid4())
        created_at = fake.date_time_between(start_date='-1y', end_date='now')
        updated_at = created_at
        
        status = random.choice(statuses)
        
        # Simulate order status updates for 30% of orders
        if random.random() < 0.3:
            updated_at = fake.date_time_between(start_date=created_at, end_date='now')
            # If updated, likely moved to a final state
            status = random.choice(['delivered', 'cancelled'])

        # Whale Order Logic: 1% chance of a massive order
        if random.random() < 0.01:
            num_items = random.randint(20, 50)
        else:
            num_items = random.randint(1, 5)

        order_total = 0
        
        for _ in range(num_items):
            product = random.choice(active_products)
            quantity = random.randint(1, 3)
            price = product['price']
            item_total = price * quantity
            order_total += item_total
            
            order_items.append({
                'id': str(uuid.uuid4()),
                'order_id': order_id,
                'product_id': product['id'],
                'quantity': quantity,
                'price_at_purchase': price,
                'updated_at': updated_at
            })
            
        orders.append({
            'id': order_id,
            'customer_id': customer['id'],
            'status': status,
            'total_amount': round(order_total, 2),
            'created_at': created_at,
            'updated_at': updated_at
        })

    return customers, products, orders, order_items

def insert_data(conn, customers, products, orders, order_items):
    print("Inserting data into database...")
    with conn.cursor() as cur:
        execute_values(cur, 
            "INSERT INTO customers (id, email, name, country, city, created_at, updated_at) VALUES %s",
            [(c['id'], c['email'], c['name'], c['country'], c['city'], c['created_at'], c['updated_at']) for c in customers])
            
        execute_values(cur, 
            "INSERT INTO products (id, name, category, price, created_at, updated_at) VALUES %s",
            [(p['id'], p['name'], p['category'], p['price'], p['created_at'], p['updated_at']) for p in products])
            
        execute_values(cur, 
            "INSERT INTO orders (id, customer_id, status, total_amount, created_at, updated_at) VALUES %s",
            [(o['id'], o['customer_id'], o['status'], o['total_amount'], o['created_at'], o['updated_at']) for o in orders])
            
        execute_values(cur, 
            "INSERT INTO order_items (id, order_id, product_id, quantity, price_at_purchase, updated_at) VALUES %s",
            [(i['id'], i['order_id'], i['product_id'], i['quantity'], i['price_at_purchase'], i['updated_at']) for i in order_items])
    
    conn.commit()
    print("Data insertion complete.")

def main():
    parser = argparse.ArgumentParser(description='Generate e-commerce data.')
    parser.add_argument('--customers', type=int, default=100, help='Number of customers')
    parser.add_argument('--orders', type=int, default=500, help='Number of orders')
    parser.add_argument('--products', type=int, default=50, help='Number of products')
    
    args = parser.parse_args()
    
    try:
        conn = get_db_connection()
        create_tables(conn)
        customers, products, orders, order_items = generate_data(args.customers, args.orders, args.products)
        insert_data(conn, customers, products, orders, order_items)
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()