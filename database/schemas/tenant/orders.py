def create_orders_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id UUID PRIMARY KEY,
            order_date TIMESTAMP NOT NULL,
            total_value DECIMAL(12, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
