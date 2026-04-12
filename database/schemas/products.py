def create_products_table(cursor):
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id UUID PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    category VARCHAR(100),
                    price DECIMAL(10, 2),
                    sku VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
