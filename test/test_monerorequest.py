import unittest
import datetime
from monerorequest import make_random_payment_id, convert_datetime_object_to_truncated_RFC3339_timestamp_format,\
                          decode_monero_payment_request, make_monero_payment_request

class TestMoneroRequest(unittest.TestCase):
    def setUp(self):
        return True

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

    def test_decode_monero_payment_request(self):
        payment_request = {
            'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': ''
        }
        request_string = 'monero-request:1:H4sIAAAAAAACAy2OS0/DMBCE/4vPbeWkTktyS0qCBAKJtpTSi+XH5iEcu7IdIEH8dxzEaXe+Wc3ON2K9GbRHGYrwCmO0QKJlugHaadkJ5o2lg1XBnp3BWtBiDOrlcPsHnDc9VYzDfOLB+UAlGx29gqW8U6rTDRWjUICyaIH00PNgmJpe2diD9i5gvED/inYyxHBBBN7WRJANyLjmIdKBUmAd/WRhzmVJ7tfnxH6cxuvR1E0/wFPq0mdvJ7mHpBigsu49v3TRtjBvvJ1GZ6bJPFbFZnrVxwd5t9vkX2XOyzIRU7Vft2G7564n7Q7O8WF+6Zn1VDIfmqMYx2SJ0yVOjlGaRTdZlKzIGl/Qzy/yB8wvQQEAAA=='
        self.assertEqual(decode_monero_payment_request(request_string), payment_request)

    def test_make_monero_payment_request(self):
        payment_request = {
            'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': ''
        }
        request_string = make_monero_payment_request(**payment_request)
        self.assertEqual(request_string, 'monero-request:1:H4sIAAAAAAACAy2OS0/DMBCE/4vPbeWkTktyS0qCBAKJtpTSi+XH5iEcu7IdIEH8dxzEaXe+Wc3ON2K9GbRHGYrwCmO0QKJlugHaadkJ5o2lg1XBnp3BWtBiDOrlcPsHnDc9VYzDfOLB+UAlGx29gqW8U6rTDRWjUICyaIH00PNgmJpe2diD9i5gvED/inYyxHBBBN7WRJANyLjmIdKBUmAd/WRhzmVJ7tfnxH6cxuvR1E0/wFPq0mdvJ7mHpBigsu49v3TRtjBvvJ1GZ6bJPFbFZnrVxwd5t9vkX2XOyzIRU7Vft2G7564n7Q7O8WF+6Zn1VDIfmqMYx2SJ0yVOjlGaRTdZlKzIGl/Qzy/yB8wvQQEAAA==')
        return True

    def test_invalid_make_monero_payment_request(self):
        with self.subTest(i=0):
            payment_request = {
                'custom_label': None, 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
                'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
                'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': ''
            }
            with self.assertRaisesRegex(ValueError, 'custom_label'):
                make_monero_payment_request(**payment_request)

        with self.subTest(i=1):
            payment_request = {
                'custom_label': 'test', 'sellers_wallet': '4',\
                'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
                'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': ''
            }
            with self.assertRaisesRegex(ValueError, 'sellers_wallet'):
                make_monero_payment_request(**payment_request)
        with self.subTest(i=2):
            payment_request = {
                'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
                'currency': '', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
                'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': ''
            }
            with self.assertRaisesRegex(ValueError, 'Currency'):
                make_monero_payment_request(**payment_request)

        with self.subTest(i=3):
            payment_request = {
                'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
                'currency': 'USD', 'amount': '', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
                'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': ''
            }
            with self.assertRaisesRegex(ValueError, 'amount'):
                make_monero_payment_request(**payment_request)
        with self.subTest(i=4):
            payment_request = {
                'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
                'currency': 'USD', 'amount': '10.00', 'payment_id': '123', 'start_date': '2024-09-05T19:18:15.430Z',
                'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': ''
            }
            with self.assertRaisesRegex(ValueError, 'payment_id'):
                make_monero_payment_request(**payment_request)
        with self.subTest(i=5):
            payment_request = {
                'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
                'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:',
                'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': ''
            }
            with self.assertRaisesRegex(ValueError, 'start_date'):
                make_monero_payment_request(**payment_request)

        with self.subTest(i=6):
            payment_request = {
                'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
                'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
                'days_per_billing_cycle': '', 'number_of_payments': 10, 'change_indicator_url': ''
            }
            with self.assertRaisesRegex(ValueError, 'billing_cycle'):
                make_monero_payment_request(**payment_request)

        with self.subTest(i=7):
            payment_request = {
                'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
                'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
                'days_per_billing_cycle': 1, 'number_of_payments': '', 'change_indicator_url': ''
            }
            with self.assertRaisesRegex(ValueError, 'number_of_payments'):
                make_monero_payment_request(**payment_request)

        with self.subTest(i=8):
            payment_request = {
                'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
                'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
                'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': None
            }
            with self.assertRaisesRegex(ValueError, 'change_indicator_url'):
                make_monero_payment_request(**payment_request)
