# ==============================================
# DERSLİK MODELİ
# ==============================================
# Bu dosya derslik işlemlerini yönetir.
# Ekleme, listeleme, güncelleme, silme işlemleri.
# ==============================================

from app.database import execute_query, execute_insert, execute_update


def get_all_classrooms():
    """
    Tüm derslikleri getirir.
    
    Döndürür:
        classrooms: Derslik listesi
    """
    # SQL sorgusu
    query = "SELECT * FROM classrooms ORDER BY building, name"
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    return results


def get_classroom_by_id(classroom_id):
    """
    ID'ye göre derslik getirir.
    
    Parametreler:
        classroom_id: Derslik ID numarası
    
    Döndürür:
        classroom: Derslik bilgileri veya None
    """
    # SQL sorgusu
    query = "SELECT * FROM classrooms WHERE id = ?"
    
    # Sorguyu çalıştır
    results = execute_query(query, (classroom_id,))
    
    # Sonuç var mı?
    if len(results) == 0:
        return None
    
    return results[0]


def get_available_classrooms():
    """
    Sınav için uygun derslikleri getirir.
    
    Döndürür:
        classrooms: Uygun derslik listesi
    """
    # SQL sorgusu
    query = """
        SELECT * FROM classrooms 
        WHERE is_available = 1 
        ORDER BY capacity DESC
    """
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    return results


def get_computer_classrooms():
    """
    Bilgisayarlı derslikleri getirir.
    
    Döndürür:
        classrooms: Bilgisayarlı derslik listesi
    """
    # SQL sorgusu
    query = """
        SELECT * FROM classrooms 
        WHERE has_computer = 1 AND is_available = 1
        ORDER BY capacity DESC
    """
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    return results


def create_classroom(name, building, capacity, has_computer, is_available):
    """
    Yeni derslik oluşturur.
    
    Parametreler:
        name: Derslik adı (A101 gibi)
        building: Bina adı
        capacity: Kapasite
        has_computer: Bilgisayar var mı?
        is_available: Sınav için uygun mu?
    
    Döndürür:
        classroom_id: Oluşturulan dersliğin ID'si veya None
    """
    # Aynı isimde derslik var mı kontrol et
    query = "SELECT id FROM classrooms WHERE name = ?"
    results = execute_query(query, (name,))
    
    if len(results) > 0:
        return None
    
    # Yeni derslik ekle
    query = """
        INSERT INTO classrooms (name, building, capacity, has_computer, is_available) 
        VALUES (?, ?, ?, ?, ?)
    """
    new_id = execute_insert(query, (name, building, capacity, has_computer, is_available))
    
    return new_id


def update_classroom(classroom_id, name, building, capacity, has_computer, is_available):
    """
    Derslik bilgilerini günceller.
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # SQL sorgusu
    query = """
        UPDATE classrooms 
        SET name = ?, building = ?, capacity = ?, has_computer = ?, is_available = ?
        WHERE id = ?
    """
    
    # Sorguyu çalıştır
    affected_rows = execute_update(query, (name, building, capacity, has_computer, is_available, classroom_id))
    
    return affected_rows > 0


def delete_classroom(classroom_id):
    """
    Dersliği siler.
    
    Parametreler:
        classroom_id: Silinecek derslik ID'si
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # Önce bu dersliğe ait sınav planı var mı kontrol et
    query = "SELECT COUNT(*) as count FROM exam_schedule WHERE classroom_id = ?"
    results = execute_query(query, (classroom_id,))
    
    if results[0]['count'] > 0:
        # Planlanmış sınav varsa silme
        return False
    
    # Dersliği sil
    query = "DELETE FROM classrooms WHERE id = ?"
    affected_rows = execute_update(query, (classroom_id,))
    
    return affected_rows > 0


def get_total_capacity():
    """
    Toplam derslik kapasitesini hesaplar.
    
    Döndürür:
        total: Toplam kapasite
    """
    # SQL sorgusu
    query = "SELECT SUM(capacity) as total FROM classrooms WHERE is_available = 1"
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    if results[0]['total'] is None:
        return 0
    
    return results[0]['total']

