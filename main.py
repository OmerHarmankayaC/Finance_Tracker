import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                type  TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL)""")
        
        conn.commit()

    except sqlite3.Error as e:
        print("Database error detected: ", e)

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")