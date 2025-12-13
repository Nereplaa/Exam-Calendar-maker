# ==============================================
# BÖLÜM MODELİ
# ==============================================
# Bu dosya bölüm işlemlerini yönetir.
# Ekleme, listeleme, güncelleme, silme işlemleri.
# ==============================================

from app.database import execute_query, execute_insert, execute_update


def get_all_departments():
    """
    Tüm bölümleri fakülte bilgisiyle birlikte getirir.
    
    Döndürür:
        departments: Bölüm listesi
    """
    # SQL sorgusu - fakülte adını da al
    query = """
        SELECT d.*, f.name as faculty_name 
        FROM departments d
        LEFT JOIN faculties f ON d.faculty_id = f.id
        ORDER BY f.name, d.name
    """
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    return results


def get_department_by_id(department_id):
    """
    ID'ye göre bölüm getirir.
    
    Parametreler:
        department_id: Bölüm ID numarası
    
    Döndürür:
        department: Bölüm bilgileri veya None
    """
    # SQL sorgusu
    query = """
        SELECT d.*, f.name as faculty_name 
        FROM departments d
        LEFT JOIN faculties f ON d.faculty_id = f.id
        WHERE d.id = ?
    """
    
    # Sorguyu çalıştır
    results = execute_query(query, (department_id,))
    
    # Sonuç var mı?
    if len(results) == 0:
        return None
    
    return results[0]


def get_departments_by_faculty(faculty_id):
    """
    Fakülteye göre bölümleri getirir.
    
    Parametreler:
        faculty_id: Fakülte ID numarası
    
    Döndürür:
        departments: Bölüm listesi
    """
    # SQL sorgusu
    query = "SELECT * FROM departments WHERE faculty_id = ? ORDER BY name"
    
    # Sorguyu çalıştır
    results = execute_query(query, (faculty_id,))
    
    return results


def create_department(name, code, faculty_id):
    """
    Yeni bölüm oluşturur.
    
    Parametreler:
        name: Bölüm adı
        code: Bölüm kodu (kısa ad)
        faculty_id: Bağlı olduğu fakülte
    
    Döndürür:
        department_id: Oluşturulan bölümün ID'si veya None
    """
    # Aynı fakültede aynı isimde bölüm var mı kontrol et
    query = "SELECT id FROM departments WHERE name = ? AND faculty_id = ?"
    results = execute_query(query, (name, faculty_id))
    
    if len(results) > 0:
        return None
    
    # Yeni bölüm ekle
    query = "INSERT INTO departments (name, code, faculty_id) VALUES (?, ?, ?)"
    new_id = execute_insert(query, (name, code, faculty_id))
    
    return new_id


def update_department(department_id, name, code, faculty_id):
    """
    Bölüm bilgilerini günceller.
    
    Parametreler:
        department_id: Güncellenecek bölüm ID'si
        name: Yeni bölüm adı
        code: Yeni bölüm kodu
        faculty_id: Yeni fakülte ID'si
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # SQL sorgusu
    query = "UPDATE departments SET name = ?, code = ?, faculty_id = ? WHERE id = ?"
    
    # Sorguyu çalıştır
    affected_rows = execute_update(query, (name, code, faculty_id, department_id))
    
    return affected_rows > 0


def delete_department(department_id):
    """
    Bölümü siler.
    
    Parametreler:
        department_id: Silinecek bölüm ID'si
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # Önce bu bölüme bağlı ders var mı kontrol et
    query = "SELECT COUNT(*) as count FROM courses WHERE department_id = ?"
    results = execute_query(query, (department_id,))
    
    if results[0]['count'] > 0:
        # Bağlı ders varsa silme
        return False
    
    # Bölümü sil
    query = "DELETE FROM departments WHERE id = ?"
    affected_rows = execute_update(query, (department_id,))
    
    return affected_rows > 0

