# ==============================================
# HOCA MÜSAİTLİK MODELİ
# ==============================================
# Bu dosya öğretim üyelerinin müsaitlik bilgilerini yönetir.
# Hangi günlerde, hangi saatlerde müsait oldukları.
# ==============================================

from app.database import execute_query, execute_insert, execute_update


def get_availability_by_instructor(instructor_id):
    """
    Öğretim üyesinin müsaitlik bilgilerini getirir.
    
    Parametreler:
        instructor_id: Öğretim üyesi ID numarası
    
    Döndürür:
        availability: Müsaitlik listesi
    """
    # SQL sorgusu
    query = """
        SELECT * FROM instructor_availability 
        WHERE instructor_id = ?
        ORDER BY 
            CASE day_of_week
                WHEN 'Pazartesi' THEN 1
                WHEN 'Salı' THEN 2
                WHEN 'Çarşamba' THEN 3
                WHEN 'Perşembe' THEN 4
                WHEN 'Cuma' THEN 5
            END,
            start_time
    """
    
    # Sorguyu çalıştır
    results = execute_query(query, (instructor_id,))
    
    return results


def get_availability_by_id(availability_id):
    """
    ID'ye göre müsaitlik kaydı getirir.
    
    Parametreler:
        availability_id: Müsaitlik kaydı ID'si
    
    Döndürür:
        availability: Müsaitlik bilgisi veya None
    """
    # SQL sorgusu
    query = "SELECT * FROM instructor_availability WHERE id = ?"
    
    # Sorguyu çalıştır
    results = execute_query(query, (availability_id,))
    
    # Sonuç var mı?
    if len(results) == 0:
        return None
    
    return results[0]


def create_availability(instructor_id, day_of_week, start_time, end_time, is_available):
    """
    Yeni müsaitlik kaydı oluşturur.
    
    Parametreler:
        instructor_id: Öğretim üyesi ID
        day_of_week: Gün (Pazartesi, Salı, vb.)
        start_time: Başlangıç saati (09:00 gibi)
        end_time: Bitiş saati (17:00 gibi)
        is_available: Müsait mi? (1=Evet, 0=Hayır)
    
    Döndürür:
        availability_id: Oluşturulan kaydın ID'si
    """
    # Yeni kayıt ekle
    query = """
        INSERT INTO instructor_availability 
        (instructor_id, day_of_week, start_time, end_time, is_available) 
        VALUES (?, ?, ?, ?, ?)
    """
    new_id = execute_insert(query, (instructor_id, day_of_week, start_time, end_time, is_available))
    
    return new_id


def update_availability(availability_id, day_of_week, start_time, end_time, is_available):
    """
    Müsaitlik kaydını günceller.
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # SQL sorgusu
    query = """
        UPDATE instructor_availability 
        SET day_of_week = ?, start_time = ?, end_time = ?, is_available = ?
        WHERE id = ?
    """
    
    # Sorguyu çalıştır
    affected_rows = execute_update(query, (day_of_week, start_time, end_time, is_available, availability_id))
    
    return affected_rows > 0


def delete_availability(availability_id):
    """
    Müsaitlik kaydını siler.
    
    Parametreler:
        availability_id: Silinecek kayıt ID'si
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # Kaydı sil
    query = "DELETE FROM instructor_availability WHERE id = ?"
    affected_rows = execute_update(query, (availability_id,))
    
    return affected_rows > 0


def delete_all_availability_by_instructor(instructor_id):
    """
    Öğretim üyesinin tüm müsaitlik kayıtlarını siler.
    
    Parametreler:
        instructor_id: Öğretim üyesi ID
    
    Döndürür:
        deleted_count: Silinen kayıt sayısı
    """
    # Tüm kayıtları sil
    query = "DELETE FROM instructor_availability WHERE instructor_id = ?"
    affected_rows = execute_update(query, (instructor_id,))
    
    return affected_rows


def check_instructor_available(instructor_id, day_of_week, start_time, end_time):
    """
    Öğretim üyesinin belirtilen gün ve saatte müsait olup olmadığını kontrol eder.
    
    Parametreler:
        instructor_id: Öğretim üyesi ID
        day_of_week: Gün
        start_time: Başlangıç saati
        end_time: Bitiş saati
    
    Döndürür:
        is_available: Müsait mi? (True/False)
    """
    # Önce bu hoca için herhangi bir müsaitlik kaydı var mı kontrol et
    check_query = "SELECT COUNT(*) as count FROM instructor_availability WHERE instructor_id = ?"
    check_result = execute_query(check_query, (instructor_id,))
    
    # Eğer hiç müsaitlik kaydı yoksa, tüm günlerde müsait kabul et
    if check_result[0]['count'] == 0:
        return True
    
    # SQL sorgusu - o gün müsait mi? (sadece gün kontrolü yeterli)
    query = """
        SELECT * FROM instructor_availability 
        WHERE instructor_id = ? 
          AND day_of_week = ? 
          AND is_available = 1
    """
    
    # Sorguyu çalıştır (saat parametreleri artık kullanılmıyor)
    results = execute_query(query, (instructor_id, day_of_week))
    
    # Sonuç varsa müsait
    return len(results) > 0


def get_all_availability_with_instructor():
    """
    Tüm müsaitlik kayıtlarını öğretim üyesi bilgisiyle getirir.
    
    Döndürür:
        availability_list: Müsaitlik listesi
    """
    # SQL sorgusu - department_id eklendi
    query = """
        SELECT a.*, i.name as instructor_name, i.title as instructor_title,
               i.department_id as department_id
        FROM instructor_availability a
        LEFT JOIN instructors i ON a.instructor_id = i.id
        ORDER BY i.name, 
            CASE a.day_of_week
                WHEN 'Pazartesi' THEN 1
                WHEN 'Salı' THEN 2
                WHEN 'Çarşamba' THEN 3
                WHEN 'Perşembe' THEN 4
                WHEN 'Cuma' THEN 5
            END
    """
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    return results

