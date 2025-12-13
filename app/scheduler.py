# ==============================================
# SINAV PLANLAMA ALGORİTMASI
# ==============================================
# Bu dosya sınavları otomatik olarak planlar.
# Greedy (açgözlü) algoritma kullanılır.
# 
# Algoritma mantığı:
# 1. Dersleri öğrenci sayısına göre sırala (büyükten küçüğe)
# 2. Her ders için uygun gün, saat ve derslik bul
# 3. Kısıtlamaları kontrol et:
#    - Derslik müsait mi?
#    - Hoca müsait mi?
#    - Kapasite yeterli mi?
# 4. Uygunsa yerleştir, değilse sonraki slotu dene
# ==============================================

from app.database import execute_query
from app.models.exam import create_exam, delete_all_exams, check_classroom_conflict, check_instructor_conflict
from app.models.classroom import get_available_classrooms, get_computer_classrooms
from app.models.course import get_courses_with_exam
from app.models.availability import check_instructor_available


def generate_exam_schedule(start_date, end_date):
    """
    Sınav programı oluşturur.
    
    Parametreler:
        start_date: Sınav dönemi başlangıç tarihi (YYYY-MM-DD)
        end_date: Sınav dönemi bitiş tarihi (YYYY-MM-DD)
    
    Döndürür:
        result: Sonuç bilgisi (başarılı sayısı, başarısız listesi)
    """
    # Önce mevcut planı temizle
    delete_all_exams()
    
    # Sınavı olan dersleri al (öğrenci sayısına göre sıralı)
    courses = get_courses_with_exam()
    
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
    # Sabit sınav saatleri
    # Her slot 2 saat (en uzun sınav 120 dk)
    slots = [
        ('09:00', '11:00'),
        ('11:00', '13:00'),
        ('14:00', '16:00'),
        ('16:00', '18:00')
    ]
    
    return slots


def place_course_exam(course, classrooms, computer_classrooms, exam_days, time_slots):
    """
    Bir dersin sınavını yerleştirir.
    
    Parametreler:
        course: Ders bilgisi
        classrooms: Tüm derslikler
        computer_classrooms: Bilgisayarlı derslikler
        exam_days: Sınav günleri
        time_slots: Saat dilimleri
    
    Döndürür:
        success: Yerleştirme başarılı mı?
    """
    # Dersin bilgilerini al
    course_id = course['id']
    student_count = course['student_count']
    needs_computer = course['needs_computer']
    instructor_id = course['instructor_id']
    
    # Hangi derslikleri kullanacağız?
    if needs_computer:
        available_rooms = computer_classrooms
    else:
        available_rooms = classrooms
    
    # Kapasiteye göre uygun derslikleri filtrele
    suitable_rooms = []
    for room in available_rooms:
        if room['capacity'] >= student_count:
            suitable_rooms.append(room)
    
    # Uygun derslik yoksa başarısız
    if len(suitable_rooms) == 0:
        return False
    
    # Her gün için dene
    for exam_date, day_name in exam_days:
        
        # Hocanın bu gün müsait olup olmadığını kontrol et
        is_instructor_free = check_instructor_available(instructor_id, day_name, '09:00', '18:00')
        
        # Hoca bu gün müsait değilse, sonraki güne geç
        if not is_instructor_free:
            continue
        
        # Her saat dilimi için dene
        for start_time, end_time in time_slots:
            
            # Hoca bu saatte başka sınavda mı?
            instructor_busy = check_instructor_conflict(instructor_id, exam_date, start_time, end_time)
            
            if instructor_busy:
                continue
            
            # Uygun derslikleri dene
            for room in suitable_rooms:
                
                # Bu derslik bu saatte müsait mi?
                room_busy = check_classroom_conflict(room['id'], exam_date, start_time, end_time)
                
                if room_busy:
                    continue
                
                # Her şey uygun! Sınavı yerleştir
                create_exam(course_id, room['id'], exam_date, start_time, end_time)
                
                return True
    
    # Hiçbir slot uygun değildi
    return False


def get_schedule_statistics():
    """
    Sınav programı istatistiklerini hesaplar.
    
    Döndürür:
        stats: İstatistik bilgileri
    """
    stats = {}
    
    # Toplam planlanmış sınav sayısı
    result = execute_query("SELECT COUNT(*) as count FROM exam_schedule")
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

