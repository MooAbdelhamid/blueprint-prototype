def create_tenant_databases_table(cursor):
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS tenants_databases(
                           database_id UUID PRIMARY KEY,
                           tenant_id UUID NOT NULL,
                           database_name VARCHAR(100),
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id));
                            """)
