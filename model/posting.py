from decimal import Decimal, ROUND_HALF_UP
from model.base import Base

import re


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
        self.tax = Decimal(str(values.get('tax', '0')))

    def get_as_dict(self):
        return {
            'title': self.title,
            'comment': self.comment,

            'unit_price': float(self.unit_price),
            'amount': self.amount,
            'tax': float(self.tax),

            'total': float(self.calc_total())
        }

    def parse_amount(self):
        """
        I can have different kinds of amount notations.
        I can have a simple number, float or whatever.
        Yet I can also have some kidn of times like
        "1:30h" or "0:45 min".

        Also every comma will be interpreted as a decimal
        dot and thousand commas should not be used here!
        Says the german guy, who does not like thousand
        separators with the comma. (;

        Method outputs the Decimal number and the suffix
        as a tupple.
        """
        # first split the suffix from the number itself
        number, suffix = self.split_amount_string(self.amount)
        number = number.replace(',', '.')

        # number might be a time notation
        if ':' in number:
            number = self.time_to_decimal(number)
        else:
            number = Decimal(number)

        return number, suffix

    def split_amount_string(self, input_string):
        pattern = r'^([\d.:]+)\s*([^\d.:]*)$'
        match = re.match(pattern, input_string.strip())

        if match:
            number = match.group(1)
            suffix = match.group(2).strip()

            return number, suffix
        else:
            raise ValueError(f'Amount format not possible in posting: {input_string}')

    def time_to_decimal(self, timestring):
        splitted = timestring.split(':')
        if len(splitted) > 1:
            a = Decimal(splitted[0].strip())
            b = Decimal(splitted[1].strip())
            return a + (b / 60)
        else:
            raise ValueError(f'Amount has invalid time string in posting: {timestring}.')

    def calc_total(self):
        amount, suffix = self.parse_amount()
        out = self.unit_price * amount
        return out.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
