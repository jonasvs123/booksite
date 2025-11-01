import sqlite3

conn = sqlite3.connect("books.db")
cur = conn.cursor()

cur.execute("ALTER TABLE books ADD COLUMN about_author TEXT;")
cur.execute("ALTER TABLE books ADD COLUMN book_summary TEXT;")
cur.execute("ALTER TABLE books ADD COLUMN discussion TEXT;")

conn.commit()
conn.close()

print("✅ Added new text fields: about_author, book_summary, discussion")
