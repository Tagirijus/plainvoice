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
        self.detail = values.get('detail', '')

        self.unit_price = Decimal(str(values.get('unit_price', '1')))
        self.quantity = values.get('quantity', '1')
        self.vat = values.get('vat', '0 %')

    def get_as_dict(self):
        return {
            'title': self.title,
            'detail': self.detail,

            'unit_price': float(self.unit_price),
            'quantity': self.quantity,
            'vat': self.vat,

            # not sure at the moment, if I want the calculations
            # in the YAML, since it crowds the human readable
            # YAML a bit and makes the plaintext principle a
            # bit off.
            # 'total': {
            #     'net': float(self.calc_total(True)),
            #     'gross': float(self.calc_total(False)),
            #     'vat': float(self.calc_vat())
            # }
        }

    def calc_total(self, including_vat=True):
        quantity, suffix = parsers.split_quantity_string(self.quantity.replace(',', '.'))
        quantity = parsers.timestring_to_decimal(quantity)
        out = self.unit_price * quantity
        if including_vat:
            vat_dec, vat_str = parsers.parse_vat_string(self.vat)
            out *= 1 + vat_dec
        return math_utils.round2(out)

    def calc_vat(self):
        total_gross = self.calc_total(False)
        vat_dec, vat_str = parsers.parse_vat_string(self.vat)
        return math_utils.round2(total_gross * vat_dec)

    def has_vat(self):
        vat_dec, vat_str = parsers.parse_vat_string(self.vat)
        return vat_dec != 0
