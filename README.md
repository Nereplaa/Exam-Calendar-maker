# 🎓 Üniversite Sınav Programı Hazırlama Uygulaması

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> **Kocaeli Sağlık ve Teknoloji Üniversitesi**  
> **Yazılım Lab I - Proje 2**  
> **2025-2026 Güz Dönemi**

Bir üniversitede dönem sonu veya ara sınavlarının **otomatik olarak planlanması** ve **dersliklere yerleştirilmesi** işlemini yapan web tabanlı uygulama.

---

## 📸 Ekran Görüntüleri

<details>
<summary>🖼️ Ekran görüntülerini görmek için tıkla</summary>

### Ana Sayfa
- Modern ve kullanıcı dostu arayüz
- Özellikler ve nasıl çalışır bölümleri

### Admin Paneli
- İstatistik kartları
- Hızlı erişim menüsü
- Role göre özelleştirilmiş içerik

### Sınav Programı
- Tablo görünümü
- Bölüm bazlı filtreleme
- PDF ve Excel export

</details>

---

## ✨ Özellikler

### 👥 Kullanıcı Yönetimi
- 4 farklı kullanıcı rolü (Admin, Bölüm Yetkilisi, Hoca, Öğrenci)
- Güvenli giriş sistemi (şifre hashleme)
- Session tabanlı oturum yönetimi

### 🏛️ Veri Yönetimi
- Fakülte, Bölüm, Ders, Derslik CRUD işlemleri
- Öğretim üyesi yönetimi
- Hoca müsaitlik bilgileri girişi

### 🤖 Otomatik Planlama
- Greedy (açgözlü) algoritma ile akıllı yerleştirme
- Çakışma kontrolü (derslik, hoca, öğrenci)
- Kapasite ve müsaitlik kontrolü
- Bilgisayarlı derslik desteği

### 📊 Raporlama
- Sınav programı görüntüleme
- Bölüm bazlı filtreleme
- PDF olarak dışa aktarma
- Excel olarak dışa aktarma

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### Adım Adım Kurulum

1. **Projeyi klonlayın:**
```bash
git clone https://github.com/KULLANICI_ADI/sinav-programi.git
cd sinav-programi
```

2. **Sanal ortam oluşturun (opsiyonel ama önerilir):**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Uygulamayı başlatın:**
```bash
python run.py
```

5. **Tarayıcıda açın:**
```
http://127.0.0.1:5000
```

---

## 🔐 Varsayılan Giriş Bilgileri

| Kullanıcı | Şifre | Rol |
|-----------|-------|-----|
| admin | admin123 | Sistem Yöneticisi |

> ⚠️ **Güvenlik:** Gerçek kullanımda varsayılan şifreyi değiştirin!

---

## 📁 Proje Yapısı

```
sinav-programi/
├── app/
│   ├── __init__.py          # Flask uygulaması fabrikası
│   ├── database.py          # Veritabanı işlemleri
│   ├── scheduler.py         # Otomatik planlama algoritması
│   ├── export.py            # PDF/Excel dışa aktarma
│   │
│   ├── models/              # Veritabanı modelleri
│   │   ├── user.py          # Kullanıcı işlemleri
│   │   ├── faculty.py       # Fakülte işlemleri
│   │   ├── department.py    # Bölüm işlemleri
│   │   ├── instructor.py    # Öğretim üyesi işlemleri
│   │   ├── course.py        # Ders işlemleri
│   │   ├── classroom.py     # Derslik işlemleri
│   │   ├── availability.py  # Müsaitlik işlemleri
│   │   └── exam.py          # Sınav planı işlemleri
│   │
│   ├── routes/              # URL rotaları
│   │   ├── auth.py          # Giriş/Kayıt/Çıkış
│   │   ├── admin.py         # Admin paneli
│   │   └── schedule.py      # Sınav programı
│   │
│   ├── templates/           # HTML şablonları
│   │   ├── base.html        # Ana şablon
│   │   ├── index.html       # Ana sayfa
│   │   ├── auth/            # Giriş/Kayıt sayfaları
│   │   ├── admin/           # Admin sayfaları
│   │   └── schedule/        # Sınav programı sayfaları
│   │
│   └── static/              # Statik dosyalar
│       ├── css/style.css    # Stiller
│       └── js/main.js       # JavaScript
│
├── database/
│   ├── schema.sql           # Veritabanı şeması (10 tablo)
│   └── seed.sql             # Örnek veriler
│
├── exports/                 # Dışa aktarılan dosyalar
├── config.py                # Uygulama ayarları
├── requirements.txt         # Python bağımlılıkları
├── run.py                   # Uygulama başlatıcı
└── README.md                # Bu dosya
```

---

## 🗄️ Veritabanı Şeması

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   faculties  │────>│  departments │────>│   courses    │
└──────────────┘     └──────────────┘     └──────────────┘
                            │                    │
                            ▼                    ▼
                     ┌──────────────┐     ┌──────────────┐
                     │  instructors │────>│ exam_schedule│
                     └──────────────┘     └──────────────┘
                            │                    │
                            ▼                    ▼
                     ┌──────────────┐     ┌──────────────┐
                     │ availability │     │  classrooms  │
                     └──────────────┘     └──────────────┘
```

### Tablolar
| Tablo | Açıklama |
|-------|----------|
| users | Kullanıcılar (admin, hoca, öğrenci) |
| faculties | Fakülteler |
| departments | Bölümler |
| instructors | Öğretim üyeleri |
| courses | Dersler |
| classrooms | Derslikler |
| instructor_availability | Hoca müsaitlikleri |
| exam_schedule | Sınav programı |
| students | Öğrenciler (opsiyonel) |
| student_courses | Öğrenci-ders ilişkisi |

---

## 🤖 Planlama Algoritması

Uygulama **Greedy (Açgözlü)** algoritma kullanır:

```
1. Dersleri öğrenci sayısına göre sırala (büyükten küçüğe)
2. Her ders için:
   ├── Sınav günlerini tara (hafta içi)
   ├── Hoca müsait mi? kontrol et
   ├── Saat dilimlerini tara (09:00-18:00)
   ├── Hoca bu saatte başka sınavda mı?
   ├── Uygun derslik bul (kapasite ≥ öğrenci)
   ├── Derslik bu saatte boş mu?
   └── Uygunsa yerleştir!
3. Sonucu raporla
```

### Kısıtlamalar
- ✅ Bir derslikte aynı anda tek sınav
- ✅ Bir hoca aynı anda tek sınavda
- ✅ Derslik kapasitesi ≥ öğrenci sayısı
- ✅ Hocanın müsait olduğu günler
- ✅ Bilgisayarlı derslik gereksinimi
- ✅ Hafta sonu sınav yapılmaz

---

## 📱 API Endpoints

| Metod | Endpoint | Açıklama |
|-------|----------|----------|
| GET | `/` | Ana sayfa |
| GET/POST | `/login` | Giriş |
| GET/POST | `/register` | Kayıt |
| GET | `/logout` | Çıkış |
| GET | `/dashboard` | Panel |
| GET | `/admin/faculties` | Fakülte listesi |
| GET | `/admin/departments` | Bölüm listesi |
| GET | `/admin/instructors` | Hoca listesi |
| GET | `/admin/courses` | Ders listesi |
| GET | `/admin/classrooms` | Derslik listesi |
| GET | `/schedule/view` | Sınav programı |
| POST | `/schedule/generate` | Otomatik planlama |
| GET | `/schedule/export/pdf` | PDF indir |
| GET | `/schedule/export/excel` | Excel indir |

---

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Versiyon | Kullanım Amacı |
|-----------|----------|----------------|
| Python | 3.11 | Backend programlama |
| Flask | 3.0.0 | Web framework |
| SQLite | 3 | Veritabanı |
| Jinja2 | 3.1 | Template engine |
| Werkzeug | 3.0.1 | Şifre hashleme |
| ReportLab | 4.0.7 | PDF oluşturma |
| OpenPyXL | 3.1.2 | Excel oluşturma |

---

## 📝 Değerlendirme Kriterleri

| Kriter | Puan | Durum |
|--------|------|-------|
| Kod Kalitesi | 20 | ✅ |
| Veritabanı Tasarımı | 20 | ✅ |
| Fonksiyonel Doğru Çalışma | 25 | ✅ |
| Arayüz | 15 | ✅ |
| Sunum Kalitesi | 10 | ⏳ |
| Kullanıcı Dostu | 10 | ✅ |
| **TOPLAM** | **100** | |

---

## 👥 Ekip

| İsim | Görev |
|------|-------|
| [İsim 1] | Backend Geliştirme |
| [İsim 2] | Frontend Geliştirme |
| [İsim 3] | Veritabanı & Test |

---

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

---

## 🙏 Teşekkürler

- Kocaeli Sağlık ve Teknoloji Üniversitesi
- Yazılım Lab I Dersi Hocalarımız

---

<p align="center">
  <b>🎓 2025 - Kocaeli Sağlık ve Teknoloji Üniversitesi</b>
</p>

