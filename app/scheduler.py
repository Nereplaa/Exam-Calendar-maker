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
from app.models.classroom import get_available_classrooms, get_computer_classrooms, get_all_classrooms
from app.models.course import get_courses_with_exam
from app.models.availability import check_instructor_available


# Her gün için hangi bölümün sınavları yapıldığını takip et
daily_department_exams = {}

def clear_exam_schedule():
    """
    Sınav programını temizler.
    """
    delete_all_exams()


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


def get_nearby_classrooms(classroom_id):
    """
    Bir dersliğin yakın dersliklerini öncelik sırasına göre döndürür.
    classroom_proximity tablosundan veri çeker.
    
    Parametreler:
        classroom_id: Ana derslik ID'si
    
    Döndürür:
        nearby_rooms: Yakın derslik listesi (öncelik sırasına göre)
    """
    query = """
        SELECT c.id, c.name, c.capacity, c.block, c.has_computer, c.is_available
        FROM classrooms c
        INNER JOIN classroom_proximity cp ON c.id = cp.nearby_classroom_id
        WHERE cp.classroom_id = ?
        ORDER BY cp.priority ASC
    """
    return execute_query(query, (classroom_id,))


def find_available_classrooms(classrooms, exam_date, start_time, end_time, needed_capacity):
    """
    Belirtilen kapasiteyi karşılayan müsait derslik(ler)i bulur.
    Yakınlık bilgisini kullanarak akıllı dağıtım yapar.
    
    Algoritma:
    1. Önce tek başına yeterli kapasiteli derslik ara
    2. Bulunamazsa, en büyük dersliği seç ve yakınlarından tamamla
    3. Yakınlık yoksa, kapasiteye göre birleştir
    
    Döndürür:
        rooms: Uygun derslik listesi veya None
    """
    available = []
    
    # Önce müsait derslikleri bul
    for room in classrooms:
        room_busy = check_classroom_conflict(room['id'], exam_date, start_time, end_time)
        if not room_busy:
            # Tek derslik yeterli mi?
            if room['capacity'] >= needed_capacity:
                return [room]  # Tek derslik yeterli, hemen döndür
            available.append(room)
    
    # Tek derslik yeterli değil - yakınlık bazlı birleştirme dene
    if not available:
        return None
    
    # Kapasiteye göre sırala (büyükten küçüğe)
    available.sort(key=lambda x: x['capacity'], reverse=True)
    
    # Her büyük derslik için yakınlık bazlı birleştirme dene
    for base_room in available:
        selected = [base_room]
        current_capacity = base_room['capacity']
        used_ids = {base_room['id']}
        
        # Yakın derslikleri al
        nearby_rooms = get_nearby_classrooms(base_room['id'])
        
        # Yakın ve müsait derslikleri ekle
        for nearby in nearby_rooms:
            if current_capacity >= needed_capacity:
                break  # Yeterli kapasite sağlandı
            
            if nearby['id'] in used_ids:
                continue  # Zaten eklendi
            
            # Yakın derslik müsait mi?
            nearby_busy = check_classroom_conflict(nearby['id'], exam_date, start_time, end_time)
            if not nearby_busy:
                # Derslik bilgisini tam olarak al
                selected.append({
                    'id': nearby['id'],
                    'name': nearby['name'],
                    'capacity': nearby['capacity'],
                    'block': nearby['block'],
                    'has_computer': nearby['has_computer'],
                    'is_available': nearby['is_available']
                })
                current_capacity += nearby['capacity']
                used_ids.add(nearby['id'])
        
        # Yakınlık ile yeterli kapasite sağlandı mı?
        if current_capacity >= needed_capacity:
            return selected
    
    # Yakınlık ile bulunamadı, genel birleştirme dene
    total_capacity = sum(room['capacity'] for room in available)
    
    if total_capacity >= needed_capacity:
        selected = []
        current_capacity = 0
        
        for room in available:
            selected.append(room)
            current_capacity += room['capacity']
            
            if current_capacity >= needed_capacity:
                return selected
    
    # Hiçbir kombinasyon yeterli değil
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


def find_best_exam_day(start_date, end_date):
    """
    Ortak sınavlar için en uygun günü bulur (en çok hocanın müsait olduğu gün).
    """
    from datetime import datetime, timedelta
    
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    days_tr = {0: 'Pazartesi', 1: 'Salı', 2: 'Çarşamba', 3: 'Perşembe', 4: 'Cuma', 5: 'Cumartesi', 6: 'Pazar'}
    
    best_day = None
    max_availability = -1
    
    while current_date <= end:
        if current_date.weekday() < 5:  # Sadece hafta içi
            day_name = days_tr[current_date.weekday()]
            date_str = current_date.strftime('%Y-%m-%d')
            
            # O gün müsait olan hoca sayısını bul
            query = """
                SELECT COUNT(DISTINCT instructor_id) as count 
                FROM instructor_availability 
                WHERE day_of_week = ? AND is_available = 1
            """
            result = execute_query(query, (day_name,))
            count = result[0]['count']
            
            if count > max_availability:
                max_availability = count
                best_day = date_str
        
        current_date += timedelta(days=1)
    
    return best_day

def place_course_exam(course, classrooms, computer_classrooms, exam_days, time_slots, common_exam_day=None, force_common_day=False):
    """
    Bir dersin sınavını yerleştirir.
    force_common_day=True ise SADECE ortak sınav gününe yerleştirir.
    Birden fazla sınıf gerekirse ve gözetmen yetmezse bir gözetmene birden fazla sınıf verebilir.
    Özel derslik ataması varsa (special_classroom_id) sadece o dersliği kullanır.
    """
    course_id = course['id']
    course_code = course['code']
    student_count = course['student_count']
    requires_computer = 1 if 'LAB' in course_code else 0
    duration = course['exam_duration'] if course['exam_duration'] else 60
    instructor_id = course['instructor_id']
    department_id = course['department_id']
    
    # Özel derslik ataması var mı?
    # sqlite3.Row .get() desteklemez, try/except kullanıyoruz
    try:
        special_classroom_id = course['special_classroom_id']
    except (KeyError, IndexError):
        special_classroom_id = None
    
    # Uygun derslik listesi
    if special_classroom_id:
        # Özel derslik atanmışsa sadece onu kullan
        from app.models.classroom import get_classroom_by_id
        special_room = get_classroom_by_id(special_classroom_id)
        if special_room:
            available_rooms = [special_room]
        else:
            available_rooms = []
    elif requires_computer:
        available_rooms = computer_classrooms
    else:
        available_rooms = classrooms
    
    # Günleri filtrele
    if force_common_day and common_exam_day:
        # Ortak sınav gününü bul ve sadece onu kullan
        target_days = [d for d in exam_days if d == common_exam_day]
    elif common_exam_day:
        # Normal sınavlar ortak sınav gününe KONMAZ
        target_days = [d for d in exam_days if d != common_exam_day]
    else:
        target_days = exam_days
        
    # Günleri sınav yoğunluğuna göre sırala (yoğundan aza değil, azdan çoğa)
    # sorted_days = sorted(target_days, key=lambda x: get_day_exam_count(x[0]))
    # Basitlik için sıralamayı şimdilik pass geçelim veya mevcut sırayı kullanalım
    
    for exam_date in target_days:
        # Tarihten gün adını bul
        from datetime import datetime
        dt = datetime.strptime(exam_date, '%Y-%m-%d')
        days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
        day_name = days[dt.weekday()]
        
        # Bölüm için ardışık sınav kontrolü
        # Ortak sınav gününde bu kuralı esnetebiliriz çünkü tek o gün var
        if not force_common_day:
            has_dept_conflict = False
            for start_time, _ in time_slots:
                if check_department_consecutive(department_id, exam_date, start_time):
                    has_dept_conflict = True
                    break
            if has_dept_conflict:
                continue
        
        for start_time, slot_end_time in time_slots:
            # Gerçek bitiş saati
            actual_end_time = calculate_end_time(start_time, duration)
            
            # Bitiş saati 18:00'ı geçiyorsa bu slotu atla
            if actual_end_time > '18:00':
                continue
            
            # Hoca müsait mi? (Dersi veren hoca)
            is_instructor_free = check_instructor_available(instructor_id, day_name, start_time, actual_end_time)
            if not is_instructor_free:
                continue
            
            # Hocanın başka sınavı/görevi var mı?
            instructor_busy = check_instructor_conflict(instructor_id, exam_date, start_time, actual_end_time)
            if instructor_busy:
                continue
                
            supervisor_busy = check_supervisor_conflict(instructor_id, exam_date, start_time, actual_end_time)
            if supervisor_busy:
                continue
                
            # Öğrenci çakışması var mı?
            student_conflict = check_student_conflict(course_id, exam_date, start_time, actual_end_time)
            if student_conflict:
                continue
            
            # Uygun derslik(ler) bul
            rooms = find_available_classrooms(available_rooms, exam_date, start_time, actual_end_time, student_count)
            
            if rooms is None:
                continue
            
            needed_supervisors = len(rooms)
            
            # Gözetmen bul (dersin hocası HARİÇ)
            available_supervisors = find_available_supervisors(
                day_name, exam_date, start_time, actual_end_time, 
                exclude_ids=[instructor_id]
            )
            
            # Çoklu gözetmen mantığı (Multi-room supervision)
            final_supervisors = []
            
            if len(available_supervisors) == 0:
                continue # Hiç kimse yok!
            
            # Mevcut gözetmenleri sırayla ata
            # Eğer yetmezse, mevcutları tekrar kullan (komşu sınıflar için)
            sup_idx = 0
            for i in range(needed_supervisors):
                if sup_idx < len(available_supervisors):
                    final_supervisors.append(available_supervisors[sup_idx])
                    sup_idx += 1
                else:
                    # Gözetmen bitti, son atanan kişiyi tekrar kullan
                    # Bu kişi birden fazla sınıfa bakacak
                    final_supervisors.append(final_supervisors[-1])
            
            # Kontrol: Her şey tamam mı?
            if len(final_supervisors) < needed_supervisors:
                continue
            
            # Sınavı yerleştir
            for i, room in enumerate(rooms):
                supervisor = final_supervisors[i]
                create_exam(course_id, room['id'], exam_date, start_time, actual_end_time, supervisor)
            
            # Bölüm programını güncelle
            update_department_schedule(department_id, exam_date, actual_end_time)
            
            return True
    
    return False


def generate_exam_schedule(start_date, end_date):
    """
    Sınav takvimini oluşturur.
    SEC908 gibi ortak dersleri özel bir güne yerleştirir.
    Ortak sınav günü: Mümkün olduğunca çok hocanın müsait olduğu gün seçilir.
    O güne sadece ortak sınavlar konur.
    """
    # Önce mevcut programı temizle
    clear_exam_schedule()
    
    # Tarih aralığındaki günleri bul
    from datetime import datetime, timedelta
    date_list = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end:
        if current_date.weekday() < 5:  # Sadece hafta içi
            date_list.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    
    # Zaman dilimleri
    time_slots = [
        ('09:00', '10:30'),
        ('11:00', '12:30'),
        ('13:30', '15:00'),
        ('15:30', '17:00')
    ]
    
    # Derslikleri getir
    classrooms = get_all_classrooms()
    normal_classrooms = [c for c in classrooms if c['has_computer'] == 0]
    computer_classrooms = [c for c in classrooms if c['has_computer'] == 1]
    
    # Dersleri getir
    courses = execute_query("SELECT * FROM courses ORDER BY student_count DESC")
    
    # Dersleri ayır: Ortak (>100) ve Normal
    common_courses = [c for c in courses if c['student_count'] >= 100]
    regular_courses = [c for c in courses if c['student_count'] < 100]
    
    # Ortak sınav gününü bul
    common_exam_day = None
    if common_courses:
        common_exam_day = find_best_exam_day(start_date, end_date)
        print(f"Ortak sinav gunu olarak belirlendi: {common_exam_day}")
    
    success_count = 0
    fail_count = 0
    
    # 1. ÖNCE ORTAK DERSLERİ YERLEŞTİR (Sadece ortak güne)
    for course in common_courses:
        print(f"Ortak ders yerlestiriliyor: {course['code']}")
        if place_course_exam(course, normal_classrooms, computer_classrooms, date_list, time_slots, common_exam_day, force_common_day=True):
            success_count += 1
            print(f"   [OK] Yerlestirildi")
        else:
            fail_count += 1
            print(f"   [X] BASARISIZ! Ortak ders {course['code']} yerlestirilemedi!")
            
    # 2. SONRA DİĞER DERSLERİ YERLEŞTİR (Ortak gün HARİÇ)
    for course in regular_courses:
        if place_course_exam(course, normal_classrooms, computer_classrooms, date_list, time_slots, common_exam_day, force_common_day=False):
            success_count += 1
        else:
            fail_count += 1
            print(f"UYARI: Ders {course['code']} yerlestirilemedi!")

    return {
        'total_courses': len(courses),
        'placed_count': success_count,
        'failed_count': fail_count
    }


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
