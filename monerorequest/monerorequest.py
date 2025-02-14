import random
from datetime import datetime, timezone
from .decode import Decode
from .request_v1 import RequestV1
from .request_v2 import RequestV2

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
