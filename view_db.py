import sqlite3
from pathlib import Path

DB_FILE = Path("data/users.db")

def view_database():
    """Display all users in the database in a readable format."""
    
    if not DB_FILE.exists():
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    if not rows:
        print("📭 Database is empty - no users registered yet.")
        conn.close()
        return
    
    print(f"\n{'='*100}")
    print(f"📊 USERS DATABASE - Total Users: {len(rows)}")
    print(f"{'='*100}\n")
    
    for row in rows:
        telegram_id, phone, coaching, batch, student_class, groups_join, last_join_time, banned = row
        
        print(f"👤 User ID: {telegram_id}")
        print(f"   📱 Phone: {phone or 'Not set'}")
        print(f"   🎓 Coaching: {coaching or 'Not selected'}")
        print(f"   🎒 Class: {student_class or 'Not selected'}")
        print(f"   📚 Batch: {batch or 'Not selected'}")
        print(f"   🔢 Groups Joined: {groups_join}")
        print(f"   ⏰ Last Join: {last_join_time or 'Never'}")
        print(f"   🚫 Banned: {'Yes' if banned else 'No'}")
        print(f"   {'-'*80}")

    
    conn.close()
    print(f"\n{'='*100}\n")

if __name__ == "__main__":
    view_database()
