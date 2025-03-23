import unittest
from src.monerorequest.cron_validation import CronValidation

class TestCronValidation(unittest.TestCase):
    def test_valid_amount_of_arguments(self):
        with self.assertRaisesRegex(ValueError, 'Invalid Cron'):
            self.assertEqual(CronValidation('* * *').parse_cron())

    def test_valid_minutes(self):
        with self.subTest(i=0):
            self.assertEqual(CronValidation('* * * * *').valid_minutes(), True)
        for idx in range(59):
            with self.subTest(i=idx+1):
                self.assertEqual(CronValidation(f'{idx} * * * *').valid_minutes(), True)
        with self.subTest(i=61):
            self.assertEqual(CronValidation('a * * * *').valid_minutes(), False)

    def test_valid_hours(self):
        with self.subTest(i=0):
            self.assertEqual(CronValidation('* * * * *').valid_hours(), True)
        for idx in range(23):
            with self.subTest(i=idx+1):
                self.assertEqual(CronValidation(f'* {idx} * * *').valid_hours(), True)
        with self.subTest(i=25):
            self.assertEqual(CronValidation('* a * * *').valid_hours(), False)

    def test_valid_days(self):
        with self.subTest(i=0):
            self.assertEqual(CronValidation('* * * * *').valid_days(), True)
        for idx in range(1, 31):
            with self.subTest(i=idx+1):
                self.assertEqual(CronValidation(f'* * {idx} * *').valid_days(), True)
        with self.subTest(i=33):
            for special in CronValidation.day_special:
                self.assertEqual(CronValidation(f'* * {special} * *').valid_days(), True)
        with self.subTest(i=34):
            self.assertEqual(CronValidation('* * a * *').valid_days(), False)

    def test_valid_months(self):
        with self.subTest(i=0):
            self.assertEqual(CronValidation('* * * * *').valid_months(), True)
        for idx in range(1, 12):
            with self.subTest(i=idx+1):
                self.assertEqual(CronValidation(f'* * * {idx} *').valid_months(), True)
        for idx, month in enumerate(CronValidation.month_codes):
            with self.subTest(i=idx+13):
                self.assertEqual(CronValidation(f'* * * {month} *').valid_months(), True)
        with self.subTest(i=14):
            self.assertEqual(CronValidation('* * * a *').valid_months(), False)

    def test_valid_dow(self):
        with self.subTest(i=0):
            self.assertEqual(CronValidation('* * * * *').valid_dow(), True)
        for idx in range(0, 7):
            with self.subTest(i=idx+1):
                self.assertEqual(CronValidation(f'* * * * {idx}').valid_dow(), True)
        for idx, dow in enumerate(CronValidation.dow_codes):
            with self.subTest(i=idx+9):
                self.assertEqual(CronValidation(f'* * * * {dow}').valid_dow(), True)
        with self.subTest(i=14):
            self.assertEqual(CronValidation('* * * * a').valid_dow(), False)
