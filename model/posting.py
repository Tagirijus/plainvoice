from decimal import Decimal


class Posting:
    def __init__(self):
        # basically set the defaults, due to the empty
        # dict, which is given as a parameter
        self.set_from_dict({})

    def set_from_dict(self, values):
        self.name = ''
        self.comment = ''

        self.unit_price = Decimal()
        self.amount = Decimal()

    def get_as_dict(self):
        return {
            'name': self.name,
            'comment': self.comment,

            'unit_price': self.unit_price,
            'amount': self.amount
        }
