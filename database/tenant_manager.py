"""
Construction
"""

import uuid

import psycopg2
from psycopg2 import sql

from database.config import DatabaseConfig


class TenantDatabaseManager:
    """
    Manages multiple databases
    """

    def __init__(self):
        """
        Initializes the manager
        """

        self.config = DatabaseConfig

        self._ensure_central_database()

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
            print(e)
            raise
        finally:
            cursor.close()
            conn.close()

    def _init_central_tables(self):
        """
        Create tables in central database
        """
        conn = self._get_central_connection()
        cursor = conn.cursor()

        try:
            # Table 1: tenants
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tenants(
                           tenant_id UUID PRIMARY KEY,
                           company_name VARCHAR(255) NOT NULL,
                           email VARCHAR(255) UNIQUE NOT NULL,
                           plan VARCHAR(255) DEFAULT 'free',
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                            """)
            # Table 2: tenants_databases
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tenants_databases(
                           database_id UUID PRIMARY KEY,
                           tenant_id UUID NOT NULL,
                           database_name VARCHAR(100),
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id));
                            """)
            # Table 3: users
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
        """
        conn_params = self.config.get_connection_string(self.config.CENTRAL_DB)
        return psycopg2.connect(**conn_params)

    def create_tenant(self, company_name, email):
        """
        Construction
        """
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
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

        # self._apply_customer_schema(database_name)

        print("Tenant created successfully!")

        return str(tenant_id)

    def _create_customer_database(self, database_name):
        """
        Construction
        """
        conn = self._get_central_connection()
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
