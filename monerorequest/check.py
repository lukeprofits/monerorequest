import re
from datetime import datetime
from .cron_validation import CronValidation
from urllib.parse import urlparse

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
