"""
Construction
"""

import psycopg2
from config import DatabaseConfig
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


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

        # self._init_central_database()

        print("Tenant database initialized")

    def _ensure_central_database(self):
        """
        Create the central database if it doesnt exist
        """
        conn_params = self.config.get_connection_string("postgres")
        conn = psycopg2.connect(**conn_params)

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()

        try:
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
