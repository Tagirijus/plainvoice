from decimal import Decimal


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
