from flask import Flask, render_template, abort, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "b702f2a1c64a21d1e4c2f3fdec16d29b"
app.jinja_env.globals['now'] = datetime.now
def login_required():
    if not session.get("logged_in"):
        return redirect(url_for("login"))


def get_books():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT id, title, author, rating, summary, image, about_author, book_summary, discussion FROM books")
    rows = cur.fetchall()
    conn.close()

    books = []
    for row in rows:
        books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "rating": row[3],
            "summary": row[4],
            "image": row[5],
            "about_author": row[6],
            "book_summary": row[7],
            "discussion": row[8],
        })

    return books


@app.route("/")
def index():
    books = get_books()
    return render_template("index.html", books=books)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "Jonas2901":
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return "Wrong password", 401

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))



@app.route("/book/<int:book_id>")
def book_page(book_id: int):
    book = next((b for b in get_books() if b["id"] == book_id), None)
    if not book:
        abort(404)
    return render_template("book.html", book=book)

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        summary = request.form["summary"]
        image = request.form.get("image")
        about_author = request.form.get("about_author")
        book_summary = request.form.get("book_summary")
        discussion = request.form.get("discussion")

        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO books (title, author, rating, summary, image, about_author, book_summary, discussion) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (title, author, rating, summary, image, about_author, book_summary, discussion)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add_book.html")

@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        summary = request.form["summary"]
        image = request.form.get("image")
        about_author = request.form.get("about_author")
        book_summary = request.form.get("book_summary")
        discussion = request.form.get("discussion")
        cur.execute("""
            SELECT id, title, author, rating, summary, image, about_author, book_summary, discussion
            FROM books WHERE id=?
        """, (book_id,))
        row = cur.fetchone()

        if row:
            cur.execute("""
                UPDATE books
                SET title = ?, author = ?, rating = ?, summary = ?, image = ?, about_author = ?, book_summary = ?, discussion = ?
                WHERE id = ?
            """, (title, author, rating, summary, image, about_author, book_summary, discussion, book_id))

        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    # GET request: load book and show form
    cur.execute("""
        SELECT id, title, author, rating, summary, image, about_author, book_summary, discussion
        FROM books WHERE id=?
    """, (book_id,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        abort(404)

    book = {
    "id": row[0],
    "title": row[1],
    "author": row[2],
    "rating": row[3],
    "summary": row[4],
    "image": row[5],
    "about_author": row[6],
    "book_summary": row[7],
    "discussion": row[8],
}

    return render_template("edit_book.html", book=book)

@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)