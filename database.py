# database.py
import sqlite3

DB_NAME = "gpa_records.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    # Unified table name: records
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        name TEXT,
        course TEXT,
        credits TEXT,
        grades TEXT,
        gpa REAL
    )
    """)
    conn.commit()
    conn.close()
