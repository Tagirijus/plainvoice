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

    def get_value(self) -> Decimal:
        '''
        Get the value as Decimal.

        Returns:
            Decimal: Returns the value das Decimal.
        '''
        return self.value / 100
