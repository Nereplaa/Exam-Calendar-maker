-- ==============================================
-- ÖRNEK VERİLER
-- ==============================================
-- Bu dosya test için örnek verileri içerir.
-- Veritabanını test etmek için kullanılır.
-- ==============================================

-- ==============================================
-- FAKÜLTELER
-- ==============================================
INSERT OR IGNORE INTO faculties (name, code) VALUES 
('Mühendislik Fakültesi', 'MUH'),
('Sağlık Bilimleri Fakültesi', 'SAG'),
('İktisadi ve İdari Bilimler Fakültesi', 'IIB');

-- ==============================================
-- BÖLÜMLER
-- ==============================================
INSERT OR IGNORE INTO departments (name, code, faculty_id) VALUES 
('Bilgisayar Mühendisliği', 'BM', 1),
('Yazılım Mühendisliği', 'YM', 1),
('Elektrik-Elektronik Mühendisliği', 'EE', 1),
('Hemşirelik', 'HEM', 2),
('Fizyoterapi', 'FZT', 2),
('İşletme', 'ISL', 3),
('İktisat', 'IKT', 3);

-- ==============================================
-- DERSLİKLER
-- ==============================================
INSERT OR IGNORE INTO classrooms (name, building, capacity, has_computer, is_available) VALUES 
('A101', 'A Blok', 50, 0, 1),
('A102', 'A Blok', 40, 0, 1),
('A103', 'A Blok', 60, 0, 1),
('B201', 'B Blok', 80, 0, 1),
('B202', 'B Blok', 100, 0, 1),
('B203', 'B Blok', 45, 0, 1),
('LAB1', 'C Blok', 30, 1, 1),
('LAB2', 'C Blok', 25, 1, 1),
('KONF', 'Ana Bina', 200, 0, 1);

-- ==============================================
-- ADMIN KULLANICISI
-- ==============================================
-- Şifre: admin123
-- NOT: Şifre daha sonra Python ile hashlenecek!
-- Şimdilik düz metin olarak bırakıyoruz, uygulama başlarken hashleyeceğiz.
INSERT OR IGNORE INTO users (username, password, email, full_name, role) VALUES 
('admin', 'admin123', 'admin@kstu.edu.tr', 'Sistem Yöneticisi', 'admin');

-- ==============================================
-- ÖĞRETİM ÜYELERİ (ÖRNEK)
-- ==============================================
INSERT OR IGNORE INTO instructors (name, title, email, department_id) VALUES 
('Ahmet Yılmaz', 'Prof. Dr.', 'ahmet.yilmaz@kstu.edu.tr', 1),
('Mehmet Demir', 'Doç. Dr.', 'mehmet.demir@kstu.edu.tr', 1),
('Ayşe Kaya', 'Dr. Öğr. Üyesi', 'ayse.kaya@kstu.edu.tr', 2),
('Fatma Şahin', 'Prof. Dr.', 'fatma.sahin@kstu.edu.tr', 2),
('Ali Öztürk', 'Doç. Dr.', 'ali.ozturk@kstu.edu.tr', 3);

-- ==============================================
-- DERSLER (ÖRNEK)
-- ==============================================
INSERT OR IGNORE INTO courses (code, name, department_id, instructor_id, student_count, exam_duration, exam_type) VALUES 
('BM101', 'Programlamaya Giriş', 1, 1, 45, 90, 'Yazılı'),
('BM201', 'Veri Yapıları', 1, 1, 40, 60, 'Yazılı'),
('BM301', 'Veritabanı Sistemleri', 1, 2, 35, 60, 'Yazılı'),
('YM101', 'Yazılım Mühendisliğine Giriş', 2, 3, 50, 60, 'Test'),
('YM201', 'Nesne Yönelimli Programlama', 2, 3, 45, 90, 'Yazılı'),
('YM301', 'Yazılım Tasarımı', 2, 4, 40, 60, 'Proje'),
('EE101', 'Devre Analizi', 3, 5, 55, 90, 'Yazılı'),
('EE201', 'Elektronik', 3, 5, 50, 60, 'Yazılı');

-- ==============================================
-- HOCA MÜSAİTLİKLERİ (ÖRNEK)
-- ==============================================
INSERT OR IGNORE INTO instructor_availability (instructor_id, day_of_week, start_time, end_time, is_available) VALUES 
-- Prof. Dr. Ahmet Yılmaz
(1, 'Pazartesi', '09:00', '17:00', 1),
(1, 'Çarşamba', '09:00', '17:00', 1),
(1, 'Cuma', '09:00', '17:00', 1),
-- Doç. Dr. Mehmet Demir
(2, 'Salı', '09:00', '17:00', 1),
(2, 'Perşembe', '09:00', '17:00', 1),
-- Dr. Öğr. Üyesi Ayşe Kaya
(3, 'Pazartesi', '09:00', '17:00', 1),
(3, 'Salı', '09:00', '17:00', 1),
(3, 'Çarşamba', '09:00', '17:00', 1),
-- Prof. Dr. Fatma Şahin
(4, 'Pazartesi', '09:00', '17:00', 1),
(4, 'Perşembe', '09:00', '17:00', 1),
(4, 'Cuma', '09:00', '17:00', 1),
-- Doç. Dr. Ali Öztürk
(5, 'Salı', '09:00', '17:00', 1),
(5, 'Çarşamba', '09:00', '17:00', 1),
(5, 'Perşembe', '09:00', '17:00', 1);

