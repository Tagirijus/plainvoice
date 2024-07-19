from decimal import Decimal

import re


# ### ### ### ### ### ### #
# Posting related parsers #
# ### ### ### ### ### ### #


def parse_vat_string(vat_string: str) -> tuple[Decimal, str]:
    '''
    Vat can be given in different ways:
      "19 %"
      "19"
      "0.19"
    It will internally parsed and split into a
    usable Decimal() for calculations and also
    a usable string for the invoice:
      (Decimal(0.19), "19 %")

    Args:
        vat_string (str): The string to be 'parsed'.

    Returns:
        tuple[Decimal, str]: \
            - Decimal: \
                The Decimal which is the vat, while 10%
                would be 0.1 here.
            - str: \
                The string which includes e.g. the percentage
                from the original vat string.
    '''
    if '%' in vat_string:
        vat_string = vat_string.replace('%', '').strip()
    dec = Decimal(vat_string)
    # assume the given percentage is like "19 %",
    # thus not usable in calculations directly.
    if dec > 1:
        dec = dec / 100
    # generate the string
    dec_str = (
        str(dec).split('.')[1] if len(str(dec).split('.')) > 1 else str(dec)
    )
    if len(dec_str) < 3:
        dec_str = str(round(dec * 100)) + ' %'
    elif len(dec_str) == 3:
        dec_str = str(round(dec * 100, 1)) + ' %'
    elif len(dec_str) > 3:
        dec_str = str(round(dec * 100, 2)) + ' %'
    return dec, dec_str


def split_quantity_string(quantity_string: str) -> tuple[str, str]:
    '''
    This function splits a given quantity string into the number
    part and the suffix part.

    Examples:
      "1.5"       ->  ("1.5", "")
      "1.5h"      ->  ("1.5", "h")
      "1:05"      ->  ("1:05", "")
      "1:30 min"  ->  ("1:30", "min")

    The number part still is a string!! It can be converted
    into a Decimal with the timestring_to_decimal() function.

    Args:
        quantity_string (str): The string to 'parse'.

    Returns:
        tuple: \
            - str: The numer of the quantity string.
            - str: The quantity descriptor of the string.

    Raises:
        ValueError: Error, if 'parsing' might not be possible.
    '''
    pattern = r'^([\d.:]+)\s*([^\d.:]*)$'
    match = re.match(pattern, quantity_string.strip())

    if match:
        number = match.group(1)
        suffix = match.group(2).strip()

        return number, suffix
    else:
        raise ValueError(f'Quantity format not possible: {quantity_string}')


def timestring_to_decimal(timestring: str) -> Decimal:
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
    if ':' in timestring:
        splitted = timestring.split(':')
        if len(splitted) > 1:
            a = Decimal(splitted[0].strip())
            b = Decimal(splitted[1].strip())
            return a + (b / 60)
        else:
            raise ValueError(f'Quantity has invalid time string: {timestring}')
    else:
        return Decimal(timestring)
