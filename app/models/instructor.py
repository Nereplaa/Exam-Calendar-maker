# ==============================================
# ÖĞRETİM ÜYESİ MODELİ
# ==============================================
# Bu dosya öğretim üyesi işlemlerini yönetir.
# Ekleme, listeleme, güncelleme, silme işlemleri.
# ==============================================

from app.database import execute_query, execute_insert, execute_update


def get_all_instructors():
    """
    Tüm öğretim üyelerini bölüm bilgisiyle birlikte getirir.
    
    Döndürür:
        instructors: Öğretim üyesi listesi
    """
    # SQL sorgusu - bölüm adını da al
    query = """
        SELECT i.*, d.name as department_name 
        FROM instructors i
        LEFT JOIN departments d ON i.department_id = d.id
        ORDER BY i.name
    """
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    return results


def get_instructor_by_id(instructor_id):
    """
    ID'ye göre öğretim üyesi getirir.
    
    Parametreler:
        instructor_id: Öğretim üyesi ID numarası
    
    Döndürür:
        instructor: Öğretim üyesi bilgileri veya None
    """
    # SQL sorgusu
    query = """
        SELECT i.*, d.name as department_name 
        FROM instructors i
        LEFT JOIN departments d ON i.department_id = d.id
        WHERE i.id = ?
    """
    
    # Sorguyu çalıştır
    results = execute_query(query, (instructor_id,))
    
    # Sonuç var mı?
    if len(results) == 0:
        return None
    
    return results[0]


def get_instructors_by_department(department_id):
    """
    Bölüme göre öğretim üyelerini getirir.
    
    Parametreler:
        department_id: Bölüm ID numarası
    
    Döndürür:
        instructors: Öğretim üyesi listesi
    """
    # SQL sorgusu
    query = "SELECT * FROM instructors WHERE department_id = ? ORDER BY name"
    
    # Sorguyu çalıştır
    results = execute_query(query, (department_id,))
    
    return results


def create_instructor(name, title, email, phone, department_id):
    """
    Yeni öğretim üyesi oluşturur.
    
    Parametreler:
        name: Ad soyad
        title: Unvan (Prof. Dr., Doç. Dr., vb.)
        email: E-posta adresi
        phone: Telefon numarası
        department_id: Bağlı olduğu bölüm
    
    Döndürür:
        instructor_id: Oluşturulan öğretim üyesinin ID'si veya None
    """
    # Aynı e-posta var mı kontrol et
    if email:
        query = "SELECT id FROM instructors WHERE email = ?"
        results = execute_query(query, (email,))
        
        if len(results) > 0:
            return None
    
    # Yeni öğretim üyesi ekle
    query = """
        INSERT INTO instructors (name, title, email, phone, department_id) 
        VALUES (?, ?, ?, ?, ?)
    """
    new_id = execute_insert(query, (name, title, email, phone, department_id))
    
    return new_id


def update_instructor(instructor_id, name, title, email, phone, department_id):
    """
    Öğretim üyesi bilgilerini günceller.
    
    Parametreler:
        instructor_id: Güncellenecek öğretim üyesi ID'si
        name: Yeni ad soyad
        title: Yeni unvan
        email: Yeni e-posta
        phone: Yeni telefon
        department_id: Yeni bölüm ID'si
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # SQL sorgusu
    query = """
        UPDATE instructors 
        SET name = ?, title = ?, email = ?, phone = ?, department_id = ? 
        WHERE id = ?
    """
    
    # Sorguyu çalıştır
    affected_rows = execute_update(query, (name, title, email, phone, department_id, instructor_id))
    
    return affected_rows > 0


def delete_instructor(instructor_id):
    """
    Öğretim üyesini siler.
    
    Parametreler:
        instructor_id: Silinecek öğretim üyesi ID'si
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # Önce bu hocaya bağlı ders var mı kontrol et
    query = "SELECT COUNT(*) as count FROM courses WHERE instructor_id = ?"
    results = execute_query(query, (instructor_id,))
    
    if results[0]['count'] > 0:
        # Bağlı ders varsa silme
        return False
    
    # Öğretim üyesini sil
    query = "DELETE FROM instructors WHERE id = ?"
    affected_rows = execute_update(query, (instructor_id,))
    
    return affected_rows > 0

