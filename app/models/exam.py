# ==============================================
# SINAV PROGRAMI MODELİ
# ==============================================
# Bu dosya sınav programı işlemlerini yönetir.
# Planlanan sınavları kaydetme, listeleme, silme.
# ==============================================

from app.database import execute_query, execute_insert, execute_update


def get_all_exams():
    """
    Tüm planlanmış sınavları getirir.
    
    Döndürür:
        exams: Sınav listesi
    """
    # SQL sorgusu
    query = """
        SELECT e.*, 
               c.code as course_code, 
               c.name as course_name,
               c.student_count,
               c.exam_duration,
               cl.name as classroom_name,
               cl.capacity as classroom_capacity,
               i.name as instructor_name,
               d.name as department_name,
               s.name as supervisor_name
        FROM exam_schedule e
        LEFT JOIN courses c ON e.course_id = c.id
        LEFT JOIN classrooms cl ON e.classroom_id = cl.id
        LEFT JOIN instructors i ON c.instructor_id = i.id
        LEFT JOIN instructors s ON e.supervisor_id = s.id
        LEFT JOIN departments d ON c.department_id = d.id
        ORDER BY e.exam_date, e.start_time, cl.name
    """
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    return results


def get_exam_by_id(exam_id):
    """
    ID'ye göre sınav getirir.
    
    Parametreler:
        exam_id: Sınav ID numarası
    
    Döndürür:
        exam: Sınav bilgileri veya None
    """
    # SQL sorgusu
    query = """
        SELECT e.*, 
               c.code as course_code, 
               c.name as course_name,
               cl.name as classroom_name
        FROM exam_schedule e
        LEFT JOIN courses c ON e.course_id = c.id
        LEFT JOIN classrooms cl ON e.classroom_id = cl.id
        WHERE e.id = ?
    """
    
    # Sorguyu çalıştır
    results = execute_query(query, (exam_id,))
    
    if len(results) == 0:
        return None
    
    return results[0]


def create_exam(course_id, classroom_id, exam_date, start_time, end_time, supervisor_id=None):
    """
    Yeni sınav kaydı oluşturur.
    
    Parametreler:
        course_id: Ders ID
        classroom_id: Derslik ID
        exam_date: Sınav tarihi (YYYY-MM-DD)
        start_time: Başlangıç saati (HH:MM)
        end_time: Bitiş saati (HH:MM)
        supervisor_id: Gözetmen ID (opsiyonel)
    
    Döndürür:
        exam_id: Oluşturulan sınavın ID'si
    """
    # Yeni kayıt ekle
    query = """
        INSERT INTO exam_schedule 
        (course_id, classroom_id, supervisor_id, exam_date, start_time, end_time, status) 
        VALUES (?, ?, ?, ?, ?, ?, 'planlandı')
    """
    new_id = execute_insert(query, (course_id, classroom_id, supervisor_id, exam_date, start_time, end_time))
    
    return new_id


def delete_exam(exam_id):
    """
    Sınav kaydını siler.
    
    Parametreler:
        exam_id: Silinecek sınav ID'si
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # Kaydı sil
    query = "DELETE FROM exam_schedule WHERE id = ?"
    affected_rows = execute_update(query, (exam_id,))
    
    return affected_rows > 0


def delete_all_exams():
    """
    Tüm sınav kayıtlarını siler.
    Yeni planlama yapmadan önce kullanılır.
    
    Döndürür:
        deleted_count: Silinen kayıt sayısı
    """
    # Tüm kayıtları sil
    query = "DELETE FROM exam_schedule"
    affected_rows = execute_update(query, ())
    
    return affected_rows


def check_classroom_conflict(classroom_id, exam_date, start_time, end_time):
    """
    Derslikte çakışma var mı kontrol eder.
    
    Bir derslikte aynı tarih ve saatte 
    başka bir sınav var mı?
    
    Döndürür:
        has_conflict: Çakışma var mı? (True/False)
    """
    # SQL sorgusu
    query = """
        SELECT id FROM exam_schedule 
        WHERE classroom_id = ? 
          AND exam_date = ?
          AND (
              (start_time <= ? AND end_time > ?)
              OR (start_time < ? AND end_time >= ?)
              OR (start_time >= ? AND end_time <= ?)
          )
    """
    
    params = (classroom_id, exam_date, 
              start_time, start_time,
              end_time, end_time,
              start_time, end_time)
    
    results = execute_query(query, params)
    
    # Sonuç varsa çakışma var
    return len(results) > 0


def check_instructor_conflict(instructor_id, exam_date, start_time, end_time):
    """
    Öğretim üyesinde çakışma var mı kontrol eder.
    
    Bir hocanın aynı tarih ve saatte 
    başka bir sınavı var mı?
    
    Döndürür:
        has_conflict: Çakışma var mı? (True/False)
    """
    # SQL sorgusu
    query = """
        SELECT e.id FROM exam_schedule e
        LEFT JOIN courses c ON e.course_id = c.id
        WHERE c.instructor_id = ? 
          AND e.exam_date = ?
          AND (
              (e.start_time <= ? AND e.end_time > ?)
              OR (e.start_time < ? AND e.end_time >= ?)
              OR (e.start_time >= ? AND e.end_time <= ?)
          )
    """
    
    params = (instructor_id, exam_date, 
              start_time, start_time,
              end_time, end_time,
              start_time, end_time)
    
    results = execute_query(query, params)
    
    return len(results) > 0


def get_exams_by_date(exam_date):
    """
    Tarihe göre sınavları getirir.
    
    Parametreler:
        exam_date: Sınav tarihi (YYYY-MM-DD)
    
    Döndürür:
        exams: O güne ait sınav listesi
    """
    # SQL sorgusu
    query = """
        SELECT e.*, 
               c.code as course_code, 
               c.name as course_name,
               cl.name as classroom_name,
               i.name as instructor_name
        FROM exam_schedule e
        LEFT JOIN courses c ON e.course_id = c.id
        LEFT JOIN classrooms cl ON e.classroom_id = cl.id
        LEFT JOIN instructors i ON c.instructor_id = i.id
        WHERE e.exam_date = ?
        ORDER BY e.start_time, cl.name
    """
    
    results = execute_query(query, (exam_date,))
    
    return results


def get_exams_by_department(department_id):
    """
    Bölüme göre sınavları getirir.
    
    Parametreler:
        department_id: Bölüm ID
    
    Döndürür:
        exams: O bölüme ait sınav listesi
    """
    # SQL sorgusu
    query = """
        SELECT e.*, 
               c.code as course_code, 
               c.name as course_name,
               cl.name as classroom_name,
               i.name as instructor_name
        FROM exam_schedule e
        LEFT JOIN courses c ON e.course_id = c.id
        LEFT JOIN classrooms cl ON e.classroom_id = cl.id
        LEFT JOIN instructors i ON c.instructor_id = i.id
        WHERE c.department_id = ?
        ORDER BY e.exam_date, e.start_time
    """
    
    results = execute_query(query, (department_id,))
    
    return results

