'''
Quantity class

With this class I want to have an object, which can handle quantity
strings like "1.5", "1" or even things like "1:45 min". It will
be able to parse such strings to an internal Decimal object so that
math operations with this object type are possible.
'''

from decimal import Decimal
from typing import Self, Any

import re


class Quantity:
    '''
    The class which can represent an invoice quantity.
    '''

    def __init__(self, value: str = '0'):
        '''
        The Quantity class can represent an invoice quantity or
        amount value. Internally it calculates with Decimal, yet
        it can get the value from different kinds of strings. E.g.
        it can get a time string with any suffix and parse it to
        the correct value: "1:45 min" == 1.75 + suffix " min".

        Args:
            value (str): The value string to use.
        '''
        self.between_number_and_suffix = ' '
        '''
        The string between number and suffix when representing the
        quantity string.
        '''

        self.full_string = str(value)
        '''
        The original value string from the input.
        '''

        self.has_colon = False
        '''
        The bool that tells, if the input original_string used
        a colon like e.g. in "1:30" or so.
        '''

        self.number_string = ''
        '''
        The number string part of the original_string value.
        '''

        self.suffix_string = ''
        '''
        The suffix string part of the original_string value.
        '''

        self.value = Decimal(1)
        '''
        The actual value to calculate with.
        '''

        self.parse(value)

    def __add__(self, other: Any):
        if isinstance(other, Quantity):
            return self._create_instance(
                str(self.get_value() + other.get_value()),
                self.suffix_string,
                self.between_number_and_suffix,
                self.has_colon,
            )
        elif isinstance(other, (int, float, Decimal)):
            return self._create_instance(
                str(self.get_value() + Decimal(str(other))),
                self.suffix_string,
                self.between_number_and_suffix,
                self.has_colon,
            )
        else:
            return NotImplemented

    def __eq__(self, other: Any):
        if isinstance(other, Quantity):
            return self.value == other.value
        elif isinstance(other, (int, float, Decimal)):
            return self.value == other
        else:
            return NotImplemented

    def __ge__(self, other: Any):
        if isinstance(other, Quantity):
            return self.value >= other.value
        elif isinstance(other, (int, float, Decimal)):
            return self.value >= other
        else:
            return NotImplemented

    def __gt__(self, other: Any):
        if isinstance(other, Quantity):
            return self.value > other.value
        elif isinstance(other, (int, float, Decimal)):
            return self.value > other
        else:
            return NotImplemented

    def __le__(self, other: Any):
        if isinstance(other, Quantity):
            return self.value <= other.value
        elif isinstance(other, (int, float, Decimal)):
            return self.value <= other
        else:
            return NotImplemented

    def __lt__(self, other: Any):
        if isinstance(other, Quantity):
            return self.value < other.value
        elif isinstance(other, (int, float, Decimal)):
            return self.value < other
        else:
            return NotImplemented

    def __sub__(self, other: Any):
        if isinstance(other, Quantity):
            return self._create_instance(
                str(self.get_value() - other.get_value()),
                self.suffix_string,
                self.between_number_and_suffix,
                self.has_colon,
            )
        elif isinstance(other, (int, float, Decimal)):
            return self._create_instance(
                str(self.get_value() - Decimal(str(other))),
                self.suffix_string,
                self.between_number_and_suffix,
                self.has_colon,
            )
        else:
            return NotImplemented

    def __mul__(self, other: Any):
        if isinstance(other, Quantity):
            return self._create_instance(
                str(self.get_value() * other.get_value()),
                self.suffix_string,
                self.between_number_and_suffix,
                self.has_colon,
            )
        elif isinstance(other, (int, float, Decimal)):
            return self._create_instance(
                str(self.get_value() * Decimal(str(other))),
                self.suffix_string,
                self.between_number_and_suffix,
                self.has_colon,
            )
        else:
            return NotImplemented

    def __truediv__(self, other: Any):
        if isinstance(other, Quantity):
            return self._create_instance(
                str(self.get_value() / other.get_value()),
                self.suffix_string,
                self.between_number_and_suffix,
                self.has_colon,
            )
        elif isinstance(other, (int, float, Decimal)):
            return self._create_instance(
                str(self.get_value() / Decimal(str(other))),
                self.suffix_string,
                self.between_number_and_suffix,
                self.has_colon,
            )
        else:
            return NotImplemented

    def __str__(self):
        '''
        Represent this quantity type with a string. It's
        probably just the bare input string anyway.
        '''
        return self.full_string

    @classmethod
    def _create_instance(
        cls, value: str, suffix: str, between_string: str, has_colon: bool
    ) -> Self:
        '''
        Return a new instance with given values

        Args:
            value (str): \
                The internal finally parsed Decimal value, yet \
                parsed from a string.
            suffix (str): \
                The suffix of the original_string.

        Returns:
            Quantity: Returns a new Quantity instance.
        '''
        output = cls()
        output.set_has_colon(has_colon)
        output.set_suffix(suffix)
        output.set_between(between_string)
        output.set_value(value)
        return output

    def get_between(self) -> str:
        '''
        Get the string between number and suffix as a string.

        Returns:
            str: Returns the wanted between string.
        '''
        return self.between_number_and_suffix

    def get_suffix(self) -> str:
        '''
        Get the suffix as a string.

        Returns:
            str: Returns the wanted suffix string.
        '''
        return self.suffix_string

    def get_value(self) -> Decimal:
        '''
        Get the value as Decimal.

        Returns:
            Decimal: Returns the value das Decimal.
        '''
        return self.value

    def parse(self, original_string: str) -> None:
        '''
        Parse a given string to internal values accordingly. It
        will behave as this is the value given on instance creation.

        Args:
            original_string (str): The original string to parse.
        '''
        self.full_string = str(original_string)
        self._split_quantity_string()
        self._time_string_to_decimal()
        self._strings_from_value()

    def set_between(self, between_string: str) -> None:
        '''
        With this you can change the string between number and suffix.
        By defualt it will be a single whitespace.

        Args:
            between_string (str): The string between number and suffix.
        '''
        self.between_number_and_suffix = str(between_string)
        self._strings_from_value()

    def set_has_colon(self, has_colon: bool) -> None:
        '''
        With this setter it is possible to change if the quantity
        should represent the internal Decimal with a colon or not.
        If True an internal value of "1.5" would be represented as
        "1:30", for example.

        Args:
            has_colon (bool): Sets if the shall be a colon or not.
        '''
        self.has_colon = bool(has_colon)
        self._strings_from_value()

    def set_suffix(self, suffix: str) -> None:
        '''
        Change the internal suffix string.

        Args:
            suffix (str): The suffix string.
        '''
        self.suffix_string = str(suffix)
        self._strings_from_value()

    def set_value(self, value: str = '0') -> None:
        '''
        Change the internal value string with a new Decimal, parsed
        from a given string.

        Args:
            value (Decimal): The new input value Decimal.
        '''
        self.value = Decimal(value)
        self._strings_from_value()

    def _split_quantity_string(self) -> None:
        '''
        This function splits a given quantity string into the number
        part and the suffix part.

        Examples:
          "1.5"       ->  ("1.5", "")
          "-1.5"      ->  ("-1.5", "")
          "1.5h"      ->  ("1.5", "h")
          "1:05"      ->  ("1:05", "")
          "1:30 min"  ->  ("1:30", "min")

        The number part still is a string!! It can be converted
        into a Decimal with the timestring_to_decimal() function.

        Args:
            quantity_string (str): The string to 'parse'.

        Raises:
            ValueError: Error, if 'parsing' might not be possible.
        '''
        pattern = r'^(-?[\d.:]+)\s*([^\d.:]*)$'
        match = re.match(pattern, self.full_string.strip())

        if match:
            self.number_string = match.group(1)
            self.suffix_string = match.group(2).strip()
            self.between_number_and_suffix = self.full_string.replace(
                self.number_string, ''
            ).replace(self.suffix_string, '')
            self.has_colon = ':' in self.number_string
        else:
            raise ValueError(f'Quantity format not possible: {self.full_string}')

    def _strings_from_value(self) -> None:
        '''
        Re-format the internal strings according to the
        actual self.value attribute.
        '''
        if self.has_colon:
            self.number_string = self._decimal_to_time_string(self.get_value())
        else:
            self.number_string = str(self.get_value())

        self.full_string = (
            self.number_string + self.between_number_and_suffix + self.suffix_string
        )

    def _time_string_to_decimal(self) -> None:
        '''
        This function is capable to convert a possible time notation
        like "1:30" into a proper Decimal(1.5). If there is no
        colon, the string will be converted to a Decimal().

        Args:
            timestring (str): The string like '1:30'.

        Returns:
            Decimal: The decimal, which gets converted from the string.

        Raises:
            ValueError: Error if string is not convertable.
        '''
        if ':' in self.number_string:
            splitted = self.number_string.split(':')
            if len(splitted) > 1:
                a = Decimal(splitted[0].strip())
                b = Decimal(splitted[1].strip())
                self.value = Decimal(str(a + (b / 60)))
            else:
                raise ValueError(
                    f'Quantity has invalid time string: {self.number_string}'
                )
        else:
            self.value = Decimal(self.number_string)

    def _decimal_to_time_string(self, decimal_value: Decimal) -> str:
        '''
        Converts a given decimal to a colon number string which
        might be used for time notation, for example. E.g.
        "1.5" will become "1:30".

        Args:
            value (Decimal): The value as a Decimal object.

        Returns:
            str: Returns the number string.
        '''
        minutes = int(decimal_value)
        seconds = (decimal_value - minutes) * 60
        seconds = int(round(seconds))
        return f'{minutes}:{seconds:02d}'
