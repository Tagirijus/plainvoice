'''
Price class

It is a special kind derived from the Quantity class. It is for
representing the currency. Basically the currency is just the
suffix so it is using this instead.


TODO:
- How does it always output the Decimal with 2 decimals after comma?
'''

from plainvoice.model.quantity.quantity import Quantity

from decimal import Decimal, ROUND_HALF_EVEN


class Price(Quantity):
    '''
    A special Quantity class, which is used for prices.
    '''

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
            rounding=ROUND_HALF_EVEN
        ))

        self.full_string = (
            self.number_string + self.between_number_and_suffix
            + self.suffix_string
        )
