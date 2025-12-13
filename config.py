# ==============================================
# PROJE KONFİGÜRASYONU
# ==============================================
# Bu dosya uygulamanın ayarlarını içerir.
# Veritabanı yolu, gizli anahtar gibi ayarlar burada tanımlanır.
# ==============================================

import os

# Proje klasörünün yolu
# os.path.dirname(__file__) = bu dosyanın bulunduğu klasör
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Veritabanı dosyasının yolu
# SQLite tek bir dosya kullanır, bu dosya database klasöründe olacak
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'sinav_programi.db')

# Flask için gizli anahtar (session güvenliği için gerekli)
# Gerçek projede bu değer gizli tutulmalı!
SECRET_KEY = 'sinav-programi-gizli-anahtar-2025'

# Sınav saatleri (sabah 09:00'dan akşam 18:00'e kadar)
SINAV_BASLANGIC_SAATI = 9   # 09:00
SINAV_BITIS_SAATI = 18      # 18:00

# Sınav süreleri (dakika cinsinden)
SINAV_SURELERI = [30, 45, 60, 90, 120]

# Sınav günleri (Pazartesi=0, Salı=1, ... Cuma=4)
SINAV_GUNLERI = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']

# Kullanıcı rolleri
ROLLER = {
    'admin': 'Admin',
    'bolum_yetkili': 'Bölüm Yetkilisi',
    'hoca': 'Öğretim Üyesi',
    'ogrenci': 'Öğrenci'
}

# Sınav türleri
SINAV_TURLERI = ['Yazılı', 'Test', 'Uygulama', 'Sözlü', 'Proje']

