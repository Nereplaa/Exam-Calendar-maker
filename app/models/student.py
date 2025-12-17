# ==============================================
# ÖĞRENCİ MODELİ
# ==============================================
# Bu dosya öğrenci işlemlerini yönetir.
# ==============================================

from app.database import execute_query, execute_insert


def get_all_students():
    """Tüm öğrencileri getirir."""
    query = """
        SELECT s.*, d.name as department_name
        FROM students s
        LEFT JOIN departments d ON s.department_id = d.id
        ORDER BY d.name, s.name
    """
    return execute_query(query)


def get_student_by_id(student_id):
    """ID'ye göre öğrenci getirir."""
    query = """
        SELECT s.*, d.name as department_name
        FROM students s
        LEFT JOIN departments d ON s.department_id = d.id
        WHERE s.id = ?
    """
    results = execute_query(query, (student_id,))
    if len(results) == 0:
        return None
    return results[0]


def get_students_by_department(department_id):
    """Bölüme göre öğrenci listesi."""
    query = """
        SELECT s.*, d.name as department_name
        FROM students s
        LEFT JOIN departments d ON s.department_id = d.id
        WHERE s.department_id = ?
        ORDER BY s.grade, s.name
    """
    return execute_query(query, (department_id,))


def get_student_courses(student_id):
    """Öğrencinin aldığı dersleri getirir."""
    query = """
        SELECT c.*, d.name as department_name, i.name as instructor_name
        FROM student_courses sc
        LEFT JOIN courses c ON sc.course_id = c.id
        LEFT JOIN departments d ON c.department_id = d.id
        LEFT JOIN instructors i ON c.instructor_id = i.id
        WHERE sc.student_id = ?
        ORDER BY c.code
    """
    return execute_query(query, (student_id,))


def get_student_count():
    """Toplam öğrenci sayısı."""
    query = "SELECT COUNT(*) as count FROM students"
    results = execute_query(query)
    return results[0]['count']


def get_student_count_by_department(department_id):
    """Bölüme göre öğrenci sayısı."""
    query = "SELECT COUNT(*) as count FROM students WHERE department_id = ?"
    results = execute_query(query, (department_id,))
    return results[0]['count']


def get_departments_with_student_count():
    """Bölümleri öğrenci sayılarıyla birlikte getirir."""
    query = """
        SELECT d.*, 
               COUNT(s.id) as student_count,
               (SELECT COUNT(*) FROM courses WHERE department_id = d.id) as course_count
        FROM departments d
        LEFT JOIN students s ON d.id = s.department_id
        GROUP BY d.id
        ORDER BY d.name
    """
    return execute_query(query)
