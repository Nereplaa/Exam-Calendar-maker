# ==============================================
# KİMLİK DOĞRULAMA ROTALARI (AUTH)
# ==============================================
# Bu dosya giriş, kayıt ve çıkış işlemlerini yönetir.
# Kullanıcı oturumu (session) burada kontrol edilir.
# ==============================================

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import get_user_by_id, create_user, check_user_password
from app.database import execute_query

# Blueprint oluştur
# Blueprint = Flask'ta modüler yapı için kullanılır
# 'auth' = bu modülün adı
# url_prefix = tüm URL'lerin başına '/auth' ekler
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Giriş sayfası.
    
    GET: Giriş formunu gösterir
    POST: Giriş bilgilerini kontrol eder
    """
    # Eğer zaten giriş yapmışsa, panele yönlendir
    if session.get('user_id'):
        return redirect(url_for('auth.dashboard'))
    
    # Form gönderildi mi? (POST isteği)
    if request.method == 'POST':
        # Form verilerini al
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Boş alan kontrolü
        if not username or not password:
            flash('Kullanıcı adı ve şifre gereklidir!', 'error')
            return render_template('auth/login.html')
        
        # Kullanıcıyı kontrol et
        user = check_user_password(username, password)
        
        # Giriş başarılı mı?
        if user is not None:
            # Session'a kullanıcı bilgilerini kaydet
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            
            # Başarı mesajı göster
            flash('Giriş başarılı! Hoş geldiniz, ' + user['full_name'], 'success')
            
            # Panele yönlendir
            return redirect(url_for('auth.dashboard'))
        else:
            # Hata mesajı göster
            flash('Kullanıcı adı veya şifre hatalı!', 'error')
    
    # Giriş sayfasını göster
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Kayıt sayfası.
    
    GET: Kayıt formunu gösterir
    POST: Yeni kullanıcı oluşturur
    """
    # Eğer zaten giriş yapmışsa, panele yönlendir
    if session.get('user_id'):
        return redirect(url_for('auth.dashboard'))
    
    # Bölümleri getir (kayıt formunda seçim için)
    departments = execute_query("SELECT * FROM departments ORDER BY name")
    
    # Form gönderildi mi? (POST isteği)
    if request.method == 'POST':
        # Form verilerini al
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        department_id = request.form.get('department_id')
        
        # Boş alan kontrolü
        if not username or not password or not email or not full_name:
            flash('Tüm alanları doldurunuz!', 'error')
            return render_template('auth/register.html', departments=departments)
        
        # Şifre uzunluğu kontrolü
        if len(password) < 6:
            flash('Şifre en az 6 karakter olmalıdır!', 'error')
            return render_template('auth/register.html', departments=departments)
        
        # Şifre eşleşme kontrolü
        if password != password_confirm:
            flash('Şifreler eşleşmiyor!', 'error')
            return render_template('auth/register.html', departments=departments)
        
        # E-posta formatı kontrolü (basit)
        if '@' not in email:
            flash('Geçerli bir e-posta adresi giriniz!', 'error')
            return render_template('auth/register.html', departments=departments)
        
        # Department ID'yi integer'a çevir (boşsa None yap)
        if department_id:
            department_id = int(department_id)
        else:
            department_id = None
        
        # Kullanıcı oluştur (varsayılan rol: ogrenci)
        new_user_id = create_user(
            username=username,
            password=password,
            email=email,
            full_name=full_name,
            role='ogrenci',  # Yeni kayıtlar öğrenci olarak başlar
            department_id=department_id
        )
        
        # Başarılı mı?
        if new_user_id is not None:
            flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Bu kullanıcı adı veya e-posta zaten kullanılıyor!', 'error')
    
    # Kayıt sayfasını göster
    return render_template('auth/register.html', departments=departments)


@bp.route('/logout')
def logout():
    """
    Çıkış işlemi.
    
    Session'daki tüm bilgileri temizler.
    """
    # Session'ı temizle
    session.clear()
    
    # Mesaj göster
    flash('Çıkış yapıldı.', 'info')
    
    # Ana sayfaya yönlendir
    return redirect(url_for('index'))


@bp.route('/dashboard')
def dashboard():
    """
    Kullanıcı paneli.
    
    Role göre farklı içerik gösterir.
    """
    # Giriş yapmış mı kontrol et
    if not session.get('user_id'):
        flash('Bu sayfayı görüntülemek için giriş yapmalısınız!', 'warning')
        return redirect(url_for('auth.login'))
    
    # Kullanıcı bilgilerini al
    user = get_user_by_id(session['user_id'])
    
    # Kullanıcı bulunamadıysa (silinmiş olabilir)
    if user is None:
        session.clear()
        flash('Kullanıcı bulunamadı!', 'error')
        return redirect(url_for('auth.login'))
    
    # Role göre istatistikleri al
    stats = get_dashboard_stats(user['role'])
    
    # Panel sayfasını göster
    return render_template('auth/dashboard.html', user=user, stats=stats)


def get_dashboard_stats(role):
    """
    Dashboard için istatistikleri getirir.
    
    Parametreler:
        role: Kullanıcının rolü
    
    Döndürür:
        stats: İstatistik dictionary'si
    """
    stats = {}
    
    # Fakülte sayısı
    result = execute_query("SELECT COUNT(*) as count FROM faculties")
    stats['faculty_count'] = result[0]['count']
    
    # Bölüm sayısı
    result = execute_query("SELECT COUNT(*) as count FROM departments")
    stats['department_count'] = result[0]['count']
    
    # Ders sayısı
    result = execute_query("SELECT COUNT(*) as count FROM courses")
    stats['course_count'] = result[0]['count']
    
    # Derslik sayısı
    result = execute_query("SELECT COUNT(*) as count FROM classrooms")
    stats['classroom_count'] = result[0]['count']
    
    # Öğretim üyesi sayısı
    result = execute_query("SELECT COUNT(*) as count FROM instructors")
    stats['instructor_count'] = result[0]['count']
    
    # Planlanan sınav sayısı
    result = execute_query("SELECT COUNT(*) as count FROM exam_schedule")
    stats['exam_count'] = result[0]['count']
    
    # Kullanıcı sayısı (sadece admin için)
    if role == 'admin':
        result = execute_query("SELECT COUNT(*) as count FROM users")
        stats['user_count'] = result[0]['count']
    
    return stats

