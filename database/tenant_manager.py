"""
Construction
"""

import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="123Mm123", port=5432
)

cur = conn.cursor()
