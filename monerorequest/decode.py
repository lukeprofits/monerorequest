import base64
import gzip
import json

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
        monero_payment_request_data['version'] = '1'
        return monero_payment_request_data

    @staticmethod
    def v2_monero_payment_request(encoded_str):
        decoded_dict = Decode.v1_monero_payment_request(encoded_str)
        decoded_dict['version'] = '2'
        return decoded_dict
