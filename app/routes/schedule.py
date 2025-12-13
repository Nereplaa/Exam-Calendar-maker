# ==============================================
# SINAV PROGRAMI ROTALARI
# ==============================================
# Bu dosya sınav programı görüntüleme ve
# otomatik planlama işlemlerini yönetir.
# ==============================================

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from datetime import datetime, timedelta

from app.models.exam import get_all_exams, delete_exam, delete_all_exams, get_exams_by_department
from app.models.department import get_all_departments
from app.scheduler import generate_exam_schedule, get_schedule_statistics
from app.export import export_to_pdf, export_to_excel

# Blueprint oluştur
bp = Blueprint('schedule', __name__, url_prefix='/schedule')


def check_admin():
    """Admin kontrolü."""
    if not session.get('user_id'):
        return False
    if session.get('role') != 'admin':
        return False
    return True


@bp.route('/view')
def view_schedule():
    """
    Sınav programını görüntüler.
    Tüm kullanıcılar görebilir.
    """
    # Giriş kontrolü
    if not session.get('user_id'):
        flash('Bu sayfayı görüntülemek için giriş yapmalısınız!', 'warning')
        return redirect(url_for('auth.login'))
    
    # Tüm sınavları getir
    exams = get_all_exams()
    
    # Bölümleri getir (filtreleme için)
    departments = get_all_departments()
    
    # İstatistikleri getir
    stats = get_schedule_statistics()
    
    return render_template('schedule/view.html', 
                           exams=exams, 
                           departments=departments,
                           stats=stats)


@bp.route('/view/department/<int:department_id>')
def view_by_department(department_id):
    """
    Bölüme göre sınav programını görüntüler.
    """
    # Giriş kontrolü
    if not session.get('user_id'):
        flash('Bu sayfayı görüntülemek için giriş yapmalısınız!', 'warning')
        return redirect(url_for('auth.login'))
    
    # Bölüme göre sınavları getir
    exams = get_exams_by_department(department_id)
    
    # Bölümleri getir
    departments = get_all_departments()
    
    # İstatistikleri getir
    stats = get_schedule_statistics()
    
    return render_template('schedule/view.html', 
                           exams=exams, 
                           departments=departments,
                           stats=stats,
                           selected_department=department_id)


@bp.route('/generate', methods=['GET', 'POST'])
def generate():
    """
    Otomatik sınav planlaması sayfası.
    Sadece admin erişebilir.
    """
    # Admin kontrolü
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Form gönderildi mi?
    if request.method == 'POST':
        # Tarihleri al
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        # Tarih kontrolü
        if not start_date or not end_date:
            flash('Başlangıç ve bitiş tarihi gereklidir!', 'error')
            return render_template('schedule/generate.html')
        
        # Tarihleri kontrol et
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start > end:
            flash('Başlangıç tarihi bitiş tarihinden sonra olamaz!', 'error')
            return render_template('schedule/generate.html')
        
        # Planlamayı çalıştır
        result = generate_exam_schedule(start_date, end_date)
        
        # Sonucu göster
        if result['failed_count'] == 0:
            flash('Tüm sınavlar başarıyla planlandı! (' + 
                  str(result['placed_count']) + ' sınav)', 'success')
        else:
            flash(str(result['placed_count']) + ' sınav planlandı, ' +
                  str(result['failed_count']) + ' sınav yerleştirilemedi.', 'warning')
        
        return redirect(url_for('schedule.view_schedule'))
    
    # Varsayılan tarihler (bugünden 2 hafta sonrasına)
    today = datetime.now()
    default_start = (today + timedelta(days=7)).strftime('%Y-%m-%d')
    default_end = (today + timedelta(days=21)).strftime('%Y-%m-%d')
    
    return render_template('schedule/generate.html',
                           default_start=default_start,
                           default_end=default_end)


@bp.route('/clear')
def clear_schedule():
    """
    Tüm sınav programını temizler.
    Sadece admin erişebilir.
    """
    # Admin kontrolü
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Tüm sınavları sil
    deleted_count = delete_all_exams()
    
    flash(str(deleted_count) + ' sınav kaydı silindi.', 'info')
    
    return redirect(url_for('schedule.view_schedule'))


@bp.route('/delete/<int:exam_id>')
def delete_single_exam(exam_id):
    """
    Tek bir sınavı siler.
    Sadece admin erişebilir.
    """
    # Admin kontrolü
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Sınavı sil
    success = delete_exam(exam_id)
    
    if success:
        flash('Sınav kaydı silindi.', 'success')
    else:
        flash('Silme sırasında hata oluştu!', 'error')
    
    return redirect(url_for('schedule.view_schedule'))


# ==============================================
# DIŞA AKTARMA (EXPORT) ROTALARI
# ==============================================

@bp.route('/export/pdf')
def export_pdf():
    """
    Sınav programını PDF olarak indirir.
    """
    # Giriş kontrolü
    if not session.get('user_id'):
        flash('Bu işlem için giriş yapmalısınız!', 'warning')
        return redirect(url_for('auth.login'))
    
    # PDF oluştur
    file_path = export_to_pdf()
    
    # Dosyayı indir
    return send_file(
        file_path,
        as_attachment=True,
        download_name='sinav_programi.pdf',
        mimetype='application/pdf'
    )


@bp.route('/export/excel')
def export_excel():
    """
    Sınav programını Excel olarak indirir.
    """
    # Giriş kontrolü
    if not session.get('user_id'):
        flash('Bu işlem için giriş yapmalısınız!', 'warning')
        return redirect(url_for('auth.login'))
    
    # Excel oluştur
    file_path = export_to_excel()
    
    # Dosyayı indir
    return send_file(
        file_path,
        as_attachment=True,
        download_name='sinav_programi.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

