# ==============================================
# FAKÜLTE MODELİ
# ==============================================
# Bu dosya fakülte işlemlerini yönetir.
# Ekleme, listeleme, güncelleme, silme işlemleri.
# ==============================================

from app.database import execute_query, execute_insert, execute_update


def get_all_faculties():
    """
    Tüm fakülteleri getirir.
    
    Döndürür:
        faculties: Fakülte listesi
    """
    # SQL sorgusu
    query = "SELECT * FROM faculties ORDER BY name"
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    return results


def get_faculty_by_id(faculty_id):
    """
    ID'ye göre fakülte getirir.
    
    Parametreler:
        faculty_id: Fakülte ID numarası
    
    Döndürür:
        faculty: Fakülte bilgileri veya None
    """
    # SQL sorgusu
    query = "SELECT * FROM faculties WHERE id = ?"
    
    # Sorguyu çalıştır
    results = execute_query(query, (faculty_id,))
    
    # Sonuç var mı?
    if len(results) == 0:
        return None
    
    return results[0]


def create_faculty(name, code):
    """
    Yeni fakülte oluşturur.
    
    Parametreler:
        name: Fakülte adı
        code: Fakülte kodu (kısa ad)
    
    Döndürür:
        faculty_id: Oluşturulan fakültenin ID'si veya None
    """
    # Aynı isimde fakülte var mı kontrol et
    query = "SELECT id FROM faculties WHERE name = ? OR code = ?"
    results = execute_query(query, (name, code))
    
    if len(results) > 0:
        return None
    
    # Yeni fakülte ekle
    query = "INSERT INTO faculties (name, code) VALUES (?, ?)"
    new_id = execute_insert(query, (name, code))
    
    return new_id


def update_faculty(faculty_id, name, code):
    """
    Fakülte bilgilerini günceller.
    
    Parametreler:
        faculty_id: Güncellenecek fakülte ID'si
        name: Yeni fakülte adı
        code: Yeni fakülte kodu
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # SQL sorgusu
    query = "UPDATE faculties SET name = ?, code = ? WHERE id = ?"
    
    # Sorguyu çalıştır
    affected_rows = execute_update(query, (name, code, faculty_id))
    
    return affected_rows > 0


def delete_faculty(faculty_id):
    """
    Fakülteyi siler.
    
    Parametreler:
        faculty_id: Silinecek fakülte ID'si
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # Önce bu fakülteye bağlı bölüm var mı kontrol et
    query = "SELECT COUNT(*) as count FROM departments WHERE faculty_id = ?"
    results = execute_query(query, (faculty_id,))
    
    if results[0]['count'] > 0:
        # Bağlı bölüm varsa silme
        return False
    
    # Fakülteyi sil
    query = "DELETE FROM faculties WHERE id = ?"
    affected_rows = execute_update(query, (faculty_id,))
    
    return affected_rows > 0

