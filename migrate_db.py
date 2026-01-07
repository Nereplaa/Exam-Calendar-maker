import sqlite3
import os

DB_PATH = 'database/sinav_programi.db'

def migrate():
    """
    Veritabanı migrasyonlarını çalıştırır.
    Yeni sütunları kontrol edip yoksa ekler.
    """
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # ========================================
        # COURSES TABLOSU MİGRASYONLARI
        # ========================================
        cursor.execute("PRAGMA table_info(courses)")
        course_columns = [info[1] for info in cursor.fetchall()]
        
        if 'day_of_week' not in course_columns:
            print("Adding day_of_week column to courses...")
            cursor.execute("ALTER TABLE courses ADD COLUMN day_of_week TEXT")
            
        if 'class_start_time' not in course_columns:
            print("Adding class_start_time column to courses...")
            cursor.execute("ALTER TABLE courses ADD COLUMN class_start_time TEXT")
            
        if 'class_end_time' not in course_columns:
            print("Adding class_end_time column to courses...")
            cursor.execute("ALTER TABLE courses ADD COLUMN class_end_time TEXT")
        
        # Özel sınıf ataması için yeni sütun
        if 'special_classroom_id' not in course_columns:
            print("Adding special_classroom_id column to courses...")
            cursor.execute("ALTER TABLE courses ADD COLUMN special_classroom_id INTEGER REFERENCES classrooms(id)")
        
        # ========================================
        # CLASSROOMS TABLOSU MİGRASYONLARI
        # ========================================
        cursor.execute("PRAGMA table_info(classrooms)")
        classroom_columns = [info[1] for info in cursor.fetchall()]
        
        # Derslik tipi için yeni sütun
        if 'classroom_type' not in classroom_columns:
            print("Adding classroom_type column to classrooms...")
            cursor.execute("ALTER TABLE classrooms ADD COLUMN classroom_type TEXT DEFAULT 'Normal'")
            
            # Mevcut bilgisayarlı derslikleri Lab olarak işaretle
            cursor.execute("UPDATE classrooms SET classroom_type = 'Lab' WHERE has_computer = 1")
            
            # Amfi dersliklerini işaretle
            cursor.execute("UPDATE classrooms SET classroom_type = 'Amfi' WHERE name LIKE '%AMF%'")
            
            print("   -> Mevcut derslik tipleri güncellendi")
            
        conn.commit()
        print("[OK] Migration successful!")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
