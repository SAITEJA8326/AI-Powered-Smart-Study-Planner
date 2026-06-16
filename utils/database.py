import sqlite3
import pandas as pd

DB_PATH = "student.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS records (
        username TEXT,
        week INTEGER,
        algebra REAL, calculus REAL, trig REAL, sp REAL, coord REAL,
        mechanics REAL, optics REAL, thermo REAL, waves REAL, elec REAL,
        organic REAL, inorganic REAL, physical REAL
    )
    """)

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?,?)", (username, password))
        conn.commit()
        return True
    except:
        return False


def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None


def save_week(username, week, scores):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("DELETE FROM records WHERE username=? AND week=?", (username, week))

    c.execute("""
    INSERT INTO records VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, [username, week] + scores)

    conn.commit()
    conn.close()


def get_history(username):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(
        f"SELECT * FROM records WHERE username='{username}' ORDER BY week",
        conn
    )
    conn.close()
    return df