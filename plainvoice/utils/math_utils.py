from decimal import Decimal, ROUND_HALF_UP


def round2(dec: Decimal) -> Decimal:
    '''
    Rounds the given Decimal to two digits after the decimal.

    Args:
        dec (Decimal): The Decimal object input.

    Returns:
        Decimal: The rounded Decimal output object.
    '''
    return dec.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def is_convertible_to_int(string):
    '''
    Checks, if the given string can be converted into an integer.
    '''
    try:
        int(string)
        return True
    except ValueError:
        return False
