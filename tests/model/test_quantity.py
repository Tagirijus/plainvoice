from plainvoice.model.quantity.quantity import Quantity

from decimal import Decimal


def test_setter_getter():
    # creating a new instance
    quantity = Quantity('1 p')

    # getting the repsecting correct parts of
    # that parsed string
    assert quantity.get_value() == Decimal('1')
    assert quantity.get_between() == ' '
    assert quantity.get_suffix() == 'p'

    # now test the setter
    quantity.set_value('2.5')
    quantity.set_between(' - ')
    quantity.set_suffix('min')
    quantity.set_has_colon(True)

    # checking the new set values with the getter
    assert quantity.get_value() == Decimal('2.5')
    assert quantity.get_between() == ' - '
    assert quantity.get_suffix() == 'min'

    # since I changed has_colon, also check the
    # final str output of that quantity
    assert str(quantity) == '2:30 - min'


def test_math():
    # creating new instances
    quantity_a = Quantity('2:00 min')
    quantity_b = Quantity('2.5')

    # let's start with division
    # dividing 2 by 2.5 is 0,8, which
    # basically is 0:48 in time format
    result_division = quantity_a / quantity_b
    assert str(result_division) == '0:48 min'

    # let's add something
    # adding 2 to 0:48 min will be 3:18 in time format
    result_added = result_division + quantity_b
    assert str(result_added) == '3:18 min'

    # let's substract again
    # 3:18 minus 2 is 1:18
    result_substracted = result_added - quantity_a
    assert str(result_substracted) == '1:18 min'

    # let's finally multiply
    # 1:18 * 2 is 2:36
    result_multiplied = result_substracted * quantity_a
    assert str(result_multiplied) == '2:36 min'
