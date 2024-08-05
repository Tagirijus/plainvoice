'''
Price class

It is a special kind derived from the Quantity class. It is for
representing the currency. Basically the currency is just the
suffix so it is using this instead.
'''

from plainvoice.model.quantity.quantity import Quantity

from decimal import Decimal, ROUND_HALF_UP


class Price(Quantity):
    '''
    A special Quantity class, which is used for prices.
    '''

    def __init__(self, value: str = '0.00 €'):
        '''
        The price class is based on the Quantity class and is
        supposed to represent a Price, which has always two
        digits, round accordingly and the suffix can be
        retrieved with .get_currecny() as well.

        Args:
            value (str): The price as a readbale str. (default: `'0.00 €'`)
        '''
        super().__init__(value)

    def get_currency(self) -> str:
        '''
        Gets the currency, which technically is just
        the suffix.

        Returns:
            str: Returns the currency / suffix as a string.
        '''
        return self.get_suffix()

    def set_currency(self, currency: str) -> None:
        '''
        Set the currency string, so basically a new suffic.

        Args:
            currency (str): The currenc string.
        '''
        self.set_suffix(currency)

    def _strings_from_value(self) -> None:
        '''
        Re-format the internal strings according to the
        actual self.value attribute.
        '''
        self.number_string = str(self.get_value().quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        ))

        self.full_string = (
            self.number_string + self.between_number_and_suffix
            + self.suffix_string
        )
