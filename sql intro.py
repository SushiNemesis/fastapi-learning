import sqlite3

conn = sqlite3.connect("store.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL
)
""")

conn.commit()
conn.close()
