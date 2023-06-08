import json
import base64
import random
import gzip
from datetime import datetime


# FUNCTIONS ############################################################################################################
def decode_monero_subscription_code(monero_subscription_code):
    # Catches user error. Code can start with "monero_subscription:", or ""
    code_parts = monero_subscription_code.split('-subscription:')

    if len(code_parts) == 2:
        monero_subscription_data = code_parts[1]
    else:
        monero_subscription_data = code_parts[0]

    # Extract the Base64-encoded string from the second part of the code
    encoded_str = monero_subscription_data

    # Decode the Base64-encoded string into bytes
    compressed_data = base64.b64decode(encoded_str.encode('ascii'))

    # Decompress the bytes using gzip decompression
    json_bytes = gzip.decompress(compressed_data)

    # Convert the decompressed bytes into a JSON string
    json_str = json_bytes.decode('utf-8')

    # Parse the JSON string into a Python object
    subscription_data_as_json = json.loads(json_str)

    return subscription_data_as_json


def make_monero_subscription_code(custom_label='Subscription', sellers_wallet='', currency='USD', amount='', payment_id='', start_date='', billing_cycle_days=30):

    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")

    if not payment_id:
        payment_id = make_payment_id()

    if check_name(custom_label):
        if check_wallet(sellers_wallet):
            if check_currency(currency):
                if check_amount(amount):
                    if check_start_date(start_date):
                        if check_billing_cycle_days(billing_cycle_days):
                            json_data = {
                                "custom_label": custom_label,
                                "sellers_wallet": sellers_wallet,
                                "currency": currency,
                                "amount": amount,
                                "payment_id": payment_id,
                                "start_date": start_date,
                                "billing_cycle_days": billing_cycle_days
                            }

                            # process data to create code
                            code = make_monero_subscription_code_from_json(json_data)
                            return code


def make_monero_subscription_code_from_json(json_data):
    # Convert the JSON data to a string
    json_str = json.dumps(json_data)

    # Compress the string using gzip compression
    compressed_data = gzip.compress(json_str.encode('utf-8'))

    # Encode the compressed data into a Base64-encoded string
    encoded_str = base64.b64encode(compressed_data).decode('ascii')

    # Add the Monero Subscription identifier
    monero_subscription = 'monero-subscription:' + encoded_str

    return monero_subscription


def make_payment_id():
    payment_id = ''.join([random.choice('0123456789abcdef') for _ in range(16)])
    return payment_id


# CHECK FUNCTIONS ######################################################################################################
def check_name(name):
    if len(name) <= 50:
        return True
    else:
        print('name error')
        return False


def check_currency(currency):
    if currency == 'USD' or currency == 'XMR':
        return True
    else:
        print('currency error')
        return False


def check_wallet(wallet_address):
    # Check if the wallet address starts with the number 4
    if wallet_address[0] != "4":
        return False

    # Check if the wallet address is exactly 95 characters long
    if len(wallet_address) != 95:
        return False

    # Check if the wallet address contains only valid characters
    valid_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    for char in wallet_address:
        if char not in valid_chars:
            return False

    # If it passed all these checks
    return True


def check_start_date(start_date):
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        return True
    except ValueError:
        print('start date error')
        return False


def check_amount(amount):
    if type(amount) is float:
        return True
    else:
        print('amount error')
        return False


def check_billing_cycle_days(billing_cycle):
    if type(billing_cycle) is int:
        return True
    else:
        print('billing cycle error')
        return False


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



#monero_subscription_code = make_monero_subscription_code(custom_label='My Subscription', sellers_wallet='4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', currency='USD', amount=19.95, billing_cycle_days=30)

#json_subscription_data = decode_monero_subscription_code(monero_subscription_code='monero-subscription:H4sIAOdsgWQC/x2OXU+DMBSG/wrh2i18D7yDCSaamTimTm9IWw6jsVDSD7U1/nfpLk7OyXue5Hl/faKl4lPHEAbm33r+QWy9VmM3kgi6KMpn/8bzJTAGQnbfaN3KkUmp4nMqvl7NcuLDZdLwVMjiWQnbHyGtNDRCfpYfNNxV/B2P1khuLT80VWbf5tNjf7/Pyp+6xHWdEtsc43G9HrCcknEP56h1UqKFgJkYp3tp71yEJq5n5w+LbZGuwYLMBLPqaH8tFSZDmO+iPAUYUE+u1RUSquuRAkdEQRRvgmwT5O6HKWN0vnTEEAYrY+TKxMHfP4UYQxEZAQAA')
