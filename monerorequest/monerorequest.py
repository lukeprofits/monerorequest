import re
import gzip
import json
import base64
import random

from datetime import datetime, timezone
from urllib.parse import urlparse


def make_random_payment_id():
    payment_id = ''.join([random.choice('0123456789abcdef') for _ in range(16)])
    return payment_id


def convert_datetime_object_to_truncated_RFC3339_timestamp_format(datetime_object):
    if datetime_object.tzinfo is None or datetime_object.tzinfo.utcoffset(datetime_object) is None:
        datetime_object = datetime_object.replace(tzinfo=timezone.utc)
    else:
        datetime_object = datetime_object.astimezone(timezone.utc)
    return datetime_object.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def decode_monero_payment_request(monero_payment_request):
    return Decode.monero_payment_request_from_code(monero_payment_request=monero_payment_request)


def make_monero_payment_request(custom_label: str = 'Unlabeled Monero Payment Request',
                                sellers_wallet: str = '',
                                currency: str = '',
                                amount: str = '',
                                payment_id: str = '',
                                start_date: str = '',
                                days_per_billing_cycle: int = 30,
                                schedule: str = '0 0 1 * *',
                                number_of_payments: int = 1,
                                change_indicator_url: str = '',
                                version: str = '2',
                                allow_standard: bool = True,
                                allow_integrated_address: bool = True,
                                allow_subaddress: bool = False,
                                allow_stagenet: bool = False):

    # Defaults To Use
    if not payment_id:
        payment_id = make_random_payment_id()
    if not start_date:
        start_date = convert_datetime_object_to_truncated_RFC3339_timestamp_format(datetime.now())

    if version == '1':
        request = RequestV1(custom_label=custom_label, sellers_wallet=sellers_wallet, currency=currency,
                            amount=amount, payment_id=payment_id, start_date=start_date, days_per_billing_cycle=days_per_billing_cycle,
                            number_of_payments=number_of_payments, change_indicator_url=change_indicator_url, allow_standard=allow_standard,
                            allow_integrated_address=allow_integrated_address, allow_subaddress=allow_subaddress, allow_stagenet=allow_stagenet)
        if request.valid():
            return request.encode()

    if version == '2':
        request = RequestV2(custom_label=custom_label, sellers_wallet=sellers_wallet, currency=currency,
                            amount=amount, payment_id=payment_id, start_date=start_date, schedule=schedule,
                            change_indicator_url=change_indicator_url, allow_standard=allow_standard, number_of_payments=number_of_payments,
                            allow_integrated_address=allow_integrated_address, allow_subaddress=allow_subaddress, allow_stagenet=allow_stagenet)
        if request.valid():
            return request.encode()
def print_monero_logo():
    print('''
                    k                                     d                   
                    0Kx                                 dOX                   
                    KMWKx                             dONMN                   
                    KMMMWKx                         dONMMMN                   
                    KMMMMMWKk                     d0NMMMMMN                   
                    KMMMMMMMMXk                 dKWMMMMMMMN                   
                    KMMMMMMMMMMXk             dKWMMMMMMMMMN                   
                    KMMMMMMMMMMMMXk         xKWMMMMMMMMMMMN                   
                    KMMMMMXkNMMMMMMXk     dKWMMMMMW00MMMMMN                   
                    KMMMMM0  xNMMMMMMXk dKWMMMMMWOc dMMMMMN                   
                    KMMMMM0    xNMMMMMMNWMMMMMWOc   dMMMMMN                   
                    KMMMMM0      dXMMMMMMMMMNkc     dMMMMMN                   
                    KMMMMM0        oXMMMMMNx;       dMMMMMN                   
KMMMMMMMMMMMMMMMMMMMMMMMMM0          dNMWk:         dMMMMMMMMMMMMMMMMMMMMMMMMK
KMMMMMMMMMMMMMMMMMMMMMMMMM0            o            dMMMMMMMMMMMMMMMMMMMMMMMMK
KMMMMMMMMMMMMMWNNNNNNNNNNNO                         oNNNNNNNNNNNNMMMMMMMMMMMMO''')


class Encode:
    @staticmethod
    def monero_payment_request_from_json(json_data, version='1'):
        encoded_str = ''

        if version == '1':
            encoded_str = Encode.v1_monero_payment_request(json_data)
        elif version == '2':
            encoded_str = Encode.v2_monero_payment_request(json_data)

        # Add the Monero Subscription identifier & version number
        monero_payment_request = 'monero-request:' + str(version) + ':' + encoded_str

        if not encoded_str:
            raise ValueError("Invalid input")

        return monero_payment_request

    # VERSIONS #########################################################################################################
    @staticmethod
    def v1_monero_payment_request(json_data):
        # Convert the JSON data to a string
        json_str = json.dumps(json_data, separators=(',', ':'), sort_keys=True)
        # Compress the string using gzip compression
        compressed_data = gzip.compress(json_str.encode('utf-8'), mtime=0)
        # Encode the compressed data into a Base64-encoded string
        encoded_str = base64.b64encode(compressed_data).decode('ascii')
        return encoded_str

    @staticmethod
    def v2_monero_payment_request(json_data):
       return Encode.v1_monero_payment_request(json_data)

class Decode:
    @staticmethod
    def monero_payment_request_from_code(monero_payment_request):
        # Extract prefix, version, and Base64-encoded data
        prefix, version, encoded_str = monero_payment_request.split(':')

        if version == '1':
            monero_payment_request_data = Decode.v1_monero_payment_request(encoded_str=encoded_str)

        elif version == '2':
           monero_payment_request_data = Decode.v2_monero_payment_request(encoded_str=encoded_str)

        else:
            raise ValueError("Invalid input")

        return monero_payment_request_data

    # VERSIONS #########################################################################################################
    @staticmethod
    def v1_monero_payment_request(encoded_str):
        # Decode the Base64-encoded string to bytes
        encoded_str = base64.b64decode(encoded_str.encode('ascii'))
        # Decompress the bytes using gzip decompression
        decompressed_data = gzip.decompress(encoded_str)
        # Convert the decompressed bytes into to a JSON string
        json_str = decompressed_data.decode('utf-8')
        # Parse the JSON string into a Python object
        monero_payment_request_data = json.loads(json_str)
        return monero_payment_request_data

    @staticmethod
    def v2_monero_payment_request(encoded_str):
        return Decode.v1_monero_payment_request(encoded_str)



class Check:
    @staticmethod
    def name(name):
        if isinstance(name, str):
            return True
        else:
            return False

    @staticmethod
    def currency(currency):
        supported_currencies = ['XMR', 'USD']
        if isinstance(currency, str) and currency in supported_currencies:
            return True
        else:
            return False

    @staticmethod
    def wallet(wallet_address, allow_standard=True, allow_integrated_address=True, allow_subaddress=False, allow_stagenet=False):
        # Check if walled_address is a string
        if not isinstance(wallet_address, str):
            return False

        # Check if the wallet address starts with the number 4 (or 8 for subaddresses)
        allowed_first_characters = []
        if allow_stagenet:
            if allow_standard:
                allowed_first_characters.append('5')
            if allow_subaddress:
                allowed_first_characters.append('7')
        else:
            if allow_standard:
                allowed_first_characters.append('4')
            if allow_subaddress:
                allowed_first_characters.append('8')

        if wallet_address[0] not in allowed_first_characters:
            return False

        # Check if the wallet address is exactly 95 characters long (or 106 for integrated addresses)
        allowed_wallet_lengths = []
        if allow_standard or allow_subaddress:
            allowed_wallet_lengths.append(95)
        if allow_integrated_address:
            allowed_wallet_lengths.append(106)

        if len(wallet_address) not in allowed_wallet_lengths:
            return False

        # Check if the wallet address contains only valid characters
        valid_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        for char in wallet_address:
            if char not in valid_chars:
                return False

        # If it passed all these checks
        return True

    @staticmethod
    def payment_id(payment_id):
        if isinstance(payment_id, str) and len(payment_id) == 16:
            for char in payment_id:
                if char not in '0123456789abcdef':
                    return False  # Invalid character found
            return True  # All checks passed
        else:
            return False  # Not a string or incorrect length

    @staticmethod
    def start_date(start_date):
        if isinstance(start_date, str):
            # If it is an empty string
            if not start_date:
                return True

            # If not empty, make sure it is in the proper format
            try:
                datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ')
                return True
            except ValueError:
                pass
        return False

    @staticmethod
    def amount(amount):
        if isinstance(amount, str):
            if re.fullmatch(r'[\d,.]+', amount):
                return True
        return False

    @staticmethod
    def days_per_billing_cycle(billing_cycle):
        if isinstance(billing_cycle, int) and billing_cycle >= 0:
            return True
        else:
            return False

    @staticmethod
    def number_of_payments(number_of_payments):
        if isinstance(number_of_payments, int) and number_of_payments >= -1:
            return True
        else:
            return False

    @staticmethod
    def change_indicator_url(change_indicator_url):
        if change_indicator_url == "":
            return True  # Empty string is allowed
        if isinstance(change_indicator_url, str):
            parsed_url = urlparse(change_indicator_url)
            if all([parsed_url.scheme, parsed_url.netloc]):
                return True  # Well-formed URL
        return False  # Invalid

    @staticmethod
    def schedule(schedule):
        return CronValidation(schedule).valid()

class RequestV1():
    def __init__(self, custom_label: str = 'Unlabeled Monero Payment Request', sellers_wallet: str = '', currency: str = '', amount: str = '', payment_id: str = '',
                 start_date: str = '', days_per_billing_cycle: int = 30, number_of_payments: int = 1, change_indicator_url: str = '',
                 allow_standard: bool = True, allow_integrated_address: bool = True, allow_subaddress: bool = False, allow_stagenet: bool = False):
        self.custom_label = custom_label
        self.sellers_wallet = sellers_wallet
        self.currency = currency
        self.amount = amount
        self.payment_id = payment_id
        self.start_date = start_date
        self.days_per_billing_cycle = days_per_billing_cycle
        self.number_of_payments = number_of_payments
        self.change_indicator_url = change_indicator_url
        self.version = '1'
        self.allow_standard = allow_standard
        self.allow_integrated_address = allow_integrated_address
        self.allow_subaddress = allow_subaddress
        self.allow_stagenet = allow_stagenet

    def valid(self):
        return_message = []
        if not Check.name(self.custom_label):
            return_message.append('custom_label is not a string.')

        if not Check.wallet(self.sellers_wallet, self.allow_standard, self.allow_integrated_address, self.allow_subaddress, self.allow_stagenet):
            return_message.append('sellers_wallet is not valid, because it is not a string, it is not exactly 95 characters long, it contains invalid characters, or it does not begin with a "4".')

        if not Check.currency(self.currency):
            return_message.append('currency is not a string, or is not supported.')

        if not Check.amount(self.amount):
            return_message.append('amount is not a string, or invalid characters in amount. Amount can only contain ",", ".", and numbers.')

        if not Check.payment_id(self.payment_id):
            return_message.append('payment_id is not a string, is not exactly 16 characters long, or contains invalid character(s).')

        if not Check.start_date(self.start_date):
            return_message.append('start_date is not a string, or is not in the correct format.')

        if not Check.days_per_billing_cycle(self.days_per_billing_cycle):
            return_message.append('billing_cycle is not an integer, or the value set was lower than 0.')

        if not Check.number_of_payments(self.number_of_payments):
            return_message.append('number_of_payments is not an integer, or is less than 1.')

        if not Check.change_indicator_url(self.change_indicator_url):
            return_message.append('change_indicator_url is not a string, or is not a valid URL.')

        if not return_message:
            return True
        else:
            raise ValueError(' '.join(return_message))

    def encode(self):
        json_data = {
            "custom_label": self.custom_label,
            "sellers_wallet": self.sellers_wallet,
            "currency": self.currency,
            "amount": self.amount,
            "payment_id": self.payment_id,
            "start_date": self.start_date,
            "days_per_billing_cycle": self.days_per_billing_cycle,
            "number_of_payments": self.number_of_payments,
            "change_indicator_url": self.change_indicator_url
        }
        return Encode.monero_payment_request_from_json(json_data=json_data, version=self.version)

class RequestV2():
    def __init__(self, custom_label: str = 'Unlabeled Monero Payment Request', sellers_wallet: str = '', currency: str = '', amount: str = '', payment_id: str = '',
                 start_date: str = '', schedule: str = '0 0 1 * *', number_of_payments: int = 1, change_indicator_url: str = '',
                 allow_standard: bool = True, allow_integrated_address: bool = True, allow_subaddress: bool = False, allow_stagenet: bool = False):
        self.custom_label = custom_label
        self.sellers_wallet = sellers_wallet
        self.currency = currency
        self.amount = amount
        self.payment_id = payment_id
        self.start_date = start_date
        self.schedule = schedule
        self.number_of_payments = number_of_payments
        self.change_indicator_url = change_indicator_url
        self.version = '2'
        self.allow_standard = allow_standard
        self.allow_integrated_address = allow_integrated_address
        self.allow_subaddress = allow_subaddress
        self.allow_stagenet = allow_stagenet

    def valid(self):
        return_message = []
        if not Check.name(self.custom_label):
            return_message.append('custom_label is not a string.')

        if not Check.wallet(self.sellers_wallet, self.allow_standard, self.allow_integrated_address, self.allow_subaddress, self.allow_stagenet):
            return_message.append('sellers_wallet is not valid, because it is not a string, it is not exactly 95 characters long, it contains invalid characters, or it does not begin with a "4".')

        if not Check.currency(self.currency):
            return_message.append('currency is not a string, or is not supported.')

        if not Check.amount(self.amount):
            return_message.append('amount is not a string, or invalid characters in amount. Amount can only contain ",", ".", and numbers.')

        if not Check.payment_id(self.payment_id):
            return_message.append('payment_id is not a string, is not exactly 16 characters long, or contains invalid character(s).')

        if not Check.start_date(self.start_date):
            return_message.append('start_date is not a string, or is not in the correct format.')

        if not Check.schedule(self.schedule):
            return_message.append('schedule is not a valid cron syntax.')

        if not Check.number_of_payments(self.number_of_payments):
            return_message.append('number_of_payments is not an integer, or is less than 1.')

        if not Check.change_indicator_url(self.change_indicator_url):
            return_message.append('change_indicator_url is not a string, or is not a valid URL.')

        if not return_message:
            return True
        else:
            raise ValueError(' '.join(return_message))

    def encode(self):
        json_data = {
            "custom_label": self.custom_label,
            "sellers_wallet": self.sellers_wallet,
            "currency": self.currency,
            "amount": self.amount,
            "payment_id": self.payment_id,
            "start_date": self.start_date,
            "schedule": self.schedule,
            "number_of_payments": self.number_of_payments,
            "change_indicator_url": self.change_indicator_url
        }
        return Encode.monero_payment_request_from_json(json_data=json_data, version=self.version)


class CronValidation():
    delimiters = ',-/'
    month_codes = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    dow_codes = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    def __init__(self, schedule):
        self.schedule = schedule
        cron_def = self.parse_cron()
        self.minutes = cron_def['minutes']
        self.hours = cron_def['hours']
        self.days = cron_def['days']
        self.months = cron_def['months']
        self.dow = cron_def['dow']
        self.any = ['*']
        self.errors = []

    def parse_cron(self):
        schedule_args = self.schedule.split(' ')

        if len(schedule_args) < 5:
            raise ValueError('Invalid Cron: Too Few Of Arguments')

        sched = {}

        sched['minutes'] = re.split(self.delimiters, schedule_args[0])
        sched['hours'] = re.split(self.delimiters, schedule_args[1])
        sched['days'] = re.split(self.delimiters, schedule_args[2])
        sched['months'] = re.split(self.delimiters, schedule_args[3])
        sched['dow'] = re.split(self.delimiters, schedule_args[4])

        return sched

    def valid(self):
        if not self.valid_minutes():
            self.errors.append('Invalid Minutes')

        if not self.valid_hours():
            self.errors.append('Invalid Hours')

        if not self.valid_days():
            self.errors.append('Invalid Day')

        if not self.valid_months():
            self.errors.append('Invalid Month')

        if not self.valid_dow():
            self.errors.append('Invalid Day of the Week')

        if self.errors:
            return False
        else:
            return True

    def valid_minutes(self):
        if self.minutes == self.any:
            return True
        try:
            results = []
            for minute in self.minutes:
                int_minute = int(minute)
                results.append(int_minute >= 0 and int_minute <= 59)
            return any(results)
        except ValueError:
            return False

    def valid_hours(self):
        if self.hours == self.any:
            return True
        try:
            results = []
            for hour in self.hours:
                int_hour = int(hour)
                results.append(int_hour >= 0 and int_hour <= 23)
            return any(results)
        except ValueError:
            return False

    def valid_days(self):
        if self.days == self.any:
            return True
        try:
            results = []
            for day in self.days:
                int_day = int(day)
                results.append(int_day >= 1 and int_day <= 31)
            return any(results)
        except ValueError:
            return False

    def valid_months(self):
        if self.months == self.any:
            return True
        results = []
        try:
            for month in self.months:
                int_month = int(month)
                results.append(int_month >= 1 and int_month <= 12)
        except ValueError:
            for month in self.months:
                results.append(month.lower() in self.month_codes)
        return any(results)

    def valid_dow(self):
        if self.dow == self.any:
            return True
        results = []
        try:
            for dow in self.dow:
                int_dow = int(dow)
                results.append(int_dow >= 0 and int_dow <= 7)
        except ValueError:
            for dow in self.dow:
                results.append(dow.lower() in self.dow_codes)
        return any(results)

'''
monero_payment_request = make_monero_payment_request(
                                custom_label='Unlabeled Monero Payment Request',
                                sellers_wallet='4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',
                                currency='USD',
                                amount='25.99',
                                payment_id='',
                                start_date='',
                                days_per_billing_cycle=30,
                                number_of_payments=1,
                                change_indicator_url='')
print(monero_payment_request)


monero_payment_request = 'monero-request:1:H4sIAAAAAAAC/y1QyU7DMBD9lcrntkriOFVyS0uKBCqCLlB6sex40kQkdvECJIh/xymc5i0z8zTzjVinnLQoQxGZpymaorJm8gy0kaIpmVWaOt16e3Sc1iDL3rPD7uYqGKs62jIOY8tBXhGIyUZJ0GryyPoOpJ1s4d2BsX5CsN7QC2jKm7Zt5JmWfdkCynAwRdJ13Duqope/OYMyL/8T2ggfEbCqSpKI45CEkESxX2mgbUEb+sl8HQ+Jc4uPRH8895e9qs6dg4fUpE9WD2ILZOlgrc1bfmrCxVK98nrojRoGtVkvk+FF7u/F7SrJv4qcFwUph/UW1x7dcdPF9QqO0W6MtExbKpiF8W9BhGdhMIuSfRBnhGR4MY9jfEI/vzFHmeFdAQAA'
monero_payment_request_data = decode_monero_payment_request(monero_payment_request=monero_payment_request)
print(monero_payment_request_data)
#'''
