from .check import Check
from .encode import Encode

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
