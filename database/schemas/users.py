def create_users_table(cursor):
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                           user_id UUID PRIMARY KEY,
                           tenant_id UUID NOT NULL,
                           email VARCHAR(255),
                           password_hash VARCHAR(255) NOT NULL,
                           role VARCHAR(50) DEFAULT 'user',
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id));
                            """)
