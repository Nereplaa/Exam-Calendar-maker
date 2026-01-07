-- ==============================================
-- MİGRASYON: Özel Sınıf Atama Özelliği
-- ==============================================
-- Bu dosya mevcut veritabanına özel sınıf atama
-- özelliği için gerekli alanları ekler.
-- ==============================================

-- Classrooms tablosuna classroom_type sütunu ekle
ALTER TABLE classrooms ADD COLUMN classroom_type TEXT DEFAULT 'Normal';

-- Courses tablosuna special_classroom_id sütunu ekle
ALTER TABLE courses ADD COLUMN special_classroom_id INTEGER REFERENCES classrooms(id);

-- Mevcut bilgisayarlı derslikleri 'Lab' olarak işaretle
UPDATE classrooms SET classroom_type = 'Lab' WHERE has_computer = 1;

-- Amfi dersliklerini işaretle (isimde AMFİ geçenler)
UPDATE classrooms SET classroom_type = 'Amfi' WHERE name LIKE '%AMF%';

