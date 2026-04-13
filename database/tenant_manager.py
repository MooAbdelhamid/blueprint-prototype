"""
Tenant Database Manager
=======================
The core of the multi-tenant system.

It handles:
1. Creating the central database if not existing
2. Registering new tenants
3. Creating a seperate database for each customer
4. Connecting to the right database for each cutomer

Key Definitions:
- Tenant = A user who uses the software
- Central Database = Main database that tracks all tenants
- Tenant Database = Separate database for each user's data
"""

import uuid

import psycopg2
from psycopg2 import sql

from database.config import DatabaseConfig
from database.schemas.customers import create_customers_table
from database.schemas.orders import create_orders_table
from database.schemas.products import create_products_table
from database.schemas.tenants import create_tenants_table
from database.schemas.tenants_databases import create_tenants_databases_table
from database.schemas.users import create_users_table


class TenantDatabaseManager:
    """
    Manages multiple databases for multi-tenant software

    Tasks:
    - Keeps track of all tenants
    - Creates tenants databases
    - Gets connection for the right database
    """

    def __init__(self):
        """
        Initializes the manager

        Steps:
        1. Connects to postgreSQL server
        2. Creates central database if doesn't exist
        3. setup central database tables from imported schemas
        """

        self.config = DatabaseConfig

        # Make sure central database exists
        self._ensure_central_database()

        # Create tables in central database if doesn't exist
        self._init_central_tables()

        print("Tenant database initialized")

    def _ensure_central_database(self):
        """
        Create the central database if it doesnt exist

        Steps:
        1. Connect to database
        2. Check if exists
        3. Create if missing
        """
        # Connect to server
        conn_params = self.config.get_connection_string("postgres")
        conn = psycopg2.connect(**conn_params)

        # Autocommit allow database creation
        conn.autocommit = True

        cursor = conn.cursor()

        try:
            # Check if database exists
            cursor.execute(
                """
                SELECT 1 FROM pg_database
                WHERE datname = %s
                """,
                (self.config.CENTRAL_DB,),
            )

            exists = cursor.fetchone()

            if not exists:
                # Create the central database
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(self.config.CENTRAL_DB)
                    )
                )

                print("Created central database")
            else:
                print("Central database exists")

        except Exception as e:
            print(f"Error ensuring central database: {e}")
            raise
        finally:
            cursor.close()
            conn.close()

    def _init_central_tables(self):
        """
        Create tables in central database

        Steps:
        1. Create tenants, tenants_databases, users tables

        Tables:
        1. tenants
        2. tenants_databases
        3. users
        """
        conn = self._get_central_connection()
        cursor = conn.cursor()

        try:
            # Table 1: tenants
            create_tenants_table(cursor)

            # Table 2: tenants_databases
            create_tenants_databases_table(cursor)

            # Table 3: users
            create_users_table(cursor)

            conn.commit()
            print("Central database tables created!")
        except Exception as e:
            conn.rollback()
            print(f"Error creating central tables: {e}")
            raise
        finally:
            cursor.close()
            conn.close()

    def _get_central_connection(self):
        """
        Get a connection to the central database

        Returns:
            psycopg2.connection: Database connection object
        """
        conn_params = self.config.get_connection_string(self.config.CENTRAL_DB)
        return psycopg2.connect(**conn_params)

    def create_tenant(self, company_name, email):
        """
        Add a new tenant and create their database

        Args:
            company_name (str): Company name
            email (str): Company email

        Returns:
            str: tenant_id (UUID)

        Steps:
        1. Generate unique tenant_id, user_id and database_id
        2. Create database name
        3. Save tenant info to central database
        4. Create postgreSQL database
        5. Apply schema to database
        """
        tenant_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        database_id = str(uuid.uuid4())
        database_name = f"customer_{company_name}"

        print(f"Creating customer {company_name} database")

        conn = self._get_central_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO tenants (tenant_id, company_name, email)
                VALUES (%s, %s, %s)
            """,
                (tenant_id, company_name, email),
            )

            cursor.execute(
                """
                INSERT INTO tenants_databases (database_id, tenant_id, database_name)
                VALUES (%s, %s, %s)
            """,
                (database_id, tenant_id, database_name),
            )

            cursor.execute(
                """
                INSERT INTO users (user_id, tenant_id, email, password_hash, role)
                VALUES (%s, %s, %s, %s, %s)
            """,
                (user_id, tenant_id, email, "password", "Admin"),
            )

            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            raise Exception(f"Tenant with email {email} exists")
        finally:
            cursor.close()
            conn.close()

        self._create_customer_database(database_name)

        self._apply_customer_schema(database_name)

        print("Tenant created successfully!")

        return str(tenant_id)

    def _create_customer_database(self, database_name):
        """
        Create a new database for the tenant

        Args:
            database_name (str): Name of the database to create

        Steps:
        1. Get connection
        2. Create tenant database
        """
        conn_params = self.config.get_connection_string("postgres")
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True

        cursor = conn.cursor()

        try:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name))
            )
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database {database_name} already exists")
        except Exception as e:
            print(f"Error creating database: {e}")
            raise
        finally:
            cursor.close()
            conn.close()

    def _apply_customer_schema(self, database_name):
        """
        Apply the imported schema to tenant's database

        Args:
            database_name (str): Database to apply schema to

        Steps:
        1. Get connection
        2. Apply schema

        Tables:
        1. cutomers
        2. products
        3. orders
        """
        conn_params = self.config.get_connection_string(database_name)
        conn = psycopg2.connect(**conn_params)

        cursor = conn.cursor()

        try:
            create_customers_table(cursor)

            create_products_table(cursor)

            create_orders_table(cursor)

            conn.commit()
            print(f"Applied schema to {database_name}")

        except Exception as e:
            conn.rollback()
            print(f"Error applying schema: {e}")
            raise
        finally:
            cursor.close()
            conn.close()

    def get_tenant_connection(self, tenant_id):
        """
        Get a database connection for a specific tenant

        Args:
            tenant_id (str): UUID of the tenant

        Returns:
            psycopg2.connection: Connection to tenant's database
        """

        conn = self._get_central_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT database_name FROM tenants_databases WHERE tenant_id = %s
                """,
                (tenant_id,),
            )
            result = cursor.fetchone()

            if not result:
                raise Exception(f"Tenant {tenant_id} not found")

            database_name = result[0]
        finally:
            cursor.close()
            conn.close()

        conn_params = self.config.get_connection_string(database_name)
        return psycopg2.connect(**conn_params)

    def get_tenant_by_email(self, email):
        """
        Look up tenant by their email

        Args:
            email (str): Tenant's email address
        Returns:
            tuple: (tenant_id, company_name) or None
        """

        conn = self._get_central_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT tenant_id, company_name FROM tenants WHERE email = %s
                """,
                (email,),
            )

            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def list_all_tenants(self):
        """
        Get list of all tenants (for admin dashboard)

        Returns:
            list: List of tuples (tenant_id, company_name, email, plan, db_name)
        """
        conn = self._get_central_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT 
                    t.tenant_id,
                    t.company_name,
                    t.email,
                    t.plan,
                    td.database_name
                FROM tenants t
                JOIN tenant_databases td ON t.tenant_id = td.tenant_id
                ORDER BY t.created_at DESC
            """)

            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
