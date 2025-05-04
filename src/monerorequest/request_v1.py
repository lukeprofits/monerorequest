from .check import Check
from .encode import Encode
from .request import Request

class RequestV1(Request):
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
        self.errors = {}

    def valid(self):
        self.errors = {}

        self.name_validity()
        self.wallet_validity()
        self.currency_validity()
        self.amount_validity()
        self.payment_id_validity()
        self.start_date_validity()
        self.billing_cycle_validity()
        self.number_of_payments_validity()
        self.change_indicator_validity()

        if not self.errors:
            return True
        else:
            return False

    def billing_cycle_validity(self):
        if not Check.days_per_billing_cycle(self.days_per_billing_cycle):
            self.errors['days_per_billing_cycle'] = []
            if not Check.is_int(self.days_per_billing_cycle):
                self.errors['days_per_billing_cycle'].append('is not an integer')
            if Check.is_int(self.days_per_billing_cycle) and not Check.billing_cycle_positive(self.days_per_billing_cycle):
                self.errors['days_per_billing_cycle'].append('the value was set lower than 0')
        return not self.errors.get('days_per_billing_cycle', False)

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
