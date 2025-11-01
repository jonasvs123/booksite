import sqlite3

conn = sqlite3.connect("books.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    rating INTEGER,
    summary TEXT
);
""")

conn.commit()
conn.close()

print("✅ Database created and table set up!")