# ==============================================
# ADMİN ROTALARI
# ==============================================
# Bu dosya admin paneli için CRUD işlemlerini yönetir.
# Fakülte, Bölüm, Öğretim Üyesi, Ders yönetimi.
# ==============================================

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# Model importları
from app.models.faculty import (
    get_all_faculties, get_faculty_by_id, 
    create_faculty, update_faculty, delete_faculty
)
from app.models.department import (
    get_all_departments, get_department_by_id,
    create_department, update_department, delete_department
)
from app.models.instructor import (
    get_all_instructors, get_instructor_by_id,
    create_instructor, update_instructor, delete_instructor
)
from app.models.course import (
    get_all_courses, get_course_by_id,
    create_course, update_course, delete_course
)
from app.models.classroom import (
    get_all_classrooms, get_classroom_by_id,
    create_classroom, update_classroom, delete_classroom
)
from app.models.availability import (
    get_availability_by_instructor, get_availability_by_id,
    create_availability, update_availability, delete_availability,
    get_all_availability_with_instructor
)
from app.models.user import get_all_users, get_user_by_id, delete_user, update_user

# Blueprint oluştur
bp = Blueprint('admin', __name__, url_prefix='/admin')


def check_admin():
    """
    Kullanıcının admin olup olmadığını kontrol eder.
    
    Döndürür:
        is_admin: Admin mi? (True/False)
    """
    # Giriş yapmış mı?
    if not session.get('user_id'):
        return False
    
    # Admin mi?
    if session.get('role') != 'admin':
        return False
    
    return True


# ==============================================
# FAKÜLTE YÖNETİMİ
# ==============================================

@bp.route('/faculties')
def faculties_list():
    """Fakülte listesi sayfası."""
    # Admin kontrolü
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Fakülteleri getir
    faculties = get_all_faculties()
    
    return render_template('admin/faculties.html', faculties=faculties)


@bp.route('/faculties/add', methods=['GET', 'POST'])
def faculty_add():
    """Yeni fakülte ekleme sayfası."""
    # Admin kontrolü
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Form gönderildi mi?
    if request.method == 'POST':
        # Form verilerini al
        name = request.form.get('name')
        code = request.form.get('code')
        
        # Boş alan kontrolü
        if not name or not code:
            flash('Tüm alanları doldurunuz!', 'error')
            return render_template('admin/faculty_form.html', faculty=None)
        
        # Fakülte oluştur
        new_id = create_faculty(name, code)
        
        if new_id:
            flash('Fakülte başarıyla eklendi!', 'success')
            return redirect(url_for('admin.faculties_list'))
        else:
            flash('Bu fakülte adı veya kodu zaten mevcut!', 'error')
    
    return render_template('admin/faculty_form.html', faculty=None)


@bp.route('/faculties/edit/<int:faculty_id>', methods=['GET', 'POST'])
def faculty_edit(faculty_id):
    """Fakülte düzenleme sayfası."""
    # Admin kontrolü
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Fakülteyi getir
    faculty = get_faculty_by_id(faculty_id)
    
    if not faculty:
        flash('Fakülte bulunamadı!', 'error')
        return redirect(url_for('admin.faculties_list'))
    
    # Form gönderildi mi?
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        
        if not name or not code:
            flash('Tüm alanları doldurunuz!', 'error')
            return render_template('admin/faculty_form.html', faculty=faculty)
        
        # Fakülteyi güncelle
        success = update_faculty(faculty_id, name, code)
        
        if success:
            flash('Fakülte başarıyla güncellendi!', 'success')
            return redirect(url_for('admin.faculties_list'))
        else:
            flash('Güncelleme sırasında hata oluştu!', 'error')
    
    return render_template('admin/faculty_form.html', faculty=faculty)


@bp.route('/faculties/delete/<int:faculty_id>')
def faculty_delete(faculty_id):
    """Fakülte silme işlemi."""
    # Admin kontrolü
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Fakülteyi sil
    success = delete_faculty(faculty_id)
    
    if success:
        flash('Fakülte başarıyla silindi!', 'success')
    else:
        flash('Bu fakülteye bağlı bölümler var, önce onları silin!', 'error')
    
    return redirect(url_for('admin.faculties_list'))


# ==============================================
# BÖLÜM YÖNETİMİ
# ==============================================

@bp.route('/departments')
def departments_list():
    """Bölüm listesi sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    departments = get_all_departments()
    return render_template('admin/departments.html', departments=departments)


@bp.route('/departments/add', methods=['GET', 'POST'])
def department_add():
    """Yeni bölüm ekleme sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    faculties = get_all_faculties()
    
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        faculty_id = request.form.get('faculty_id')
        
        if not name or not code or not faculty_id:
            flash('Tüm alanları doldurunuz!', 'error')
            return render_template('admin/department_form.html', 
                                   department=None, faculties=faculties)
        
        new_id = create_department(name, code, int(faculty_id))
        
        if new_id:
            flash('Bölüm başarıyla eklendi!', 'success')
            return redirect(url_for('admin.departments_list'))
        else:
            flash('Bu bölüm adı zaten mevcut!', 'error')
    
    return render_template('admin/department_form.html', 
                           department=None, faculties=faculties)


@bp.route('/departments/edit/<int:department_id>', methods=['GET', 'POST'])
def department_edit(department_id):
    """Bölüm düzenleme sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    department = get_department_by_id(department_id)
    faculties = get_all_faculties()
    
    if not department:
        flash('Bölüm bulunamadı!', 'error')
        return redirect(url_for('admin.departments_list'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        faculty_id = request.form.get('faculty_id')
        
        if not name or not code or not faculty_id:
            flash('Tüm alanları doldurunuz!', 'error')
            return render_template('admin/department_form.html', 
                                   department=department, faculties=faculties)
        
        success = update_department(department_id, name, code, int(faculty_id))
        
        if success:
            flash('Bölüm başarıyla güncellendi!', 'success')
            return redirect(url_for('admin.departments_list'))
        else:
            flash('Güncelleme sırasında hata oluştu!', 'error')
    
    return render_template('admin/department_form.html', 
                           department=department, faculties=faculties)


@bp.route('/departments/delete/<int:department_id>')
def department_delete(department_id):
    """Bölüm silme işlemi."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    success = delete_department(department_id)
    
    if success:
        flash('Bölüm başarıyla silindi!', 'success')
    else:
        flash('Bu bölüme bağlı dersler var, önce onları silin!', 'error')
    
    return redirect(url_for('admin.departments_list'))


# ==============================================
# ÖĞRETİM ÜYESİ YÖNETİMİ
# ==============================================

@bp.route('/instructors')
def instructors_list():
    """Öğretim üyesi listesi sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    instructors = get_all_instructors()
    return render_template('admin/instructors.html', instructors=instructors)


@bp.route('/instructors/add', methods=['GET', 'POST'])
def instructor_add():
    """Yeni öğretim üyesi ekleme sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    departments = get_all_departments()
    
    if request.method == 'POST':
        name = request.form.get('name')
        title = request.form.get('title')
        email = request.form.get('email')
        phone = request.form.get('phone')
        department_id = request.form.get('department_id')
        
        if not name or not department_id:
            flash('Ad ve bölüm alanları zorunludur!', 'error')
            return render_template('admin/instructor_form.html', 
                                   instructor=None, departments=departments)
        
        new_id = create_instructor(name, title, email, phone, int(department_id))
        
        if new_id:
            flash('Öğretim üyesi başarıyla eklendi!', 'success')
            return redirect(url_for('admin.instructors_list'))
        else:
            flash('Bu e-posta adresi zaten mevcut!', 'error')
    
    return render_template('admin/instructor_form.html', 
                           instructor=None, departments=departments)


@bp.route('/instructors/edit/<int:instructor_id>', methods=['GET', 'POST'])
def instructor_edit(instructor_id):
    """Öğretim üyesi düzenleme sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    instructor = get_instructor_by_id(instructor_id)
    departments = get_all_departments()
    
    if not instructor:
        flash('Öğretim üyesi bulunamadı!', 'error')
        return redirect(url_for('admin.instructors_list'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        title = request.form.get('title')
        email = request.form.get('email')
        phone = request.form.get('phone')
        department_id = request.form.get('department_id')
        
        if not name or not department_id:
            flash('Ad ve bölüm alanları zorunludur!', 'error')
            return render_template('admin/instructor_form.html', 
                                   instructor=instructor, departments=departments)
        
        success = update_instructor(instructor_id, name, title, email, phone, int(department_id))
        
        if success:
            flash('Öğretim üyesi başarıyla güncellendi!', 'success')
            return redirect(url_for('admin.instructors_list'))
        else:
            flash('Güncelleme sırasında hata oluştu!', 'error')
    
    return render_template('admin/instructor_form.html', 
                           instructor=instructor, departments=departments)


@bp.route('/instructors/delete/<int:instructor_id>')
def instructor_delete(instructor_id):
    """Öğretim üyesi silme işlemi."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    success = delete_instructor(instructor_id)
    
    if success:
        flash('Öğretim üyesi başarıyla silindi!', 'success')
    else:
        flash('Bu öğretim üyesine bağlı dersler var, önce onları silin!', 'error')
    
    return redirect(url_for('admin.instructors_list'))


# ==============================================
# DERS YÖNETİMİ
# ==============================================

@bp.route('/courses')
def courses_list():
    """Ders listesi sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    courses = get_all_courses()
    return render_template('admin/courses.html', courses=courses)


@bp.route('/courses/add', methods=['GET', 'POST'])
def course_add():
    """Yeni ders ekleme sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    departments = get_all_departments()
    instructors = get_all_instructors()
    
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        department_id = request.form.get('department_id')
        instructor_id = request.form.get('instructor_id')
        student_count = request.form.get('student_count', 0)
        exam_duration = request.form.get('exam_duration', 60)
        exam_type = request.form.get('exam_type', 'Yazılı')
        needs_computer = 1 if request.form.get('needs_computer') else 0
        has_exam = 1 if request.form.get('has_exam') else 0
        
        if not code or not name or not department_id or not instructor_id:
            flash('Zorunlu alanları doldurunuz!', 'error')
            return render_template('admin/course_form.html', 
                                   course=None, departments=departments, 
                                   instructors=instructors)
        
        new_id = create_course(
            code, name, int(department_id), int(instructor_id),
            int(student_count), int(exam_duration), exam_type,
            needs_computer, has_exam
        )
        
        if new_id:
            flash('Ders başarıyla eklendi!', 'success')
            return redirect(url_for('admin.courses_list'))
        else:
            flash('Bu ders kodu zaten mevcut!', 'error')
    
    return render_template('admin/course_form.html', 
                           course=None, departments=departments, 
                           instructors=instructors)


@bp.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
def course_edit(course_id):
    """Ders düzenleme sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    course = get_course_by_id(course_id)
    departments = get_all_departments()
    instructors = get_all_instructors()
    
    if not course:
        flash('Ders bulunamadı!', 'error')
        return redirect(url_for('admin.courses_list'))
    
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        department_id = request.form.get('department_id')
        instructor_id = request.form.get('instructor_id')
        student_count = request.form.get('student_count', 0)
        exam_duration = request.form.get('exam_duration', 60)
        exam_type = request.form.get('exam_type', 'Yazılı')
        needs_computer = 1 if request.form.get('needs_computer') else 0
        has_exam = 1 if request.form.get('has_exam') else 0
        
        if not code or not name or not department_id or not instructor_id:
            flash('Zorunlu alanları doldurunuz!', 'error')
            return render_template('admin/course_form.html', 
                                   course=course, departments=departments, 
                                   instructors=instructors)
        
        success = update_course(
            course_id, code, name, int(department_id), int(instructor_id),
            int(student_count), int(exam_duration), exam_type,
            needs_computer, has_exam
        )
        
        if success:
            flash('Ders başarıyla güncellendi!', 'success')
            return redirect(url_for('admin.courses_list'))
        else:
            flash('Güncelleme sırasında hata oluştu!', 'error')
    
    return render_template('admin/course_form.html', 
                           course=course, departments=departments, 
                           instructors=instructors)


@bp.route('/courses/delete/<int:course_id>')
def course_delete(course_id):
    """Ders silme işlemi."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    success = delete_course(course_id)
    
    if success:
        flash('Ders başarıyla silindi!', 'success')
    else:
        flash('Bu derse ait sınav planı var, önce onu silin!', 'error')
    
    return redirect(url_for('admin.courses_list'))


# ==============================================
# DERSLİK YÖNETİMİ
# ==============================================

@bp.route('/classrooms')
def classrooms_list():
    """Derslik listesi sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    classrooms = get_all_classrooms()
    return render_template('admin/classrooms.html', classrooms=classrooms)


@bp.route('/classrooms/add', methods=['GET', 'POST'])
def classroom_add():
    """Yeni derslik ekleme sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        building = request.form.get('building')
        capacity = request.form.get('capacity', 0)
        has_computer = 1 if request.form.get('has_computer') else 0
        is_available = 1 if request.form.get('is_available') else 0
        
        if not name or not capacity:
            flash('Derslik adı ve kapasite zorunludur!', 'error')
            return render_template('admin/classroom_form.html', classroom=None)
        
        new_id = create_classroom(name, building, int(capacity), has_computer, is_available)
        
        if new_id:
            flash('Derslik başarıyla eklendi!', 'success')
            return redirect(url_for('admin.classrooms_list'))
        else:
            flash('Bu derslik adı zaten mevcut!', 'error')
    
    return render_template('admin/classroom_form.html', classroom=None)


@bp.route('/classrooms/edit/<int:classroom_id>', methods=['GET', 'POST'])
def classroom_edit(classroom_id):
    """Derslik düzenleme sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    classroom = get_classroom_by_id(classroom_id)
    
    if not classroom:
        flash('Derslik bulunamadı!', 'error')
        return redirect(url_for('admin.classrooms_list'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        building = request.form.get('building')
        capacity = request.form.get('capacity', 0)
        has_computer = 1 if request.form.get('has_computer') else 0
        is_available = 1 if request.form.get('is_available') else 0
        
        if not name or not capacity:
            flash('Derslik adı ve kapasite zorunludur!', 'error')
            return render_template('admin/classroom_form.html', classroom=classroom)
        
        success = update_classroom(classroom_id, name, building, int(capacity), 
                                   has_computer, is_available)
        
        if success:
            flash('Derslik başarıyla güncellendi!', 'success')
            return redirect(url_for('admin.classrooms_list'))
        else:
            flash('Güncelleme sırasında hata oluştu!', 'error')
    
    return render_template('admin/classroom_form.html', classroom=classroom)


@bp.route('/classrooms/delete/<int:classroom_id>')
def classroom_delete(classroom_id):
    """Derslik silme işlemi."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    success = delete_classroom(classroom_id)
    
    if success:
        flash('Derslik başarıyla silindi!', 'success')
    else:
        flash('Bu dersliğe ait sınav planı var, önce onu silin!', 'error')
    
    return redirect(url_for('admin.classrooms_list'))


# ==============================================
# MÜSAİTLİK YÖNETİMİ
# ==============================================

@bp.route('/availability')
def availability_list():
    """Müsaitlik listesi sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    availability = get_all_availability_with_instructor()
    return render_template('admin/availability.html', availability=availability)


@bp.route('/availability/add', methods=['GET', 'POST'])
def availability_add():
    """Yeni müsaitlik ekleme sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    instructors = get_all_instructors()
    
    if request.method == 'POST':
        instructor_id = request.form.get('instructor_id')
        day_of_week = request.form.get('day_of_week')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        is_available = 1 if request.form.get('is_available') else 0
        
        if not instructor_id or not day_of_week or not start_time or not end_time:
            flash('Tüm alanları doldurunuz!', 'error')
            return render_template('admin/availability_form.html', 
                                   availability=None, instructors=instructors)
        
        new_id = create_availability(int(instructor_id), day_of_week, 
                                     start_time, end_time, is_available)
        
        if new_id:
            flash('Müsaitlik kaydı başarıyla eklendi!', 'success')
            return redirect(url_for('admin.availability_list'))
        else:
            flash('Ekleme sırasında hata oluştu!', 'error')
    
    return render_template('admin/availability_form.html', 
                           availability=None, instructors=instructors)


@bp.route('/availability/delete/<int:availability_id>')
def availability_delete(availability_id):
    """Müsaitlik kaydı silme işlemi."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    success = delete_availability(availability_id)
    
    if success:
        flash('Müsaitlik kaydı başarıyla silindi!', 'success')
    else:
        flash('Silme sırasında hata oluştu!', 'error')
    
    return redirect(url_for('admin.availability_list'))


# ==============================================
# KULLANICI YÖNETİMİ
# ==============================================

@bp.route('/users')
def users_list():
    """Kullanıcı listesi sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    users = get_all_users()
    return render_template('admin/users.html', users=users)


@bp.route('/users/delete/<int:user_id>')
def user_delete(user_id):
    """Kullanıcı silme (pasif yapma) işlemi."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kendini silmeye çalışıyorsa engelle
    if user_id == session.get('user_id'):
        flash('Kendinizi silemezsiniz!', 'error')
        return redirect(url_for('admin.users_list'))
    
    success = delete_user(user_id)
    
    if success:
        flash('Kullanıcı pasif yapıldı!', 'success')
    else:
        flash('Silme sırasında hata oluştu!', 'error')
    
    return redirect(url_for('admin.users_list'))


@bp.route('/users/activate/<int:user_id>')
def user_activate(user_id):
    """Kullanıcıyı aktif yapar."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcıyı bul
    user = get_user_by_id(user_id)
    
    if user:
        # Aktif yap
        success = update_user(user_id, user['full_name'], user['email'], 
                             user['role'], user['department_id'], is_active=1)
        if success:
            flash('Kullanıcı aktif edildi!', 'success')
    
    return redirect(url_for('admin.users_list'))

