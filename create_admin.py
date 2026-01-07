# Admin kullanıcısı oluşturma scripti
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = 'database/sinav_programi.db'

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Admin şifresini hashle (werkzeug ile)
password = generate_password_hash('admin123')

# Admin kullanıcısını ekle
cur.execute('''
    INSERT OR REPLACE INTO users (id, username, password, email, full_name, role, is_active) 
    VALUES (1, 'admin', ?, 'admin@kostu.edu.tr', 'Sistem Yöneticisi', 'admin', 1)
''', (password,))

conn.commit()
conn.close()

print('✅ Admin hesabı oluşturuldu!')
print('   Kullanıcı adı: admin')
print('   Şifre: admin123')
