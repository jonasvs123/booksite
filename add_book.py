import sqlite3

book = ("The Pragmatic Programmer", "Andrew Hunt, David Thomas", 5, "A classic for software craftsmanship.")

conn = sqlite3.connect("books.db")
cur = conn.cursor()

cur.execute("INSERT INTO books (title, author, rating, summary) VALUES (?, ?, ?, ?)", book)

conn.commit()
conn.close()

print("✅ Book added!")
