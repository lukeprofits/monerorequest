import json
import base64
import gzip

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
