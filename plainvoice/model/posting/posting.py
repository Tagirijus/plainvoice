'''
Posting Class

This class shall represent a single posting on an invoice or
quote. It has special classes as component and certain math
operations to be executed on demand.
'''


from plainvoice.model.data.data_model import DataModel
from plainvoice.model.quantity.quantity import Quantity
from plainvoice.model.quantity.price import Price
from plainvoice.model.quantity.percentage import Percentage

from typing import Any


class Posting(DataModel):
    '''
    This class represents an invoice posting.
    '''

    def __init__(self, title: str = ''):
        '''
        This class is for representign an invoice posting.

        Args:
            title (str): \
                The title of the posting. Set as a readable \
                format. (Default '`''`')
        '''
        super().__init__()
        self._init_fixed_fields()
        self.set_fixed('title', title, True)

    def _init_fixed_fields(self) -> None:
        '''
        Initialize the fixed fields for this special DataModel child.
        '''
        self.define_fixed_field_type('str', str, str)
        self.define_fixed_field_type(
            'Quantity',
            lambda x: Quantity(str(x)),
            str
        )
        self.define_fixed_field_type(
            'Price',
            lambda x: Price(str(x)),
            str
        )
        self.define_fixed_field_type(
            'Percentage',
            lambda x: Percentage(str(x)),
            str
        )

        self.add_field_descriptor('title', 'str', '')
        self.add_field_descriptor('detail', 'str', '')
        self.add_field_descriptor('unit_price', 'Price', '1.00 €')
        self.add_field_descriptor('quantity', 'Quantity', '1')
        self.add_field_descriptor('vat', 'Percentage', '0 %')

    def __str__(self) -> str:
        '''
        Represent this class as a string.

        Returns:
            srt: The readable string.
        '''
        quantity = self.get_fixed('quantity', True)
        title = self.get_fixed('title', True)
        net_total = self.get_total(False)
        vat = self.get_vat(False)
        total = self.fixed_field_conversion_manager.convert_value_to_readable(
            net_total + vat,
            'Price'
        )
        vat_str = self.get_vat(True)
        return f'{quantity}, {title}: {total} ({vat_str} VAT)'

    def get_total(self, readable: bool = False) -> Price | Any:
        '''
        Calculate and return the total net value.

        Args:
            readable (bool): Convert the output to a readable.

        Returns:
            Price | Any: Returns the net total as a Price or Any object.
        '''
        total_price = (
            self.get_fixed('unit_price', False)
            * self.get_fixed('quantity', False)
        )
        if readable:
            total_price = \
                self.fixed_field_conversion_manager.convert_value_to_readable(
                    total_price,
                    'Price'
                )
        return total_price

    def get_vat(self, readable: bool = False) -> Price:
        '''
        Calculate the vat from the total and return it.

        readable (bool): \
                Convert the output to a readable.

        Returns:
            Price: Returns the vat of the total as a Price object.
        '''
        vat_price = self.get_total(False) * self.get_fixed('vat', False)
        if readable:
            vat_price = \
                self.fixed_field_conversion_manager.convert_value_to_readable(
                    vat_price,
                    'Price'
                )
        return vat_price

    def has_vat(self):
        return self.get_fixed('vat', False) != 0
