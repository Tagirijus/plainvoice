from decimal import Decimal
from model.base import Base


class Posting(Base):
    def __init__(self):
        super(Posting, self).__init__()

    def folder(self, filename):
        return 'templates/postings/' + filename

    def set_from_dict(self, values):
        self.title = ''
        self.comment = ''

        self.unit_price = Decimal()
        self.amount = Decimal()
        self.tax = Decimal()

    def get_as_dict(self):
        return {
            'title': self.title,
            'comment': self.comment,

            'unit_price': self.unit_price,
            'amount': self.amount,
            'tax': self.tax
        }
