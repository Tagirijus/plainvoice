from decimal import Decimal

import re


# ### ### ### ### ### ### #
# Posting related parsers #
# ### ### ### ### ### ### #


def split_amount_string(amount_string):
    """
    This function splits a given amount string into the number
    part and the suffix part.

    Examples:
      "1.5"       ->  ("1.5", "")
      "1.5h"      ->  ("1.5", "h")
      "1:05"      ->  ("1:05", "")
      "1:30 min"  ->  ("1:30", "min")

    The number part still is a string!! It can be converted
    into a Decimal with the timestring_to_decimal() function.
    """
    pattern = r'^([\d.:]+)\s*([^\d.:]*)$'
    match = re.match(pattern, amount_string.strip())

    if match:
        number = match.group(1)
        suffix = match.group(2).strip()

        return number, suffix
    else:
        raise ValueError(f'Amount format not possible: {amount_string}')

def timestring_to_decimal(timestring):
    """
    This function is capable to convert a possible time notation
    like "1:30" into a proper Decimal(1.5). If there is no
    colon, the string will be converted to a Decimal().
    """
    if ':' in timestring:
        splitted = timestring.split(':')
        if len(splitted) > 1:
            a = Decimal(splitted[0].strip())
            b = Decimal(splitted[1].strip())
            return a + (b / 60)
        else:
            raise ValueError(f'Amount has invalid time string: {timestring}')
    else:
        return Decimal(timestring)

