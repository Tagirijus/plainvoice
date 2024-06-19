from decimal import Decimal
from controller.file import File


class Client(object):
    def __init__(self):
        # basically set the defaults, due to the empty
        # dict, which is given as a parameter
        self.set_from_dict({})

    def folder(self, filename):
        """Prepend the subfolder for this class."""
        return 'clients/' + filename

    def set_from_dict(self, values):
        self.client_id = values.get('client_id', '')

        self.company_a = values.get('company_a', '')
        self.company_b = values.get('company_b', '')
        self.tax_id = values.get('tax_id', '')

        self.attention = values.get('attention', '')
        self.salutation = values.get('salutation', '')
        self.first_name = values.get('first_name', '')
        self.last_name = values.get('last_name', '')

        self.street = values.get('street', '')
        self.city = values.get('city', '')
        self.postcode = values.get('postcode', '')
        self.country = values.get('country', '')

        self.default_currency = values.get('default_currency', '€')
        self.default_wage = Decimal(str(values.get('default_wage', 40.0)))

        self.language = values.get('language', 'en')

    def get_as_dict(self):
        return {
            'client_id': self.client_id,

            'company_a': self.company_a,
            'company_b': self.company_b,
            'tax_id': self.tax_id,

            'attention': self.attention,
            'salutation': self.salutation,
            'first_name': self.first_name,
            'last_name': self.last_name,

            'street': self.street,
            'city': self.city,
            'postcode': self.postcode,
            'country': self.country,

            'default_currency': self.default_currency,
            'default_wage': float(self.default_wage),

            'language': self.language
        }

    def load(self, filename):
        try:
            data = File().load(self.folder(filename))
            self.set_from_dict(data)
            return True
        except Exception as e:
            # print(e)
            return False

    def save(self, filename):
        try:
            data = self.get_as_dict()
            return File().save(self.folder(filename), data)
        except Exception as e:
            # print(e)
            return False