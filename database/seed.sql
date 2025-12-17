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
-- ÖĞRETİM ÜYELERİ (Azaltılmış - 16 öğretmen)
-- ==============================================
INSERT OR IGNORE INTO instructors (name, title, email, phone, department_id) VALUES 
-- Bilgisayar Mühendisliği (3 hoca - 8 ders)
('Ahmet Yılmaz', 'Prof. Dr.', 'ahmet.yilmaz@kstu.edu.tr', '0262 555 0101', 1),
('Mehmet Demir', 'Doç. Dr.', 'mehmet.demir@kstu.edu.tr', '0262 555 0102', 1),
('Zeynep Kara', 'Dr. Öğr. Üyesi', 'zeynep.kara@kstu.edu.tr', '0262 555 0103', 1),
-- Yazılım Mühendisliği (2 hoca - 6 ders)
('Ayşe Kaya', 'Prof. Dr.', 'ayse.kaya@kstu.edu.tr', '0262 555 0201', 2),
('Fatma Şahin', 'Doç. Dr.', 'fatma.sahin@kstu.edu.tr', '0262 555 0202', 2),
-- Hemşirelik (2 hoca - 6 ders)
('Elif Yıldız', 'Prof. Dr.', 'elif.yildiz@kstu.edu.tr', '0262 555 0301', 3),
('Selin Arslan', 'Doç. Dr.', 'selin.arslan@kstu.edu.tr', '0262 555 0302', 3),
-- Fizyoterapi (2 hoca - 5 ders)
('Ali Öztürk', 'Prof. Dr.', 'ali.ozturk@kstu.edu.tr', '0262 555 0401', 4),
('Deniz Aydın', 'Doç. Dr.', 'deniz.aydin@kstu.edu.tr', '0262 555 0402', 4),
-- Psikoloji (2 hoca - 5 ders)
('Burak Koç', 'Prof. Dr.', 'burak.koc@kstu.edu.tr', '0262 555 0501', 5),
('Seda Yılmaz', 'Doç. Dr.', 'seda.yilmaz@kstu.edu.tr', '0262 555 0502', 5),
-- İşletme (2 hoca - 5 ders)
('Hakan Erdoğan', 'Prof. Dr.', 'hakan.erdogan@kstu.edu.tr', '0262 555 0601', 6),
('Canan Tekin', 'Doç. Dr.', 'canan.tekin@kstu.edu.tr', '0262 555 0602', 6),
-- Eczacılık (2 hoca - 5 ders)
('Selim Duman', 'Prof. Dr.', 'selim.duman@kstu.edu.tr', '0262 555 0701', 7),
('Aylin Kurt', 'Doç. Dr.', 'aylin.kurt@kstu.edu.tr', '0262 555 0702', 7),
-- Diş Hekimliği (1 hoca - 4 ders)
('Serkan Yücel', 'Prof. Dr.', 'serkan.yucel@kstu.edu.tr', '0262 555 0801', 8);

-- ==============================================
-- DERSLER (Artırılmış - 44 ders, 16 öğretmen)
-- ==============================================
INSERT OR IGNORE INTO courses (code, name, department_id, instructor_id, student_count, exam_duration, exam_type, needs_computer, has_exam) VALUES 
-- BİLGİSAYAR MÜHENDİSLİĞİ (8 ders - 3 hoca)
('BM101', 'Programlamaya Giriş', 1, 1, 65, 90, 'Yazılı', 1, 1),
('BM102', 'Matematik I', 1, 2, 70, 90, 'Yazılı', 0, 1),
('BM201', 'Veri Yapıları', 1, 1, 55, 90, 'Yazılı', 1, 1),
('BM202', 'Ayrık Matematik', 1, 2, 50, 60, 'Yazılı', 0, 1),
('BM301', 'Veritabanı Sistemleri', 1, 3, 45, 90, 'Yazılı', 1, 1),
('BM302', 'Algoritma Analizi', 1, 1, 48, 60, 'Yazılı', 0, 1),
('BM401', 'Yapay Zeka', 1, 2, 40, 90, 'Proje', 1, 1),
('BM402', 'Bilgisayar Ağları', 1, 3, 42, 60, 'Yazılı', 0, 1),

-- YAZILIM MÜHENDİSLİĞİ (6 ders - 2 hoca)
('YM101', 'Yazılım Mühendisliğine Giriş', 2, 4, 60, 60, 'Yazılı', 0, 1),
('YM102', 'Programlama Temelleri', 2, 5, 65, 90, 'Yazılı', 1, 1),
('YM201', 'Nesne Yönelimli Programlama', 2, 4, 55, 90, 'Yazılı', 1, 1),
('YM202', 'Web Programlama', 2, 5, 50, 60, 'Proje', 1, 1),
('YM301', 'Yazılım Tasarımı', 2, 4, 48, 60, 'Proje', 0, 1),
('YM302', 'Mobil Uygulama Geliştirme', 2, 5, 45, 60, 'Proje', 1, 1),

-- HEMŞİRELİK (6 ders - 2 hoca)
('HEM101', 'Hemşireliğe Giriş', 3, 6, 80, 60, 'Yazılı', 0, 1),
('HEM102', 'Anatomi', 3, 7, 85, 90, 'Yazılı', 0, 1),
('HEM201', 'Fizyoloji', 3, 6, 75, 90, 'Yazılı', 0, 1),
('HEM202', 'Temel Hemşirelik', 3, 7, 78, 60, 'Yazılı', 0, 1),
('HEM301', 'İç Hastalıkları Hemşireliği', 3, 6, 70, 60, 'Yazılı', 0, 1),
('HEM302', 'Cerrahi Hemşireliği', 3, 7, 72, 60, 'Yazılı', 0, 1),

-- FİZYOTERAPİ (5 ders - 2 hoca)
('FTR101', 'Fizyoterapiye Giriş', 4, 8, 55, 60, 'Yazılı', 0, 1),
('FTR102', 'Anatomi I', 4, 9, 60, 90, 'Yazılı', 0, 1),
('FTR201', 'Kinezyoloji', 4, 8, 52, 60, 'Yazılı', 0, 1),
('FTR202', 'Elektroterapi', 4, 9, 50, 60, 'Yazılı', 0, 1),
('FTR301', 'Ortopedik Rehabilitasyon', 4, 8, 48, 60, 'Yazılı', 0, 1),

-- PSİKOLOJİ (5 ders - 2 hoca)
('PSK101', 'Psikolojiye Giriş', 5, 10, 90, 60, 'Yazılı', 0, 1),
('PSK102', 'Sosyal Psikoloji', 5, 11, 85, 60, 'Yazılı', 0, 1),
('PSK201', 'Gelişim Psikolojisi', 5, 10, 80, 60, 'Yazılı', 0, 1),
('PSK202', 'Klinik Psikoloji', 5, 11, 75, 60, 'Yazılı', 0, 1),
('PSK301', 'Davranış Bozuklukları', 5, 10, 70, 60, 'Yazılı', 0, 1),

-- İŞLETME (5 ders - 2 hoca)
('ISL101', 'İşletme Bilimine Giriş', 6, 12, 95, 60, 'Yazılı', 0, 1),
('ISL102', 'Temel Ekonomi', 6, 13, 90, 60, 'Yazılı', 0, 1),
('ISL201', 'Muhasebe Prensipleri', 6, 12, 85, 90, 'Yazılı', 0, 1),
('ISL202', 'Pazarlama İlkeleri', 6, 13, 80, 60, 'Yazılı', 0, 1),
('ISL301', 'Finansal Yönetim', 6, 12, 75, 60, 'Yazılı', 0, 1),

-- ECZACILIK (5 ders - 2 hoca)
('ECZ101', 'Eczacılığa Giriş', 7, 14, 65, 60, 'Yazılı', 0, 1),
('ECZ102', 'Genel Kimya', 7, 15, 70, 90, 'Yazılı', 0, 1),
('ECZ201', 'Farmakoloji I', 7, 14, 62, 90, 'Yazılı', 0, 1),
('ECZ202', 'Biyokimya', 7, 15, 58, 60, 'Yazılı', 0, 1),
('ECZ301', 'Farmasötik Teknoloji', 7, 14, 55, 60, 'Yazılı', 0, 1),

-- DİŞ HEKİMLİĞİ (4 ders - 1 hoca)
('DHK101', 'Diş Hekimliğine Giriş', 8, 16, 55, 60, 'Yazılı', 0, 1),
('DHK102', 'Diş Anatomisi', 8, 16, 58, 90, 'Yazılı', 0, 1),
('DHK201', 'Periodontoloji', 8, 16, 52, 60, 'Yazılı', 0, 1),
('DHK202', 'Endodonti', 8, 16, 50, 60, 'Yazılı', 0, 1);

-- ==============================================
-- HOCA MÜSAİTLİKLERİ (Sınav Dönemi - Kısıtlı)
-- Her hoca farklı saatlerde 1-3 saatlik boşluklar
-- ==============================================
INSERT OR IGNORE INTO instructor_availability (instructor_id, day_of_week, start_time, end_time, is_available) VALUES 
-- Prof. Dr. Ahmet Yılmaz (BM) - Pazartesi 2 saat, Çarşamba 3 saat, Cuma 2 saat
(1, 'Pazartesi', '09:00', '11:00', 1),
(1, 'Çarşamba', '11:00', '14:00', 1),
(1, 'Cuma', '14:00', '16:00', 1),

-- Doç. Dr. Mehmet Demir (BM) - Salı 3 saat, Perşembe 2 saat
(2, 'Salı', '09:00', '12:00', 1),
(2, 'Perşembe', '14:00', '16:00', 1),

-- Dr. Öğr. Üyesi Zeynep Kara (BM) - Pazartesi 2 saat, Salı 1 saat, Perşembe 3 saat
(3, 'Pazartesi', '14:00', '16:00', 1),
(3, 'Salı', '14:00', '15:00', 1),
(3, 'Perşembe', '09:00', '12:00', 1),

-- Prof. Dr. Ayşe Kaya (YM) - Pazartesi 3 saat, Çarşamba 2 saat, Cuma 1 saat
(4, 'Pazartesi', '11:00', '14:00', 1),
(4, 'Çarşamba', '09:00', '11:00', 1),
(4, 'Cuma', '09:00', '10:00', 1),

-- Doç. Dr. Fatma Şahin (YM) - Salı 2 saat, Perşembe 3 saat
(5, 'Salı', '11:00', '13:00', 1),
(5, 'Perşembe', '11:00', '14:00', 1),

-- Prof. Dr. Elif Yıldız (HEM) - Pazartesi 2 saat, Çarşamba 2 saat, Cuma 2 saat
(6, 'Pazartesi', '09:00', '11:00', 1),
(6, 'Çarşamba', '14:00', '16:00', 1),
(6, 'Cuma', '11:00', '13:00', 1),

-- Doç. Dr. Selin Arslan (HEM) - Salı 3 saat, Perşembe 2 saat
(7, 'Salı', '09:00', '12:00', 1),
(7, 'Perşembe', '09:00', '11:00', 1),

-- Prof. Dr. Ali Öztürk (FTR) - Pazartesi 2 saat, Çarşamba 3 saat
(8, 'Pazartesi', '14:00', '16:00', 1),
(8, 'Çarşamba', '09:00', '12:00', 1),

-- Doç. Dr. Deniz Aydın (FTR) - Salı 2 saat, Cuma 3 saat
(9, 'Salı', '14:00', '16:00', 1),
(9, 'Cuma', '09:00', '12:00', 1),

-- Prof. Dr. Burak Koç (PSK) - Pazartesi 3 saat, Perşembe 2 saat
(10, 'Pazartesi', '09:00', '12:00', 1),
(10, 'Perşembe', '14:00', '16:00', 1),

-- Doç. Dr. Seda Yılmaz (PSK) - Salı 2 saat, Çarşamba 2 saat, Cuma 1 saat
(11, 'Salı', '09:00', '11:00', 1),
(11, 'Çarşamba', '11:00', '13:00', 1),
(11, 'Cuma', '14:00', '15:00', 1),

-- Prof. Dr. Hakan Erdoğan (ISL) - Pazartesi 2 saat, Salı 2 saat, Perşembe 2 saat
(12, 'Pazartesi', '11:00', '13:00', 1),
(12, 'Salı', '14:00', '16:00', 1),
(12, 'Perşembe', '09:00', '11:00', 1),

-- Doç. Dr. Canan Tekin (ISL) - Çarşamba 3 saat, Cuma 2 saat
(13, 'Çarşamba', '09:00', '12:00', 1),
(13, 'Cuma', '09:00', '11:00', 1),

-- Prof. Dr. Selim Duman (ECZ) - Pazartesi 2 saat, Çarşamba 2 saat, Perşembe 2 saat
(14, 'Pazartesi', '09:00', '11:00', 1),
(14, 'Çarşamba', '14:00', '16:00', 1),
(14, 'Perşembe', '11:00', '13:00', 1),

-- Doç. Dr. Aylin Kurt (ECZ) - Salı 3 saat, Cuma 2 saat
(15, 'Salı', '09:00', '12:00', 1),
(15, 'Cuma', '14:00', '16:00', 1),

-- Prof. Dr. Serkan Yücel (DHK) - Pazartesi 2 saat, Salı 2 saat, Çarşamba 2 saat, Perşembe 2 saat, Cuma 2 saat
(16, 'Pazartesi', '14:00', '16:00', 1),
(16, 'Salı', '11:00', '13:00', 1),
(16, 'Çarşamba', '09:00', '11:00', 1),
(16, 'Perşembe', '14:00', '16:00', 1),
(16, 'Cuma', '11:00', '13:00', 1);

-- ==============================================
-- ÖĞRENCİ VERİLERİ
-- ==============================================
-- 800+ öğrenci verisi students_data.sql dosyasından yüklenir
-- Bu dosya database.py tarafından otomatik olarak işlenir
-- ==============================================


