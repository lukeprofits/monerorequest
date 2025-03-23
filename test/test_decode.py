import unittest
from src.monerorequest.decode import Decode

class TestDecode(unittest.TestCase):
    def test_invalid_payment_request_decoding(self):
        with self.assertRaisesRegex(ValueError, 'Invalid input'):
            Decode.monero_payment_request_from_code('::')