import unittest
import datetime
from monerorequest import make_random_payment_id, convert_datetime_object_to_truncated_RFC3339_timestamp_format,\
                          decode_monero_payment_request, make_monero_payment_request, CronValidation, RequestV1, RequestV2

class TestMoneroRequest(unittest.TestCase):
    def test_make_random_payment_id(self):
        valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        payment_id = make_random_payment_id()
        self.assertEqual(len(payment_id), 16)
        no_invalid_chars = payment_id
        for char in valid_chars:
            no_invalid_chars = no_invalid_chars.replace(char, '')
        self.assertEqual(no_invalid_chars, '')

    def test_convert_datetime_object_to_truncated_RFC3339_timestamp_format(self):
        timestamp = datetime.datetime.now()
        date_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.assertEqual(convert_datetime_object_to_truncated_RFC3339_timestamp_format(timestamp), timestamp.strftime(date_format)[:-3] + 'Z')

    def test_decode_monero_payment_request_v1(self):
        payment_request = {
            'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': '', 'version': '1'
        }
        request_string = 'monero-request:1:H4sIAAAAAAACAy2OS0/DMBCE/4vPbeWkTktyS0qCBAKJtpTSi+XH5iEcu7IdIEH8dxzEaXe+Wc3ON2K9GbRHGYrwCmO0QKJlugHaadkJ5o2lg1XBnp3BWtBiDOrlcPsHnDc9VYzDfOLB+UAlGx29gqW8U6rTDRWjUICyaIH00PNgmJpe2diD9i5gvED/inYyxHBBBN7WRJANyLjmIdKBUmAd/WRhzmVJ7tfnxH6cxuvR1E0/wFPq0mdvJ7mHpBigsu49v3TRtjBvvJ1GZ6bJPFbFZnrVxwd5t9vkX2XOyzIRU7Vft2G7564n7Q7O8WF+6Zn1VDIfmqMYx2SJ0yVOjlGaRTdZlKzIGl/Qzy/yB8wvQQEAAA=='
        without_version = payment_request.copy()
        del(without_version['version'])
        self.assertEqual(decode_monero_payment_request(request_string), without_version)

    def test_make_monero_payment_request_v1(self):
        payment_request = {
            'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': '', 'version': '1'
        }
        request_string = make_monero_payment_request(**payment_request)
        self.assertEqual(request_string, 'monero-request:1:H4sIAAAAAAACAy2OS0/DMBCE/4vPbeWkTktyS0qCBAKJtpTSi+XH5iEcu7IdIEH8dxzEaXe+Wc3ON2K9GbRHGYrwCmO0QKJlugHaadkJ5o2lg1XBnp3BWtBiDOrlcPsHnDc9VYzDfOLB+UAlGx29gqW8U6rTDRWjUICyaIH00PNgmJpe2diD9i5gvED/inYyxHBBBN7WRJANyLjmIdKBUmAd/WRhzmVJ7tfnxH6cxuvR1E0/wFPq0mdvJ7mHpBigsu49v3TRtjBvvJ1GZ6bJPFbFZnrVxwd5t9vkX2XOyzIRU7Vft2G7564n7Q7O8WF+6Zn1VDIfmqMYx2SJ0yVOjlGaRTdZlKzIGl/Qzy/yB8wvQQEAAA==')
        return True

    def test_decode_monero_payment_request_v2(self):
        payment_request = {
            'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'schedule': '* * * * *', 'number_of_payments': 10, 'change_indicator_url': '', 'version': '2'
        }
        request_string = 'monero-request:2:H4sIAAAAAAACAy1O206DQBD9FbOPpm0WWFrhDSo10WhiW7X2ZbOXoRBht9mLCsZ/dzHNPMycW+b8INZrrxzKUYQXGKMZEg1TJ6Ctkq1gThvqTRfkSfHGgBJDQC+723/COt3TjnGYLA6sC6zyPQdDdU3PbOhBOYvyCM/QBdFWBi8XROBVTQRZgoxrHnJWNCB9B0G9vrrMREPXgbH0i4U9FSWFSw6p+Xwdzntdn3oPT5nNnp0Z5RbS0sPG2I/i2EarUr/zZhysHkf9uCmX45vaP8i79bL4rgpeVakYN9ukCdc9tz1p1nCId9NLx4yjkrmpS4xjMsfZHKf7KMujmzxKFyTBR/T7BxO/cqM9AQAA'
        without_version = payment_request.copy()
        del(without_version['version'])
        self.assertEqual(decode_monero_payment_request(request_string), without_version)

    def test_make_monero_payment_request_v2(self):
        payment_request = {
            'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'schedule': '* * * * *', 'number_of_payments': 10, 'change_indicator_url': '', 'version': '2'
        }
        request_string = make_monero_payment_request(**payment_request)
        self.assertEqual(request_string, 'monero-request:2:H4sIAAAAAAACAy1O206DQBD9FbOPpm0WWFrhDSo10WhiW7X2ZbOXoRBht9mLCsZ/dzHNPMycW+b8INZrrxzKUYQXGKMZEg1TJ6Ctkq1gThvqTRfkSfHGgBJDQC+723/COt3TjnGYLA6sC6zyPQdDdU3PbOhBOYvyCM/QBdFWBi8XROBVTQRZgoxrHnJWNCB9B0G9vrrMREPXgbH0i4U9FSWFSw6p+Xwdzntdn3oPT5nNnp0Z5RbS0sPG2I/i2EarUr/zZhysHkf9uCmX45vaP8i79bL4rgpeVakYN9ukCdc9tz1p1nCId9NLx4yjkrmpS4xjMsfZHKf7KMujmzxKFyTBR/T7BxO/cqM9AQAA')
        return True

class TestRequestV1(unittest.TestCase):
    def setUp(self):
        self.valid_payment = {
            'custom_label': 'Test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'days_per_billing_cycle': '1', 'number_of_payments': 10, 'change_indicator_url': ''
        }

    def test_invalid_make_monero_payment_request(self):
        with self.subTest(i=0):
            payment_request = self.valid_payment.copy()
            payment_request['custom_label'] = None
            with self.assertRaisesRegex(ValueError, 'custom_label'):
                RequestV1(**payment_request).valid()

        with self.subTest(i=1):
            payment_request = self.valid_payment.copy()
            payment_request['sellers_wallet'] = '4'
            with self.assertRaisesRegex(ValueError, 'sellers_wallet'):
                RequestV1(**payment_request).valid()

        with self.subTest(i=2):
            payment_request = self.valid_payment.copy()
            payment_request['currency'] = ''
            with self.assertRaisesRegex(ValueError, 'currency'):
                RequestV1(**payment_request).valid()

        with self.subTest(i=3):
            payment_request = self.valid_payment.copy()
            payment_request['amount'] = ''
            with self.assertRaisesRegex(ValueError, 'amount'):
                RequestV1(**payment_request).valid()

        with self.subTest(i=4):
            payment_request = self.valid_payment.copy()
            payment_request['payment_id'] = '123'
            with self.assertRaisesRegex(ValueError, 'payment_id'):
                RequestV1(**payment_request).valid()

        with self.subTest(i=5):
            payment_request = self.valid_payment.copy()
            payment_request['start_date'] = '2024-09-05T19:'
            with self.assertRaisesRegex(ValueError, 'start_date'):
                RequestV1(**payment_request).valid()

        with self.subTest(i=6):
            payment_request = self.valid_payment.copy()
            payment_request['days_per_billing_cycle'] = ''
            with self.assertRaisesRegex(ValueError, 'billing_cycle'):
                RequestV1(**payment_request).valid()

        with self.subTest(i=7):
            payment_request = self.valid_payment.copy()
            payment_request['number_of_payments'] = ''
            with self.assertRaisesRegex(ValueError, 'number_of_payments'):
                RequestV1(**payment_request).valid()

        with self.subTest(i=8):
            payment_request = self.valid_payment.copy()
            payment_request['change_indicator_url'] = None
            with self.assertRaisesRegex(ValueError, 'change_indicator_url'):
                RequestV1(**payment_request).valid()

class TestRequestV2(unittest.TestCase):
    def setUp(self):
        self.valid_payment = {
            'custom_label': 'Test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'schedule': '* * * * *', 'number_of_payments': 10, 'change_indicator_url': ''
        }

    def test_invalid_make_monero_payment_request(self):
        with self.subTest(i=0):
            payment_request = self.valid_payment.copy()
            payment_request['custom_label'] = None
            with self.assertRaisesRegex(ValueError, 'custom_label'):
                RequestV2(**payment_request).valid()

        with self.subTest(i=1):
            payment_request = self.valid_payment.copy()
            payment_request['sellers_wallet'] = '4'
            with self.assertRaisesRegex(ValueError, 'sellers_wallet'):
                RequestV2(**payment_request).valid()

        with self.subTest(i=2):
            payment_request = self.valid_payment.copy()
            payment_request['currency'] = ''
            with self.assertRaisesRegex(ValueError, 'currency'):
                RequestV2(**payment_request).valid()

        with self.subTest(i=3):
            payment_request = self.valid_payment.copy()
            payment_request['amount'] = ''
            with self.assertRaisesRegex(ValueError, 'amount'):
                RequestV2(**payment_request).valid()

        with self.subTest(i=4):
            payment_request = self.valid_payment.copy()
            payment_request['payment_id'] = '123'
            with self.assertRaisesRegex(ValueError, 'payment_id'):
                RequestV2(**payment_request).valid()

        with self.subTest(i=5):
            payment_request = self.valid_payment.copy()
            payment_request['start_date'] = '2024-09-05T19:'
            with self.assertRaisesRegex(ValueError, 'start_date'):
                RequestV2(**payment_request).valid()

        with self.subTest(i=6):
            payment_request = self.valid_payment.copy()
            payment_request['schedule'] = 'a a a a a'
            with self.assertRaisesRegex(ValueError, 'schedule'):
                RequestV2(**payment_request).valid()

        with self.subTest(i=7):
            payment_request = self.valid_payment.copy()
            payment_request['number_of_payments'] = ''
            with self.assertRaisesRegex(ValueError, 'number_of_payments'):
                RequestV2(**payment_request).valid()

        with self.subTest(i=8):
            payment_request = self.valid_payment.copy()
            payment_request['change_indicator_url'] = None
            with self.assertRaisesRegex(ValueError, 'change_indicator_url'):
                RequestV2(**payment_request).valid()

class TestCronValidation(unittest.TestCase):
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