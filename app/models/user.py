# ==============================================
# KULLANICI MODELİ
# ==============================================
# Bu dosya kullanıcı işlemlerini yönetir.
# Giriş, kayıt, şifre kontrolü gibi işlemler burada.
# ==============================================

from werkzeug.security import generate_password_hash, check_password_hash
from app.database import execute_query, execute_insert, execute_update


def get_user_by_id(user_id):
    """
    ID'ye göre kullanıcı getirir.
    
    Parametreler:
        user_id: Kullanıcının ID numarası
    
    Döndürür:
        user: Kullanıcı bilgileri (dict) veya None
    """
    # SQL sorgusu hazırla
    query = "SELECT * FROM users WHERE id = ?"
    
    # Sorguyu çalıştır
    results = execute_query(query, (user_id,))
    
    # Sonuç var mı kontrol et
    if len(results) == 0:
        return None
    
    # İlk sonucu döndür
    return results[0]


def get_user_by_username(username):
    """
    Kullanıcı adına göre kullanıcı getirir.
    
    Parametreler:
        username: Kullanıcı adı
    
    Döndürür:
        user: Kullanıcı bilgileri (dict) veya None
    """
    # SQL sorgusu hazırla
    query = "SELECT * FROM users WHERE username = ?"
    
    # Sorguyu çalıştır
    results = execute_query(query, (username,))
    
    # Sonuç var mı kontrol et
    if len(results) == 0:
        return None
    
    # İlk sonucu döndür
    return results[0]


def get_user_by_email(email):
    """
    E-posta adresine göre kullanıcı getirir.
    
    Parametreler:
        email: E-posta adresi
    
    Döndürür:
        user: Kullanıcı bilgileri (dict) veya None
    """
    # SQL sorgusu hazırla
    query = "SELECT * FROM users WHERE email = ?"
    
    # Sorguyu çalıştır
    results = execute_query(query, (email,))
    
    # Sonuç var mı kontrol et
    if len(results) == 0:
        return None
    
    # İlk sonucu döndür
    return results[0]


def create_user(username, password, email, full_name, role, department_id=None):
    """
    Yeni kullanıcı oluşturur.
    
    Parametreler:
        username: Kullanıcı adı
        password: Şifre (düz metin, hashlenecek)
        email: E-posta adresi
        full_name: Ad soyad
        role: Rol (admin, bolum_yetkili, hoca, ogrenci)
        department_id: Bağlı olduğu bölüm (opsiyonel)
    
    Döndürür:
        user_id: Oluşturulan kullanıcının ID'si veya None (hata varsa)
    """
    # Kullanıcı adı zaten var mı kontrol et
    existing_user = get_user_by_username(username)
    if existing_user is not None:
        return None
    
    # E-posta zaten var mı kontrol et
    existing_email = get_user_by_email(email)
    if existing_email is not None:
        return None
    
    # Şifreyi hashle (güvenlik için)
    hashed_password = generate_password_hash(password)
    
    # SQL sorgusu hazırla
    query = """
        INSERT INTO users (username, password, email, full_name, role, department_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    
    # Parametreleri hazırla
    parameters = (username, hashed_password, email, full_name, role, department_id)
    
    # Sorguyu çalıştır ve yeni ID'yi al
    new_id = execute_insert(query, parameters)
    
    return new_id


def check_user_password(username, password):
    """
    Kullanıcı adı ve şifreyi kontrol eder.
    
    Parametreler:
        username: Kullanıcı adı
        password: Şifre (düz metin)
    
    Döndürür:
        user: Doğruysa kullanıcı bilgileri, yanlışsa None
    """
    # Kullanıcıyı bul
    user = get_user_by_username(username)
    
    # Kullanıcı bulunamadıysa
    if user is None:
        return None
    
    # Hesap aktif mi kontrol et
    if user['is_active'] == 0:
        return None
    
    # Şifre doğru mu kontrol et
    # check_password_hash: hashlenmiş şifre ile düz metni karşılaştırır
    is_password_correct = check_password_hash(user['password'], password)
    
    if is_password_correct:
        return user
    else:
        return None


def get_all_users():
    """
    Tüm kullanıcıları getirir.
    
    Döndürür:
        users: Kullanıcı listesi
    """
    # SQL sorgusu hazırla
    query = """
        SELECT u.*, d.name as department_name 
        FROM users u
        LEFT JOIN departments d ON u.department_id = d.id
        ORDER BY u.created_at DESC
    """
    
    # Sorguyu çalıştır
    results = execute_query(query)
    
    return results


def update_user(user_id, full_name, email, role, department_id=None, is_active=1):
    """
    Kullanıcı bilgilerini günceller.
    
    Parametreler:
        user_id: Güncellenecek kullanıcının ID'si
        full_name: Yeni ad soyad
        email: Yeni e-posta
        role: Yeni rol
        department_id: Yeni bölüm
        is_active: Aktif mi?
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # SQL sorgusu hazırla
    query = """
        UPDATE users 
        SET full_name = ?, email = ?, role = ?, department_id = ?, is_active = ?
        WHERE id = ?
    """
    
    # Parametreleri hazırla
    parameters = (full_name, email, role, department_id, is_active, user_id)
    
    # Sorguyu çalıştır
    affected_rows = execute_update(query, parameters)
    
    # En az 1 satır etkilendiyse başarılı
    return affected_rows > 0


def delete_user(user_id):
    """
    Kullanıcıyı siler (pasif yapar).
    
    Parametreler:
        user_id: Silinecek kullanıcının ID'si
    
    Döndürür:
        success: Başarılı mı? (True/False)
    """
    # SQL sorgusu hazırla (tamamen silmek yerine pasif yapıyoruz)
    query = "UPDATE users SET is_active = 0 WHERE id = ?"
    
    # Sorguyu çalıştır
    affected_rows = execute_update(query, (user_id,))
    
    # En az 1 satır etkilendiyse başarılı
    return affected_rows > 0


def get_users_by_role(role):
    """
    Belirli bir role sahip kullanıcıları getirir.
    
    Parametreler:
        role: Rol adı (admin, bolum_yetkili, hoca, ogrenci)
    
    Döndürür:
        users: Kullanıcı listesi
    """
    # SQL sorgusu hazırla
    query = """
        SELECT u.*, d.name as department_name 
        FROM users u
        LEFT JOIN departments d ON u.department_id = d.id
        WHERE u.role = ? AND u.is_active = 1
        ORDER BY u.full_name
    """
    
    # Sorguyu çalıştır
    results = execute_query(query, (role,))
    
    return results

