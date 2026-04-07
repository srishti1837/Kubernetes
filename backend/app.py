from flask import Flask
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "students.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rollno TEXT NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM student")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute(
            "INSERT INTO student (name, rollno) VALUES (?, ?)",
            ("Srishti Gupta", "13501032024")
        )

    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "Backend Running Successfully"

@app.route('/db')
def db_check():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name, rollno FROM student LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            return f"Database Connected Successfully | Name: {row[0]} | Roll No: {row[1]}"
        else:
            return "Database Connected but no data found"
    except Exception as e:
        return f"Database Connection Failed: {str(e)}"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)