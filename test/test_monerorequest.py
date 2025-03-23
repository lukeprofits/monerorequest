import unittest
from datetime import datetime, timezone, timedelta
from src.monerorequest import make_random_payment_id, convert_datetime_object_to_truncated_RFC3339_timestamp_format,\
                          decode_monero_payment_request, make_monero_payment_request
from src.monerorequest.check import Check

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
        timestamp = datetime.now()
        date_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.assertEqual(convert_datetime_object_to_truncated_RFC3339_timestamp_format(timestamp), timestamp.strftime(date_format)[:-3] + 'Z')

        #Test with timezone conversion
        tz_delta = timedelta(hours=6)
        timestamp = datetime.now(timezone(tz_delta))
        self.assertEqual(convert_datetime_object_to_truncated_RFC3339_timestamp_format(timestamp), (timestamp - tz_delta).strftime(date_format)[:-3] + 'Z')

    def test_decode_monero_payment_request_v1(self):
        payment_request = {
            'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': '', 'version': '1'
        }
        request_string = 'monero-request:1:H4sIAAAAAAACAy2OS0/DMBCE/4vPbeWkTktyS0qCBAKJtpTSi+XH5iEcu7IdIEH8dxzEaXe+Wc3ON2K9GbRHGYrwCmO0QKJlugHaadkJ5o2lg1XBnp3BWtBiDOrlcPsHnDc9VYzDfOLB+UAlGx29gqW8U6rTDRWjUICyaIH00PNgmJpe2diD9i5gvED/inYyxHBBBN7WRJANyLjmIdKBUmAd/WRhzmVJ7tfnxH6cxuvR1E0/wFPq0mdvJ7mHpBigsu49v3TRtjBvvJ1GZ6bJPFbFZnrVxwd5t9vkX2XOyzIRU7Vft2G7564n7Q7O8WF+6Zn1VDIfmqMYx2SJ0yVOjlGaRTdZlKzIGl/Qzy/yB8wvQQEAAA=='
        self.assertEqual(decode_monero_payment_request(request_string), payment_request)

    def test_make_monero_payment_request_v1(self):
        payment_request = {
            'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': '', 'version': '1'
        }
        request_string = make_monero_payment_request(**payment_request)
        self.maxDiff = None
        self.assertEqual(request_string, 'monero-request:1:H4sIAAAAAAACAy2OS0/DMBCE/4vPbeWkTktyS0qCBAKJtpTSi+XH5iEcu7IdIEH8dxzEaXe+Wc3ON2K9GbRHGYrwCmO0QKJlugHaadkJ5o2lg1XBnp3BWtBiDOrlcPsHnDc9VYzDfOLB+UAlGx29gqW8U6rTDRWjUICyaIH00PNgmJpe2diD9i5gvED/inYyxHBBBN7WRJANyLjmIdKBUmAd/WRhzmVJ7tfnxH6cxuvR1E0/wFPq0mdvJ7mHpBigsu49v3TRtjBvvJ1GZ6bJPFbFZnrVxwd5t9vkX2XOyzIRU7Vft2G7564n7Q7O8WF+6Zn1VDIfmqMYx2SJ0yVOjlGaRTdZlKzIGl/Qzy/yB8wvQQEAAA==')

    def test_make_monero_payment_request_v1_w_defaults(self):
        payment_request = {
            'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'days_per_billing_cycle': 1, 'number_of_payments': 10, 'change_indicator_url': '', 'version': '1'
        }

        request_string = make_monero_payment_request(**payment_request)

        #Can't just test the output string because we don't know the start date/payment_id.

        result_pr = decode_monero_payment_request(request_string)

        for key, value in payment_request.items():
            self.assertEqual(result_pr[key], value)

        self.assertEqual(Check.payment_id(result_pr['payment_id']), True)
        self.assertEqual(Check.start_date(result_pr['start_date']), True)

    def test_decode_monero_payment_request_v2(self):
        payment_request = {
            'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'schedule': '* * * * *', 'number_of_payments': 10, 'change_indicator_url': '', 'version': '2'
        }
        request_string = 'monero-request:2:H4sIAAAAAAACAy1O206DQBD9FbOPpm0WWFrhDSo10WhiW7X2ZbOXoRBht9mLCsZ/dzHNPMycW+b8INZrrxzKUYQXGKMZEg1TJ6Ctkq1gThvqTRfkSfHGgBJDQC+723/COt3TjnGYLA6sC6zyPQdDdU3PbOhBOYvyCM/QBdFWBi8XROBVTQRZgoxrHnJWNCB9B0G9vrrMREPXgbH0i4U9FSWFSw6p+Xwdzntdn3oPT5nNnp0Z5RbS0sPG2I/i2EarUr/zZhysHkf9uCmX45vaP8i79bL4rgpeVakYN9ukCdc9tz1p1nCId9NLx4yjkrmpS4xjMsfZHKf7KMujmzxKFyTBR/T7BxO/cqM9AQAA'
        self.assertEqual(decode_monero_payment_request(request_string), payment_request)

    def test_make_monero_payment_request_v2(self):
        payment_request = {
            'custom_label': 'test', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',\
            'currency': 'USD', 'amount': '10.00', 'payment_id': 'bc4c07f4c46ed2fb', 'start_date': '2024-09-05T19:18:15.430Z',
            'schedule': '* * * * *', 'number_of_payments': 10, 'change_indicator_url': '', 'version': '2'
        }
        request_string = make_monero_payment_request(**payment_request)
        self.maxDiff = None
        self.assertEqual(request_string, 'monero-request:2:H4sIAAAAAAACAy1O206DQBD9FbOPpm0WWFrhDSo10WhiW7X2ZbOXoRBht9mLCsZ/dzHNPMycW+b8INZrrxzKUYQXGKMZEg1TJ6Ctkq1gThvqTRfkSfHGgBJDQC+723/COt3TjnGYLA6sC6zyPQdDdU3PbOhBOYvyCM/QBdFWBi8XROBVTQRZgoxrHnJWNCB9B0G9vrrMREPXgbH0i4U9FSWFSw6p+Xwdzntdn3oPT5nNnp0Z5RbS0sPG2I/i2EarUr/zZhysHkf9uCmX45vaP8i79bL4rgpeVakYN9ukCdc9tz1p1nCId9NLx4yjkrmpS4xjMsfZHKf7KMujmzxKFyTBR/T7BxO/cqM9AQAA')