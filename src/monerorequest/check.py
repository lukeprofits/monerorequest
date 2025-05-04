import re
from datetime import datetime
from .cron_validation import CronValidation
from urllib.parse import urlparse

class Check:
    @staticmethod
    def is_string(field):
        return isinstance(field, str)

    @staticmethod
    def is_int(field):
        return isinstance(field, int)

    @staticmethod
    def name(name):
        if Check.is_string(name):
            return True
        else:
            return False

    @staticmethod
    def currency(currency):
        if Check.is_string(currency) and Check.currency_is_supported(currency):
            return True
        else:
            return False

    @staticmethod
    def currency_is_supported(currency):
        supported_currencies = ['XMR', 'USD']
        return currency in supported_currencies

    @staticmethod
    def wallet(wallet_address, allow_standard=True, allow_integrated_address=True, allow_subaddress=False, allow_stagenet=False):
        # Check if walled_address is a string
        if not Check.is_string(wallet_address):
            return False

        if not Check.wallet_allowed_length(wallet_address, allow_standard=allow_standard, allow_subaddress=allow_subaddress, allow_integrated_address=allow_integrated_address):
            return False

        if not Check.wallet_first_character(wallet_address, allow_standard=allow_standard, allow_stagenet=allow_stagenet, allow_subaddress=allow_subaddress):
            return False

        # Check if the wallet address contains only valid characters
        if not Check.wallet_valid_characters(wallet_address):
            return False

        # If it passed all these checks
        return True

    @staticmethod
    def wallet_allowed_length(address, allow_standard=True, allow_subaddress=False, allow_integrated_address=True):
        return len(address) in Check.allowed_wallet_lengths(allow_standard=allow_standard, allow_subaddress=allow_subaddress, allow_integrated_address=allow_integrated_address)

    @staticmethod
    def wallet_first_character(address, allow_standard=True, allow_stagenet=False, allow_subaddress=False):
        return len(address) > 1 and address[0] in Check.allowed_first_wallet_characters(allow_standard=allow_standard, allow_stagenet=allow_stagenet, allow_subaddress=allow_subaddress)

    @staticmethod
    def wallet_valid_characters(address):
        valid_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        for char in address:
            if char not in valid_chars:
                return False
        return True

    @staticmethod
    def allowed_first_wallet_characters(allow_standard=True, allow_stagenet=False, allow_subaddress=False):
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

        return allowed_first_characters

    @staticmethod
    def allowed_wallet_lengths(allow_standard=True, allow_subaddress=False, allow_integrated_address=False):
        allowed_wallet_lengths = []
        if allow_standard or allow_subaddress:
            allowed_wallet_lengths.append(95)
        if allow_integrated_address:
            allowed_wallet_lengths.append(106)
        return allowed_wallet_lengths

    @staticmethod
    def payment_id(payment_id):
        if Check.is_string(payment_id) and Check.payment_id_length(payment_id):
            if not Check.payment_id_characters(payment_id):
                return False
            return True  # All checks passed
        else:
            return False  # Not a string or incorrect length

    @staticmethod
    def payment_id_length(payment_id):
        return len(payment_id) == 16

    @staticmethod
    def payment_id_characters(payment_id):
        for char in payment_id:
            if char not in '0123456789abcdef':
                return False
        return True

    @staticmethod
    def start_date(start_date):
        if Check.is_string(start_date):
            # If it is an empty string
            if not start_date:
                return True

            # If not empty, make sure it is in the proper format
            return Check.start_date_format(start_date)
        return False

    @staticmethod
    def start_date_format(start_date):
        try:
            datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            return True
        except ValueError:
            return False

    @staticmethod
    def amount(amount):
        if Check.is_string(amount):
            if Check.amount_characters(amount):
                return True
        return False

    @staticmethod
    def amount_characters(amount):
        if re.fullmatch(r'[\d,.]+', amount):
            return True
        return False

    @staticmethod
    def days_per_billing_cycle(billing_cycle):
        if Check.is_int(billing_cycle) and Check.billing_cycle_positive(billing_cycle):
            return True
        else:
            return False

    @staticmethod
    def billing_cycle_positive(billing_cycle):
        return billing_cycle >= 0

    @staticmethod
    def number_of_payments(number_of_payments):
        if Check.is_int(number_of_payments) and Check.payments_valid(number_of_payments):
            return True
        else:
            return False

    @staticmethod
    def payments_valid(number_of_payments):
        return number_of_payments >= -1

    @staticmethod
    def change_indicator_url(change_indicator_url):
        if change_indicator_url == "":
            return True  # Empty string is allowed
        if Check.is_string(change_indicator_url):
            if Check.url_parseable(change_indicator_url):
                return True
        return False  # Invalid

    @staticmethod
    def url_parseable(change_url):
        parsed_url = urlparse(change_url)
        if all([parsed_url.scheme, parsed_url.netloc]):
            return True  # Well-formed URL
        return False

    @staticmethod
    def schedule(schedule):
        return CronValidation(schedule).valid()
