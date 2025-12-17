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
    create_instructor, update_instructor, delete_instructor,
    get_instructors_by_department
)
from app.models.course import (
    get_all_courses, get_course_by_id,
    create_course, update_course, delete_course,
    get_courses_by_department
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
from app.models.student import (
    get_all_students, get_student_by_id, get_students_by_department,
    get_student_courses, get_student_count, get_departments_with_student_count
)

# Blueprint oluştur
bp = Blueprint('admin', __name__, url_prefix='/admin')


def check_logged_in():
    """
    Kullanıcının giriş yapıp yapmadığını kontrol eder.
    
    Döndürür:
        is_logged_in: Giriş yapmış mı? (True/False)
    """
    # Giriş yapmış mı?
    if not session.get('user_id'):
        return False
    return True


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


def check_admin_or_department_manager():
    """
    Kullanıcının admin veya bölüm yetkilisi olup olmadığını kontrol eder.
    
    Döndürür:
        has_access: Admin veya bölüm yetkilisi mi? (True/False)
    """
    # Giriş yapmış mı?
    if not session.get('user_id'):
        return False
    
    # Rolü kontrol et
    role = session.get('role')
    
    # Admin veya bölüm yetkilisi mi?
    if role == 'admin' or role == 'bolum_yetkili':
        return True
    
    return False


def get_user_department_id():
    """
    Giriş yapan kullanıcının bölüm ID'sini döndürür.
    
    Döndürür:
        department_id: Bölüm ID veya None
    """
    # Kullanıcı bilgisini al
    user_id = session.get('user_id')
    
    if not user_id:
        return None
    
    # Kullanıcıyı getir
    user = get_user_by_id(user_id)
    
    if not user:
        return None
    
    # sqlite3.Row objesi dictionary key access kullanır
    return user['department_id'] if 'department_id' in user.keys() else None


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
    # Admin veya bölüm yetkilisi mi kontrol et
    if not check_admin_or_department_manager():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcının rolünü kontrol et
    role = session.get('role')
    
    # Admin ise tüm öğretim üyelerini göster
    if role == 'admin':
        instructors = get_all_instructors()
    else:
        # Bölüm yetkilisi ise sadece kendi bölümündekileri göster
        user_dept_id = get_user_department_id()
        if user_dept_id:
            instructors = get_instructors_by_department(user_dept_id)
        else:
            instructors = []
    
    return render_template('admin/instructors.html', instructors=instructors)


@bp.route('/instructors/add', methods=['GET', 'POST'])
def instructor_add():
    """Yeni öğretim üyesi ekleme sayfası."""
    # Admin veya bölüm yetkilisi mi kontrol et
    if not check_admin_or_department_manager():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcının rolünü kontrol et
    role = session.get('role')
    user_dept_id = get_user_department_id()
    
    # Admin ise tüm bölümleri göster, değilse sadece kendi bölümünü
    if role == 'admin':
        departments = get_all_departments()
    else:
        # Bölüm yetkilisi sadece kendi bölümünü görür
        from app.models.department import get_department_by_id
        dept = get_department_by_id(user_dept_id)
        departments = [dept] if dept else []
    
    if request.method == 'POST':
        name = request.form.get('name')
        title = request.form.get('title')
        email = request.form.get('email')
        phone = request.form.get('phone')
        department_id = request.form.get('department_id')
        
        # Bölüm yetkilisi sadece kendi bölümüne ekleyebilir
        if role != 'admin' and int(department_id) != user_dept_id:
            flash('Sadece kendi bölümünüze öğretim üyesi ekleyebilirsiniz!', 'error')
            return render_template('admin/instructor_form.html', 
                                   instructor=None, departments=departments)
        
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
    # Admin veya bölüm yetkilisi mi kontrol et
    if not check_admin_or_department_manager():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcının rolünü kontrol et
    role = session.get('role')
    user_dept_id = get_user_department_id()
    
    instructor = get_instructor_by_id(instructor_id)
    
    if not instructor:
        flash('Öğretim üyesi bulunamadı!', 'error')
        return redirect(url_for('admin.instructors_list'))
    
    # Bölüm yetkilisi sadece kendi bölümündeki hocaları düzenleyebilir
    if role != 'admin' and instructor['department_id'] != user_dept_id:
        flash('Bu öğretim üyesini düzenleme yetkiniz yok!', 'error')
        return redirect(url_for('admin.instructors_list'))
    
    # Admin ise tüm bölümleri göster, değilse sadece kendi bölümünü
    if role == 'admin':
        departments = get_all_departments()
    else:
        from app.models.department import get_department_by_id
        dept = get_department_by_id(user_dept_id)
        departments = [dept] if dept else []
    
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
    # Admin veya bölüm yetkilisi mi kontrol et
    if not check_admin_or_department_manager():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcının rolünü kontrol et
    role = session.get('role')
    user_dept_id = get_user_department_id()
    
    # Bölüm yetkilisi sadece kendi bölümündeki hocaları silebilir
    if role != 'admin':
        instructor = get_instructor_by_id(instructor_id)
        if instructor and instructor['department_id'] != user_dept_id:
            flash('Bu öğretim üyesini silme yetkiniz yok!', 'error')
            return redirect(url_for('admin.instructors_list'))
    
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
    # Admin veya bölüm yetkilisi mi kontrol et
    if not check_admin_or_department_manager():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcının rolünü kontrol et
    role = session.get('role')
    
    # Admin ise tüm dersleri göster
    if role == 'admin':
        courses = get_all_courses()
    else:
        # Bölüm yetkilisi ise sadece kendi bölümünün derslerini göster
        user_dept_id = get_user_department_id()
        if user_dept_id:
            courses = get_courses_by_department(user_dept_id)
        else:
            courses = []
    
    return render_template('admin/courses.html', courses=courses)


@bp.route('/courses/add', methods=['GET', 'POST'])
def course_add():
    """Yeni ders ekleme sayfası."""
    # Admin veya bölüm yetkilisi mi kontrol et
    if not check_admin_or_department_manager():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcının rolünü kontrol et
    role = session.get('role')
    user_dept_id = get_user_department_id()
    
    # Admin ise tüm bölümleri ve hocaları göster
    if role == 'admin':
        departments = get_all_departments()
        instructors = get_all_instructors()
    else:
        # Bölüm yetkilisi sadece kendi bölümünü görür
        from app.models.department import get_department_by_id
        dept = get_department_by_id(user_dept_id)
        departments = [dept] if dept else []
        instructors = get_instructors_by_department(user_dept_id) if user_dept_id else []
    
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
        
        # Bölüm yetkilisi sadece kendi bölümüne ders ekleyebilir
        if role != 'admin' and int(department_id) != user_dept_id:
            flash('Sadece kendi bölümünüze ders ekleyebilirsiniz!', 'error')
            return render_template('admin/course_form.html', 
                                   course=None, departments=departments, 
                                   instructors=instructors)
        
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
    # Admin veya bölüm yetkilisi mi kontrol et
    if not check_admin_or_department_manager():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcının rolünü kontrol et
    role = session.get('role')
    user_dept_id = get_user_department_id()
    
    course = get_course_by_id(course_id)
    
    if not course:
        flash('Ders bulunamadı!', 'error')
        return redirect(url_for('admin.courses_list'))
    
    # Bölüm yetkilisi sadece kendi bölümündeki dersleri düzenleyebilir
    if role != 'admin' and course['department_id'] != user_dept_id:
        flash('Bu dersi düzenleme yetkiniz yok!', 'error')
        return redirect(url_for('admin.courses_list'))
    
    # Admin ise tüm bölümleri ve hocaları göster
    if role == 'admin':
        departments = get_all_departments()
        instructors = get_all_instructors()
    else:
        from app.models.department import get_department_by_id
        dept = get_department_by_id(user_dept_id)
        departments = [dept] if dept else []
        instructors = get_instructors_by_department(user_dept_id) if user_dept_id else []
    
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
    # Admin veya bölüm yetkilisi mi kontrol et
    if not check_admin_or_department_manager():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcının rolünü kontrol et
    role = session.get('role')
    user_dept_id = get_user_department_id()
    
    # Bölüm yetkilisi sadece kendi bölümündeki dersleri silebilir
    if role != 'admin':
        course = get_course_by_id(course_id)
        if course and course['department_id'] != user_dept_id:
            flash('Bu dersi silme yetkiniz yok!', 'error')
            return redirect(url_for('admin.courses_list'))
    
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
    # Admin veya bölüm yetkilisi mi kontrol et
    if not check_admin_or_department_manager():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcının rolünü kontrol et
    role = session.get('role')
    
    # Admin ise tüm müsaitlikleri göster
    if role == 'admin':
        availability = get_all_availability_with_instructor()
        instructors = get_all_instructors()
    else:
        # Bölüm yetkilisi ise sadece kendi bölümündeki hocaların müsaitliklerini göster
        user_dept_id = get_user_department_id()
        # Tüm müsaitlikleri al ve filtrele
        all_availability = get_all_availability_with_instructor()
        availability = []
        for item in all_availability:
            if item['department_id'] == user_dept_id:
                availability.append(item)
        instructors = get_instructors_by_department(user_dept_id) if user_dept_id else []
    
    # Instructor filtresi
    selected_instructor = request.args.get('instructor', type=int)
    if selected_instructor:
        availability = [item for item in availability if item['instructor_id'] == selected_instructor]
    
    # Takvim verisi hazırla - gün ve saate göre
    # Her müsaitlik kaydını tüm kapsadığı saatlere genişlet
    calendar_data = {}
    for item in availability:
        day = item['day_of_week']
        # Başlangıç ve bitiş saatlerini al
        start_hour = int(item['start_time'].split(':')[0])
        end_hour = int(item['end_time'].split(':')[0])
        
        # Her saat için kayıt ekle
        for hour in range(start_hour, end_hour):
            if day not in calendar_data:
                calendar_data[day] = {}
            
            if hour not in calendar_data[day]:
                calendar_data[day][hour] = []
            
            # Bu saatte bu hocanın kaydı var mı kontrol et
            already_exists = False
            for existing in calendar_data[day][hour]:
                if existing['id'] == item['id']:
                    already_exists = True
                    break
            
            if not already_exists:
                calendar_data[day][hour].append({
                    'id': item['id'],
                    'instructor_id': item['instructor_id'],
                    'instructor_name': item['instructor_name'],
                    'start_time': item['start_time'],
                    'end_time': item['end_time'],
                    'is_available': item['is_available']
                })
    
    return render_template('admin/availability.html', 
                          availability=availability,
                          instructors=instructors,
                          calendar_data=calendar_data,
                          selected_instructor=selected_instructor)


@bp.route('/availability/add', methods=['GET', 'POST'])
def availability_add():
    """Yeni müsaitlik ekleme sayfası."""
    # Admin veya bölüm yetkilisi mi kontrol et
    if not check_admin_or_department_manager():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcının rolünü kontrol et
    role = session.get('role')
    user_dept_id = get_user_department_id()
    
    # Admin ise tüm hocaları göster
    if role == 'admin':
        instructors = get_all_instructors()
    else:
        # Bölüm yetkilisi sadece kendi bölümündeki hocaları görür
        instructors = get_instructors_by_department(user_dept_id) if user_dept_id else []
    
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


@bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def user_edit(user_id):
    """
    Kullanıcı rol düzenleme sayfası.
    Sadece admin erişebilir.
    """
    # Admin kontrolü
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    # Kullanıcıyı getir
    user = get_user_by_id(user_id)
    
    if not user:
        flash('Kullanıcı bulunamadı!', 'error')
        return redirect(url_for('admin.users_list'))
    
    # Bölümleri getir
    departments = get_all_departments()
    
    # Form gönderildi mi?
    if request.method == 'POST':
        # Form verilerini al
        new_role = request.form.get('role')
        new_department_id = request.form.get('department_id')
        
        # Department ID'yi integer'a çevir
        if new_department_id:
            new_department_id = int(new_department_id)
        else:
            new_department_id = None
        
        # Kendini admin'den düşürmeye çalışıyorsa engelle
        if user_id == session.get('user_id') and new_role != 'admin':
            flash('Kendi admin yetkilerinizi kaldıramazsınız!', 'error')
            return render_template('admin/user_role_form.html', 
                                   user=user, departments=departments)
        
        # Kullanıcıyı güncelle
        success = update_user(
            user_id, 
            user['full_name'], 
            user['email'], 
            new_role, 
            new_department_id, 
            user['is_active']
        )
        
        if success:
            flash('Kullanıcı rolü başarıyla güncellendi!', 'success')
            return redirect(url_for('admin.users_list'))
        else:
            flash('Güncelleme sırasında hata oluştu!', 'error')
    
    return render_template('admin/user_role_form.html', 
                           user=user, departments=departments)


# ==============================================
# ÖĞRENCİ YÖNETİMİ
# ==============================================

@bp.route('/students')
def students_list():
    """Öğrenci yönetimi sayfası."""
    if not check_admin():
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('auth.login'))
    
    departments = get_departments_with_student_count()
    total_students = get_student_count()
    
    return render_template('admin/students.html',
                           departments=departments,
                           total_students=total_students)


@bp.route('/students/department/<int:department_id>')
def students_by_department(department_id):
    """Bölüme göre öğrenci listesi (JSON)."""
    if not check_admin():
        return {'error': 'Yetkisiz erişim'}, 403
    
    students = get_students_by_department(department_id)
    
    # sqlite3.Row'ları dict'e çevir
    students_list = []
    for s in students:
        students_list.append({
            'id': s['id'],
            'student_no': s['student_no'],
            'name': s['name'],
            'email': s['email'],
            'phone': s['phone'] if 'phone' in s.keys() else None,
            'grade': s['grade'] if 'grade' in s.keys() else 1,
            'department_name': s['department_name']
        })
    
    return {'students': students_list}


@bp.route('/students/<int:student_id>')
def student_detail(student_id):
    """Öğrenci detayı (JSON)."""
    if not check_admin():
        return {'error': 'Yetkisiz erişim'}, 403
    
    student = get_student_by_id(student_id)
    
    if not student:
        return {'error': 'Öğrenci bulunamadı'}, 404
    
    courses = get_student_courses(student_id)
    
    # sqlite3.Row'ları dict'e çevir
    student_dict = {
        'id': student['id'],
        'student_no': student['student_no'],
        'tc_no': student['tc_no'] if 'tc_no' in student.keys() else None,
        'name': student['name'],
        'email': student['email'],
        'phone': student['phone'] if 'phone' in student.keys() else None,
        'address': student['address'] if 'address' in student.keys() else None,
        'birth_date': student['birth_date'] if 'birth_date' in student.keys() else None,
        'grade': student['grade'] if 'grade' in student.keys() else 1,
        'department_name': student['department_name']
    }
    
    courses_list = []
    for c in courses:
        courses_list.append({
            'id': c['id'],
            'code': c['code'],
            'name': c['name'],
            'instructor_name': c['instructor_name'] if 'instructor_name' in c.keys() else None
        })
    
    return {'student': student_dict, 'courses': courses_list}


@bp.route('/students/<int:student_id>/update', methods=['POST'])
def student_update(student_id):
    """Öğrenci günceller (JSON)."""
    if not check_admin():
        return {'error': 'Yetkisiz erişim'}, 403
    
    from app.database import execute_update
    
    data = request.get_json()
    
    if not data:
        return {'error': 'Veri bulunamadı'}, 400
    
    try:
        query = """
            UPDATE students SET
                name = ?,
                tc_no = ?,
                email = ?,
                phone = ?,
                birth_date = ?,
                grade = ?,
                address = ?
            WHERE id = ?
        """
        
        execute_update(query, (
            data.get('name'),
            data.get('tc_no'),
            data.get('email'),
            data.get('phone'),
            data.get('birth_date'),
            data.get('grade'),
            data.get('address'),
            student_id
        ))
        
        return {'success': True}
    
    except Exception as e:
        return {'error': str(e)}, 500


