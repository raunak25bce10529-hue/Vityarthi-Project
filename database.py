import sqlite3

def get_connection():
    conn = sqlite3.connect("gpa_records.db")
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records(
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
