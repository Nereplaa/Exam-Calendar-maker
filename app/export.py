# ==============================================
# DIŞA AKTARMA (EXPORT) MODÜLÜ
# ==============================================
# Bu dosya sınav programını PDF ve Excel
# formatlarında dışa aktarma işlemlerini yapar.
# ==============================================

import os
from datetime import datetime

# PDF oluşturma için
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Excel oluşturma için
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

from app.models.exam import get_all_exams


def get_export_folder():
    """
    Export klasörünün yolunu döndürür.
    Klasör yoksa oluşturur.
    """
    # Proje klasörünü bul
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Export klasörü
    export_folder = os.path.join(base_dir, 'exports')
    
    # Klasör yoksa oluştur
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    
    return export_folder


def export_to_pdf():
    """
    Sınav programını PDF olarak dışa aktarır.
    
    Döndürür:
        file_path: Oluşturulan PDF dosyasının yolu
    """
    # Sınavları al
    exams = get_all_exams()
    
    # Dosya adını oluştur
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = 'sinav_programi_' + timestamp + '.pdf'
    
    # Dosya yolunu oluştur
    export_folder = get_export_folder()
    file_path = os.path.join(export_folder, filename)
    
    # Türkçe karakter desteği için font kaydet
    # Windows'ta Arial veya başka TTF font kullan
    font_registered = False
    font_name = 'Helvetica'  # Varsayılan
    font_name_bold = 'Helvetica-Bold'
    
    # DejaVuSans fontunu dene (eğer varsa)
    try:
        # Proje klasöründe fonts klasörü oluştur ve oradan oku
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(base_dir, 'fonts', 'DejaVuSans.ttf')
        font_path_bold = os.path.join(base_dir, 'fonts', 'DejaVuSans-Bold.ttf')
        
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
            if os.path.exists(font_path_bold):
                pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path_bold))
                font_name_bold = 'DejaVuSans-Bold'
            font_name = 'DejaVuSans'
            font_registered = True
    except:
        pass
    
    # Windows Arial fontunu dene
    if not font_registered:
        try:
            # Windows Arial font yolu
            arial_path = 'C:/Windows/Fonts/arial.ttf'
            arial_bold_path = 'C:/Windows/Fonts/arialbd.ttf'
            
            if os.path.exists(arial_path):
                pdfmetrics.registerFont(TTFont('Arial', arial_path))
                if os.path.exists(arial_bold_path):
                    pdfmetrics.registerFont(TTFont('Arial-Bold', arial_bold_path))
                    font_name_bold = 'Arial-Bold'
                font_name = 'Arial'
                font_registered = True
        except:
            pass
    
    # PDF belgesi oluştur (yatay A4)
    doc = SimpleDocTemplate(
        file_path,
        pagesize=landscape(A4),
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm
    )
    
    # Stil ayarları
    styles = getSampleStyleSheet()
    
    # Başlık stili
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=font_name_bold if font_registered else 'Helvetica-Bold',
        fontSize=18,
        alignment=1,  # Ortalı
        spaceAfter=20
    )
    
    # Alt başlık stili
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontName=font_name if font_registered else 'Helvetica',
        fontSize=10,
        alignment=1,
        spaceAfter=30
    )
    
    # İçerik listesi
    elements = []
    
    # Başlık ekle
    title = Paragraph("SINAV PROGRAMI", title_style)
    elements.append(title)
    
    # Alt başlık (tarih)
    today = datetime.now().strftime('%d.%m.%Y')
    subtitle = Paragraph("Olusturulma Tarihi: " + today, subtitle_style)
    elements.append(subtitle)
    
    # Sınav verisi yoksa
    if len(exams) == 0:
        no_data_style = ParagraphStyle(
            'NoData',
            parent=styles['Normal'],
            fontName=font_name if font_registered else 'Helvetica'
        )
        no_data = Paragraph("Henuz planlanmis sinav bulunmamaktadir.", no_data_style)
        elements.append(no_data)
    else:
        # Tablo verilerini hazırla
        table_data = []
        
        # Başlık satırı
        headers = ['Tarih', 'Saat', 'Ders Kodu', 'Ders Adi', 'Bolum', 'Ogretim Uyesi', 'Derslik', 'Ogrenci']
        table_data.append(headers)
        
        # Veri satırları
        for exam in exams:
            # Türkçe karakterleri temizle (font yoksa)
            course_name = exam['course_name']
            department_name = exam['department_name']
            instructor_name = exam['instructor_name']
            
            if not font_registered:
                # Türkçe karakterleri ASCII'ye çevir
                tr_chars = {'ı': 'i', 'İ': 'I', 'ğ': 'g', 'Ğ': 'G', 
                           'ü': 'u', 'Ü': 'U', 'ş': 's', 'Ş': 'S',
                           'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C'}
                for tr, en in tr_chars.items():
                    course_name = course_name.replace(tr, en)
                    department_name = department_name.replace(tr, en)
                    instructor_name = instructor_name.replace(tr, en)
            
            row = [
                exam['exam_date'],
                exam['start_time'] + '-' + exam['end_time'],
                exam['course_code'],
                course_name,
                department_name,
                instructor_name,
                exam['classroom_name'],
                str(exam['student_count'])
            ]
            table_data.append(row)
        
        # Tablo oluştur
        table = Table(table_data, repeatRows=1)
        
        # Tablo stili
        table_style = TableStyle([
            # Başlık satırı
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), font_name_bold if font_registered else 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Tüm hücreler
            ('FONTNAME', (0, 1), (-1, -1), font_name if font_registered else 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Kenarlıklar
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            
            # Alternatif satır renkleri
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ])
        
        table.setStyle(table_style)
        elements.append(table)
    
    # PDF'i oluştur
    doc.build(elements)
    
    return file_path


def export_to_excel():
    """
    Sınav programını Excel olarak dışa aktarır.
    
    Döndürür:
        file_path: Oluşturulan Excel dosyasının yolu
    """
    # Sınavları al
    exams = get_all_exams()
    
    # Dosya adını oluştur
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = 'sinav_programi_' + timestamp + '.xlsx'
    
    # Dosya yolunu oluştur
    export_folder = get_export_folder()
    file_path = os.path.join(export_folder, filename)
    
    # Excel çalışma kitabı oluştur
    workbook = Workbook()
    
    # Aktif sayfa
    sheet = workbook.active
    sheet.title = "Sınav Programı"
    
    # Sütun genişlikleri
    column_widths = {
        'A': 12,  # Tarih
        'B': 12,  # Saat
        'C': 12,  # Ders Kodu
        'D': 30,  # Ders Adı
        'E': 25,  # Bölüm
        'F': 20,  # Öğretim Üyesi
        'G': 10,  # Derslik
        'H': 10,  # Öğrenci
    }
    
    for col, width in column_widths.items():
        sheet.column_dimensions[col].width = width
    
    # Stiller
    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill(start_color='2563eb', end_color='2563eb', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center')
    
    cell_alignment = Alignment(horizontal='center', vertical='center')
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Başlık satırı
    headers = ['Tarih', 'Saat', 'Ders Kodu', 'Ders Adı', 'Bölüm', 'Öğretim Üyesi', 'Derslik', 'Öğrenci']
    
    for col_num, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col_num, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = thin_border
    
    # Veri satırları
    for row_num, exam in enumerate(exams, 2):
        # Tarih
        sheet.cell(row=row_num, column=1, value=exam['exam_date'])
        
        # Saat
        time_str = exam['start_time'] + '-' + exam['end_time']
        sheet.cell(row=row_num, column=2, value=time_str)
        
        # Ders Kodu
        sheet.cell(row=row_num, column=3, value=exam['course_code'])
        
        # Ders Adı
        sheet.cell(row=row_num, column=4, value=exam['course_name'])
        
        # Bölüm
        sheet.cell(row=row_num, column=5, value=exam['department_name'])
        
        # Öğretim Üyesi
        sheet.cell(row=row_num, column=6, value=exam['instructor_name'])
        
        # Derslik
        sheet.cell(row=row_num, column=7, value=exam['classroom_name'])
        
        # Öğrenci Sayısı
        sheet.cell(row=row_num, column=8, value=exam['student_count'])
        
        # Hücre stilleri
        for col_num in range(1, 9):
            cell = sheet.cell(row=row_num, column=col_num)
            cell.alignment = cell_alignment
            cell.border = thin_border
            
            # Alternatif satır rengi
            if row_num % 2 == 0:
                cell.fill = PatternFill(start_color='f8fafc', end_color='f8fafc', fill_type='solid')
    
    # Dosyayı kaydet
    workbook.save(file_path)
    
    return file_path

