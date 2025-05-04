import unittest
from src.monerorequest.request_v2 import RequestV2

class TestRequestV2(unittest.TestCase):
    def setUp(self):
        self.valid_payment = {
            'custom_label': 'Test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'schedule': '* * * * *', 'number_of_payments': 10, 'change_indicator_url': ''
        }

    def test_valid_make_monero_payment_request(self):
        payment_request = self.valid_payment
        request = RequestV2(**payment_request)
        self.assertEqual(request.valid(), True)
        self.assertEqual(request.name_validity(), True)
        self.assertEqual(request.wallet_validity(), True)
        self.assertEqual(request.currency_validity(), True)
        self.assertEqual(request.amount_validity(), True)
        self.assertEqual(request.payment_id_validity(), True)
        self.assertEqual(request.start_date_validity(), True)
        self.assertEqual(request.number_of_payments_validity(), True)
        self.assertEqual(request.change_indicator_validity(), True)
        self.assertEqual(request.schedule_validity(), True)

    def test_invalid_make_monero_payment_request(self):
        with self.subTest(i=0):
            payment_request = self.valid_payment.copy()
            payment_request['custom_label'] = None
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.name_validity(), False)
            self.assertEqual(request.errors['custom_label'], ['is not a string'])

        with self.subTest(i=1):
            payment_request = self.valid_payment.copy()
            payment_request['sellers_wallet'] = '@!%!#%'
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.wallet_validity(), False)
            self.assertEqual(request.errors['sellers_wallet'], ['contains invalid characters', 'is not exactly 95 or 106 characters long', 'it does not begin with a 4'])

            payment_request['sellers_wallet'] = None
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.wallet_validity(), False)
            self.assertEqual(request.errors['sellers_wallet'], ['is not a string'])

        with self.subTest(i=2):
            payment_request = self.valid_payment.copy()
            payment_request['currency'] = None
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.currency_validity(), False)
            self.assertEqual(request.errors['currency'], ['is not a string', 'is not supported'])

        with self.subTest(i=3):
            payment_request = self.valid_payment.copy()
            payment_request['amount'] = ''
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.amount_validity(), False)
            self.assertEqual(request.errors['amount'], ['contains invalid characters'])

            payment_request['amount'] = None
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.amount_validity(), False)
            self.assertEqual(request.errors['amount'], ['is not a string'])

        with self.subTest(i=4):
            payment_request = self.valid_payment.copy()
            payment_request['payment_id'] = '123%$@'
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.payment_id_validity(), False)
            self.assertEqual(request.errors['payment_id'], ['is not exactly 16 characters', 'contains invalid characters'])

            payment_request['payment_id'] = None
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.payment_id_validity(), False)
            self.assertEqual(request.errors['payment_id'], ['is not a string'])

        with self.subTest(i=5):
            payment_request = self.valid_payment.copy()
            payment_request['start_date'] = '2024-09-05T19:'
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.start_date_validity(), False)
            self.assertEqual(request.errors['start_date'], ['is not in the correct format'])

            payment_request['start_date'] = None
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.start_date_validity(), False)
            self.assertEqual(request.errors['start_date'], ['is not a string'])

        with self.subTest(i=6):
            payment_request = self.valid_payment.copy()
            payment_request['schedule'] = 'a a a a a'
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.schedule_validity(), False)
            self.assertEqual(request.errors['schedule'], ['is not a valid cron syntax'])

        with self.subTest(i=7):
            payment_request = self.valid_payment.copy()
            payment_request['number_of_payments'] = ''
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.number_of_payments_validity(), False)
            self.assertEqual(request.errors['number_of_payments'], ['is not an integer'])

        with self.subTest(i=8):
            payment_request = self.valid_payment.copy()
            payment_request['change_indicator_url'] = None
            request = RequestV2(**payment_request)
            self.assertEqual(request.valid(), False)
            self.assertEqual(request.change_indicator_validity(), False)
            self.assertEqual(request.errors['change_indicator_url'], ['is not a string', 'is not a valid URL'])
