import sqlite3

conn = sqlite3.connect("books.db")
cur = conn.cursor()
cur.execute("SELECT id, title, image FROM books")
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
