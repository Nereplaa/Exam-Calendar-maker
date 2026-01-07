# ==============================================
# CSV VERİ İMPORT SCRİPTİ
# ==============================================
# Bu script, CSV dosyalarından verileri okuyup
# veritabanına aktarır. Mevcut fake verileri temizler.
# ==============================================

import csv
import os
import sqlite3
import re
from pathlib import Path

# Veritabanı yolu
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'sinav_programi.db')

# CSV dosyalarının bulunduğu klasör
CSV_DIR = os.path.join(os.path.dirname(__file__), 'asdasdasd', 'Yeni klasör')


def get_db_connection():
    """Veritabanı bağlantısı oluşturur."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_schema():
    """
    Veritabanı şemasını oluşturur.
    schema.sql dosyasını okuyup çalıştırır.
    """
    print("📋 Veritabanı şeması oluşturuluyor...")
    
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    
    if not os.path.exists(schema_path):
        print(f"   ✗ Schema dosyası bulunamadı: {schema_path}")
        return False
    
    conn = get_db_connection()
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    
    print("   ✓ Tüm tablolar oluşturuldu")
    print("✅ Veritabanı şeması hazır!\n")
    return True


def clean_database():
    """
    Mevcut veritabanındaki tüm verileri temizler.
    Tablolar korunur, sadece veriler silinir.
    """
    print("🗑️  Mevcut veriler temizleniyor...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Sırayla tabloları temizle (foreign key sırası önemli)
    tables = [
        'exam_schedule',      # Sınav programı
        'classroom_proximity', # Derslik yakınlık
        'student_courses',    # Öğrenci-ders ilişkisi
        'instructor_availability',  # Hoca müsaitlik
        'courses',            # Dersler
        'students',           # Öğrenciler
        'instructors',        # Hocalar
        'classrooms',         # Derslikler
        'departments',        # Bölümler
        'faculties',          # Fakülteler
    ]
    
    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"   ✓ {table} tablosu temizlendi")
        except Exception as e:
            pass  # Tablo yoksa sessizce geç
    
    # Auto-increment sıfırla
    try:
        cursor.execute("DELETE FROM sqlite_sequence")
    except:
        pass  # sqlite_sequence yoksa sessizce geç
    
    conn.commit()
    conn.close()
    print("✅ Tüm veriler temizlendi!\n")


def import_classrooms_and_proximity():
    """
    Derslik Yakınlık.csv dosyasından derslikleri ve yakınlık bilgisini import eder.
    """
    print("🏫 Derslikler ve yakınlık bilgisi import ediliyor...")
    
    csv_path = os.path.join(CSV_DIR, 'Derslik Yakınlık.csv')
    
    if not os.path.exists(csv_path):
        print(f"   ✗ Dosya bulunamadı: {csv_path}")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Derslik kapasiteleri (gerçekçi değerler: 20-50 arası)
    capacity_map = {
        'M101': 30, 'M201': 35, 'M301': 30,
        'S101': 40, 'S201': 35, 'S202': 35,
        'K001': 25, 'K002': 25,  # Bilgisayar labları daha küçük
        'D101': 25, 'D102': 25, 'D103': 25, 'D104': 25,
        'D201': 30, 'D202': 30,
        'D301': 35, 'D302': 35,
        'D401': 40, 'D402': 40, 'D403': 40,
        'E101': 20, 'E102': 20,
        'AMFİA': 50, 'AMFİB': 50,  # Amfiler en büyük, max 50
    }
    
    # Blok -> Bina eşlemesi (yakın bloklar aynı binada)
    block_building_map = {
        'M': 'Mühendislik Binası',      # M Blok - Mühendislik
        'S': 'Mühendislik Binası',      # S Blok - Mühendislik (M'ye yakın)
        'D': 'Ders Binaları',           # D Blok - Merkezi derslikler
        'E': 'Ders Binaları',           # E Blok - Ders binaları (D'ye yakın)
        'K': 'Bilgisayar Merkezi',      # K Blok - Lab'lar
        'A': 'Konferans Merkezi',       # A Blok - Amfiler
    }
    
    def get_building_for_block(block_code):
        """Blok koduna göre bina adı döndürür."""
        return block_building_map.get(block_code, 'Diğer Binalar')
    
    classrooms_added = set()
    proximity_data = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            block = row['BLOK'].strip()
            classroom_name = row['DERSLİK'].strip()
            nearby_str = row['YAKIN DERSLİK'].strip()
            
            # Ana dersliği ekle
            if classroom_name not in classrooms_added:
                capacity = capacity_map.get(classroom_name, 40)
                has_computer = 1 if classroom_name.startswith('K') else 0
                building = get_building_for_block(block)
                
                cursor.execute("""
                    INSERT INTO classrooms (name, building, block, capacity, has_computer, is_available)
                    VALUES (?, ?, ?, ?, ?, 1)
                """, (classroom_name, building, block, capacity, has_computer))
                
                classrooms_added.add(classroom_name)
            
            # Yakın derslikleri parse et ve ekle
            if nearby_str:
                nearby_list = [n.strip() for n in nearby_str.split(',')]
                for i, nearby_name in enumerate(nearby_list):
                    # Yakın dersliği de ekle (yoksa)
                    if nearby_name not in classrooms_added:
                        capacity = capacity_map.get(nearby_name, 40)
                        nearby_block = nearby_name[0] if nearby_name else ''
                        has_computer = 1 if nearby_name.startswith('K') else 0
                        building = get_building_for_block(nearby_block)
                        
                        cursor.execute("""
                            INSERT INTO classrooms (name, building, block, capacity, has_computer, is_available)
                            VALUES (?, ?, ?, ?, ?, 1)
                        """, (nearby_name, building, nearby_block, capacity, has_computer))
                        
                        classrooms_added.add(nearby_name)
                    
                    # Yakınlık ilişkisini kaydet
                    proximity_data.append((classroom_name, nearby_name, i + 1))
    
    conn.commit()
    
    # Şimdi yakınlık ilişkilerini ekle
    for classroom_name, nearby_name, priority in proximity_data:
        # ID'leri bul
        cursor.execute("SELECT id FROM classrooms WHERE name = ?", (classroom_name,))
        classroom_row = cursor.fetchone()
        
        cursor.execute("SELECT id FROM classrooms WHERE name = ?", (nearby_name,))
        nearby_row = cursor.fetchone()
        
        if classroom_row and nearby_row:
            cursor.execute("""
                INSERT INTO classroom_proximity (classroom_id, nearby_classroom_id, priority)
                VALUES (?, ?, ?)
            """, (classroom_row['id'], nearby_row['id'], priority))
    
    conn.commit()
    conn.close()
    
    print(f"   ✓ {len(classrooms_added)} derslik eklendi")
    print(f"   ✓ {len(proximity_data)} yakınlık ilişkisi eklendi")
    print("✅ Derslik verileri import edildi!\n")


def parse_csv_header(csv_path):
    """
    CSV dosyasının header'ından ders bilgilerini çıkarır.
    
    Döndürür:
        dict: {
            'faculty': 'MÜHENDİSLİK VE DOĞA BİLİMLERİ FAKÜLTESİ',
            'department': 'BİLGİSAYAR MÜHENDİSLİĞİ',
            'course_code': 'BLM111',
            'course_name': 'BİLGİSAYAR MÜHENDİSLİĞİNE GİRİŞ',
            'instructor': 'Dr. Öğr. Üyesi ELİF PINAR HACIBEYOĞLU'
        }
    """
    with open(csv_path, 'r', encoding='utf-8') as f:
        # İlk birkaç satırı oku
        lines = []
        for i, line in enumerate(f):
            if i < 10:
                lines.append(line)
    
    # Header bilgisi genelde 4-7. satırlar arasında
    header_text = '\n'.join(lines)
    
    result = {
        'faculty': None,
        'department': None,
        'course_code': None,
        'course_name': None,
        'instructor': None
    }
    
    # Fakülte ve bölüm (4. satır gibi)
    # Örnek: "MÜHENDİSLİK VE DOĞA BİLİMLERİ FAKÜLTESİ 1 BİLGİSAYAR MÜHENDİSLİĞİ"
    faculty_match = re.search(r'(.*?FAKÜLTESİ|.*?YÜKSEKOKULU)\s+\d?\s*(.*?)$', header_text, re.MULTILINE)
    if faculty_match:
        result['faculty'] = faculty_match.group(1).strip()
        result['department'] = faculty_match.group(2).strip()
    
    # Ders kodu ve adı (5. satır gibi)
    # Örnek: "BLM111 BİLGİSAYAR MÜHENDİSLİĞİNE GİRİŞ"
    course_match = re.search(r'([A-Z]{2,4}\d{3})\s+(.+?)$', header_text, re.MULTILINE)
    if course_match:
        result['course_code'] = course_match.group(1).strip()
        result['course_name'] = course_match.group(2).strip()
    
    # Hoca adı (6. satır gibi)
    # Örnek: "Dr. Öğr. Üyesi ELİF PINAR HACIBEYOĞLU" veya "Öğr.Gör. ORKUN KARABATAK"
    # Unvanlar: Prof., Doç., Dr., Öğr.Gör., Dr. Öğr. Üyesi
    instructor_match = re.search(
        r'((?:Prof\.|Doç\.|Dr\.|Öğr\.Gör\.|Öğr\.)\s*(?:Dr\.)?\s*(?:Öğr\.)?\s*(?:Gör\.)?\s*(?:Üyesi)?\s*[A-ZÇĞİÖŞÜa-zçğıöşü\s]+?)(?:\n|Sınıf)', 
        header_text
    )
    if instructor_match:
        result['instructor'] = instructor_match.group(1).strip()
    
    return result


def get_exam_duration(course_code):
    """
    Ders koduna göre sınav süresini belirler.
    
    Mantık:
    - MAT dersler (Matematik): 90 dk
    - LAB içeren dersler: 120 dk
    - SEC dersler (Seçmeli): 60 dk
    - Diğer mühendislik dersleri: 90 dk
    - Giriş dersleri (1xx): 60 dk
    """
    code = course_code.upper()
    
    # Ders numarasını çıkar
    num_match = re.search(r'\d+', code)
    course_num = int(num_match.group()) if num_match else 100
    
    # Matematik dersleri - 90 dk
    if code.startswith('MAT'):
        return 90
    
    # Seçmeli dersler - 60 dk
    if code.startswith('SEC'):
        return 60
    
    # Lab dersleri - 120 dk
    if 'LAB' in code:
        return 120
    
    # 1. sınıf giriş dersleri (1xx) - 60 dk
    if 100 <= course_num < 200:
        return 60
    
    # 2. sınıf dersleri (2xx) - 90 dk
    if 200 <= course_num < 300:
        return 90
    
    # 3-4. sınıf dersleri (3xx, 4xx) - 90 dk
    if 300 <= course_num < 500:
        return 90
    
    # Varsayılan
    return 60


def import_courses_and_students():
    """
    Tüm SınıfListesi CSV dosyalarından ders ve öğrenci bilgilerini import eder.
    """
    print("📚 Dersler ve öğrenciler import ediliyor...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fakülte ve bölüm cache'i
    faculty_cache = {}
    department_cache = {}
    instructor_cache = {}
    student_cache = {}
    
    # CSV dosyalarını bul
    csv_files = [f for f in os.listdir(CSV_DIR) if f.startswith('SınıfListesi') and f.endswith('.csv')]
    
    print(f"   📁 {len(csv_files)} ders dosyası bulundu")
    
    for csv_file in csv_files:
        csv_path = os.path.join(CSV_DIR, csv_file)
        
        # Header bilgilerini parse et
        info = parse_csv_header(csv_path)
        
        if not info['course_code']:
            print(f"   ⚠️  {csv_file} - ders kodu bulunamadı, atlanıyor")
            continue
        
        # Fakülte ekle/al
        faculty_name = info['faculty'] or 'Bilinmeyen Fakülte'
        if faculty_name not in faculty_cache:
            cursor.execute("SELECT id FROM faculties WHERE name = ?", (faculty_name,))
            row = cursor.fetchone()
            if row:
                faculty_cache[faculty_name] = row['id']
            else:
                faculty_code = ''.join([w[0] for w in faculty_name.split()[:3]])
                cursor.execute("""
                    INSERT INTO faculties (name, code) VALUES (?, ?)
                """, (faculty_name, faculty_code))
                faculty_cache[faculty_name] = cursor.lastrowid
        
        faculty_id = faculty_cache[faculty_name]
        
        # Bölüm ekle/al
        dept_name = info['department'] or 'Bilinmeyen Bölüm'
        dept_key = f"{faculty_id}_{dept_name}"
        if dept_key not in department_cache:
            cursor.execute("SELECT id FROM departments WHERE name = ? AND faculty_id = ?", (dept_name, faculty_id))
            row = cursor.fetchone()
            if row:
                department_cache[dept_key] = row['id']
            else:
                dept_code = ''.join([w[0] for w in dept_name.split()[:2]])
                cursor.execute("""
                    INSERT INTO departments (name, code, faculty_id) VALUES (?, ?, ?)
                """, (dept_name, dept_code, faculty_id))
                department_cache[dept_key] = cursor.lastrowid
        
        department_id = department_cache[dept_key]
        
        # Hoca ekle/al
        instructor_name = info['instructor'] or 'Bilinmeyen Hoca'
        if instructor_name not in instructor_cache:
            cursor.execute("SELECT id FROM instructors WHERE name = ?", (instructor_name,))
            row = cursor.fetchone()
            if row:
                instructor_cache[instructor_name] = row['id']
            else:
                # Hoca unvanını ayır
                title_match = re.match(r'^((?:Prof\.|Doç\.|Dr\.|Öğr\.)[^A-Z]*)', instructor_name)
                title = title_match.group(1).strip() if title_match else ''
                
                cursor.execute("""
                    INSERT INTO instructors (name, title, department_id) VALUES (?, ?, ?)
                """, (instructor_name, title, department_id))
                instructor_cache[instructor_name] = cursor.lastrowid
        
        instructor_id = instructor_cache[instructor_name]
        
        # Öğrencileri oku ve say
        student_count = 0
        students_in_course = []
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            # Header satırlarını atla (ilk 11 satır genelde header)
            in_data = False
            
            for row in reader:
                # Veri satırlarını bul
                if len(row) >= 6 and row[4] and re.match(r'^\d{9}$', str(row[4]).strip()):
                    student_no = row[4].strip()
                    student_name = row[5].strip() if len(row) > 5 else ''
                    student_dept = row[1].strip() if len(row) > 1 else dept_name
                    
                    if student_no and student_name:
                        student_count += 1
                        students_in_course.append((student_no, student_name, student_dept))
        
        # Sınav süresini belirle
        exam_duration = get_exam_duration(info['course_code'])
        
        # Dersi ekle
        cursor.execute("""
            INSERT INTO courses (code, name, department_id, instructor_id, student_count, exam_duration, exam_type, has_exam)
            VALUES (?, ?, ?, ?, ?, ?, 'Yazılı', 1)
        """, (info['course_code'], info['course_name'], department_id, instructor_id, student_count, exam_duration))
        
        course_id = cursor.lastrowid
        
        # Öğrencileri ekle ve ilişkilendir
        for student_no, student_name, student_dept in students_in_course:
            # Öğrenci daha önce eklendiyse sadece ID'sini al
            if student_no not in student_cache:
                cursor.execute("SELECT id FROM students WHERE student_no = ?", (student_no,))
                row = cursor.fetchone()
                if row:
                    student_cache[student_no] = row['id']
                else:
                    cursor.execute("""
                        INSERT INTO students (student_no, name, department_id, grade)
                        VALUES (?, ?, ?, 1)
                    """, (student_no, student_name, department_id))
                    student_cache[student_no] = cursor.lastrowid
            
            student_id = student_cache[student_no]
            
            # Öğrenci-ders ilişkisini ekle
            cursor.execute("""
                INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)
            """, (student_id, course_id))
        
        print(f"   ✓ {info['course_code']}: {student_count} öğrenci, {exam_duration} dk sınav")
    
    conn.commit()
    conn.close()
    
    print(f"✅ {len(csv_files)} ders ve öğrenci verileri import edildi!\n")


def add_instructor_availability():
    """
    Hocaların müsaitliğini gerçekçi şekilde ayarlar.
    
    Mantık:
    1. Her derse rastgele ama gerçekçi bir gün/saat ata
    2. Hoca hangi gün dersi varsa o gün okula geliyor
    3. Okula geldiği günlerde tüm gün müsait (09:00-18:00)
    4. Dersi olmayan günlerde okula gelmiyor = müsait değil
    """
    print("📅 Ders programı ve hoca müsaitlikleri ayarlanıyor...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Ders günleri ve saatleri
    days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']
    time_slots = [
        ('09:00', '10:30'),  # 1. ders
        ('10:45', '12:15'),  # 2. ders
        ('13:00', '14:30'),  # 3. ders
        ('14:45', '16:15'),  # 4. ders
        ('16:30', '18:00'),  # 5. ders
    ]
    
    # Tüm dersleri al
    cursor.execute("SELECT id, code, instructor_id FROM courses")
    courses = cursor.fetchall()
    
    # Her hoca için hangi günler okula geliyor
    instructor_days = {}
    
    import random
    random.seed(42)  # Tutarlı sonuçlar için
    
    # Her derse gün ve saat ata
    for i, course in enumerate(courses):
        course_id = course['id']
        instructor_id = course['instructor_id']
        
        # Her derse 1-2 gün ata (haftada 2-4 saat ders)
        num_days = random.choice([1, 2])
        course_days = random.sample(days, num_days)
        
        for day in course_days:
            # O güne rastgele bir saat ata
            start_time, end_time = random.choice(time_slots)
            
            # Dersi güncelle (ilk gün bilgisi)
            cursor.execute("""
                UPDATE courses SET day_of_week = ?, class_start_time = ?, class_end_time = ?
                WHERE id = ?
            """, (day, start_time, end_time, course_id))
            
            # Hoca o gün okula geliyor
            if instructor_id not in instructor_days:
                instructor_days[instructor_id] = set()
            instructor_days[instructor_id].add(day)
    
    conn.commit()
    print(f"   ✓ {len(courses)} derse gün ve saat atandı")
    
    # Hoca müsaitliklerini ayarla - sadece okula geldiği günler
    for instructor_id, school_days in instructor_days.items():
        for day in school_days:
            # O gün tüm gün müsait (09:00-18:00)
            cursor.execute("""
                INSERT INTO instructor_availability (instructor_id, day_of_week, start_time, end_time, is_available)
                VALUES (?, ?, '09:00', '18:00', 1)
            """, (instructor_id, day))
    
    conn.commit()
    conn.close()
    
    # Özet
    total_availability = sum(len(days) for days in instructor_days.values())
    print(f"   ✓ {len(instructor_days)} hoca için toplam {total_availability} gün müsaitlik eklendi")
    
    # Detaylı döküm
    cursor = get_db_connection().cursor()
    cursor.execute("SELECT id, name FROM instructors")
    for instructor in cursor.fetchall():
        school_days = instructor_days.get(instructor['id'], set())
        if school_days:
            days_str = ', '.join(sorted(school_days, key=lambda x: days.index(x)))
            print(f"      - {instructor['name']}: {days_str}")
        else:
            print(f"      - {instructor['name']}: (ders yok)")
    
    print("✅ Ders programı ve müsaitlikler ayarlandı!\n")


def print_summary():
    """Import sonrası özet bilgi yazdırır."""
    print("\n" + "="*50)
    print("📊 IMPORT ÖZETİ")
    print("="*50)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    tables = [
        ('Fakülteler', 'faculties'),
        ('Bölümler', 'departments'),
        ('Hocalar', 'instructors'),
        ('Derslikler', 'classrooms'),
        ('Derslik Yakınlıkları', 'classroom_proximity'),
        ('Dersler', 'courses'),
        ('Öğrenciler', 'students'),
        ('Öğrenci-Ders İlişkileri', 'student_courses'),
    ]
    
    for name, table in tables:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        count = cursor.fetchone()['count']
        print(f"   {name}: {count}")
    
    # En kalabalık dersler
    print("\n📚 En Kalabalık 5 Ders:")
    cursor.execute("""
        SELECT c.code, c.name, c.student_count, c.exam_duration
        FROM courses c
        ORDER BY c.student_count DESC
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"   {row['code']}: {row['student_count']} öğrenci ({row['exam_duration']} dk)")
    
    conn.close()
    print("="*50 + "\n")


def main():
    """Ana fonksiyon - tüm import işlemlerini sırayla çalıştırır."""
    print("\n" + "="*50)
    print("🚀 CSV VERİ İMPORT İŞLEMİ BAŞLIYOR")
    print("="*50 + "\n")
    
    # 0. Önce şemayı oluştur (tablolar yoksa)
    create_schema()
    
    # 1. Mevcut verileri temizle
    clean_database()
    
    # 2. Derslikleri ve yakınlık bilgisini import et
    import_classrooms_and_proximity()
    
    # 3. Dersleri ve öğrencileri import et
    import_courses_and_students()
    
    # 4. Hoca müsaitlik bilgilerini ekle
    add_instructor_availability()
    
    # 5. Özet bilgi
    print_summary()
    
    print("✅ TÜM VERİLER BAŞARIYLA İMPORT EDİLDİ!")


if __name__ == '__main__':
    main()
