from decimal import Decimal
from model.base import Base
from model import parsers
from utils import math_utils


class Posting(Base):
    """
    The class containign data for a single posting of
    an invoice or quote or similar.
    """

    title: str
    """
    The title of the posting.
    """

    detail: str
    """
    The details / description of a posting.
    """

    unit_price: Decimal
    """
    The unit price of a single posting.
    """

    quantity: str
    """
    The quantity of a single posting. This is just a string
    and will be 'parsed' later. This way a quantity can become
    almost everything the user wants. E.g. '1 pieces' or
    '1:45 hours'.
    """

    var: str
    """
    Similar to the self.quantity attribute this is a string,
    which will be parsed later. This way it's a bit more human
    readable in the YAML file later instead of just a single
    Decimal for the vat percentage.
    """

    def __init__(self):
        super(Posting, self).__init__()
        self.FOLDER = 'presets/postings/'

    def set_from_dict(self, values: dict = {}) -> None:
        """
        Set the posting object from a given dict.

        Args:
            values (dict): \
                The dict to set the objects attributes from. (default: `{}`)
        """
        self.title = values.get('title', '')
        self.detail = values.get('detail', '')

        self.unit_price = Decimal(str(values.get('unit_price', '1')))
        self.quantity = values.get('quantity', '1')
        self.vat = values.get('vat', '0 %')

    def get_as_dict(self) -> dict:
        """
        Returns the class attributes as a dict.

        Returns:
            dict: The class attributes as a dict.
        """
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
            #     'net': float(self.calc_total(False)),
            #     'gross': float(self.calc_total(True)),
            #     'vat': float(self.calc_vat())
            # }
        }

    def calc_total(self, including_vat: bool = True) -> Decimal:
        """
        Calculates and returns the postings total.

        Args:
            including_vat (bool): \
                If set to True, the total will include vat. (default: `True`)

        Returns:
            Decimal: The total as a Decimal object.
        """
        quantity, _ = parsers.split_quantity_string(
            self.quantity.replace(',', '.')
        )
        quantity = parsers.timestring_to_decimal(quantity)
        out = self.unit_price * quantity
        if including_vat:
            vat_dec, _ = parsers.parse_vat_string(self.vat)
            out *= 1 + vat_dec
        return math_utils.round2(out)

    def calc_vat(self) -> Decimal:
        """
        Calculates and return the vat of the posting
        as a Decimal.

        Returns:
            Decimal: The vat of the posting as a Decimal.
        """
        total_gross = self.calc_total(False)
        vat_dec, _ = parsers.parse_vat_string(self.vat)
        return math_utils.round2(total_gross * vat_dec)

    def has_vat(self) -> bool:
        """
        Checks if the posting has a vat after all.

        Returns:
            bool: True if posting has a vat.
        """
        vat_dec, _ = parsers.parse_vat_string(self.vat)
        return vat_dec != 0
