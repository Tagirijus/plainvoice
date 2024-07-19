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
