"""
Construction
"""

import psycopg2
from config import DatabaseConfig
from psycopg2 import sql


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

        self._init_central_database()

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

    def _init_central_database(self):
        """
        Create tables in central database
        """
        conn = self._get_central_connection()
        cursor = conn.cursor()

        try:
            pass
        except Exception:
            pass
        finally:
            cursor.close()
            conn.close()

    def _get_central_connection(self):
        """
        Get a connection to the central database
        """
        conn_params = self.config.get_connection_string(self.config.CENTRAL_DB)
        return psycopg2.connect(**conn_params)
