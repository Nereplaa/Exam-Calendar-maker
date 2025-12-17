import sqlite3
import random

DB_PATH = 'database/sinav_programi.db'

# Günler ve saat dilimleri
DAYS = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']
TIME_SLOTS = [
    ('09:00', '10:30'),
    ('10:30', '12:00'),
    ('13:00', '14:30'),
    ('14:30', '16:00'),
    ('16:00', '17:30'),
]

def populate_schedules():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Tüm dersleri al
        cursor.execute("SELECT id, code, name FROM courses")
        courses = cursor.fetchall()
        
        print(f"Toplam {len(courses)} ders bulundu.")
        print("\nDers programları atanıyor...\n")
        
        for course_id, code, name in courses:
            # Rastgele gün ve saat seç
            day = random.choice(DAYS)
            start_time, end_time = random.choice(TIME_SLOTS)
            
            # Güncelle
            cursor.execute("""
                UPDATE courses 
                SET day_of_week = ?, class_start_time = ?, class_end_time = ?
                WHERE id = ?
            """, (day, start_time, end_time, course_id))
            
            print(f"  {code} - {name}: {day} {start_time}-{end_time}")
        
        conn.commit()
        print(f"\n✅ {len(courses)} ders için program atandı!")
        print("\nArtık bu saatlerde hocalar müsait olmayacak ve sınav atanamayacak.")
        
    except Exception as e:
        print(f"Hata: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    populate_schedules()
