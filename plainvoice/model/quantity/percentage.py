'''
Percentage class

It is a special kind derived from the Quantity class. It is for
calculating with percentages. Internally it will just use the
value divided by 100 to reflect the percentage during math
operations.
'''

from plainvoice.model.quantity.quantity import Quantity

from decimal import Decimal


class Percentage(Quantity):
    '''
    A special Quantity class, which calculates with its
    value divided by 100 internally
    '''

    def __init__(self, value: str = '0 %'):
        '''
        The percentage class is based on the Quantity class and is
        supposed to represent percentage values. Its value getter is
        a division of the value by 100.

        Args:
            value (str): The percentage as a readbale str. (default: `'0 %'`)
        '''
        super().__init__(value)

    def get_value(self) -> Decimal:
        '''
        Get the value as Decimal.

        Returns:
            Decimal: Returns the value das Decimal.
        '''
        return self.value / 100

    def _strings_from_value(self) -> None:
        '''
        Re-format the internal strings according to the
        actual self.value attribute.
        '''
        self.number_string = str((self.get_value() * 100).quantize(Decimal('1')))

        self.full_string = (
            self.number_string + self.between_number_and_suffix + self.suffix_string
        )
