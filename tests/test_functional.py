import os
import sys
import importlib
import unittest
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import config


class ExamAppTest(unittest.TestCase):
    """Uygulamanın temel işlevlerini test eder."""

    @classmethod
    def setUpClass(cls):
        """Test veritabanını hazırlar ve modülleri yükler."""
        config.DATABASE_PATH = os.path.join(
            config.BASE_DIR,
            'database',
            'test_sinav_programi.db'
        )

        if os.path.exists(config.DATABASE_PATH):
            os.remove(config.DATABASE_PATH)

        import app.database as database
        importlib.reload(database)
        database.init_database()
        database.load_seed_data()

        cls.database = database

        import app.models.course as course_model
        importlib.reload(course_model)
        cls.course_model = course_model

        import app.models.exam as exam_model
        importlib.reload(exam_model)
        cls.exam_model = exam_model

        import app.models.classroom as classroom_model
        importlib.reload(classroom_model)
        cls.classroom_model = classroom_model

        import app.models.availability as availability_model
        importlib.reload(availability_model)
        cls.availability_model = availability_model

        import app.scheduler as scheduler
        importlib.reload(scheduler)
        cls.scheduler = scheduler

    @classmethod
    def tearDownClass(cls):
        """Test veritabanını temizler."""
        if os.path.exists(config.DATABASE_PATH):
            os.remove(config.DATABASE_PATH)

    def setUp(self):
        """Her testten önce planlanmış sınavları temizler."""
        self.exam_model.delete_all_exams()

    def test_admin_password_is_hashed(self):
        """Admin şifresinin hashlenip hashlenmediğini kontrol eder."""
        rows = self.database.execute_query(
            "SELECT password FROM users WHERE username = 'admin'"
        )
        hashed_password = rows[0]['password']
        self.assertTrue(
            hashed_password != 'admin123',
            "Admin şifresi düz metin olarak saklanıyor."
        )
        self.assertIn(':', hashed_password, "Admin şifresi hash formatında değil.")

    def test_generate_exam_days_skips_weekend(self):
        """Hafta sonunun planlamadan çıkarıldığını kontrol eder."""
        days = self.scheduler.generate_exam_days('2025-01-04', '2025-01-10')

        for day_item in days:
            date_text = day_item[0]
            date_value = datetime.strptime(date_text, '%Y-%m-%d')
            weekday = date_value.weekday()
            self.assertLess(
                weekday,
                5,
                "Hafta sonu planlama listesine eklendi."
            )

        self.assertGreater(
            len(days),
            0,
            "Hiç çalışma günü oluşturulamadı."
        )

    def test_schedule_creates_exams_for_all_courses(self):
        """Planlamanın tüm sınavları yerleştirdiğini kontrol eder."""
        start_date = '2025-01-06'
        end_date = '2025-01-17'

        result = self.scheduler.generate_exam_schedule(start_date, end_date)
        courses = self.course_model.get_courses_with_exam()
        exams = self.exam_model.get_all_exams()

        self.assertEqual(
            result['total_courses'],
            len(courses),
            "Toplam ders sayısı beklenen ile uyuşmuyor."
        )
        self.assertEqual(
            result['failed_count'],
            0,
            "Planlanamayan dersler var."
        )
        self.assertEqual(
            len(exams),
            len(courses),
            "Planlanan sınav sayısı ders sayısıyla uyuşmuyor."
        )

    def test_schedule_respects_capacity_and_conflicts(self):
        """Kapasite, çakışma ve hoca müsaitliğini kontrol eder."""
        start_date = '2025-01-06'
        end_date = '2025-01-17'
        self.scheduler.generate_exam_schedule(start_date, end_date)

        exams = self.exam_model.get_all_exams()
        day_names = [
            'Pazartesi',
            'Salı',
            'Çarşamba',
            'Perşembe',
            'Cuma',
            'Cumartesi',
            'Pazar'
        ]

        for exam in exams:
            self.assertLessEqual(
                exam['student_count'],
                exam['classroom_capacity'],
                "Derslik kapasitesi aşıldı."
            )

            date_value = datetime.strptime(exam['exam_date'], '%Y-%m-%d')
            weekday = date_value.weekday()
            self.assertLess(weekday, 5, "Hafta sonu sınavı oluşturuldu.")

            day_name = day_names[weekday]
            course = self.course_model.get_course_by_id(exam['course_id'])
            instructor_id = course['instructor_id']
            is_available = self.availability_model.check_instructor_available(
                instructor_id,
                day_name,
                '09:00',
                '18:00'
            )
            self.assertTrue(
                is_available,
                "Müsait olmayan hocaya sınav atandı."
            )

        for i in range(len(exams)):
            for j in range(i + 1, len(exams)):
                exam_a = exams[i]
                exam_b = exams[j]

                same_day = exam_a['exam_date'] == exam_b['exam_date']

                if same_day:
                    if exam_a['classroom_id'] == exam_b['classroom_id']:
                        overlap = self._time_overlaps(exam_a, exam_b)
                        self.assertFalse(
                            overlap,
                            "Aynı derslikte çakışan sınavlar var."
                        )

                    course_a = self.course_model.get_course_by_id(
                        exam_a['course_id']
                    )
                    course_b = self.course_model.get_course_by_id(
                        exam_b['course_id']
                    )

                    if course_a['instructor_id'] == course_b['instructor_id']:
                        overlap = self._time_overlaps(exam_a, exam_b)
                        self.assertFalse(
                            overlap,
                            "Aynı hocada çakışan sınavlar var."
                        )

    def _time_overlaps(self, exam_a, exam_b):
        """İki sınav saatinin çakışıp çakışmadığını kontrol eder."""
        start_a = exam_a['start_time']
        end_a = exam_a['end_time']
        start_b = exam_b['start_time']
        end_b = exam_b['end_time']

        if start_a <= start_b and end_a > start_b:
            return True

        if start_a < end_b and end_a >= end_b:
            return True

        if start_a >= start_b and end_a <= end_b:
            return True

        return False


if __name__ == '__main__':
    unittest.main()

