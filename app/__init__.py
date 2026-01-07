# ==============================================
# FLASK UYGULAMASI BAŞLATICI
# ==============================================
# Bu dosya Flask uygulamasını oluşturur ve
# yapılandırır. Tüm route'lar buradan bağlanır.
# ==============================================

from flask import Flask
import os
import sys

# Config dosyasını import edebilmek için yolu ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SECRET_KEY


def create_app():
    """
    Flask uygulamasını oluşturur ve yapılandırır.
    
    Bu fonksiyon 'Factory Pattern' kullanır.
    Yani uygulamayı bir fonksiyon içinde oluştururuz.
    
    Döndürür:
        app: Yapılandırılmış Flask uygulaması
    """
    # Flask uygulamasını oluştur
    # __name__ = bu dosyanın adı (Python'a uygulamanın nerede olduğunu söyler)
    app = Flask(__name__)
    
    # Gizli anahtarı ayarla (session güvenliği için)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # Template klasörünün yolunu ayarla
    template_folder = os.path.join(os.path.dirname(__file__), 'templates')
    app.template_folder = template_folder
    
    # Static dosyaların yolunu ayarla (CSS, JS, resimler)
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    app.static_folder = static_folder
    
    # Jinja filter: Unvanları kaldırarak sadece isim göster
    import re
    @app.template_filter('strip_title')
    def strip_title_filter(name):
        """
        Hoca isminden unvanı kaldırır.
        Örnek: "Dr. Öğr. Üyesi ELİF PINAR HACIBEYOĞLU" -> "ELİF PINAR HACIBEYOĞLU"
        """
        if not name:
            return name
        # Unvan kalıplarını kaldır
        pattern = r'^(Prof\.|Doç\.|Dr\.|Öğr\.Gör\.|Öğr\.)\s*(Dr\.)?\s*(Öğr\.)?\s*(Gör\.)?\s*(Üyesi)?\s*'
        cleaned = re.sub(pattern, '', name).strip()
        return cleaned if cleaned else name
    
    # Veritabanını başlat
    from app.database import init_database, load_seed_data
    init_database()
    
    # Örnek verileri yükle (ilk çalıştırmada)
    load_seed_data()
    
    # Ana sayfa route'u
    @app.route('/')
    def index():
        """
        Ana sayfa.
        Kullanıcıyı karşılayan ilk sayfa.
        """
        from flask import render_template
        return render_template('index.html')
    
    # ==============================================
    # ROUTE'LARI KAYDET
    # ==============================================
    
    # Auth (Kimlik Doğrulama) route'ları
    from app.routes import auth
    app.register_blueprint(auth.bp)
    
    # Admin route'ları
    from app.routes import admin
    app.register_blueprint(admin.bp)
    
    # Schedule (Sınav Programı) route'ları
    from app.routes import schedule
    app.register_blueprint(schedule.bp)
    
    # Kısayol route'ları (/login, /logout, /register, /dashboard)
    # Bu sayede kullanıcılar /auth/login yerine /login yazabilir
    @app.route('/login')
    def login_redirect():
        """Login sayfasına kısayol."""
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))
    
    @app.route('/logout')
    def logout_redirect():
        """Logout işlemine kısayol."""
        from flask import redirect, url_for
        return redirect(url_for('auth.logout'))
    
    @app.route('/register')
    def register_redirect():
        """Register sayfasına kısayol."""
        from flask import redirect, url_for
        return redirect(url_for('auth.register'))
    
    @app.route('/dashboard')
    def dashboard_redirect():
        """Dashboard sayfasına kısayol."""
        from flask import redirect, url_for
        return redirect(url_for('auth.dashboard'))
    
    return app

