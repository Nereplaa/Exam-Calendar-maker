# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from app.export import get_departments, get_exams_by_department

print('Bolumler:')
depts = get_departments()
for d in depts[:3]:
    print(f"  - {d['id']}: {d['name']}")

print()
print('Ilk bolumun sinavlari:')
if depts:
    exams = get_exams_by_department(depts[0]['id'])
    print(f"Toplam {len(exams)} sinav")
    for e in exams[:5]:
        print(f"  - {e['exam_date']} {e['start_time']} - {e['course_code']}")

