# MoneroRequest
![Version 1.0](https://img.shields.io/badge/Version-1.0.0-orange.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776ab.svg)

MoneroRequest is an easy way to create/decode [Monero Payment Requests](https://github.com/lukeprofits/Monero_Payment_Request_Standard).


# How To Use:
* Install this package: `pip install monerorequest`
* Import it at the top of your project: `import monerorequest`
* Use: `monerorequest.make_monero_payment_request()`
* Or use: `monerorequest.decode_monero_payment_request()`


# Example Usage:
* To create a Monero Payment Request:
```
monero_payment_request = monerorequest.make_monero_payment_request(custom_label='Unlabeled Monero Payment Request', sellers_wallet='4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', currency='USD', amount='25.99', payment_id='', start_date='', schedule='0 0 1 * *', number_of_payments=1, change_indicator_url='')
```

* To decode a Monero Payment Request:
```
monero_payment_request_data = monerorequest.decode_monero_payment_request(monero_payment_request='monero-request:2:H4sIAAAAAAACAy1PyU7DMBD9FcvHqq2yNOstLS0SqAi6QOnFsuNpE5HYxQuQIP4dp3Cat8yb5RvTVlphcI6DaJpleIzLioozkFrwuqRGKmJV4+zBsUqBKDvH9tubq6CNbElDGQwte3FFwNFaClASPdKuBWHQBt4taOMSwrYMFJEncvnzNM79Mf4npOZuTJqmGU98xsIkLpMkdTFdVsBtA871kId8NEKjQYamAaXJJ3V1+GFWmPAQqY/n7rKTp3Nr4SHT2ZNRPd9ANLewUvqtONZ+MpevrOo7LfterlfzuH8Ru3t+u4iLr2XBlsuo7FebsHLojul2Vi3gEGyHlYYqQzg1wy2BF8wmXjbxw52f5lGQh940jZMj/vkFse3xMVgBAAA=')
```

# Example Monero Payment Request:
* A Monero Payment Request looks like this: 
```monero-request:2:H4sIAAAAAAACAy1PyU7DMBD9FcvHqq2yNOstLS0SqAi6QOnFsuNpE5HYxQuQIP4dp3Cat8yb5RvTVlphcI6DaJpleIzLioozkFrwuqRGKmJV4+zBsUqBKDvH9tubq6CNbElDGQwte3FFwNFaClASPdKuBWHQBt4taOMSwrYMFJEncvnzNM79Mf4npOZuTJqmGU98xsIkLpMkdTFdVsBtA871kId8NEKjQYamAaXJJ3V1+GFWmPAQqY/n7rKTp3Nr4SHT2ZNRPd9ANLewUvqtONZ+MpevrOo7LfterlfzuH8Ru3t+u4iLr2XBlsuo7FebsHLojul2Vi3gEGyHlYYqQzg1wy2BF8wmXjbxw52f5lGQh940jZMj/vkFse3xMVgBAAA=```

* When decoded, it is a dictionary with this information: `{'amount': '25.99', 'change_indicator_url': '', 'currency': 'USD', 'custom_label': 'Unlabeled Monero Payment Request', schedule='0 0 1 * *', 'number_of_payments': 0, 'payment_id': '0aff662b3151e624', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', 'start_date': '2023-10-26T04:55:37.443Z', 'version': '2;'}`


# Defaults For `make_monero_payment_request()`
* If `payment_id` is left blank, a random one will be generated. *(If you do not want to use a payment_id, set payment_id to `0000000000000000`.)*
* If `start_date` is left blank, the current time will be used.
* If `custom_label` is left blank, it will be set to `Unlabeled Monero Payment Request`
* If `schedule` is left blank, it will be set to `0 0 1 * *`
* If `number_of_payments` is left blank, it will be set to `1`
* If `version` is left blank, the latest version will be used.


# Supplemental Functions: 
* Generate a random payment_id: `monerorequest.make_random_payment_id()`
* Create an RFC3339 timestamp for `start_date` from a datetime object: `monerorequest.convert_datetime_object_to_truncated_RFC3339_timestamp_format(datetime_object)`
* Print the Monero logo to console: `monerorequest.print_monero_logo()`

# Contributing
* For changes to the protocol, see [the payment request standard project](https://github.com/lukeprofits/Monero_Payment_Request_Standard)
* There are no dependencies for the project besides python.
* To run the tests locally run `python -m unittest discover test`
* If you want to run the coverage check locally before opening a PR, install `coverage` and run `coverage html --include='./monerorequest/**'` and open `./htmlcov/index.html` in your browser.
* If you want to run the linting check locally before opening a PR, install `ruff` and run `ruff check .`, if there is no output that means there are no errors.

# Donate
- XMR: `4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S`
- BTC: `1ACCQMwHYUkA1v449DvQ9t6dm3yv1enN87`
- Cash App: `$LukeProfits`
<a href="https://www.buymeacoffee.com/lukeprofits" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;">
</a><br>

## Requirements
* [Python 3.8](https://www.python.org/downloads/) or above


## License
[MIT](/LICENSE)
