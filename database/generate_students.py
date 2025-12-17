# ==============================================
# ÖĞRENCİ VERİSİ OLUŞTURMA SCRIPT
# ==============================================
# 800+ öğrenci verisi üretir
# ==============================================

import random

# Türk isimleri
ad_erkek = ["Ahmet", "Mehmet", "Mustafa", "Ali", "Hasan", "Hüseyin", "Ömer", "Can", "Emre", "Burak", 
            "Cem", "Kaan", "Tolga", "Serhan", "Onur", "Oğuz", "Arda", "Mert", "Baran", "Efe",
            "Kerem", "Deniz", "Eren", "Berk", "Umut", "Koray", "Alp", "Doruk", "Tuna", "Yiğit"]

ad_kadin = ["Ayşe", "Fatma", "Zeynep", "Elif", "Merve", "Selin", "Büşra", "Gizem", "Cansu", "Gül",
            "Derin", "İrem", "Ece", "Pelin", "Yasemin", "Seda", "Defne", "Nil", "Yaren", "Buse",
            "Aslı", "Dilan", "Simge", "Naz", "Lale", "Ecem", "Aylin", "Gülşen", "Deren", "Melisa"]

soyad = ["Yılmaz", "Demir", "Şahin", "Çelik", "Öztürk", "Kaya", "Arslan", "Koç", "Aydın", "Polat",
         "Korkmaz", "Kara", "Aksoy", "Erdoğan", "Özkan", "Tekin", "Kurt", "Yıldız", "Duman", "Güneş",
         "Aktaş", "Bulut", "Çetin", "Doğan", "Kaplan", "Aslan", "Şen", "Yücel", "Sezer", "Güler"]

adres_ilce = ["İzmit", "Gebze", "Kartepe", "Derince", "Başiskele", "Gölcük", "Körfez", "Çayırova", "Dilovası"]

# Bölümler ve kontenjanları
bolumler = [
    (1, "Bilgisayar Mühendisliği", 100),
    (2, "Yazılım Mühendisliği", 100),
    (3, "Hemşirelik", 100),
    (4, "Fizyoterapi", 100),
    (5, "Psikoloji", 100),
    (6, "İşletme", 100),
    (7, "Eczacılık", 100),
    (8, "Diş Hekimliği", 100)
]

# Ders aralıkları (bölüm_id: (başlangıç_ders_id, bitiş_ders_id))
ders_araliklari = {
    1: (1, 8),    # BM dersleri
    2: (9, 14),   # YM dersleri
    3: (15, 20),  # HEM dersleri
    4: (21, 25),  # FTR dersleri
    5: (26, 30),  # PSK dersleri
    6: (31, 35),  # ISL dersleri
    7: (36, 40),  # ECZ dersleri
    8: (41, 44),  # DHK dersleri
}

def generate_tc():
    """Rastgele TC numarası üretir."""
    return ''.join([str(random.randint(0, 9)) for _ in range(11)])

def generate_phone():
    """Rastgele telefon numarası üretir."""
    return f"053{random.randint(1,9)} {random.randint(100,999)} {random.randint(1000,9999)}"

def generate_birth_date(grade):
    """Sınıfa göre doğum tarihi üretir."""
    base_year = 2024 - 18 - grade
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{base_year}-{month:02d}-{day:02d}"

def generate_student_no(bolum_id, yil, sira):
    """Öğrenci numarası üretir."""
    return f"{yil}{bolum_id:02d}{sira:04d}"

def generate_email(ad, soyad):
    """E-posta adresi üretir."""
    ad_clean = ad.lower().replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c').replace('İ', 'i')
    soyad_clean = soyad.lower().replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c').replace('İ', 'i')
    return f"{ad_clean}.{soyad_clean}@kstu.edu.tr"

# Öğrenci verileri
ogrenci_sayaci = 0
students_sql = []
student_courses_sql = []

for bolum_id, bolum_adi, kontenjan in bolumler:
    ogrenci_per_sinif = kontenjan // 4
    
    for sinif in range(1, 5):
        yil = 2024 - sinif + 1
        
        for sira in range(1, ogrenci_per_sinif + 1):
            ogrenci_sayaci += 1
            
            # Cinsiyet rastgele
            if random.random() < 0.5:
                ad = random.choice(ad_erkek)
            else:
                ad = random.choice(ad_kadin)
            
            soyisim = random.choice(soyad)
            tam_isim = f"{ad} {soyisim}"
            
            student_no = generate_student_no(bolum_id, yil, sira)
            tc = generate_tc()
            email = generate_email(ad, soyisim)
            phone = generate_phone()
            adres = f"Kocaeli, {random.choice(adres_ilce)}"
            birth = generate_birth_date(sinif)
            
            # SQL satırı
            sql = f"('{student_no}', '{tc}', '{tam_isim}', '{email}', '{phone}', '{adres}', '{birth}', {bolum_id}, {sinif})"
            students_sql.append(sql)
            
            # Ders kayıtları (her öğrenci 4-5 ders)
            ders_baslangic, ders_bitis = ders_araliklari[bolum_id]
            ders_sayisi = random.randint(4, 5)
            dersler = random.sample(range(ders_baslangic, ders_bitis + 1), min(ders_sayisi, ders_bitis - ders_baslangic + 1))
            
            for ders_id in dersler:
                student_courses_sql.append(f"({ogrenci_sayaci}, {ders_id})")

# SQL çıktısı oluştur (UTF-8 dosyaya yaz)
import os
output_path = os.path.join(os.path.dirname(__file__), 'students_data.sql')

with open(output_path, 'w', encoding='utf-8') as f:
    f.write("-- ==============================================\n")
    f.write("-- ORNEK OGRENCILER (800+ Ogrenci)\n")
    f.write("-- ==============================================\n")
    f.write("INSERT OR IGNORE INTO students (student_no, tc_no, name, email, phone, address, birth_date, department_id, grade) VALUES\n")
    f.write(",\n".join(students_sql) + ";\n")
    
    f.write("\n-- ==============================================\n")
    f.write("-- OGRENCI-DERS ILISKILERI\n")
    f.write("-- ==============================================\n")
    f.write("INSERT OR IGNORE INTO student_courses (student_id, course_id) VALUES\n")
    f.write(",\n".join(student_courses_sql) + ";\n")

print(f"Toplam {ogrenci_sayaci} ogrenci olusturuldu.")
print(f"Dosya: {output_path}")
