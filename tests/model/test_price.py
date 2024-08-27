from plainvoice.model.quantity.price import Price

from decimal import Decimal


def test_price_deicmal():
    # creating instances
    # they should always have
    # two decimal
    price = Price('2')
    assert str(price) == '2.00'

    price = Price('2.5')
    assert str(price) == '2.50'

    price = Price('0')
    assert str(price) == '0.00'


def test_price_currency():
    # create an instance
    price = Price('1 €')

    # the suffix is "€" and it should be gettable
    # with .get_currency() as well
    assert price.get_currency() == '€'


def test_price_rounding():
    # create an instance
    price = Price('1 €')

    # add something, which would generate a third decimal
    price = price + 1.004

    # it should be rounded down, due to the "4"
    assert str(price) == '2.00 €'

    # add something, which would generate a third decimal again
    price = price + 1.005

    # this now should round up, due to .5
    assert str(price) == '3.01 €'

    # also a price should always use only twi digits
    # after comma
    percent_of_price = price * 0.05
    assert percent_of_price.value == Decimal('0.15')
