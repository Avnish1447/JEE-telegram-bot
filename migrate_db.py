import sqlite3
from pathlib import Path

DB_FILE = Path("data/users.db")

def migrate_database():
    """Add student_class column to existing database if it doesn't exist."""
    
    if not DB_FILE.exists():
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check if student_class column exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if "student_class" not in columns:
        print("🔧 Adding student_class column to database...")
        cursor.execute("ALTER TABLE users ADD COLUMN student_class TEXT")
        conn.commit()
        print("✅ Migration complete! student_class column added.")
    else:
        print("✅ Database already has student_class column. No migration needed.")
    
    conn.close()

if __name__ == "__main__":
    migrate_database()
