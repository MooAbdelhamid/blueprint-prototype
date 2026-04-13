"""
Database Configuration
======================
This file stores connection settings for PostgreSQL server.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    """
    Configuration for PostgreSQL connection

    Attributes:
        HOST: Where PostgreSQL server is running
        PORT: PostgreSQL default port is 5432
        USER: Database username
        PASSWORD: Database password
        CENTRAL_DB: Name of the central database
    """

    HOST = os.getenv("DB_HOST", "localhost")
    PORT = int(os.getenv("DB_PORT", 5432))

    USER = os.getenv("DB_USER", "postgres")
    PASSWORD = os.getenv("DB_PASSWORD", "No")

    CENTRAL_DB = "blueprint_central"

    @classmethod
    def get_connection_string(cls, database=None):
        """
        Build a connection string for psycopg2

        Args:
            database(str): Which database to connect to

        Returns:
            dict: Connection parameters
        """

        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "user": cls.USER,
            "password": cls.PASSWORD,
            "database": database or "postgres",
        }
