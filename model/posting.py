from decimal import Decimal
from model.base import Base
from model import parsers
from utils import math_utils


class Posting(Base):
    def __init__(self):
        super(Posting, self).__init__()

    def folder(self, filename):
        return 'templates/postings/' + filename

    def set_from_dict(self, values={}):
        self.title = values.get('title', '')
        self.comment = values.get('comment', '')

        self.unit_price = Decimal(str(values.get('unit_price', '1')))
        self.amount = values.get('amount', '1')
        self.vat = values.get('vat', '0 %')

    def get_as_dict(self):
        return {
            'title': self.title,
            'comment': self.comment,

            'unit_price': float(self.unit_price),
            'amount': self.amount,
            'vat': self.vat,

            'total': float(self.calc_total())
        }

    def calc_total(self, net=True):
        amount, suffix = parsers.split_amount_string(self.amount.replace(',', '.'))
        amount = parsers.timestring_to_decimal(amount)
        out = self.unit_price * amount
        if net:
            vat_dec, vat_str = parsers.parse_vat_string(self.vat)
            out *= 1 + vat_dec
        return math_utils.round2(out)

    def calc_vat(self):
        total_gross = self.calc_total(False)
        vat_dec, vat_str = parsers.parse_vat_string(self.vat)
        return math_utils.round2(total_gross * vat_dec)
