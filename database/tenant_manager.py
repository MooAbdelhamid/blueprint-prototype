"""
Construction

"""

import psycopg2
from config import DatabaseConfig

config = DatabaseConfig()

conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password=config.PASSWORD,
    port=5432,
)

cur = conn.cursor()
