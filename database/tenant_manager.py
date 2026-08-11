"""
Tenant Database Manager
=======================
The core of the multi-tenant system.
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

from database.config import DatabaseConfig
from database.schemas.tenant.orders import create_orders_table


class TenantDatabaseManager:
    """
    Manages multiple databases for multi-tenant software
    """

    def __init__(self):
        self.config = DatabaseConfig

        self._create_main_database()

        self._apply_main_schema()

        print("Main database initialized")

    def _get_central_connection(self):
        """
        Get a connection to the central database
        """
        conn_params = self.config.get_connection_string(self.config.CENTRAL_DB)
        return psycopg2.connect(**conn_params)

    def _create_main_database(self, database_name="blueprint-main"):

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

    def _apply_main_schema(self, database_name="blueprint-main"):
        """
        Apply the imported schema to tenant's database

        Args:
            database_name (str): Database to apply schema to
        """
        conn_params = self.config.get_connection_string(database_name)
        conn = psycopg2.connect(**conn_params)

        cursor = conn.cursor()

        try:
            # create_customers_table(cursor)

            # create_products_table(cursor)

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

    def insert_orders(self, database_name, orders):
        conn_params = self.config.get_connection_string(database_name)
        conn = psycopg2.connect(**conn_params)

        query = sql.SQL("""
        INSERT INTO {table}
        (order_id, order_date, total_value)
        VALUES %s
        """).format(table=sql.Identifier("orders"))

        with conn.cursor() as cur:
            execute_values(cur, query, orders)

        conn.commit()
