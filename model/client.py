from decimal import Decimal


class Client(object):
    def __init__(self):
        self.client_id = ''

        self.company_a = ''
        self.company_b = ''
        self.tax_id = ''

        self.attention = ''
        self.salutation = ''
        self.first_name = ''
        self.last_name = ''

        self.street = ''
        self.city = ''
        self.postcode = ''
        self.country = ''

        self.default_currency = '€'
        self.default_wage = Decimal()

        self.language = 'de'
