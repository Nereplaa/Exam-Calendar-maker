-- ==============================================
-- KSTÜ ÖRNEK VERİLERİ (Güncellenmiş)
-- ==============================================
-- Daha az öğretmen, daha fazla ders
-- Sınav dönemi - kısıtlı müsaitlik
-- ==============================================

-- ==============================================
-- FAKÜLTELER (KSTÜ)
-- ==============================================
INSERT OR IGNORE INTO faculties (name, code) VALUES 
('Mühendislik ve Doğa Bilimleri Fakültesi', 'MDB'),
('Sağlık Bilimleri Fakültesi', 'SBF'),
('Sosyal ve Beşeri Bilimler Fakültesi', 'SBB'),
('Eczacılık Fakültesi', 'ECZ'),
('Diş Hekimliği Fakültesi', 'DHF');

-- ==============================================
-- BÖLÜMLER (KSTÜ)
-- ==============================================
INSERT OR IGNORE INTO departments (name, code, faculty_id) VALUES 
('Bilgisayar Mühendisliği', 'BM', 1),
('Yazılım Mühendisliği', 'YM', 1),
('Hemşirelik', 'HEM', 2),
('Fizyoterapi ve Rehabilitasyon', 'FTR', 2),
('Psikoloji', 'PSK', 3),
('İşletme', 'ISL', 3),
('Eczacılık', 'ECZ', 4),
('Diş Hekimliği', 'DHK', 5);

-- ==============================================
-- DERSLİKLER
-- ==============================================
INSERT OR IGNORE INTO classrooms (name, building, capacity, has_computer, is_available) VALUES 
-- A Blok - Normal Derslikler
('A101', 'A Blok', 50, 0, 1),
('A102', 'A Blok', 45, 0, 1),
('A103', 'A Blok', 40, 0, 1),
('A104', 'A Blok', 35, 0, 1),
('A201', 'A Blok', 60, 0, 1),
('A202', 'A Blok', 55, 0, 1),
('A203', 'A Blok', 50, 0, 1),
('A301', 'A Blok', 80, 0, 1),
('A302', 'A Blok', 70, 0, 1),
-- B Blok
('B101', 'B Blok', 45, 0, 1),
('B102', 'B Blok', 40, 0, 1),
('B201', 'B Blok', 65, 0, 1),
('B202', 'B Blok', 60, 0, 1),
-- C Blok - Bilgisayar Laboratuvarları
('LAB-1', 'C Blok', 30, 1, 1),
('LAB-2', 'C Blok', 30, 1, 1),
('LAB-3', 'C Blok', 35, 1, 1),
-- Konferans Salonları
('KONF-A', 'Ana Bina', 150, 0, 1),
('KONF-B', 'Ana Bina', 120, 0, 1);

-- ==============================================
-- ADMIN KULLANICISI
-- ==============================================
INSERT OR IGNORE INTO users (username, password, email, full_name, role) VALUES 
('admin', 'admin123', 'admin@kstu.edu.tr', 'Sistem Yöneticisi', 'admin');

-- ==============================================
-- ÖĞRETİM ÜYELERİ (15 öğretmen)
-- 4'ten fazla dersi olan bölümler: 2 hoca
-- 4 veya daha az dersi olan bölümler: 1 hoca
-- ==============================================
INSERT OR IGNORE INTO instructors (name, title, email, phone, department_id) VALUES 
-- Bilgisayar Mühendisliği (8 ders = 2 hoca)
('Ahmet Yılmaz', 'Prof. Dr.', 'ahmet.yilmaz@kstu.edu.tr', '0262 555 0101', 1),
('Mehmet Demir', 'Doç. Dr.', 'mehmet.demir@kstu.edu.tr', '0262 555 0102', 1),
-- Yazılım Mühendisliği (6 ders = 2 hoca)
('Ayşe Kaya', 'Prof. Dr.', 'ayse.kaya@kstu.edu.tr', '0262 555 0201', 2),
('Fatma Şahin', 'Doç. Dr.', 'fatma.sahin@kstu.edu.tr', '0262 555 0202', 2),
-- Hemşirelik (6 ders = 2 hoca)
('Elif Yıldız', 'Prof. Dr.', 'elif.yildiz@kstu.edu.tr', '0262 555 0301', 3),
('Selin Arslan', 'Doç. Dr.', 'selin.arslan@kstu.edu.tr', '0262 555 0302', 3),
-- Fizyoterapi (5 ders = 2 hoca)
('Ali Öztürk', 'Prof. Dr.', 'ali.ozturk@kstu.edu.tr', '0262 555 0401', 4),
('Deniz Aydın', 'Doç. Dr.', 'deniz.aydin@kstu.edu.tr', '0262 555 0402', 4),
-- Psikoloji (5 ders = 2 hoca)
('Burak Koç', 'Prof. Dr.', 'burak.koc@kstu.edu.tr', '0262 555 0501', 5),
('Seda Yılmaz', 'Doç. Dr.', 'seda.yilmaz@kstu.edu.tr', '0262 555 0502', 5),
-- İşletme (5 ders = 2 hoca)
('Hakan Erdoğan', 'Prof. Dr.', 'hakan.erdogan@kstu.edu.tr', '0262 555 0601', 6),
('Canan Tekin', 'Doç. Dr.', 'canan.tekin@kstu.edu.tr', '0262 555 0602', 6),
-- Eczacılık (5 ders = 2 hoca)
('Selim Duman', 'Prof. Dr.', 'selim.duman@kstu.edu.tr', '0262 555 0701', 7),
('Aylin Kurt', 'Doç. Dr.', 'aylin.kurt@kstu.edu.tr', '0262 555 0702', 7),
-- Diş Hekimliği (4 ders = 1 hoca)
('Serkan Yücel', 'Prof. Dr.', 'serkan.yucel@kstu.edu.tr', '0262 555 0801', 8);

-- ==============================================
-- ==============================================
-- DERSLER (44 ders - 15 öğretmen)
-- Her dersin günü ve saati belirlendi
-- ==============================================
INSERT OR IGNORE INTO courses (code, name, department_id, instructor_id, student_count, exam_duration, exam_type, needs_computer, has_exam, day_of_week, class_start_time, class_end_time) VALUES 
-- BİLGİSAYAR MÜHENDİSLİĞİ (8 ders - 2 hoca: ID 1,2)
('BM101', 'Programlamaya Giriş', 1, 1, 65, 90, 'Yazılı', 1, 1, 'Pazartesi', '09:00', '10:30'),
('BM102', 'Matematik I', 1, 2, 70, 90, 'Yazılı', 0, 1, 'Salı', '09:00', '10:30'),
('BM201', 'Veri Yapıları', 1, 1, 55, 90, 'Yazılı', 1, 1, 'Çarşamba', '09:00', '10:30'),
('BM202', 'Ayrık Matematik', 1, 2, 50, 60, 'Yazılı', 0, 1, 'Perşembe', '09:00', '10:30'),
('BM301', 'Veritabanı Sistemleri', 1, 1, 45, 90, 'Yazılı', 1, 1, 'Pazartesi', '13:00', '14:30'),
('BM302', 'Algoritma Analizi', 1, 2, 48, 60, 'Yazılı', 0, 1, 'Cuma', '09:00', '10:30'),
('BM401', 'Yapay Zeka', 1, 1, 40, 90, 'Proje', 1, 1, 'Çarşamba', '13:00', '14:30'),
('BM402', 'Bilgisayar Ağları', 1, 2, 42, 60, 'Yazılı', 0, 1, 'Perşembe', '13:00', '14:30'),

-- YAZILIM MÜHENDİSLİĞİ (6 ders - 2 hoca: ID 3,4)
('YM101', 'Yazılım Mühendisliğine Giriş', 2, 3, 60, 60, 'Yazılı', 0, 1, 'Pazartesi', '09:00', '10:30'),
('YM102', 'Programlama Temelleri', 2, 4, 65, 90, 'Yazılı', 1, 1, 'Salı', '09:00', '10:30'),
('YM201', 'Nesne Yönelimli Programlama', 2, 3, 55, 90, 'Yazılı', 1, 1, 'Çarşamba', '09:00', '10:30'),
('YM202', 'Web Programlama', 2, 4, 50, 60, 'Proje', 1, 1, 'Perşembe', '09:00', '10:30'),
('YM301', 'Yazılım Tasarımı', 2, 3, 48, 60, 'Proje', 0, 1, 'Cuma', '09:00', '10:30'),
('YM302', 'Mobil Uygulama Geliştirme', 2, 4, 45, 60, 'Proje', 1, 1, 'Pazartesi', '13:00', '14:30'),

-- HEMŞİRELİK (6 ders - 2 hoca: ID 5,6)
('HEM101', 'Hemşireliğe Giriş', 3, 5, 80, 60, 'Yazılı', 0, 1, 'Pazartesi', '09:00', '10:30'),
('HEM102', 'Anatomi', 3, 6, 85, 90, 'Yazılı', 0, 1, 'Salı', '09:00', '10:30'),
('HEM201', 'Fizyoloji', 3, 5, 75, 90, 'Yazılı', 0, 1, 'Çarşamba', '09:00', '10:30'),
('HEM202', 'Temel Hemşirelik', 3, 6, 78, 60, 'Yazılı', 0, 1, 'Perşembe', '09:00', '10:30'),
('HEM301', 'İç Hastalıkları Hemşireliği', 3, 5, 70, 60, 'Yazılı', 0, 1, 'Cuma', '09:00', '10:30'),
('HEM302', 'Cerrahi Hemşireliği', 3, 6, 72, 60, 'Yazılı', 0, 1, 'Pazartesi', '13:00', '14:30'),

-- FİZYOTERAPİ (5 ders - 2 hoca: ID 7,8)
('FTR101', 'Fizyoterapiye Giriş', 4, 7, 55, 60, 'Yazılı', 0, 1, 'Pazartesi', '09:00', '10:30'),
('FTR102', 'Anatomi I', 4, 8, 60, 90, 'Yazılı', 0, 1, 'Salı', '09:00', '10:30'),
('FTR201', 'Kinezyoloji', 4, 7, 52, 60, 'Yazılı', 0, 1, 'Çarşamba', '09:00', '10:30'),
('FTR202', 'Elektroterapi', 4, 8, 50, 60, 'Yazılı', 0, 1, 'Perşembe', '09:00', '10:30'),
('FTR301', 'Ortopedik Rehabilitasyon', 4, 7, 48, 60, 'Yazılı', 0, 1, 'Cuma', '09:00', '10:30'),

-- PSİKOLOJİ (5 ders - 2 hoca: ID 9,10)
('PSK101', 'Psikolojiye Giriş', 5, 9, 90, 60, 'Yazılı', 0, 1, 'Pazartesi', '09:00', '10:30'),
('PSK102', 'Sosyal Psikoloji', 5, 10, 85, 60, 'Yazılı', 0, 1, 'Salı', '09:00', '10:30'),
('PSK201', 'Gelişim Psikolojisi', 5, 9, 80, 60, 'Yazılı', 0, 1, 'Çarşamba', '09:00', '10:30'),
('PSK202', 'Klinik Psikoloji', 5, 10, 75, 60, 'Yazılı', 0, 1, 'Perşembe', '09:00', '10:30'),
('PSK301', 'Davranış Bozuklukları', 5, 9, 70, 60, 'Yazılı', 0, 1, 'Cuma', '09:00', '10:30'),

-- İŞLETME (5 ders - 2 hoca: ID 11,12)
('ISL101', 'İşletme Bilimine Giriş', 6, 11, 95, 60, 'Yazılı', 0, 1, 'Pazartesi', '09:00', '10:30'),
('ISL102', 'Temel Ekonomi', 6, 12, 90, 60, 'Yazılı', 0, 1, 'Salı', '09:00', '10:30'),
('ISL201', 'Muhasebe Prensipleri', 6, 11, 85, 90, 'Yazılı', 0, 1, 'Çarşamba', '09:00', '10:30'),
('ISL202', 'Pazarlama İlkeleri', 6, 12, 80, 60, 'Yazılı', 0, 1, 'Perşembe', '09:00', '10:30'),
('ISL301', 'Finansal Yönetim', 6, 11, 75, 60, 'Yazılı', 0, 1, 'Cuma', '09:00', '10:30'),

-- ECZACILIK (5 ders - 2 hoca: ID 13,14)
('ECZ101', 'Eczacılığa Giriş', 7, 13, 65, 60, 'Yazılı', 0, 1, 'Pazartesi', '13:00', '14:30'),
('ECZ102', 'Genel Kimya', 7, 14, 70, 90, 'Yazılı', 0, 1, 'Salı', '13:00', '14:30'),
('ECZ201', 'Farmakoloji I', 7, 13, 62, 90, 'Yazılı', 0, 1, 'Çarşamba', '13:00', '14:30'),
('ECZ202', 'Biyokimya', 7, 14, 58, 60, 'Yazılı', 0, 1, 'Perşembe', '13:00', '14:30'),
('ECZ301', 'Farmasötik Teknoloji', 7, 13, 55, 60, 'Yazılı', 0, 1, 'Cuma', '13:00', '14:30'),

-- DİŞ HEKİMLİĞİ (4 ders - 1 hoca: ID 15)
('DHK101', 'Diş Hekimliğine Giriş', 8, 15, 55, 60, 'Yazılı', 0, 1, 'Pazartesi', '14:30', '16:00'),
('DHK102', 'Diş Anatomisi', 8, 15, 58, 90, 'Yazılı', 0, 1, 'Salı', '14:30', '16:00'),
('DHK201', 'Periodontoloji', 8, 15, 52, 60, 'Yazılı', 0, 1, 'Çarşamba', '14:30', '16:00'),
('DHK202', 'Endodonti', 8, 15, 50, 60, 'Yazılı', 0, 1, 'Perşembe', '14:30', '16:00');

-- ==============================================
-- HOCA MÜSAİTLİKLERİ (Ders Saatlerine Göre)
-- is_available=0: Meşgul (Kırmızı) - Ders veriyor
-- is_available=1: Müsait (Yeşil) - Sınav yapabilir
-- ==============================================
INSERT OR IGNORE INTO instructor_availability (instructor_id, day_of_week, start_time, end_time, is_available) VALUES 
-- Prof. Dr. Ahmet Yılmaz (BM - ID 1)
-- Meşgul: Pzt 09-11, 13-15 | Çrş 09-11, 13-15
(1, 'Pazartesi', '09:00', '11:00', 0),
(1, 'Pazartesi', '11:00', '13:00', 1),
(1, 'Pazartesi', '13:00', '15:00', 0),
(1, 'Pazartesi', '15:00', '17:00', 1),
(1, 'Salı', '09:00', '17:00', 1),
(1, 'Çarşamba', '09:00', '11:00', 0),
(1, 'Çarşamba', '11:00', '13:00', 1),
(1, 'Çarşamba', '13:00', '15:00', 0),
(1, 'Çarşamba', '15:00', '17:00', 1),
(1, 'Perşembe', '09:00', '17:00', 1),
(1, 'Cuma', '09:00', '17:00', 1),

-- Doç. Dr. Mehmet Demir (BM - ID 2)
-- Meşgul: Salı 09-11 | Prş 09-11, 13-15 | Cuma 09-11
(2, 'Pazartesi', '09:00', '17:00', 1),
(2, 'Salı', '09:00', '11:00', 0),
(2, 'Salı', '11:00', '17:00', 1),
(2, 'Çarşamba', '09:00', '17:00', 1),
(2, 'Perşembe', '09:00', '11:00', 0),
(2, 'Perşembe', '11:00', '13:00', 1),
(2, 'Perşembe', '13:00', '15:00', 0),
(2, 'Perşembe', '15:00', '17:00', 1),
(2, 'Cuma', '09:00', '11:00', 0),
(2, 'Cuma', '11:00', '17:00', 1),

-- Prof. Dr. Ayşe Kaya (YM - ID 3)
-- Meşgul: Pzt 09-11 | Çrş 09-11 | Cuma 09-11
(3, 'Pazartesi', '09:00', '11:00', 0),
(3, 'Pazartesi', '11:00', '17:00', 1),
(3, 'Salı', '09:00', '17:00', 1),
(3, 'Çarşamba', '09:00', '11:00', 0),
(3, 'Çarşamba', '11:00', '17:00', 1),
(3, 'Perşembe', '09:00', '17:00', 1),
(3, 'Cuma', '09:00', '11:00', 0),
(3, 'Cuma', '11:00', '17:00', 1),

-- Doç. Dr. Fatma Şahin (YM - ID 4)
-- Meşgul: Pzt 13-15 | Salı 09-11 | Prş 09-11
(4, 'Pazartesi', '09:00', '13:00', 1),
(4, 'Pazartesi', '13:00', '15:00', 0),
(4, 'Pazartesi', '15:00', '17:00', 1),
(4, 'Salı', '09:00', '11:00', 0),
(4, 'Salı', '11:00', '17:00', 1),
(4, 'Çarşamba', '09:00', '17:00', 1),
(4, 'Perşembe', '09:00', '11:00', 0),
(4, 'Perşembe', '11:00', '17:00', 1),
(4, 'Cuma', '09:00', '17:00', 1),

-- Prof. Dr. Elif Yıldız (HEM - ID 5)
-- Meşgul: Pzt 09-11 | Çrş 09-11 | Cuma 09-11
(5, 'Pazartesi', '09:00', '11:00', 0),
(5, 'Pazartesi', '11:00', '17:00', 1),
(5, 'Salı', '09:00', '17:00', 1),
(5, 'Çarşamba', '09:00', '11:00', 0),
(5, 'Çarşamba', '11:00', '17:00', 1),
(5, 'Perşembe', '09:00', '17:00', 1),
(5, 'Cuma', '09:00', '11:00', 0),
(5, 'Cuma', '11:00', '17:00', 1),

-- Doç. Dr. Selin Arslan (HEM - ID 6)
-- Meşgul: Pzt 13-15 | Salı 09-11 | Prş 09-11
(6, 'Pazartesi', '09:00', '13:00', 1),
(6, 'Pazartesi', '13:00', '15:00', 0),
(6, 'Pazartesi', '15:00', '17:00', 1),
(6, 'Salı', '09:00', '11:00', 0),
(6, 'Salı', '11:00', '17:00', 1),
(6, 'Çarşamba', '09:00', '17:00', 1),
(6, 'Perşembe', '09:00', '11:00', 0),
(6, 'Perşembe', '11:00', '17:00', 1),
(6, 'Cuma', '09:00', '17:00', 1),

-- Prof. Dr. Ali Öztürk (FTR - ID 7)
-- Meşgul: Pzt 09-11 | Çrş 09-11 | Cuma 09-11
(7, 'Pazartesi', '09:00', '11:00', 0),
(7, 'Pazartesi', '11:00', '17:00', 1),
(7, 'Salı', '09:00', '17:00', 1),
(7, 'Çarşamba', '09:00', '11:00', 0),
(7, 'Çarşamba', '11:00', '17:00', 1),
(7, 'Perşembe', '09:00', '17:00', 1),
(7, 'Cuma', '09:00', '11:00', 0),
(7, 'Cuma', '11:00', '17:00', 1),

-- Doç. Dr. Deniz Aydın (FTR - ID 8)
-- Meşgul: Salı 09-11 | Prş 09-11
(8, 'Pazartesi', '09:00', '17:00', 1),
(8, 'Salı', '09:00', '11:00', 0),
(8, 'Salı', '11:00', '17:00', 1),
(8, 'Çarşamba', '09:00', '17:00', 1),
(8, 'Perşembe', '09:00', '11:00', 0),
(8, 'Perşembe', '11:00', '17:00', 1),
(8, 'Cuma', '09:00', '17:00', 1),

-- Prof. Dr. Burak Koç (PSK - ID 9)
-- Meşgul: Pzt 09-11 | Çrş 09-11 | Cuma 09-11
(9, 'Pazartesi', '09:00', '11:00', 0),
(9, 'Pazartesi', '11:00', '17:00', 1),
(9, 'Salı', '09:00', '17:00', 1),
(9, 'Çarşamba', '09:00', '11:00', 0),
(9, 'Çarşamba', '11:00', '17:00', 1),
(9, 'Perşembe', '09:00', '17:00', 1),
(9, 'Cuma', '09:00', '11:00', 0),
(9, 'Cuma', '11:00', '17:00', 1),

-- Doç. Dr. Seda Yılmaz (PSK - ID 10)
-- Meşgul: Salı 09-11 | Prş 09-11
(10, 'Pazartesi', '09:00', '17:00', 1),
(10, 'Salı', '09:00', '11:00', 0),
(10, 'Salı', '11:00', '17:00', 1),
(10, 'Çarşamba', '09:00', '17:00', 1),
(10, 'Perşembe', '09:00', '11:00', 0),
(10, 'Perşembe', '11:00', '17:00', 1),
(10, 'Cuma', '09:00', '17:00', 1),

-- Prof. Dr. Hakan Erdoğan (ISL - ID 11)
-- Meşgul: Pzt 09-11 | Çrş 09-11 | Cuma 09-11
(11, 'Pazartesi', '09:00', '11:00', 0),
(11, 'Pazartesi', '11:00', '17:00', 1),
(11, 'Salı', '09:00', '17:00', 1),
(11, 'Çarşamba', '09:00', '11:00', 0),
(11, 'Çarşamba', '11:00', '17:00', 1),
(11, 'Perşembe', '09:00', '17:00', 1),
(11, 'Cuma', '09:00', '11:00', 0),
(11, 'Cuma', '11:00', '17:00', 1),

-- Doç. Dr. Canan Tekin (ISL - ID 12)
-- Meşgul: Salı 09-11 | Prş 09-11
(12, 'Pazartesi', '09:00', '17:00', 1),
(12, 'Salı', '09:00', '11:00', 0),
(12, 'Salı', '11:00', '17:00', 1),
(12, 'Çarşamba', '09:00', '17:00', 1),
(12, 'Perşembe', '09:00', '11:00', 0),
(12, 'Perşembe', '11:00', '17:00', 1),
(12, 'Cuma', '09:00', '17:00', 1),

-- Prof. Dr. Selim Duman (ECZ - ID 13)
-- Meşgul: Pzt 13-15 | Çrş 13-15 | Cuma 13-15
(13, 'Pazartesi', '09:00', '13:00', 1),
(13, 'Pazartesi', '13:00', '15:00', 0),
(13, 'Pazartesi', '15:00', '17:00', 1),
(13, 'Salı', '09:00', '17:00', 1),
(13, 'Çarşamba', '09:00', '13:00', 1),
(13, 'Çarşamba', '13:00', '15:00', 0),
(13, 'Çarşamba', '15:00', '17:00', 1),
(13, 'Perşembe', '09:00', '17:00', 1),
(13, 'Cuma', '09:00', '13:00', 1),
(13, 'Cuma', '13:00', '15:00', 0),
(13, 'Cuma', '15:00', '17:00', 1),

-- Doç. Dr. Aylin Kurt (ECZ - ID 14)
-- Meşgul: Salı 13-15 | Prş 13-15
(14, 'Pazartesi', '09:00', '17:00', 1),
(14, 'Salı', '09:00', '13:00', 1),
(14, 'Salı', '13:00', '15:00', 0),
(14, 'Salı', '15:00', '17:00', 1),
(14, 'Çarşamba', '09:00', '17:00', 1),
(14, 'Perşembe', '09:00', '13:00', 1),
(14, 'Perşembe', '13:00', '15:00', 0),
(14, 'Perşembe', '15:00', '17:00', 1),
(14, 'Cuma', '09:00', '17:00', 1),

-- Prof. Dr. Serkan Yücel (DHK - ID 15)
-- Meşgul: Pzt 14-16 | Salı 14-16 | Çrş 14-16 | Prş 14-16
(15, 'Pazartesi', '09:00', '14:00', 1),
(15, 'Pazartesi', '14:00', '16:00', 0),
(15, 'Pazartesi', '16:00', '17:00', 1),
(15, 'Salı', '09:00', '14:00', 1),
(15, 'Salı', '14:00', '16:00', 0),
(15, 'Salı', '16:00', '17:00', 1),
(15, 'Çarşamba', '09:00', '14:00', 1),
(15, 'Çarşamba', '14:00', '16:00', 0),
(15, 'Çarşamba', '16:00', '17:00', 1),
(15, 'Perşembe', '09:00', '14:00', 1),
(15, 'Perşembe', '14:00', '16:00', 0),
(15, 'Perşembe', '16:00', '17:00', 1),
(15, 'Cuma', '09:00', '17:00', 1);

-- ==============================================
-- ÖĞRENCİ VERİLERİ
-- ==============================================
-- 800+ öğrenci verisi students_data.sql dosyasından yüklenir
-- Bu dosya database.py tarafından otomatik olarak işlenir
-- ==============================================


