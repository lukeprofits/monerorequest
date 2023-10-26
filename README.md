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

* When decoded, it holds this information: `{'amount': '25.99', 'change_indicator_url': '', 'currency': 'USD', 'custom_label': 'Unlabeled Monero Payment Request', 'days_per_billing_cycle': 30, 'number_of_payments': 0, 'payment_id': '0aff662b3151e624', 'sellers_wallet': '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', 'start_date': '2023-10-26T04:55:37.443Z'}`

# Example Usage:
* To create a Monero Payment Request:
```
monero_payment_request = make_monero_payment_request(custom_label='Unlabeled Monero Payment Request', sellers_wallet='4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', currency='USD', amount='25.99', payment_id='', start_date='', days_per_billing_cycle=30, number_of_payments=1, change_indicator_url='')
```

* To decode a Monero Payment Request:
```
decode_monero_payment_request(monero_payment_request='monero-request:1:H4sIAAAAAAAC/y1QyU7DMBD9lcrntkriOFVyS0uKBCqCLlB6sex40kQkdvECJIh/xymc5i0z8zTzjVinnLQoQxGZpymaorJm8gy0kaIpmVWaOt16e3Sc1iDL3rPD7uYqGKs62jIOY8tBXhGIyUZJ0GryyPoOpJ1s4d2BsX5CsN7QC2jKm7Zt5JmWfdkCynAwRdJ13Duqope/OYMyL/8T2ggfEbCqSpKI45CEkESxX2mgbUEb+sl8HQ+Jc4uPRH8895e9qs6dg4fUpE9WD2ILZOlgrc1bfmrCxVK98nrojRoGtVkvk+FF7u/F7SrJv4qcFwUph/UW1x7dcdPF9QqO0W6MtExbKpiF8W9BhGdhMIuSfRBnhGR4MY9jfEI/vzFHmeFdAQAA')
```

# Donate

## Requirements
* [Python 3.8](https://www.python.org/downloads/) or above


## License
[MIT](https://github.com/Equim-chan/vanity-monero/blob/master/LICENSE)
