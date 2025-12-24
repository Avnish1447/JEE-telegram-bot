"""
Database migration script to add created_at column
Run this once to add timestamp tracking to existing database
"""

import sqlite3
from pathlib import Path
from datetime import datetime

DB_FILE = Path("data/users.db")


def migrate_add_created_at():
    """Add created_at column to users table for existing database."""
    
    if not DB_FILE.exists():
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check if created_at column already exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if "created_at" in columns:
        print("✅ created_at column already exists. No migration needed.")
        conn.close()
        return
    
    print("🔧 Adding created_at column to users table...")
    
    # Add the column without DEFAULT (SQLite limitation with ALTER TABLE)
    cursor.execute("ALTER TABLE users ADD COLUMN created_at TEXT")
    
    # Set created_at to current time for all existing users
    now = datetime.utcnow().isoformat()
    cursor.execute("UPDATE users SET created_at = ?", (now,))
    
    conn.commit()
    conn.close()
    
    print("✅ Migration complete! created_at column added.")
    print(f"   Existing users have been timestamped with: {now}")


if __name__ == "__main__":
    migrate_add_created_at()
