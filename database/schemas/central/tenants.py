def create_tenants_table(cursor):
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS tenants(
                           tenant_id UUID PRIMARY KEY,
                           company_name VARCHAR(255) UNIQUE NOT NULL,
                           plan VARCHAR(255) DEFAULT 'free',
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                            """)
