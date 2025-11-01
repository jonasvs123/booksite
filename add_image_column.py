import sqlite3

conn = sqlite3.connect("books.db")
cur = conn.cursor()

cur.execute("ALTER TABLE books ADD COLUMN image TEXT;")

conn.commit()
conn.close()

print("✅ Added 'image' column to the books table")
