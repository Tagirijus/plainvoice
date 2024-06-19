from decimal import Decimal, ROUND_HALF_UP


def round2(dec):
    """Rounds the given Decimal to two digits after the decimal."""
    return dec.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
