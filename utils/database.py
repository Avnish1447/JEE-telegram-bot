import sqlite3
from pathlib import Path
from datetime import datetime

DB_FILE = Path("data/users.db")

# utils/database.py

def init_db():
    """Initialize the database (create tables if not exists)."""
    conn = get_connection()
    conn.close()


def get_connection():
    """Create/connect to SQLite DB and ensure table exists."""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            phone TEXT UNIQUE,
            selected_coaching TEXT,
            selected_batch TEXT,
            student_class TEXT,
            groups_join INTEGER DEFAULT 0,
            last_join_time TEXT,
            banned INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn


# --- User CRUD Operations ---

def get_user(telegram_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    # convert row to dict
    keys = ["telegram_id", "phone", "selected_coaching", "selected_batch", "student_class", "groups_join", "last_join_time", "banned"]
    return dict(zip(keys, row))


def get_user_by_phone(phone: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE phone = ?", (phone,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    keys = ["telegram_id", "phone", "selected_coaching", "selected_batch", "student_class", "groups_join", "last_join_time", "banned"]
    return dict(zip(keys, row))




def update_user(telegram_id: int, fields: dict):
    """
    Insert or update user.
    If user exists, updates specified fields.
    If user does not exist, creates new record with fields.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Check if user exists
    cur.execute("SELECT telegram_id FROM users WHERE telegram_id = ?", (telegram_id,))
    if not cur.fetchone():
        # Insert with all provided fields or defaults
        default_values = {
            "phone": None,
            "selected_coaching": None,
            "selected_batch": None,
            "student_class": None,
            "groups_join": 0,
            "last_join_time": None,
            "banned": 0
        }
        default_values.update(fields)
        cur.execute("""
            INSERT INTO users (telegram_id, phone, selected_coaching, selected_batch, student_class, groups_join, last_join_time, banned)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            telegram_id,
            default_values["phone"],
            default_values["selected_coaching"],
            default_values["selected_batch"],
            default_values["student_class"],
            default_values["groups_join"],
            default_values["last_join_time"],
            default_values["banned"]
        ))
    else:
        # Update only specified fields
        for key, value in fields.items():
            if key not in {"phone", "selected_coaching", "selected_batch", "student_class", "groups_join", "last_join_time", "banned"}:
                continue
            cur.execute(f"UPDATE users SET {key} = ? WHERE telegram_id = ?", (value, telegram_id))

    conn.commit()
    conn.close()




def record_join(telegram_id: int):
    """Increment user's groups_join and set last_join_time."""
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    cur.execute("""
        UPDATE users
        SET groups_join = COALESCE(groups_join, 0) + 1,
            last_join_time = ?
        WHERE telegram_id = ?
    """, (now, telegram_id))
    conn.commit()
    conn.close()

def increment_groups_join(telegram_id: int):
    """Increment groups_join by 1 and update last_join_time."""
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    # Use COALESCE to handle NULL values
    cur.execute(
        "UPDATE users SET groups_join = COALESCE(groups_join, 0) + 1, last_join_time = ? WHERE telegram_id = ?",
        (now, telegram_id)
    )
    conn.commit()
    conn.close()
