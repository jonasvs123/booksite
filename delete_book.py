import sqlite3

def show_books():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT id, title, author FROM books")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("📚 No books found.")
        return []

    print("\n📚 Current books:")
    for row in rows:
        print(f"{row[0]} — {row[1]} by {row[2]}")
    return rows

def delete_book(book_id):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    print(f"✅ Book with ID {book_id} deleted.")

# Run script
books = show_books()
if not books:
    exit()

try:
    book_id = int(input("\nEnter the ID of the book you want to delete: "))
    delete_book(book_id)
except ValueError:
    print("❌ Invalid ID. Please enter a number.")
