import os
import psycopg2

# Connect to Neon PostgreSQL
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    rating INTEGER,
    summary TEXT,
    image TEXT,
    about_author TEXT,
    book_summary TEXT,
    discussion TEXT
);
""")

conn.commit()
conn.close()

print("✅ PostgreSQL DB initialized successfully.")
