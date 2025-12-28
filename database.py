import os
import psycopg2
from const import CONST_DATABASE_URL

DATABASE_URL = CONST_DATABASE_URL

if DATABASE_URL is None:
    print("DATABASE_URL not set!")
    exit()

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("Connected to PostgreSQL database!")

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        date DATE,
        time TIME,
        status VARCHAR(50)
    )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully!")

except Exception as e:
    print("Error connecting to database:", e)
    exit()
print("Database ready!")
