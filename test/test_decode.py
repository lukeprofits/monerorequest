import unittest
from src.monerorequest.decode import Decode

class TestDecode(unittest.TestCase):
    def test_invalid_payment_request_decoding(self):
        self.assertEqual(Decode.monero_payment_request_from_code('::'), False)

        self.assertEqual(Decode.monero_payment_request_from_code(':'), False)