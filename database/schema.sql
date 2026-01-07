-- ==============================================
-- VERİTABANI ŞEMASI (Tablo Yapıları)
-- ==============================================
-- Bu dosya veritabanındaki tüm tabloları tanımlar.
-- Her tablo ayrı ayrı açıklanmıştır.
-- ==============================================

-- ==============================================
-- TABLO 1: KULLANICILAR (users)
-- ==============================================
-- Sisteme giriş yapan kullanıcıları tutar.
-- Admin, Bölüm Yetkilisi, Hoca, Öğrenci olabilir.
-- ==============================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Otomatik artan benzersiz numara
    username TEXT NOT NULL UNIQUE,          -- Kullanıcı adı (benzersiz olmalı)
    password TEXT NOT NULL,                 -- Şifre (hashlenmiş olarak saklanır)
    email TEXT NOT NULL UNIQUE,             -- E-posta adresi (benzersiz)
    full_name TEXT NOT NULL,                -- Ad Soyad
    role TEXT NOT NULL,                     -- Rol: admin, bolum_yetkili, hoca, ogrenci
    department_id INTEGER,                  -- Bağlı olduğu bölüm (varsa)
    is_active INTEGER DEFAULT 1,            -- Aktif mi? (1=Evet, 0=Hayır)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP  -- Oluşturulma tarihi
);

-- ==============================================
-- TABLO 2: FAKÜLTELER (faculties)
-- ==============================================
-- Üniversitedeki fakülteleri tutar.
-- Örnek: Mühendislik Fakültesi, Tıp Fakültesi
-- ==============================================
CREATE TABLE IF NOT EXISTS faculties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Fakülte ID
    name TEXT NOT NULL UNIQUE,              -- Fakülte adı (benzersiz)
    code TEXT NOT NULL UNIQUE,              -- Kısa kod (MUH, TIP gibi)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================
-- TABLO 3: BÖLÜMLER (departments)
-- ==============================================
-- Fakültelere bağlı bölümleri tutar.
-- Örnek: Bilgisayar Mühendisliği, Yazılım Mühendisliği
-- ==============================================
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Bölüm ID
    name TEXT NOT NULL,                     -- Bölüm adı
    code TEXT NOT NULL,                     -- Kısa kod (BM, YM gibi)
    faculty_id INTEGER NOT NULL,            -- Hangi fakülteye bağlı?
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (faculty_id) REFERENCES faculties(id)  -- Fakülte tablosuna bağlantı
);

-- ==============================================
-- TABLO 4: ÖĞRETİM ÜYELERİ (instructors)
-- ==============================================
-- Ders veren öğretim üyelerini tutar.
-- Her öğretim üyesi bir bölüme bağlıdır.
-- ==============================================
CREATE TABLE IF NOT EXISTS instructors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Öğretim üyesi ID
    name TEXT NOT NULL,                     -- Ad Soyad
    title TEXT,                             -- Unvan (Prof. Dr., Doç. Dr., vb.)
    email TEXT UNIQUE,                      -- E-posta
    phone TEXT,                             -- Telefon
    department_id INTEGER NOT NULL,         -- Bağlı olduğu bölüm
    user_id INTEGER,                        -- Sisteme giriş için kullanıcı hesabı
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ==============================================
-- TABLO 5: DERSLİKLER (classrooms)
-- ==============================================
-- Sınav yapılabilecek derslikleri tutar.
-- Kapasite ve uygunluk bilgisi içerir.
-- ==============================================
CREATE TABLE IF NOT EXISTS classrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Derslik ID
    name TEXT NOT NULL UNIQUE,              -- Derslik adı (A101, B202 gibi)
    building TEXT,                          -- Bina adı
    block TEXT,                             -- Blok kodu (M, S, K, D, E, A)
    capacity INTEGER NOT NULL,              -- Kaç öğrenci sığar?
    has_computer INTEGER DEFAULT 0,         -- Bilgisayar var mı? (1=Evet, 0=Hayır)
    is_available INTEGER DEFAULT 1,         -- Sınav için uygun mu? (1=Evet, 0=Hayır)
    classroom_type TEXT DEFAULT 'Normal',   -- Derslik tipi: Normal, Lab, Dekanlık, Konferans, Amfi
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================
-- TABLO 6: DERSLER (courses)
-- ==============================================
-- Sınavı yapılacak dersleri tutar.
-- Her ders bir bölüme ve öğretim üyesine bağlıdır.
-- ==============================================
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Ders ID
    code TEXT NOT NULL,                     -- Ders kodu (BM101, YM201 gibi)
    name TEXT NOT NULL,                     -- Ders adı
    department_id INTEGER NOT NULL,         -- Hangi bölümün dersi?
    instructor_id INTEGER NOT NULL,         -- Dersi veren hoca
    student_count INTEGER DEFAULT 0,        -- Kayıtlı öğrenci sayısı
    exam_duration INTEGER DEFAULT 60,       -- Sınav süresi (dakika)
    exam_type TEXT DEFAULT 'Yazılı',        -- Sınav türü (Yazılı, Test, vb.)
    needs_computer INTEGER DEFAULT 0,       -- Bilgisayarlı derslik gerekli mi?
    has_exam INTEGER DEFAULT 1,             -- Bu dersin sınavı var mı? (1=Var, 0=Yok)
    special_classroom_id INTEGER,           -- Özel derslik ataması (Dekanlık, Lab vb.)
    day_of_week TEXT,                       -- Dersin günü (Pazartesi, Salı, vb.)
    class_start_time TEXT,                  -- Ders başlangıç saati (09:00)
    class_end_time TEXT,                    -- Ders bitiş saati (10:30)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (instructor_id) REFERENCES instructors(id),
    FOREIGN KEY (special_classroom_id) REFERENCES classrooms(id)
);

-- ==============================================
-- TABLO 7: HOCA MÜSAİTLİKLERİ (instructor_availability)
-- ==============================================
-- Öğretim üyelerinin hangi günlerde müsait olduğunu tutar.
-- Sınav planlamasında bu bilgi kullanılır.
-- ==============================================
CREATE TABLE IF NOT EXISTS instructor_availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instructor_id INTEGER NOT NULL,         -- Hangi öğretim üyesi?
    day_of_week TEXT NOT NULL,              -- Gün (Pazartesi, Salı, vb.)
    start_time TEXT NOT NULL,               -- Başlangıç saati (09:00 gibi)
    end_time TEXT NOT NULL,                 -- Bitiş saati (17:00 gibi)
    is_available INTEGER DEFAULT 1,         -- Müsait mi? (1=Evet, 0=Hayır)
    FOREIGN KEY (instructor_id) REFERENCES instructors(id)
);

-- ==============================================
-- TABLO 8: SINAV PROGRAMI (exam_schedule)
-- ==============================================
-- Planlanan sınavları tutar.
-- Hangi ders, hangi gün, saat ve derslikte yapılacak.
-- ==============================================
CREATE TABLE IF NOT EXISTS exam_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,             -- Hangi dersin sınavı?
    classroom_id INTEGER NOT NULL,          -- Hangi derslikte?
    supervisor_id INTEGER,                  -- Gözetmen (sınıf sorumlusu)
    exam_date TEXT NOT NULL,                -- Sınav tarihi (2025-01-15 gibi)
    start_time TEXT NOT NULL,               -- Başlangıç saati (09:00 gibi)
    end_time TEXT NOT NULL,                 -- Bitiş saati (10:30 gibi)
    status TEXT DEFAULT 'planlandı',        -- Durum: planlandı, onaylandı, iptal
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (classroom_id) REFERENCES classrooms(id),
    FOREIGN KEY (supervisor_id) REFERENCES instructors(id)
);

-- ==============================================
-- TABLO 9: ÖĞRENCİLER (students)
-- ==============================================
-- Öğrenci bilgilerini tutar.
-- ==============================================
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_no TEXT NOT NULL UNIQUE,        -- Öğrenci numarası
    tc_no TEXT,                             -- TC Kimlik Numarası
    name TEXT NOT NULL,                     -- Ad Soyad
    email TEXT,                             -- E-posta
    phone TEXT,                             -- Telefon
    address TEXT,                           -- Adres
    birth_date TEXT,                        -- Doğum tarihi
    department_id INTEGER NOT NULL,         -- Bölümü
    grade INTEGER DEFAULT 1,                -- Sınıf (1,2,3,4)
    user_id INTEGER,                        -- Giriş için kullanıcı hesabı
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ==============================================
-- TABLO 10: ÖĞRENCİ-DERS İLİŞKİSİ (student_courses)
-- ==============================================
-- Hangi öğrenci hangi derslere kayıtlı?
-- Çakışma kontrolünde kullanılır.
-- ==============================================
CREATE TABLE IF NOT EXISTS student_courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,            -- Öğrenci
    course_id INTEGER NOT NULL,             -- Ders
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- ==============================================
-- İNDEKSLER (Hızlı Arama İçin)
-- ==============================================
-- Sık aranan sütunlar için indeks oluşturuyoruz.
-- Bu sayede sorgular daha hızlı çalışır.
-- ==============================================
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_courses_department ON courses(department_id);
CREATE INDEX IF NOT EXISTS idx_courses_instructor ON courses(instructor_id);
CREATE INDEX IF NOT EXISTS idx_exam_schedule_date ON exam_schedule(exam_date);
CREATE INDEX IF NOT EXISTS idx_exam_schedule_classroom ON exam_schedule(classroom_id);
CREATE INDEX IF NOT EXISTS idx_student_courses_student ON student_courses(student_id);
CREATE INDEX IF NOT EXISTS idx_student_courses_course ON student_courses(course_id);

-- ==============================================
-- TABLO 11: DERSLİK YAKINLIK İLİŞKİSİ (classroom_proximity)
-- ==============================================
-- Hangi derslikler birbirine yakın?
-- Sınav planlamasında kapasite yetersiz olduğunda
-- yakın derslikler tercih edilir.
-- ==============================================
CREATE TABLE IF NOT EXISTS classroom_proximity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classroom_id INTEGER NOT NULL,        -- Ana derslik
    nearby_classroom_id INTEGER NOT NULL, -- Yakın derslik
    priority INTEGER DEFAULT 1,           -- Yakınlık sırası (1=en yakın)
    FOREIGN KEY (classroom_id) REFERENCES classrooms(id),
    FOREIGN KEY (nearby_classroom_id) REFERENCES classrooms(id)
);

CREATE INDEX IF NOT EXISTS idx_proximity_classroom ON classroom_proximity(classroom_id);

