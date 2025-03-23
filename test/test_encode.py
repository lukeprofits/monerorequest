import unittest
from src.monerorequest.encode import Encode

class TestEncode(unittest.TestCase):
    def test_invalid_payment_request_encoding(self):
        with self.assertRaisesRegex(ValueError, 'Invalid input'):
            Encode.monero_payment_request_from_json(json_data='', version='')
