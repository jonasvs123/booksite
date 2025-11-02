from flask import Flask, render_template, abort, request, redirect, url_for, session
from datetime import datetime
import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    return psycopg2.connect(
        os.environ["DATABASE_URL"],
        cursor_factory=RealDictCursor
    )


app = Flask(__name__)
app.secret_key = "b702f2a1c64a21d1e4c2f3fdec16d29b"
app.jinja_env.globals['now'] = datetime.now
def login_required():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
def get_books():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books ORDER BY id DESC;")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_book(book_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE id=%s", (book_id,))
    book = cur.fetchone()
    conn.close()
    return book



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
    book = get_book(book_id)
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

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO books (title, author, rating, summary, image, about_author, book_summary, discussion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
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
    conn = get_db_connection()
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
            FROM books WHERE id=%s
        """, (book_id,))
        row = cur.fetchone()

        if row:
            cur.execute("""
                UPDATE books
                SET title = %s, author = %s, rating = %s, summary = %s, image = %s, about_author = %s, book_summary = %s, discussion = %s
                WHERE id = %s
            """, (title, author, rating, summary, image, about_author, book_summary, discussion, book_id))

        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    # GET request: load book and show form
    cur.execute("""
        SELECT * FROM books WHERE id=%s
    """, (book_id,))
    row = cur.fetchone()

    conn.close()

    if row is None:
        abort(404)

    book = row


    return render_template("edit_book.html", book=book)

@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=%s", (book_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)