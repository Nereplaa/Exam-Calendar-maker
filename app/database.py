# ==============================================
# VERİTABANI İŞLEMLERİ
# ==============================================
# Bu dosya veritabanı bağlantısı ve temel
# işlemleri için fonksiyonlar içerir.
# ==============================================

import sqlite3
import os

# Config dosyasından ayarları al
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_PATH, BASE_DIR


def get_db_connection():
    """
    Veritabanına bağlantı açar.
    
    Bu fonksiyon her veritabanı işleminden önce çağrılır.
    İşlem bitince bağlantı kapatılmalıdır.
    
    Döndürür:
        connection: SQLite veritabanı bağlantısı
    """
    # Veritabanı dosyasına bağlan
    connection = sqlite3.connect(DATABASE_PATH)
    
    # Sonuçları dictionary olarak almak için
    # Bu sayede sütun ismiyle erişebiliriz: row['name']
    connection.row_factory = sqlite3.Row
    
    return connection


def init_database():
    """
    Veritabanını oluşturur ve tabloları hazırlar.
    
    Bu fonksiyon uygulama ilk çalıştığında çağrılır.
    Eğer tablolar zaten varsa, tekrar oluşturmaz.
    """
    # Veritabanı klasörünü oluştur (yoksa)
    database_folder = os.path.dirname(DATABASE_PATH)
    if not os.path.exists(database_folder):
        os.makedirs(database_folder)
    
    # Schema dosyasının yolunu bul
    schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
    
    # Schema dosyasını oku
    schema_file = open(schema_path, 'r', encoding='utf-8')
    schema_sql = schema_file.read()
    schema_file.close()
    
    # Veritabanına bağlan
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # SQL komutlarını çalıştır (tabloları oluştur)
    cursor.executescript(schema_sql)
    
    # Değişiklikleri kaydet
    connection.commit()
    
    # Bağlantıyı kapat
    connection.close()
    
    print("Veritabani basariyla olusturuldu!")


def load_seed_data():
    """
    Örnek verileri veritabanına yükler.
    
    Bu fonksiyon sadece veritabanı boşsa çalışır.
    Test için kullanışlı veriler ekler.
    """
    # Önce veritabanında veri var mı kontrol et
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fakülte sayısını kontrol et
    cursor.execute("SELECT COUNT(*) FROM faculties")
    result = cursor.fetchone()
    faculty_count = result[0]
    
    # Eğer fakülte varsa, seed verileri zaten yüklenmiş demektir
    if faculty_count > 0:
        connection.close()
        print("Ornek veriler zaten yuklenmis.")
        return
    
    # Bağlantıyı kapat
    connection.close()
    
    # Seed dosyasının yolunu bul
    seed_path = os.path.join(BASE_DIR, 'database', 'seed.sql')
    
    # Seed dosyasını oku
    seed_file = open(seed_path, 'r', encoding='utf-8')
    seed_sql = seed_file.read()
    seed_file.close()
    
    # Veritabanına bağlan
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # SQL komutlarını çalıştır (örnek verileri ekle)
    cursor.executescript(seed_sql)
    
    # Değişiklikleri kaydet
    connection.commit()
    
    # Öğrenci verilerini yükle (800+ öğrenci)
    students_data_path = os.path.join(BASE_DIR, 'database', 'students_data.sql')
    if os.path.exists(students_data_path):
        students_file = open(students_data_path, 'r', encoding='utf-8')
        students_sql = students_file.read()
        students_file.close()
        
        cursor.executescript(students_sql)
        connection.commit()
        print(f"800+ ogrenci verisi yuklendi!")
    
    # Bağlantıyı kapat
    connection.close()
    
    # Admin şifresini hashle
    hash_admin_password()
    
    print("Ornek veriler basariyla yuklendi!")


def hash_admin_password():
    """
    Admin kullanıcısının şifresini hashler.
    
    Seed dosyasında düz metin olarak kaydedilen
    admin şifresini güvenli hale getirir.
    """
    from werkzeug.security import generate_password_hash
    
    # Veritabanına bağlan
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Admin kullanıcısını bul
    cursor.execute("SELECT id, password FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    # Admin bulunamadıysa çık
    if admin is None:
        connection.close()
        return
    
    # Şifre zaten hashlenmiş mi kontrol et
    # Hashlenmiş şifreler 'pbkdf2:sha256' ile başlar
    current_password = admin['password']
    if current_password.startswith('pbkdf2:'):
        connection.close()
        return
    
    # Şifreyi hashle
    hashed_password = generate_password_hash(current_password)
    
    # Veritabanını güncelle
    cursor.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (hashed_password, admin['id'])
    )
    
    # Değişiklikleri kaydet
    connection.commit()
    
    # Bağlantıyı kapat
    connection.close()
    
    print("Admin sifresi hashlendi.")


def execute_query(query, parameters=None):
    """
    SELECT sorgusu çalıştırır ve sonuçları döndürür.
    
    Parametreler:
        query: SQL sorgusu (SELECT ...)
        parameters: Sorgu parametreleri (opsiyonel)
    
    Döndürür:
        rows: Sorgu sonuçları (liste olarak)
    """
    # Veritabanına bağlan
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Sorguyu çalıştır
    if parameters is None:
        cursor.execute(query)
    else:
        cursor.execute(query, parameters)
    
    # Sonuçları al
    rows = cursor.fetchall()
    
    # Bağlantıyı kapat
    connection.close()
    
    return rows


def execute_insert(query, parameters):
    """
    INSERT sorgusu çalıştırır ve eklenen kaydın ID'sini döndürür.
    
    Parametreler:
        query: SQL sorgusu (INSERT INTO ...)
        parameters: Eklenecek değerler
    
    Döndürür:
        new_id: Eklenen kaydın ID numarası
    """
    # Veritabanına bağlan
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Sorguyu çalıştır
    cursor.execute(query, parameters)
    
    # Değişiklikleri kaydet
    connection.commit()
    
    # Eklenen kaydın ID'sini al
    new_id = cursor.lastrowid
    
    # Bağlantıyı kapat
    connection.close()
    
    return new_id


def execute_update(query, parameters):
    """
    UPDATE veya DELETE sorgusu çalıştırır.
    
    Parametreler:
        query: SQL sorgusu (UPDATE ... veya DELETE ...)
        parameters: Sorgu parametreleri
    
    Döndürür:
        affected_rows: Etkilenen satır sayısı
    """
    # Veritabanına bağlan
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Sorguyu çalıştır
    cursor.execute(query, parameters)
    
    # Değişiklikleri kaydet
    connection.commit()
    
    # Kaç satır etkilendi?
    affected_rows = cursor.rowcount
    
    # Bağlantıyı kapat
    connection.close()
    
    return affected_rows

