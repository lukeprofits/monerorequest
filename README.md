# MoneroRequest
![Version 1.0](https://img.shields.io/badge/Version-1.0.0-orange.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776ab.svg)

MoneroRequest is an easy way to create and decode Monero Payment Requests.


# How To Use:
* Install this package: `pip install monerorequest`
* Import it at the top of your project: `import monerorequest`
* Use: `make_monero_payment_request()`
* Or use: `decode_monero_payment_request()`


# Example Usage:
* To create a Monero Payment Request: `make_monero_payment_request(custom_label='My Subscription', sellers_wallet='4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S', currency='USD', amount=19.95, billing_cycle_days=30)`
* To decode a Monero Payment Request: `decode_monero_payment_request(monero_subscription_code='monero-subscription:H4sIAOdsgWQC/x2OXU+DMBSG/wrh2i18D7yDCSaamTimTm9IWw6jsVDSD7U1/nfpLk7OyXue5Hl/faKl4lPHEAbm33r+QWy9VmM3kgi6KMpn/8bzJTAGQnbfaN3KkUmp4nMqvl7NcuLDZdLwVMjiWQnbHyGtNDRCfpYfNNxV/B2P1khuLT80VWbf5tNjf7/Pyp+6xHWdEtsc43G9HrCcknEP56h1UqKFgJkYp3tp71yEJq5n5w+LbZGuwYLMBLPqaH8tFSZDmO+iPAUYUE+u1RUSquuRAkdEQRRvgmwT5O6HKWN0vnTEEAYrY+TKxMHfP4UYQxEZAQAA')`


# Donate

## Requirements
* [Python 3.8](https://www.python.org/downloads/) or above


## License
[MIT](https://github.com/Equim-chan/vanity-monero/blob/master/LICENSE)
