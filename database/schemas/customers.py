def create_customers_table(cursor):
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id UUID PRIMARY KEY,
                    email VARCHAR(255),
                    name VARCHAR(255),
                    city VARCHAR(100),
                    state VARCHAR(100),
                    first_purchase_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            """)
