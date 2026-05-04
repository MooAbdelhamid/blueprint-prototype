# Database System Architecture

This sub system is a multi-tenant data ingestion and processing pipeline

Each tenant (customer/company):
- Has their own isolated PostgreSQL database
- Can connect to multiple data sources(CSV, Shopify)
- Data is Extracted -> Transformed -> loaded into their databases

---

## Core Components

### 1. Tenant Manager Layer

Manages the databases

Main Component:
- TenantDatabaseManager(Class)

Functions:
- Init
- Creating tenants
- Creating users
- Creating isolated databases per tenant
- Get tenant database connection
- Get tenant by email
- List all tenants

Databases:
- Central Database:
    - tenants
    - tenants_databases
    - users

- Tenant Database (per customer):
    - customers
    - products
    - orders

---

### 2. Data Ingestion Layer(Connectors)

Main Components:
- BaseConnector(BaseClass)
- CSVConnector

BaseConnector Functions:
- init
- authenticate
- test connection
- extract customers data
- extract orders data
- extract products data

Input:
- Data source

Output:
- Raw data in source format - List of Dict

### 3. Transformation Layer

Main Components:
- BaseTransformer(BaseClass)
- CustomerTransformer
- OrdersTransformer
- ProductsTransformer

BaseTransformer Functions:
- init
- Clean
- Map to database schema

Input:
- Raw data in source format - List of Dict

Output:
- Data ready to ingest
