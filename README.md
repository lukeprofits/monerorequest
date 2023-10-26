# MoneroRequest
![Version 1.0](https://img.shields.io/badge/Version-1.0.0-orange.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776ab.svg)

MoneroRequest is an easy way to create and decode Monero Payment Requests.


# How To Use:
* Install this package: `pip install monerorequest`
* Import it at the top of your project: `import monerorequest`
* Use: `make_monero_payment_request()`
* Or use: `decode_monero_payment_request()`

# Example Monero Payment Request:
* A Monero Payment Request looks like this: 
```monero-request:1:H4sIAAAAAAAC/y1QXVPCMBD8K0yegWmbftC+FQRndHAUiiIvmTS50o5pgkmqto7/3RR9ut3b29u5+0a0VZ20KENBNE9TNEWspvIMpJG8YdQqTTotnDwqndYgWe/YYX9zbRirWiJoCePIQV4R8MlWSdBq8kj7FqSd7OC9A2Odg9PekAtoUjZCNPJMWM8EoAx7UyS7tnSKqsjlz2dQ5k/RPyENdxF+sAjjsEpwxfwkwcytNCAEaEM+qavjIWFu8THSH8/9pVDVue3gITXpk9UD30G07GCjzVt+avxkqV7LeuiNGga13Szj4UUW9/x2Fedf67xcryM2bHa4duiuNG1Yr+AY7MdIS7UlnFoY/+YFeOZ7syAuvCjDi8xP5zEOT+jnF8JbIrJdAQAA```

* When decoded, it holds this information:
```{'amount': '25.99', 'change_indicator_url': '', 'currency': 'USD', 'custom_label': 'Unlabeled Monero Payment Request', 'days_per_billing_cycle': 30, 'number_of_payments': 0, 'payment_id': '0aff662b3151e624', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', 'start_date': '2023-10-26T04:55:37.443Z'}
```

# Example Usage:
* To create a Monero Payment Request: `make_monero_payment_request(custom_label='My Subscription', sellers_wallet='4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', currency='USD', amount=19.95, billing_cycle_days=30)`
* To decode a Monero Payment Request: `decode_monero_payment_request(monero_subscription_code='monero-subscription:H4sIAOdsgWQC/x2OXU+DMBSG/wrh2i18D7yDCSaamTimTm9IWw6jsVDSD7U1/nfpLk7OyXue5Hl/faKl4lPHEAbm33r+QWy9VmM3kgi6KMpn/8bzJTAGQnbfaN3KkUmp4nMqvl7NcuLDZdLwVMjiWQnbHyGtNDRCfpYfNNxV/B2P1khuLT80VWbf5tNjf7/Pyp+6xHWdEtsc43G9HrCcknEP56h1UqKFgJkYp3tp71yEJq5n5w+LbZGuwYLMBLPqaH8tFSZDmO+iPAUYUE+u1RUSquuRAkdEQRRvgmwT5O6HKWN0vnTEEAYrY+TKxMHfP4UYQxEZAQAA')`


# Donate

## Requirements
* [Python 3.8](https://www.python.org/downloads/) or above


## License
[MIT](https://github.com/Equim-chan/vanity-monero/blob/master/LICENSE)
