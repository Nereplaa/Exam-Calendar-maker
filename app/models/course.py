# ==============================================
# DERS MODELİ
# ==============================================
# Bu dosya ders işlemlerini yönetir.
# Ekleme, listeleme, güncelleme, silme işlemleri.
# ==============================================

from app.database import execute_query, execute_insert, execute_update


def get_all_courses():
    """
    Tüm dersleri bölüm ve hoca bilgisiyle birlikte getirir.
    
    Döndürür:
        courses: Ders listesi
    """
    # SQL sorgusu - bölüm ve hoca adını da al
    query = """
        SELECT c.*, 
               d.name as department_name,
               i.name as instructor_name,
               i.title as instructor_title
        FROM courses c
        LEFT JOIN departments d ON c.department_id = d.id
        LEFT JOIN instructors i ON c.instructor_id = i.id
        ORDER BY d.name, c.code
    """
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    return results


def get_course_by_id(course_id):
    """
    ID'ye göre ders getirir.
    
    Parametreler:
        course_id: Ders ID numarası
    
    Döndürür:
        course: Ders bilgileri veya None
    """
    # SQL sorgusu
    query = """
        SELECT c.*, 
               d.name as department_name,
               i.name as instructor_name,
               i.title as instructor_title
        FROM courses c
        LEFT JOIN departments d ON c.department_id = d.id
        LEFT JOIN instructors i ON c.instructor_id = i.id
        WHERE c.id = ?
    """
    
    # Sorguyu çalıştır
    results = execute_query(query, (course_id,))
    
    # Sonuç var mı?
    if len(results) == 0:
        return None
    
    return results[0]


def get_courses_by_department(department_id):
    """
    Bölüme göre dersleri getirir.
    
    Parametreler:
        department_id: Bölüm ID numarası
    
    Döndürür:
        courses: Ders listesi
    """
    # SQL sorgusu - department_name eklendi
    query = """
        SELECT c.*, 
               d.name as department_name,
               i.name as instructor_name, 
               i.title as instructor_title
        FROM courses c
        LEFT JOIN departments d ON c.department_id = d.id
        LEFT JOIN instructors i ON c.instructor_id = i.id
        WHERE c.department_id = ? 
        ORDER BY c.code
    """
    
    # Sorguyu çalıştır
    results = execute_query(query, (department_id,))
    
    return results


def get_courses_by_instructor(instructor_id):
    """
    Öğretim üyesine göre dersleri getirir.
    
    Parametreler:
        instructor_id: Öğretim üyesi ID numarası
    
    Döndürür:
        courses: Ders listesi
    """
    # SQL sorgusu
    query = """
        SELECT c.*, d.name as department_name
        FROM courses c
        LEFT JOIN departments d ON c.department_id = d.id
        WHERE c.instructor_id = ? 
        ORDER BY c.code
    """
    
    # Sorguyu çalıştır
    results = execute_query(query, (instructor_id,))
    
    return results


def create_course(code, name, department_id, instructor_id, student_count, 
                  exam_duration, exam_type, needs_computer, has_exam):
    """
    Yeni ders oluşturur.
    
    Parametreler:
        code: Ders kodu (BM101 gibi)
        name: Ders adı
        department_id: Bölüm ID
        instructor_id: Öğretim üyesi ID
        student_count: Öğrenci sayısı
        exam_duration: Sınav süresi (dakika)
        exam_type: Sınav türü (Yazılı, Test, vb.)
        needs_computer: Bilgisayar gerekli mi?
        has_exam: Sınavı var mı?
    
    Döndürür:
        course_id: Oluşturulan dersin ID'si veya None
    """
    # Aynı ders kodu var mı kontrol et
    query = "SELECT id FROM courses WHERE code = ?"
    results = execute_query(query, (code,))
    
    if len(results) > 0:
        return None
    
    # Yeni ders ekle
    query = """
        INSERT INTO courses (code, name, department_id, instructor_id, 
                            student_count, exam_duration, exam_type, 
                            needs_computer, has_exam) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (code, name, department_id, instructor_id, student_count,
              exam_duration, exam_type, needs_computer, has_exam)
    
    new_id = execute_insert(query, params)
    
    return new_id


def update_course(course_id, code, name, department_id, instructor_id, 
                  student_count, exam_duration, exam_type, needs_computer, has_exam):
    """
    Ders bilgilerini günceller.
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # SQL sorgusu
    query = """
        UPDATE courses 
        SET code = ?, name = ?, department_id = ?, instructor_id = ?,
            student_count = ?, exam_duration = ?, exam_type = ?,
            needs_computer = ?, has_exam = ?
        WHERE id = ?
    """
    
    params = (code, name, department_id, instructor_id, student_count,
              exam_duration, exam_type, needs_computer, has_exam, course_id)
    
    # Sorguyu çalıştır
    affected_rows = execute_update(query, params)
    
    return affected_rows > 0


def delete_course(course_id):
    """
    Dersi siler.
    
    Parametreler:
        course_id: Silinecek ders ID'si
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # Önce bu derse ait sınav planı var mı kontrol et
    query = "SELECT COUNT(*) as count FROM exam_schedule WHERE course_id = ?"
    results = execute_query(query, (course_id,))
    
    if results[0]['count'] > 0:
        # Planlanmış sınav varsa silme
        return False
    
    # Dersi sil
    query = "DELETE FROM courses WHERE id = ?"
    affected_rows = execute_update(query, (course_id,))
    
    return affected_rows > 0


def get_courses_with_exam():
    """
    Sınavı olan dersleri getirir (planlama için).
    
    Döndürür:
        courses: Sınavı olan ders listesi
    """
    # SQL sorgusu
    query = """
        SELECT c.*, 
               d.name as department_name,
               i.name as instructor_name
        FROM courses c
        LEFT JOIN departments d ON c.department_id = d.id
        LEFT JOIN instructors i ON c.instructor_id = i.id
        WHERE c.has_exam = 1
        ORDER BY c.student_count DESC
    """
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    return results

