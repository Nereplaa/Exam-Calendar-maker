import sqlite3
import os

DB_PATH = 'database/sinav_programi.db'

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(courses)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'day_of_week' not in columns:
            print("Adding day_of_week column...")
            cursor.execute("ALTER TABLE courses ADD COLUMN day_of_week TEXT")
            
        if 'class_start_time' not in columns:
            print("Adding class_start_time column...")
            cursor.execute("ALTER TABLE courses ADD COLUMN class_start_time TEXT")
            
        if 'class_end_time' not in columns:
            print("Adding class_end_time column...")
            cursor.execute("ALTER TABLE courses ADD COLUMN class_end_time TEXT")
            
        conn.commit()
        print("Migration successful!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
