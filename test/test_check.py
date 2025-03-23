import unittest
from src.monerorequest.check import Check

class TestCheck(unittest.TestCase):
    def test_wallet(self):
        #Check for valid type
        self.assertEqual(Check.wallet([]), False)
        #Check for standard stagenet
        self.assertEqual(Check.wallet('5At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', allow_stagenet=True), True)
        #Check for stagenet subaddress
        self.assertEqual(Check.wallet('7At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', allow_stagenet=True, allow_subaddress=True), True)
        #Check for standard mainnet
        self.assertEqual(Check.wallet('4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S'), True)
        #Check for mainnet subaddress
        self.assertEqual(Check.wallet('8At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', allow_subaddress=True), True)
        #Check for no match of stagenet or mainnet standard or subaddress validity
        self.assertEqual(Check.wallet('1At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', allow_subaddress=True, allow_stagenet=True), False)
        #Check for entire character list validity
        self.assertEqual(Check.wallet('4$t3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', allow_subaddress=True, allow_stagenet=True), False)

    def test_payment_id(self):
        self.assertEqual(Check.payment_id('1234567890123456'), True)
        self.assertEqual(Check.payment_id('12354567890-----'), False)
        self.assertEqual(Check.payment_id(''), False)

    def test_start_date(self):
        self.assertEqual(Check.start_date(''), True)
        self.assertEqual(Check.start_date(start_date=None), False)
        self.assertEqual(Check.start_date('2024-09-05T19:18:15.430Z'), True)

    def test_change_indicator_url(self):
        self.assertEqual(Check.change_indicator_url(''), True)
        self.assertEqual(Check.change_indicator_url('https://getmonero.org'), True)
        self.assertEqual(Check.change_indicator_url('abcd'), False)