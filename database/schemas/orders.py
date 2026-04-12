def create_orders_table(cursor):
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders(
                           order_id UUID PRIMARY KEY,
                           customer_id UUID,
                           order_date TIMESTAMP NOT NULL,
                           total_value DECIMAL(12, 2),
                           status VARCHAR(50),
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY (customer_id) REFERENCES customers(customer_id))
            """)
