from .check import Check

class Request():
    def name_validity(self):
        if not Check.name(self.custom_label):
            self.errors['custom_label'] = ['is not a string']
        return not self.errors.get('custom_label', False)

    def wallet_validity(self):
        if not Check.wallet(self.sellers_wallet, self.allow_standard, self.allow_integrated_address, self.allow_subaddress, self.allow_stagenet):
            self.errors['sellers_wallet'] = []
            if not Check.is_string(self.sellers_wallet):
                self.errors['sellers_wallet'].append('is not a string')
                return False
            if Check.is_string(self.sellers_wallet):
                if not Check.wallet_valid_characters(self.sellers_wallet):
                    self.errors['sellers_wallet'].append('contains invalid characters')
                if not Check.wallet_allowed_length(self.sellers_wallet, allow_standard=self.allow_standard, allow_subaddress=self.allow_subaddress, allow_integrated_address=self.allow_integrated_address):
                    allowed_wallet_lengths_text = ' or '.join([str(i) for i in Check.allowed_wallet_lengths(allow_standard=self.allow_standard, allow_subaddress=self.allow_subaddress, allow_integrated_address=self.allow_integrated_address)])
                    self.errors['sellers_wallet'].append(f'is not exactly {allowed_wallet_lengths_text} characters long')
                if not Check.wallet_first_character(self.sellers_wallet, allow_standard=self.allow_standard, allow_stagenet=self.allow_stagenet, allow_subaddress=self.allow_subaddress):
                    allowed_first_wallet_characters_text = ' or '.join(Check.allowed_first_wallet_characters(allow_standard=self.allow_standard, allow_stagenet=self.allow_stagenet, allow_subaddress=self.allow_subaddress))
                    self.errors['sellers_wallet'].append(f'it does not begin with a {allowed_first_wallet_characters_text}')
        return not self.errors.get('sellers_wallet', False)

    def currency_validity(self):
        if not Check.currency(self.currency):
            self.errors['currency'] = []
            if not Check.is_string(self.currency):
                self.errors['currency'].append('is not a string')
            if not Check.currency_is_supported(self.currency):
                self.errors['currency'].append('is not supported')
        return not self.errors.get('currency', False)

    def amount_validity(self):
        if not Check.amount(self.amount):
            self.errors['amount'] = []
            if not Check.is_string(self.amount):
                self.errors['amount'].append('is not a string')
            if Check.is_string(self.amount) and not Check.amount_characters(self.amount):
                self.errors['amount'].append('contains invalid characters')
        return not self.errors.get('amount', False)

    def payment_id_validity(self):
        if not Check.payment_id(self.payment_id):
            self.errors['payment_id'] = []
            if not Check.is_string(self.payment_id):
                self.errors['payment_id'].append('is not a string')
            if Check.is_string(self.payment_id):
                if not Check.payment_id_length(self.payment_id):
                    self.errors['payment_id'].append('is not exactly 16 characters')
                if not Check.payment_id_characters(self.payment_id):
                    self.errors['payment_id'].append('contains invalid characters')
        return not self.errors.get('payment_id', False)

    def start_date_validity(self):
        if not Check.start_date(self.start_date):
            self.errors['start_date'] = []
            if not Check.is_string(self.start_date):
                self.errors['start_date'].append('is not a string')
            if Check.is_string(self.start_date) and not Check.start_date_format(self.start_date):
                self.errors['start_date'].append('is not in the correct format')
        return not self.errors.get('start_date', False)

    def number_of_payments_validity(self):
        if not Check.number_of_payments(self.number_of_payments):
            self.errors['number_of_payments'] = []
            if not Check.is_int(self.number_of_payments):
                self.errors['number_of_payments'].append('is not an integer')
            if Check.is_int(self.number_of_payments) and not Check.payments_valid(self.number_of_payments):
                self.errors['number_of_payments'].append('is less than -1')
        return not self.errors.get('number_of_payments', False)

    def change_indicator_validity(self):
        if not Check.change_indicator_url(self.change_indicator_url):
            self.errors['change_indicator_url'] = []
            if not Check.is_string(self.change_indicator_url):
                self.errors['change_indicator_url'].append('is not a string')
            if not Check.url_parseable(self.change_indicator_url):
                self.errors['change_indicator_url'].append('is not a valid URL')
        return not self.errors.get('change_indicator_url', False)