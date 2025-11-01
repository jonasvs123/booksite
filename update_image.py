import sqlite3

conn = sqlite3.connect("books.db")
cur = conn.cursor()

# Change these values for each book you want to update
book_id = 5
image_filename = "A_Thousand_Splendid_Suns.png"

cur.execute("UPDATE books SET image = ? WHERE id = ?", (image_filename, book_id))

conn.commit()
conn.close()

print("✅ Updated book image!")
