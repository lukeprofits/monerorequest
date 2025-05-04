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
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.errors['custom_label'], ['is not a string'])

        with self.subTest(i=1):
            payment_request = self.valid_payment.copy()
            payment_request['sellers_wallet'] = '4'
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.errors['sellers_wallet'], ['is not exactly 95 or 106 characters long', 'it does not begin with a 4'])

        with self.subTest(i=2):
            payment_request = self.valid_payment.copy()
            payment_request['currency'] = ''
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.errors['currency'], ['is not supported'])

        with self.subTest(i=3):
            payment_request = self.valid_payment.copy()
            payment_request['amount'] = ''
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.errors['amount'], ['contains invalid characters'])

        with self.subTest(i=4):
            payment_request = self.valid_payment.copy()
            payment_request['payment_id'] = '123'
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.errors['payment_id'], ['is not exactly 16 characters'])

        with self.subTest(i=5):
            payment_request = self.valid_payment.copy()
            payment_request['start_date'] = '2024-09-05T19:'
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.errors['start_date'], ['is not in the correct format'])

        with self.subTest(i=6):
            payment_request = self.valid_payment.copy()
            payment_request['schedule'] = 'a a a a a'
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.errors['schedule'], ['is not a valid cron syntax'])

        with self.subTest(i=7):
            payment_request = self.valid_payment.copy()
            payment_request['number_of_payments'] = ''
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.errors['number_of_payments'], ['is not an integer'])

        with self.subTest(i=8):
            payment_request = self.valid_payment.copy()
            payment_request['change_indicator_url'] = None
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.errors['change_indicator_url'], ['is not a string', 'is not a valid URL'])
