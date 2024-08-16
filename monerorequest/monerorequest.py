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
                                number_of_payments: int = 1,
                                change_indicator_url: str = '',
                                version: str = '1',
                                allow_standard: bool = True,
                                allow_integrated_address: bool = True,
                                allow_subaddress: bool = False,
                                allow_stagenet: bool = False):

    # Defaults To Use
    if not payment_id:
        payment_id = make_random_payment_id()
    if not start_date:
        start_date = convert_datetime_object_to_truncated_RFC3339_timestamp_format(datetime.now())

    # Make sure all arguments are valid
    if Check.name(custom_label):
        if Check.wallet(sellers_wallet, allow_standard, allow_integrated_address, allow_subaddress, allow_stagenet):
            if Check.currency(currency):
                if Check.amount(amount):
                    if Check.payment_id(payment_id):
                        if Check.start_date(start_date):
                            if Check.days_per_billing_cycle(days_per_billing_cycle):
                                if Check.number_of_payments(number_of_payments):
                                    if Check.change_indicator_url(change_indicator_url):
                                        json_data = {
                                            "custom_label": custom_label,
                                            "sellers_wallet": sellers_wallet,
                                            "currency": currency,
                                            "amount": amount,
                                            "payment_id": payment_id,
                                            "start_date": start_date,
                                            "days_per_billing_cycle": days_per_billing_cycle,
                                            "number_of_payments": number_of_payments,
                                            "change_indicator_url": change_indicator_url
                                        }

                                        # process data to create code
                                        monero_payment_request = Encode.monero_payment_request_from_json(json_data=json_data, version=version)
                                        return monero_payment_request
                                    else:  # change_indicatior_url
                                        raise ValueError('change_indicator_url is not a string, or is not a valid URL.')
                                else:  # number_of_payments
                                    raise ValueError('number_of_payments is not an integer, or is less than 1.')
                            else:  # days_per_billing_cycle
                                raise ValueError('billing_cycle is not an integer, or the value set was lower than 0.')
                        else:  # start_date
                            raise ValueError('start_date is not a string, or is not in the correct format.')
                    else:  #payment_id
                        raise ValueError('payment_id is not a string, is not exactly 16 characters long, or contains invalid character(s).')
                else:  # amount
                    raise ValueError('amount is not a string, or invalid characters in amount. Amount can only contain ",", ".", and numbers.')
            else:  # currency
                raise ValueError('Currency is not a string, or is not a supported.')
        else:  # sellers_wallet
            raise ValueError('sellers_wallet is not valid, because it is not a string, it is not exactly 95 characters long, it contains invalid characters, or it does not begin with a "4".')
    else:  # custom_label
        raise ValueError('custom_label is not a string.')


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
        # elif version == '2':
        # encoded_str = encode_v2_monero_payment_request(json_data)

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

    '''
    @staticmethod
    def v2_monero_payment_request(json_data):
       pass
    '''


class Decode:
    @staticmethod
    def monero_payment_request_from_code(monero_payment_request):
        # Extract prefix, version, and Base64-encoded data
        prefix, version, encoded_str = monero_payment_request.split(':')

        if version == '1':
            monero_payment_request_data = Decode.v1_monero_payment_request(encoded_str=encoded_str)

        #elif version == '2':
        #    monero_payment_request = Decode.v2_monero_payment_request(encoded_str=encoded_str)

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

    '''
    @staticmethod
    def v2_monero_payment_request(encoded_str):
        pass
    '''


class Check:
    @staticmethod
    def name(name):
        if type(name) == str:
            return True
        else:
            return False

    @staticmethod
    def currency(currency):
        supported_currencies = ['XMR', 'USD']
        if type(currency) == str and currency in supported_currencies:
            return True
        else:
            return False

    @staticmethod
    def wallet(wallet_address, allow_standard=True, allow_integrated_address=True, allow_subaddress=False, allow_stagenet=False):
        # Check if walled_address is a string
        if type(wallet_address) != str:
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
        if type(payment_id) == str and len(payment_id) == 16:
            for char in payment_id:
                if char not in '0123456789abcdef':
                    return False  # Invalid character found
            return True  # All checks passed
        else:
            return False  # Not a string or incorrect length

    @staticmethod
    def start_date(start_date):
        if type(start_date) == str:
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
        if type(amount) == str:
            if re.fullmatch(r'[\d,.]+', amount):
                return True
        return False

    @staticmethod
    def days_per_billing_cycle(billing_cycle):
        if type(billing_cycle) is int and billing_cycle >= 0:
            return True
        else:
            return False

    @staticmethod
    def number_of_payments(number_of_payments):
        if type(number_of_payments) == int and number_of_payments >= 0:
            return True
        else:
            return False

    @staticmethod
    def change_indicator_url(change_indicator_url):
        if change_indicator_url == "":
            return True  # Empty string is allowed
        if type(change_indicator_url) == str:
            parsed_url = urlparse(change_indicator_url)
            if all([parsed_url.scheme, parsed_url.netloc]):
                return True  # Well-formed URL
        return False  # Invalid

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
