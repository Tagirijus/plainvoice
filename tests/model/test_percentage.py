from plainvoice.model.quantity.percentage import Percentage
from plainvoice.model.quantity.quantity import Quantity


def test_percentage_calculation():
    # create a quantity and percentage instance
    quantity = Quantity('10')
    percentage = Percentage('10 %')

    # the percentage of the quantity should result in
    # Quantity('1.0'). "1.0", due to the fact that
    # Decimal('10') * Decimal('0.1') just results in
    # Decimal('1.0')
    assert str(quantity * percentage) == '1.0'
