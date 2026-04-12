# BluePrint

A multi-tenant SaaS platform built with database-per-tenant architecture for secure data isolation and scalability.

## Overview

BluePrint implements a robust multi-tenant system where each tenant receives an isolated database, ensuring complete data separation and independent scaling capabilities. The platform leverages FastAPI for high-performance API endpoints and PostgreSQL for reliable data persistence.

## Architecture

The system employs a **database-per-tenant** architecture pattern:

- **Central Database**: Manages tenant metadata, user authentication, and tenant-to-database mappings
- **Tenant Databases**: Isolated databases provisioned automatically for each tenant upon registration
- **Dynamic Provisioning**: New tenant databases are created on-demand with pre-configured schemas

### Key Components

```
blueprint-prototype/
├── backend/           # FastAPI REST API
├── database/          # Schema management and tenant provisioning
├── frontend/          # Streamlit interface
└── notebooks/         # Data analysis and exploration
```

## Features

### Current
- Multi-tenant registration with automatic database provisioning
- Isolated tenant data stores
- RESTful API endpoints
- Basic user management


## Technology Stack

**Backend**
- FastAPI - High-performance async web framework
- PostgreSQL - Primary data store
- psycopg2 - PostgreSQL adapter

**Frontend**
- Streamlit - Rapid UI development

**Analysis**
- Pandas - Data manipulation and analysis

## Database Schema

### Central Database
- `tenants` - Tenant organization records
- `tenant_databases` - Tenant-to-database mappings
- `users` - User authentication and authorization

### Tenant Databases
- `customers` - Customer records
- `products` - Product catalog
- `orders` - Order transactions

## Development Status

This project is under active development. Breaking changes may occur as the architecture evolves.

## Contributing

Contributions are welcome. Please open an issue first to discuss proposed changes.

## Contact

For questions or feedback, please open an issue on GitHub.