from .check import Check
from .encode import Encode
from .cron_validation import CronValidation
from .request import Request

class RequestV2(Request):
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
        self.errors = {}

    def valid(self):
        self.errors = {}

        self.name_validity()
        self.wallet_validity()
        self.currency_validity()
        self.amount_validity()
        self.payment_id_validity()
        self.start_date_validity()
        self.number_of_payments_validity()
        self.change_indicator_validity()
        self.schedule_validity()

        if not self.errors:
            return True
        else:
            return False

    def schedule_validity(self):
        if not Check.schedule(self.schedule):
            self.errors['schedule'] = ['is not a valid cron syntax']
            cv = CronValidation(self.schedule)
            if not cv.valid():
                self.errors['schedule'] + cv.errors
        return not self.errors.get('schedule', False)


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
