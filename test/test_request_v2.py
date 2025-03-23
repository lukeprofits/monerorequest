import unittest
from src.monerorequest.request_v2 import RequestV2

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