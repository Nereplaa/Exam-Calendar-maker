# ==============================================
# SINAV PLANLAMA ALGORİTMASI (Geliştirilmiş)
# ==============================================
# Bu dosya sınavları otomatik olarak planlar.
# Geliştirilmiş Greedy (açgözlü) algoritma kullanılır.
# 
# Algoritma mantığı:
# 1. Dersleri öğrenci sayısına göre sırala (büyükten küçüğe)
# 2. Aynı bölüm sınavları aynı güne ardışık gelmesin
# 3. Sınavları günlere eşit dağıt
# 4. Büyük sınavlar için birden fazla derslik kullan
# 5. Kısıtlamaları kontrol et:
#    - Derslik müsait mi?
#    - Hoca müsait mi? (sadece müsait saatlerde)
#    - Kapasite yeterli mi? (veya derslik birleştir)
#    - Öğrenci çakışması var mı?
# 6. Uygunsa yerleştir, değilse sonraki slotu dene
# ==============================================

from app.database import execute_query
from app.models.exam import create_exam, delete_all_exams, check_classroom_conflict, check_instructor_conflict
from app.models.classroom import get_available_classrooms, get_computer_classrooms
from app.models.course import get_courses_with_exam
from app.models.availability import check_instructor_available


# Her gün için hangi bölümün sınavları yapıldığını takip et
daily_department_exams = {}


def generate_exam_schedule(start_date, end_date):
    """
    Sınav programı oluşturur.
    
    Parametreler:
        start_date: Sınav dönemi başlangıç tarihi (YYYY-MM-DD)
        end_date: Sınav dönemi bitiş tarihi (YYYY-MM-DD)
    
    Döndürür:
        result: Sonuç bilgisi (başarılı sayısı, başarısız listesi)
    """
    global daily_department_exams
    daily_department_exams = {}
    
    # Önce mevcut planı temizle
    delete_all_exams()
    
    # Sınavı olan dersleri al (öğrenci sayısına göre sıralı)
    courses = get_courses_with_exam()
    
    # Dersleri bölüme göre grupla ve karıştır
    # Aynı bölüm sınavlarının ardışık gelmemesi için
    courses = shuffle_by_department(courses)
    
    # Uygun derslikleri al
    classrooms = get_available_classrooms()
    
    # Bilgisayarlı derslikleri ayrı al
    computer_classrooms = get_computer_classrooms()
    
    # Sınav günlerini oluştur
    exam_days = generate_exam_days(start_date, end_date)
    
    # Sınav saatlerini tanımla
    time_slots = generate_time_slots()
    
    # Sonuçları takip et
    placed_count = 0
    failed_courses = []
    
    # Her ders için planlama yap
    for course in courses:
        # Bu dersi yerleştir
        success = place_course_exam(course, classrooms, computer_classrooms, 
                                    exam_days, time_slots)
        
        if success:
            placed_count = placed_count + 1
        else:
            # Yerleştirilemedi
            failed_courses.append(course)
    
    # Sonuç döndür
    result = {
        'total_courses': len(courses),
        'placed_count': placed_count,
        'failed_count': len(failed_courses),
        'failed_courses': failed_courses
    }
    
    return result


def shuffle_by_department(courses):
    """
    Dersleri bölümlere göre karıştırır.
    Aynı bölüm sınavları ardışık gelmesin.
    
    Round-robin yöntemi kullanır:
    Bölüm1-Ders1, Bölüm2-Ders1, Bölüm3-Ders1, Bölüm1-Ders2, ...
    """
    # Bölümlere göre grupla
    dept_courses = {}
    for course in courses:
        dept_id = course['department_id']
        if dept_id not in dept_courses:
            dept_courses[dept_id] = []
        dept_courses[dept_id].append(course)
    
    # Round-robin şeklinde birleştir
    shuffled = []
    max_len = max(len(courses) for courses in dept_courses.values()) if dept_courses else 0
    
    for i in range(max_len):
        for dept_id in dept_courses:
            if i < len(dept_courses[dept_id]):
                shuffled.append(dept_courses[dept_id][i])
    
    return shuffled


def generate_exam_days(start_date, end_date):
    """
    Sınav günlerini oluşturur.
    Hafta sonlarını atlar.
    
    Parametreler:
        start_date: Başlangıç tarihi (YYYY-MM-DD)
        end_date: Bitiş tarihi (YYYY-MM-DD)
    
    Döndürür:
        days: Gün listesi [(tarih, gün_adı), ...]
    """
    from datetime import datetime, timedelta
    
    # Gün isimleri
    day_names = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
    
    # Tarihleri parse et
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    days = []
    current = start
    
    # Her gün için
    while current <= end:
        # Haftanın günü (0=Pazartesi, 6=Pazar)
        weekday = current.weekday()
        
        # Hafta sonu değilse ekle (Cumartesi=5, Pazar=6)
        if weekday < 5:
            date_str = current.strftime('%Y-%m-%d')
            day_name = day_names[weekday]
            days.append((date_str, day_name))
        
        # Sonraki güne geç
        current = current + timedelta(days=1)
    
    return days


def generate_time_slots():
    """
    Sınav saat dilimlerini oluşturur.
    
    Döndürür:
        slots: Saat dilimleri listesi [(başlangıç, bitiş), ...]
    """
    # Sabit sınav saatleri - daha fazla slot
    slots = [
        ('09:00', '11:00'),
        ('11:00', '13:00'),
        ('14:00', '16:00'),
        ('16:00', '18:00')
    ]
    
    return slots


def calculate_end_time(start_time, duration_minutes):
    """
    Başlangıç saatine göre bitiş saatini hesaplar.
    """
    from datetime import datetime, timedelta
    
    start = datetime.strptime(start_time, '%H:%M')
    end = start + timedelta(minutes=duration_minutes)
    end_time = end.strftime('%H:%M')
    
    return end_time


def check_student_conflict(course_id, exam_date, start_time, end_time):
    """
    Öğrenci çakışması olup olmadığını kontrol eder.
    """
    query = """
        SELECT COUNT(*) as count
        FROM student_courses sc1
        INNER JOIN student_courses sc2 ON sc1.student_id = sc2.student_id
        INNER JOIN exam_schedule e ON sc2.course_id = e.course_id
        WHERE sc1.course_id = ?
          AND sc2.course_id != ?
          AND e.exam_date = ?
          AND (
              (e.start_time <= ? AND e.end_time > ?)
              OR (e.start_time < ? AND e.end_time >= ?)
              OR (e.start_time >= ? AND e.end_time <= ?)
          )
    """
    
    params = (course_id, course_id, exam_date,
              start_time, start_time,
              end_time, end_time,
              start_time, end_time)
    
    results = execute_query(query, params)
    
    if results[0]['count'] > 0:
        return True
    
    return False


def check_department_consecutive(department_id, exam_date, start_time):
    """
    Aynı bölümün sınavının aynı gün ardışık olup olmadığını kontrol eder.
    En az 2 saat ara olmalı.
    """
    global daily_department_exams
    
    key = f"{exam_date}_{department_id}"
    
    if key not in daily_department_exams:
        return False  # Bu gün bu bölümün sınavı yok, OK
    
    # Bu gündeki son sınav saatini kontrol et
    last_end_time = daily_department_exams[key]
    
    # En az 2 saat ara olmalı
    from datetime import datetime, timedelta
    
    last_end = datetime.strptime(last_end_time, '%H:%M')
    current_start = datetime.strptime(start_time, '%H:%M')
    
    diff = (current_start - last_end).total_seconds() / 3600  # Saat farkı
    
    if diff < 2:
        return True  # Çok yakın, çakışma
    
    return False


def update_department_schedule(department_id, exam_date, end_time):
    """
    Bölümün günlük sınav programını günceller.
    """
    global daily_department_exams
    
    key = f"{exam_date}_{department_id}"
    
    # Son bitiş saatini güncelle
    if key not in daily_department_exams or end_time > daily_department_exams[key]:
        daily_department_exams[key] = end_time


def get_day_exam_count(exam_date):
    """
    Belirli bir günde kaç sınav planlandığını döndürür.
    """
    query = "SELECT COUNT(*) as count FROM exam_schedule WHERE exam_date = ?"
    results = execute_query(query, (exam_date,))
    return results[0]['count']


def find_available_classrooms(classrooms, exam_date, start_time, end_time, needed_capacity):
    """
    Belirtilen kapasiteyi karşılayan müsait derslik(ler)i bulur.
    Gerekirse birden fazla derslik birleştirir.
    
    Döndürür:
        rooms: Uygun derslik listesi veya None
    """
    available = []
    total_capacity = 0
    
    # Önce tek bir uygun derslik ara
    for room in classrooms:
        room_busy = check_classroom_conflict(room['id'], exam_date, start_time, end_time)
        if not room_busy:
            if room['capacity'] >= needed_capacity:
                return [room]  # Tek derslik yeterli
            available.append(room)
            total_capacity += room['capacity']
    
    # Tek derslik bulunamadı, birden fazla derslik birleştir
    if total_capacity >= needed_capacity:
        # Kapasiteye göre sırala (büyükten küçüğe)
        available.sort(key=lambda x: x['capacity'], reverse=True)
        
        selected = []
        current_capacity = 0
        
        for room in available:
            selected.append(room)
            current_capacity += room['capacity']
            
            if current_capacity >= needed_capacity:
                return selected
    
    return None


def check_supervisor_conflict(instructor_id, exam_date, start_time, end_time):
    """
    Gözetmenin (supervisor) başka bir sınavda görevli olup olmadığını kontrol eder.
    """
    query = """
        SELECT id FROM exam_schedule 
        WHERE supervisor_id = ? 
          AND exam_date = ?
          AND (
              (start_time <= ? AND end_time > ?)
              OR (start_time < ? AND end_time >= ?)
              OR (start_time >= ? AND end_time <= ?)
          )
    """
    
    params = (instructor_id, exam_date, 
              start_time, start_time,
              end_time, end_time,
              start_time, end_time)
    
    results = execute_query(query, params)
    
    return len(results) > 0


def find_available_supervisors(day_name, exam_date, start_time, end_time, exclude_ids=None):
    """
    Belirtilen saatte müsait olan gözetmenleri bulur.
    
    Parametreler:
        day_name: Gün adı (Pazartesi, Salı, ...)
        exam_date: Sınav tarihi
        start_time: Başlangıç saati
        end_time: Bitiş saati
        exclude_ids: Hariç tutulacak instructor ID'leri
    
    Döndürür:
        supervisors: Müsait gözetmen ID'leri listesi
    """
    if exclude_ids is None:
        exclude_ids = []
    
    # Tüm öğretim üyelerini al
    query = "SELECT id FROM instructors"
    all_instructors = execute_query(query)
    
    available = []
    
    for instructor in all_instructors:
        instructor_id = instructor['id']
        
        # Hariç tutulan listede mi?
        if instructor_id in exclude_ids:
            continue
        
        # O gün müsait mi?
        is_free = check_instructor_available(instructor_id, day_name, start_time, end_time)
        if not is_free:
            continue
        
        # Dersi var mı? (course instructor olarak başka sınavda)
        instructor_busy = check_instructor_conflict(instructor_id, exam_date, start_time, end_time)
        if instructor_busy:
            continue
        
        # Gözetmen olarak başka sınavda mı?
        supervisor_busy = check_supervisor_conflict(instructor_id, exam_date, start_time, end_time)
        if supervisor_busy:
            continue
        
        available.append(instructor_id)
    
    return available


def place_course_exam(course, classrooms, computer_classrooms, exam_days, time_slots):
    """
    Bir dersin sınavını yerleştirir.
    Birden fazla sınıf gerekirse farklı gözetmenler atar.
    """
    course_id = course['id']
    student_count = course['student_count']
    needs_computer = course['needs_computer']
    instructor_id = course['instructor_id']
    department_id = course['department_id']
    exam_duration = course['exam_duration'] if course['exam_duration'] else 60
    
    # Hangi derslikleri kullanacağız?
    if needs_computer:
        available_rooms = computer_classrooms
    else:
        available_rooms = classrooms
    
    # Günlere göre sınav sayısını takip et ve dengeli dağıt
    sorted_days = sorted(exam_days, key=lambda x: get_day_exam_count(x[0]))
    
    # Her gün için dene
    for exam_date, day_name in sorted_days:
        
        # Her saat dilimi için dene
        for start_time, slot_end_time in time_slots:
            
            # Sınav süresine göre bitiş saatini hesapla
            actual_end_time = calculate_end_time(start_time, exam_duration)
            
            # Bitiş saati 18:00'ı geçiyorsa bu slotu atla
            if actual_end_time > '18:00':
                continue
            
            # Hocanın bu günde bu saatte müsait olup olmadığını kontrol et
            is_instructor_free = check_instructor_available(instructor_id, day_name, start_time, actual_end_time)
            
            if not is_instructor_free:
                continue
            
            # Hoca bu saatte başka sınavda mı?
            instructor_busy = check_instructor_conflict(instructor_id, exam_date, start_time, actual_end_time)
            
            if instructor_busy:
                continue
            
            # Hoca gözetmen olarak başka sınavda mı?
            supervisor_busy = check_supervisor_conflict(instructor_id, exam_date, start_time, actual_end_time)
            
            if supervisor_busy:
                continue
            
            # Aynı bölüm ardışık sınav kontrolü
            dept_consecutive = check_department_consecutive(department_id, exam_date, start_time)
            
            if dept_consecutive:
                continue
            
            # Öğrenci çakışması var mı?
            student_conflict = check_student_conflict(course_id, exam_date, start_time, actual_end_time)
            
            if student_conflict:
                continue
            
            # Uygun derslik(ler) bul
            rooms = find_available_classrooms(available_rooms, exam_date, start_time, actual_end_time, student_count)
            
            if rooms is None:
                continue
            
            # Birden fazla derslik varsa yeterli gözetmen var mı kontrol et
            needed_supervisors = len(rooms) - 1  # İlk sınıf dersin hocası
            
            if needed_supervisors > 0:
                # Diğer sınıflar için gözetmen bul
                additional_supervisors = find_available_supervisors(
                    day_name, exam_date, start_time, actual_end_time, 
                    exclude_ids=[instructor_id]
                )
                
                if len(additional_supervisors) < needed_supervisors:
                    continue  # Yeterli gözetmen yok
            
            # Her şey uygun! Sınavı yerleştir
            for i, room in enumerate(rooms):
                if i == 0:
                    # İlk sınıf - dersin öğretmeni gözetmen
                    supervisor = instructor_id
                else:
                    # Diğer sınıflar - farklı gözetmenler
                    supervisor = additional_supervisors[i - 1]
                
                create_exam(course_id, room['id'], exam_date, start_time, actual_end_time, supervisor)
            
            # Bölüm programını güncelle
            update_department_schedule(department_id, exam_date, actual_end_time)
            
            return True
    
    # Hiçbir slot uygun değildi
    return False


def get_schedule_statistics():
    """
    Sınav programı istatistiklerini hesaplar.
    """
    stats = {}
    
    # Toplam planlanmış sınav sayısı (ders bazında)
    result = execute_query("SELECT COUNT(DISTINCT course_id) as count FROM exam_schedule")
    stats['total_exams'] = result[0]['count']
    
    # Sınavı olan ders sayısı
    result = execute_query("SELECT COUNT(*) as count FROM courses WHERE has_exam = 1")
    stats['total_courses_with_exam'] = result[0]['count']
    
    # Henüz planlanmamış ders sayısı
    stats['unplanned_courses'] = stats['total_courses_with_exam'] - stats['total_exams']
    
    # Kullanılan derslik sayısı
    result = execute_query("SELECT COUNT(DISTINCT classroom_id) as count FROM exam_schedule")
    stats['used_classrooms'] = result[0]['count']
    
    # Sınav yapılan gün sayısı
    result = execute_query("SELECT COUNT(DISTINCT exam_date) as count FROM exam_schedule")
    stats['exam_days'] = result[0]['count']
    
    return stats
