# ==============================================
# UYGULAMA BAŞLATICI
# ==============================================
# Bu dosya Flask uygulamasını çalıştırır.
# Terminal'de "python run.py" yazarak başlatılır.
# ==============================================

from app import create_app

# Flask uygulamasını oluştur
app = create_app()

# Eğer bu dosya doğrudan çalıştırılıyorsa
# (import edilmiyorsa)
if __name__ == '__main__':
    # Uygulamayı başlat
    # debug=True: Kod değişikliklerinde otomatik yeniden başlatır
    # host='127.0.0.1': Sadece bu bilgisayardan erişilebilir
    # port=5000: http://127.0.0.1:5000 adresinde çalışır
    print("=" * 50)
    print("🎓 Üniversite Sınav Programı Uygulaması")
    print("=" * 50)
    print("Uygulama başlatılıyor...")
    print("Tarayıcıda açın: http://127.0.0.1:5000")
    print("Durdurmak için: Ctrl+C")
    print("=" * 50)
    
    app.run(debug=True, host='127.0.0.1', port=5000)

